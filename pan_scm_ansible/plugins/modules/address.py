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
in the SCM (Security Control Manager) system. It handles various address types
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec import ScmSpec  # noqa: F401
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client  # noqa: F401
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import serialize_response  # noqa: F401
from scm.config.objects.address import Address
from scm.exceptions import NotFoundError

DOCUMENTATION = r'''
---
module: address_group

short_description: Manage address group objects in SCM.

version_added: "0.1.0"

description:
    - Manage address group objects within Strata Cloud Manager (SCM).
    - Supports both static and dynamic address groups.
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
    fqdn:
        description: Fully Qualified Domain Name (FQDN) of the address.
        required: false
        type: str
    ip_netmask:
        description: IP address and netmask in CIDR notation.
        required: false
        type: str
    ip_range:
        description: IP address range in CIDR notation.
        required: false
        type: str
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
'''

EXAMPLES = r'''
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
        state: "present"

    - name: Create an address object with ip_range
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "Test_Address_Range"
        description: "An address object with ip_range"
        ip_range: "192.168.2.1-192.168.2.254"
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

    - name: Update the address object with new description
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "Test_Address_Netmask"
        description: "Updated description for netmask address"
        ip_netmask: "192.168.1.0/24"
        folder: "Texas"
        state: "present"

    - name: Clean up the address object
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "{{ item }}"
        folder: "Texas"
        state: "absent"
      loop:
        - "Test_Address_FQDN"
        - "Test_Address_Range"
        - "Test_Address_Netmask"
'''

RETURN = r'''
address:
    description: Details about the address object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Test Address"
        fqdn: "test_network2.example.com"
        folder: "Shared"
'''


def build_address_data(module_params):
    """
    Build address data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant address parameters
    """
    return {k: v for k, v in module_params.items() if k not in ['provider', 'state'] and v is not None}


def get_existing_address(address_api, address_data):
    """
    Attempt to fetch an existing address object.

    Args:
        address_api: Address API instance
        address_data (dict): Address parameters to search for

    Returns:
        tuple: (bool, object) indicating if address exists and the address object if found
    """
    try:
        existing = address_api.fetch(
            name=address_data['name'],
            folder=address_data.get('folder'),
            snippet=address_data.get('snippet'),
            device=address_data.get('device'),
        )
        return True, existing
    except NotFoundError:
        return False, None


def main():
    """
    Main execution path for the address object module.
    """
    module = AnsibleModule(
        argument_spec=ScmSpec.address_spec(),
        supports_check_mode=True,
    )

    try:
        client = get_scm_client(module)
        address_api = Address(client)

        address_data = build_address_data(module.params)
        exists, existing_address = get_existing_address(
            address_api,
            address_data,
        )

        if module.params['state'] == 'present':
            if not exists:
                if not module.check_mode:
                    result = address_api.create(data=address_data)
                    module.exit_json(
                        changed=True,
                        address=serialize_response(result),
                    )
                module.exit_json(changed=True)
            else:
                # Compare and update if needed
                need_update = False  # TODO: Implement comparison logic here
                if need_update and not module.check_mode:
                    result = address_api.update(address=existing_address)
                    module.exit_json(
                        changed=True,
                        address=serialize_response(result),
                    )
                module.exit_json(
                    changed=False,
                    address=serialize_response(existing_address),
                )

        elif module.params['state'] == 'absent':
            if exists:
                if not module.check_mode:
                    address_api.delete(str(existing_address.id))
                module.exit_json(changed=True)
            module.exit_json(changed=False)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == '__main__':
    main()
