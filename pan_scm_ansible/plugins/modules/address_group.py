# ansible_collections/cdot65/scm/plugins/modules/address_group.py

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
Ansible module for managing address group objects in SCM.

This module provides functionality to create, update, and delete address group objects
in the SCM (Security Control Manager) system. It handles both static and dynamic address groups
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec import ScmSpec  # noqa: F401
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client  # noqa: F401
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import serialize_response  # noqa: F401
from pydantic import ValidationError
from scm.config.objects.address_group import AddressGroup
from scm.exceptions import NotFoundError
from scm.models.objects.address_group import AddressGroupCreateModel, AddressGroupUpdateModel

DOCUMENTATION = r'''
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
'''

EXAMPLES = r'''
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
'''

RETURN = r'''
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
'''


def build_address_group_data(module_params):
    """
    Build address group data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant address group parameters
    """
    return {k: v for k, v in module_params.items() if k not in ['provider', 'state'] and v is not None}


def get_existing_address_group(address_group_api, address_group_data):
    """
    Attempt to fetch an existing address group object.

    Args:
        address_group_api: AddressGroup API instance
        address_group_data (dict): Address group parameters to search for

    Returns:
        tuple: (bool, object) indicating if address group exists and the address group object if found
    """
    try:
        existing = address_group_api.fetch(
            name=address_group_data['name'],
            folder=address_group_data.get('folder'),
            snippet=address_group_data.get('snippet'),
            device=address_group_data.get('device'),
        )
        return True, existing
    except NotFoundError:
        return False, None


def main():
    """
    Main execution path for the address group object module.
    """
    module = AnsibleModule(
        argument_spec=ScmSpec.address_group_spec(),
        supports_check_mode=True,
    )

    try:
        client = get_scm_client(module)
        address_group_api = AddressGroup(client)

        address_group_data = build_address_group_data(module.params)

        exists, existing_address_group = get_existing_address_group(
            address_group_api,
            address_group_data,
        )

        if module.params['state'] == 'present':
            if not exists:
                # Validate using Pydantic
                try:
                    AddressGroupCreateModel(**address_group_data)
                except ValidationError as e:
                    module.fail_json(msg=str(e))

                if not module.check_mode:
                    result = address_group_api.create(data=address_group_data)
                    module.exit_json(
                        changed=True,
                        address_group=serialize_response(result),
                    )
                module.exit_json(changed=True)
            else:
                # Compare and update if needed
                need_update = False
                # Implement comparison logic to determine if update is needed
                # Compare existing attributes with desired attributes
                if existing_address_group.description != address_group_data.get('description'):
                    need_update = True
                if existing_address_group.tag != address_group_data.get('tag'):
                    need_update = True
                if existing_address_group.static != address_group_data.get('static'):
                    need_update = True
                if existing_address_group.dynamic != address_group_data.get('dynamic'):
                    need_update = True

                if need_update:
                    # Prepare update data
                    update_data = address_group_data.copy()
                    update_data['id'] = str(existing_address_group.id)
                    # Validate using Pydantic
                    try:
                        address_group_update_model = AddressGroupUpdateModel(**update_data)
                    except ValidationError as e:
                        module.fail_json(msg=str(e))

                    if not module.check_mode:
                        result = address_group_api.update(address_group=address_group_update_model)
                        module.exit_json(
                            changed=True,
                            address_group=serialize_response(result),
                        )
                    module.exit_json(changed=True)
                else:
                    module.exit_json(
                        changed=False,
                        address_group=serialize_response(existing_address_group),
                    )

        elif module.params['state'] == 'absent':
            if exists:
                if not module.check_mode:
                    address_group_api.delete(str(existing_address_group.id))
                module.exit_json(changed=True)
            module.exit_json(changed=False)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == '__main__':
    main()
