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
Ansible module for managing address group objects in SCM.

This module provides functionality to create, update, and delete address group objects
in the SCM (Strata Cloud Manager) system. It handles both static and dynamic address groups
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.address_group import (
    AddressGroupSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.objects import AddressGroupUpdateModel

DOCUMENTATION = r"""
---
module: address_group

short_description: Manage address group objects in SCM.

version_added: "0.1.0"

description:
    - Manage address group objects within Strata Cloud Manager (SCM).
    - Supports both static and dynamic address groups.
    - Validation is delegated to Pydantic models.
    - Ensures that exactly one of 'static' or 'dynamic' is provided.
    - Ensures that exactly one of 'folder', 'snippet', or 'device' is provided.

options:
    name:
        description: The name of the address group.
        required: true
        type: str
    description:
        description: Description of the address group.
        required: false
        type: str
    tag:
        description: List of tags associated with the address group.
        required: false
        type: list
        elements: str
    dynamic:
        description: Dynamic filter defining group membership.
        required: false
        type: dict
        suboptions:
            filter:
                description: Tag-based filter defining group membership.
                required: true
                type: str
    static:
        description: List of static addresses in the group.
        required: false
        type: list
        elements: str
    folder:
        description: The folder in which the resource is defined.
        required: false
        type: str
    snippet:
        description: The snippet in which the resource is defined.
        required: false
        type: str
    device:
        description: The device in which the resource is defined.
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
        description: Desired state of the address group object.
        required: true
        type: str
        choices:
          - present
          - absent

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
- name: Create a static address group
  cdot65.scm.address_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "Test Address Group"
    static:
      - "test_network1"
      - "test_network2"
    folder: "Shared"
    state: "present"

- name: Create a dynamic address group
  cdot65.scm.address_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "Dynamic Address Group"
    dynamic:
      filter: "'tag1' or 'tag2'"
    folder: "Shared"
    state: "present"

- name: Delete an address group
  cdot65.scm.address_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "Test Address Group"
    folder: "Shared"
    state: "absent"
"""

RETURN = r"""
address_group:
    description: Details about the address group object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Test Address Group"
        static:
          - "test_network1"
          - "test_network2"
        folder: "Shared"
"""


def build_address_group_data(module_params):
    """
    Build address group data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant address group parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(address_group_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        address_group_data (dict): Address group parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [
        address_group_data.get(container) for container in ["folder", "snippet", "device"]
    ]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the address group object needs to be updated.

    Args:
        existing: Existing address group object from the SCM API
        params (dict): Address group parameters with desired state from Ansible module

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

    # Check each parameter that can be updated
    for param in ["description"]:
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
    # If existing tag is None, use empty list to avoid Pydantic validation error
    update_data["tag"] = [] if current_tag is None else current_tag

    # If user provided a tag value, use it and check if it's different
    if "tag" in params and params["tag"] is not None:
        if current_tag != params["tag"]:
            update_data["tag"] = params["tag"]
            changed = True

    # Check and set static or dynamic address group type
    # Handle static address group
    if hasattr(existing, "static") and existing.static is not None:
        update_data["static"] = existing.static
        if "static" in params and params["static"] is not None:
            if existing.static != params["static"]:
                update_data["static"] = params["static"]
                changed = True

    # Handle dynamic address group
    if hasattr(existing, "dynamic") and existing.dynamic is not None:
        update_data["dynamic"] = {"filter": existing.dynamic.filter}
        if "dynamic" in params and params["dynamic"] is not None:
            if existing.dynamic.filter != params["dynamic"]["filter"]:
                update_data["dynamic"] = params["dynamic"]
                changed = True

    return changed, update_data


def get_existing_address_group(client, address_group_data):
    """
    Attempt to fetch an existing address group object.

    Args:
        client: SCM client instance
        address_group_data (dict): Address group parameters to search for

    Returns:
        tuple: (bool, object) indicating if address group exists and the address group object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if container in address_group_data and address_group_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in address_group_data:
            return False, None

        # Fetch the address group using the appropriate container
        existing = client.address_group.fetch(
            name=address_group_data["name"], **{container_type: address_group_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the address group object module.

    This module provides functionality to create, update, and delete address group objects
    in the SCM (Strata Cloud Manager) system. It handles both static and dynamic address groups
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=AddressGroupSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[["static", "dynamic"], ["folder", "snippet", "device"]],
        required_one_of=[["folder", "snippet", "device"]],
        required_if=[["state", "present", ["static", "dynamic"], True]],
    )

    result = {"changed": False, "address_group": None}

    try:
        client = get_scm_client(module)
        address_group_data = build_address_group_data(module.params)

        # Validate container is specified
        if not is_container_specified(address_group_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing address group
        exists, existing_address_group = get_existing_address_group(client, address_group_data)

        if module.params["state"] == "present":
            # Group type validation is now handled by required_if in the AnsibleModule definition

            if not exists:
                # Create new address group
                if not module.check_mode:
                    try:
                        new_address_group = client.address_group.create(data=address_group_data)
                        result["address_group"] = serialize_response(new_address_group)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"An address group with name '{address_group_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid address group data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_address_group, address_group_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = AddressGroupUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_address_group = client.address_group.update(update_model)
                        result["address_group"] = serialize_response(updated_address_group)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["address_group"] = serialize_response(existing_address_group)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.address_group.delete(str(existing_address_group.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
