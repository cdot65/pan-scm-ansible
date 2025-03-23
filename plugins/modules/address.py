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
Ansible module for managing address objects in SCM.

This module provides functionality to create, update, and delete address objects
in the SCM (Strata Cloud Manager) system. It handles various address types
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.address import AddressSpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.objects import AddressUpdateModel

DOCUMENTATION = r"""
---
module: address

short_description: Manage address objects in SCM.

version_added: "0.1.0"

description:
    - Manage address objects within Strata Cloud Manager (SCM).
    - Create, update, and delete address objects of various types including IP/Netmask, IP Range, IP Wildcard, and FQDN.
    - Ensures that exactly one address type (ip_netmask, ip_range, ip_wildcard, fqdn) is provided for create/update operations.
    - Ensures that exactly one container type (folder, snippet, device) is provided.

options:
    name:
        description: The name of the address object (max 63 chars).
        required: true
        type: str
    description:
        description: Description of the address object (max 1023 chars).
        required: false
        type: str
    tag:
        description: List of tags associated with the address object (max 64 chars each).
        required: false
        type: list
        elements: str
    fqdn:
        description: Fully Qualified Domain Name (FQDN) of the address (max 255 chars).
        required: false
        type: str
    ip_netmask:
        description: IP address with CIDR notation (e.g. "192.168.1.0/24").
        required: false
        type: str
    ip_range:
        description: IP address range (e.g. "192.168.1.100-192.168.1.200").
        required: false
        type: str
    ip_wildcard:
        description: IP wildcard mask format (e.g. "10.20.1.0/0.0.248.255").
        required: false
        type: str
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
        description: Desired state of the address object.
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
- name: Manage Address Objects in Strata Cloud Manager
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

    - name: Create an address object with ip_netmask
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "Test_Address_Netmask"
        description: "An address object with ip_netmask"
        ip_netmask: "192.168.1.0/24"
        folder: "Texas"
        tag: ["Network", "Internal"]
        state: "present"

    - name: Create an address object with ip_range
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "Test_Address_Range"
        description: "An address object with ip_range"
        ip_range: "192.168.2.1-192.168.2.254"
        folder: "Texas"
        state: "present"

    - name: Create an address object with ip_wildcard
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "Test_Address_Wildcard"
        description: "An address object with ip_wildcard"
        ip_wildcard: "10.20.1.0/0.0.248.255"
        folder: "Texas"
        state: "present"

    - name: Create an address object with fqdn
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "Test_Address_FQDN"
        description: "An address object with fqdn"
        fqdn: "example.com"
        folder: "Texas"
        state: "present"

    - name: Update an address object with new description and tags
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "Test_Address_Netmask"
        description: "Updated description for netmask address"
        ip_netmask: "192.168.1.0/24"
        folder: "Texas"
        tag: ["Network", "Internal", "Updated"]
        state: "present"

    - name: Delete address object
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "Test_Address_FQDN"
        folder: "Texas"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
address:
    description: Details about the address object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Test_Address_Netmask"
        description: "An address object with ip_netmask"
        ip_netmask: "192.168.1.0/24"
        folder: "Texas"
        tag: ["Network", "Internal"]
"""


def build_address_data(module_params):
    """
    Build address data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant address parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(address_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        address_data (dict): Address parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [address_data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def is_address_type_specified(address_data):
    """
    Check if exactly one address type is specified.

    Args:
        address_data (dict): Address parameters

    Returns:
        bool: True if exactly one address type is specified, False otherwise
    """
    address_types = [
        address_data.get(addr_type)
        for addr_type in ["ip_netmask", "ip_range", "ip_wildcard", "fqdn"]
    ]
    return sum(addr_type is not None for addr_type in address_types) == 1


def needs_update(existing, params):
    """
    Determine if the address object needs to be updated.

    Args:
        existing: Existing address object from the SCM API
        params (dict): Address parameters with desired state from Ansible module

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

    # Check and set address type parameter
    # Only one address type will be set due to mutual exclusivity
    for addr_type in ["ip_netmask", "ip_range", "ip_wildcard", "fqdn"]:
        current_value = getattr(existing, addr_type, None)

        # Set the current address type value
        if current_value is not None:
            update_data[addr_type] = current_value

        # If user provided this address type, check if it needs updating
        if addr_type in params and params[addr_type] is not None:
            if current_value != params[addr_type]:
                update_data[addr_type] = params[addr_type]
                changed = True

    return changed, update_data


def get_existing_address(client, address_data):
    """
    Attempt to fetch an existing address object.

    Args:
        client: SCM client instance
        address_data (dict): Address parameters to search for

    Returns:
        tuple: (bool, object) indicating if address exists and the address object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if container in address_data and address_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in address_data:
            return False, None

        # Fetch the address using the appropriate container
        existing = client.address.fetch(
            name=address_data["name"], **{container_type: address_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the address object module.

    This module provides functionality to create, update, and delete address objects
    in the SCM (Strata Cloud Manager) system. It handles various address types
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=AddressSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["ip_netmask", "ip_range", "ip_wildcard", "fqdn"],
            ["folder", "snippet", "device"],
        ],
        required_one_of=[["folder", "snippet", "device"]],
        required_if=[["state", "present", ["ip_netmask", "ip_range", "ip_wildcard", "fqdn"], True]],
    )

    result = {"changed": False, "address": None}

    try:
        client = get_scm_client(module)
        address_data = build_address_data(module.params)

        # Validate container is specified
        if not is_container_specified(address_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing address
        exists, existing_address = get_existing_address(client, address_data)

        if module.params["state"] == "present":
            # Address type validation is now handled by required_if in the AnsibleModule definition

            if not exists:
                # Create new address
                if not module.check_mode:
                    try:
                        new_address = client.address.create(data=address_data)
                        result["address"] = serialize_response(new_address)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"An address with name '{address_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid address data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_address, address_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = AddressUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_address = client.address.update(update_model)
                        result["address"] = serialize_response(updated_address)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["address"] = serialize_response(existing_address)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.address.delete(str(existing_address.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
