# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.

"""
Ansible module for managing dynamic user group objects in SCM.

This module provides functionality to create, update, and delete dynamic user group objects
in the SCM (Strata Cloud Manager) system. It handles tag-based filter expressions and supports
check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.dynamic_user_group import (
    DynamicUserGroupSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.objects import DynamicUserGroupUpdateModel

DOCUMENTATION = r"""
---
module: dynamic_user_group

short_description: Manage dynamic user group objects in SCM.

version_added: "0.1.0"

description:
    - Manage dynamic user group objects within Strata Cloud Manager (SCM).
    - Create, update, and delete dynamic user group objects with tag-based filter expressions.
    - Ensures that exactly one container type (folder, snippet, device) is provided.

options:
    name:
        description: The name of the dynamic user group object (max 63 chars). Must match pattern ^[a-zA-Z\d\-_. ]+$.
        required: true
        type: str
    filter:
        description: Tag-based filter expression for the dynamic user group (max 2047 chars).
        required: false
        type: str
    description:
        description: Description of the dynamic user group object (max 1023 chars).
        required: false
        type: str
    tag:
        description: List of tags associated with the dynamic user group object (max 127 chars each).
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
        description: Desired state of the dynamic user group object.
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
- name: Manage Dynamic User Group Objects in Strata Cloud Manager
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

    - name: Create a dynamic user group with a simple filter
      cdot65.scm.dynamic_user_group:
        provider: "{{ provider }}"
        name: "high_risk_users"
        filter: "tag.criticality.high"
        description: "Users with high risk classification"
        folder: "Security"
        tag: ["RiskManagement", "Security"]
        state: "present"

    - name: Create a dynamic user group with a complex filter
      cdot65.scm.dynamic_user_group:
        provider: "{{ provider }}"
        name: "risky_contractors"
        filter: "tag.user_type.contractor and (tag.criticality.high or tag.risk_score.gt.80)"
        description: "High risk contractors"
        folder: "Security"
        tag: ["RiskManagement", "Contractors"]
        state: "present"

    - name: Update an existing dynamic user group's filter and tags
      cdot65.scm.dynamic_user_group:
        provider: "{{ provider }}"
        name: "high_risk_users"
        filter: "tag.criticality.high or tag.risk_score.gt.90"
        description: "Updated user group for high risk classification"
        folder: "Security"
        tag: ["RiskManagement", "Security", "HighPriority"]
        state: "present"

    - name: Delete a dynamic user group
      cdot65.scm.dynamic_user_group:
        provider: "{{ provider }}"
        name: "risky_contractors"
        folder: "Security"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
dynamic_user_group:
    description: Details about the dynamic user group object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "high_risk_users"
        filter: "tag.criticality.high"
        description: "Users with high risk classification"
        folder: "Security"
        tag: ["RiskManagement", "Security"]
"""


def build_dug_data(module_params):
    """
    Build dynamic user group data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant dynamic user group parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(dug_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        dug_data (dict): Dynamic user group parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [dug_data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the dynamic user group object needs to be updated.

    Args:
        existing: Existing dynamic user group object from the SCM API
        params (dict): Dynamic user group parameters with desired state from Ansible module

    Returns:
        (bool, dict): Tuple containing:
            - bool: Whether an update is needed
            - dict: Complete object data for update including all fields from the existing
                   object with any modifications from the params
    """
    changed = False

    # Start with the fields from existing object
    update_data = {
        "id": str(existing.id),  # Convert UUID to string for Pydantic
        "name": existing.name,
        "filter": existing.filter,
    }

    # Add the container field (folder, snippet, or device)
    for container in ["folder", "snippet", "device"]:
        container_value = getattr(existing, container, None)
        if container_value is not None:
            update_data[container] = container_value

    # Check each parameter that can be updated
    for param in ["description", "filter"]:
        # Set the current value as default
        current_value = getattr(existing, param, None)
        update_data[param] = current_value

        # If user provided a new value, use it and check if it's different
        if param in params and params[param] is not None:
            if current_value != params[param]:
                update_data[param] = params[param]
                changed = True

    # Handle the tag parameter specially due to Pydantic validation requirements
    # For tag, if it's None in the existing object, we need to set an empty list []
    current_tag = getattr(existing, "tag", None)
    update_data["tag"] = [] if current_tag is None else current_tag

    # If user provided a tag value, use it and check if it's different
    if "tag" in params and params["tag"] is not None:
        if current_tag != params["tag"]:
            update_data["tag"] = params["tag"]
            changed = True

    return changed, update_data


def get_existing_dug(client, dug_data):
    """
    Attempt to fetch an existing dynamic user group object.

    Args:
        client: SCM client instance
        dug_data (dict): Dynamic user group parameters to search for

    Returns:
        tuple: (bool, object) indicating if dynamic user group exists and the object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if container in dug_data and dug_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in dug_data:
            return False, None

        # Fetch the dynamic user group using the appropriate container
        existing = client.dynamic_user_group.fetch(
            name=dug_data["name"], **{container_type: dug_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the dynamic_user_group module.

    This module provides functionality to create, update, and delete dynamic user group objects
    in the SCM (Strata Cloud Manager) system. It handles tag-based filter expressions and supports
    check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=DynamicUserGroupSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        required_one_of=[["folder", "snippet", "device"]],
        required_if=[["state", "present", ["filter"], True]],
    )

    result = {"changed": False, "dynamic_user_group": None}

    try:
        client = get_scm_client(module)
        dug_data = build_dug_data(module.params)

        # Validate container is specified
        if not is_container_specified(dug_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing dynamic user group
        exists, existing_dug = get_existing_dug(client, dug_data)

        if module.params["state"] == "present":
            # Ensure filter is provided for creating/updating dynamic user groups
            if "filter" not in dug_data or dug_data["filter"] is None:
                module.fail_json(msg="Parameter 'filter' is required when state is 'present'.")

            if not exists:
                # Create new dynamic user group
                if not module.check_mode:
                    try:
                        new_dug = client.dynamic_user_group.create(data=dug_data)
                        result["dynamic_user_group"] = serialize_response(new_dug)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"A dynamic user group with name '{dug_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid dynamic user group data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_dug, dug_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = DynamicUserGroupUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_dug = client.dynamic_user_group.update(update_model)
                        result["dynamic_user_group"] = serialize_response(updated_dug)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["dynamic_user_group"] = serialize_response(existing_dug)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.dynamic_user_group.delete(str(existing_dug.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
