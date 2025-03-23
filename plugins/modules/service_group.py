# -*- coding: utf-8 -*-

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.

"""
Ansible module for managing service group objects in SCM.

This module provides functionality to create, update, and delete service group objects
in the SCM (Strata Cloud Manager) system. It handles service group members
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from pydantic import ValidationError

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.service_group import (
    ServiceGroupSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.config.objects.service_group import ServiceGroup
from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.objects.service_group import ServiceGroupCreateModel, ServiceGroupUpdateModel

DOCUMENTATION = r"""
---
module: service_group

short_description: Manage service group objects in SCM.

version_added: "0.1.0"

description:
    - Manage service group objects within Strata Cloud Manager (SCM).
    - Supports creation, modification, and deletion of service group objects.
    - Ensures proper validation of service group members.
    - Ensures that exactly one of 'folder', 'snippet', or 'device' is provided.

options:
    name:
        description: The name of the service group (max 63 chars).
        required: true
        type: str
    members:
        description: List of service objects that are members of this group.
        required: false
        type: list
        elements: str
    tag:
        description: List of tags associated with the service group. These must be references to existing tag objects in SCM, not just string labels.
        required: false
        type: list
        elements: str
    folder:
        description: The folder in which the resource is defined (max 64 chars).
        required: false
        type: str
    snippet:
        description: The snippet in which the resource is defined (max 64 chars).
        required: false
        type: str
    device:
        description: The device in which the resource is defined (max 64 chars).
        required: false
        type: str
    provider:
        description: Authentication credentials.
        required: true
        type: dict
        suboptions:
            client_id:
                description: Client ID for authentication.
                required: true
                type: str
            client_secret:
                description: Client secret for authentication.
                required: true
                type: str
                no_log: True
            tsg_id:
                description: Tenant Service Group ID.
                required: true
                type: str
            log_level:
                description: Log level for the SDK.
                required: false
                type: str
                default: "INFO"
    state:
        description: Desired state of the service group object.
        required: true
        type: str
        choices:
          - present
          - absent

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
---
- name: Manage Service Group Objects in Strata Cloud Manager
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:
    # First, create tag objects to use in the service group
    - name: Create tag objects
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "{{ item }}"
        color: "Blue"
        folder: "Texas"
        state: "present"
      loop:
        - "Web"
        - "Automation"

    # Create a service group using the tag objects
    - name: Create a service group
      cdot65.scm.service_group:
        provider: "{{ provider }}"
        name: "web-services"
        members:
          - "HTTPS"  # References to existing service objects
          - "SSH"
          - "web-custom-service"  # Custom service previously created
        folder: "Texas"
        tag:
          - "Web"
          - "Automation"
        state: "present"

    - name: Update service group members
      cdot65.scm.service_group:
        provider: "{{ provider }}"
        name: "web-services"
        members:
          - "HTTPS"
          - "SSH"
          - "FTP"  # Add FTP service to the group
          - "web-custom-service"
        folder: "Texas"
        state: "present"

    - name: Remove service group
      cdot65.scm.service_group:
        provider: "{{ provider }}"
        name: "web-services"
        folder: "Texas"
        state: "absent"

    # Clean up the tag objects
    - name: Clean up tag objects
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "{{ item }}"
        folder: "Texas"
        state: "absent"
      loop:
        - "Web"
        - "Automation"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
service_group:
    description: Details about the service group object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "web-services"
        members:
          - "HTTPS"
          - "SSH"
          - "web-custom-service"
        folder: "Texas"
        tag: ["Web", "Automation"]
"""


def build_service_group_data(module_params):
    """
    Build service group data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant service group parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(service_group_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        service_group_data (dict): Service group parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [
        service_group_data.get(container) for container in ["folder", "snippet", "device"]
    ]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the service group object needs to be updated.

    Args:
        existing: Existing service group object from the SCM API
        params (dict): Service group parameters with desired state from Ansible module

    Returns:
        (bool, dict): Tuple containing:
            - bool: Whether an update is needed
            - dict: Complete object data for update including all fields from the existing
                   object with any modifications from the params
    """
    changed = False

    # Start with a fresh update model using all fields from existing object
    update_data = {
        "id": str(existing.id),  # Convert UUID to string for Pydantic
        "name": existing.name,
    }

    # Add the container field (folder, snippet, or device)
    for container in ["folder", "snippet", "device"]:
        container_value = getattr(existing, container, None)
        if container_value is not None:
            update_data[container] = container_value

    # No additional parameters to update for service groups

    # Handle members field
    current_members = getattr(existing, "members", None)
    update_data["members"] = [] if current_members is None else current_members

    if "members" in params and params["members"] is not None:
        # Compare sets to ignore order
        if set(current_members or []) != set(params["members"]):
            update_data["members"] = params["members"]
            changed = True

    # Handle the tag parameter
    current_tag = getattr(existing, "tag", None)
    update_data["tag"] = [] if current_tag is None else current_tag

    if "tag" in params and params["tag"] is not None:
        # Compare sets to ignore order
        if set(current_tag or []) != set(params["tag"]):
            update_data["tag"] = params["tag"]
            changed = True

    return changed, update_data


def get_existing_service_group(client, service_group_data):
    """
    Attempt to fetch an existing service group object.

    Args:
        client: SCM client instance
        service_group_data (dict): Service group parameters to search for

    Returns:
        tuple: (bool, object) indicating if service group exists and the service group object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if container in service_group_data and service_group_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in service_group_data:
            return False, None

        # Fetch the service group using the appropriate container
        existing = client.service_group.fetch(
            name=service_group_data["name"], **{container_type: service_group_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the service group object module.

    This module provides functionality to create, update, and delete service group objects
    in the SCM (Strata Cloud Manager) system. It handles service group members
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=ServiceGroupSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        required_one_of=[["folder", "snippet", "device"]],
        required_if=[["state", "present", ["members"]]],
    )

    result = {"changed": False, "service_group": None}

    try:
        client = get_scm_client(module)
        service_group_data = build_service_group_data(module.params)

        # Validate container is specified (handled by mutually_exclusive and required_one_of)
        if not is_container_specified(service_group_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing service group
        exists, existing_service_group = get_existing_service_group(client, service_group_data)

        if module.params["state"] == "present":
            if not exists:
                # Create new service group
                if not module.check_mode:
                    try:
                        # Validate using Pydantic
                        try:
                            ServiceGroupCreateModel(**service_group_data)
                        except ValidationError as e:
                            module.fail_json(msg=f"Validation error: {str(e)}")

                        new_service_group = client.service_group.create(data=service_group_data)
                        result["service_group"] = serialize_response(new_service_group)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"A service group with name '{service_group_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid service group data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_service_group, service_group_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        try:
                            update_model = ServiceGroupUpdateModel(**update_data)
                        except ValidationError as e:
                            module.fail_json(msg=f"Invalid service group update data: {str(e)}")

                        # Perform update with complete object
                        updated_service_group = client.service_group.update(update_model)
                        result["service_group"] = serialize_response(updated_service_group)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["service_group"] = serialize_response(existing_service_group)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.service_group.delete(str(existing_service_group.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
