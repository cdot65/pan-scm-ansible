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
in the SCM (Security Control Manager) system. It handles service group members
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
from scm.config.objects.service_group import ServiceGroup
from scm.exceptions import NotFoundError
from scm.models.objects.service_group import ServiceGroupCreateModel, ServiceGroupUpdateModel

DOCUMENTATION = r'''
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
        description: The name of the service group.
        required: true
        type: str
    members:
        description: List of service objects that are members of this group.
        required: true
        type: list
        elements: str
    tag:
        description: List of tags associated with the service group.
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
                no_log: true
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
'''

EXAMPLES = r'''
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
    - name: Create a service group
      cdot65.scm.service_group:
        provider: "{{ provider }}"
        name: "web-services"
        members:
          - "HTTP"
          - "HTTPS"
          - "SSH"
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
          - "HTTP"
          - "HTTPS"
          - "SSH"
          - "FTP"
        folder: "Texas"
        state: "present"

    - name: Remove service group
      cdot65.scm.service_group:
        provider: "{{ provider }}"
        name: "web-services"
        folder: "Texas"
        state: "absent"
'''

RETURN = r'''
service_group:
    description: Details about the service group object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "web-services"
        members:
          - "HTTP"
          - "HTTPS"
          - "SSH"
        folder: "Texas"
'''


def build_service_group_data(module_params):
    """
    Build service group data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant service group parameters
    """
    return {k: v for k, v in module_params.items() if k not in ['provider', 'state'] and v is not None}


def get_existing_service_group(service_group_api, service_group_data):
    """
    Attempt to fetch an existing service group object.

    Args:
        service_group_api: ServiceGroup API instance
        service_group_data (dict): Service group parameters to search for

    Returns:
        tuple: (bool, object) indicating if service group exists and the service group object if found
    """
    try:
        existing = service_group_api.fetch(
            name=service_group_data['name'],
            folder=service_group_data.get('folder'),
            snippet=service_group_data.get('snippet'),
            device=service_group_data.get('device'),
        )
        return True, existing
    except NotFoundError:
        return False, None


def main():
    """
    Main execution path for the service group object module.
    """
    module = AnsibleModule(
        argument_spec=ScmSpec.service_group_spec(),
        supports_check_mode=True,
        required_if=[
            ('state', 'present', ['members']),
        ],
    )

    try:
        client = get_scm_client(module)
        service_group_api = ServiceGroup(client)

        service_group_data = build_service_group_data(module.params)
        exists, existing_service_group = get_existing_service_group(
            service_group_api,
            service_group_data,
        )

        if module.params['state'] == 'present':
            if not exists:
                # Validate using Pydantic
                try:
                    ServiceGroupCreateModel(**service_group_data)
                except ValidationError as e:
                    module.fail_json(msg=str(e))

                if not module.check_mode:
                    result = service_group_api.create(data=service_group_data)
                    module.exit_json(
                        changed=True,
                        service_group=serialize_response(result),
                    )
                module.exit_json(changed=True)
            else:
                # Compare and update if needed
                need_update = False
                if set(existing_service_group.members) != set(service_group_data.get('members', [])):
                    need_update = True
                if existing_service_group.tag != service_group_data.get('tag'):
                    need_update = True

                if need_update:
                    # Prepare update data
                    update_data = service_group_data.copy()
                    update_data['id'] = str(existing_service_group.id)

                    # Validate using Pydantic
                    try:
                        service_group_update_model = ServiceGroupUpdateModel(**update_data)
                    except ValidationError as e:
                        module.fail_json(msg=str(e))

                    if not module.check_mode:
                        result = service_group_api.update(service_group=service_group_update_model)
                        module.exit_json(
                            changed=True,
                            service_group=serialize_response(result),
                        )
                    module.exit_json(changed=True)
                else:
                    module.exit_json(
                        changed=False,
                        service_group=serialize_response(existing_service_group),
                    )

        elif module.params['state'] == 'absent':
            if exists:
                if not module.check_mode:
                    service_group_api.delete(str(existing_service_group.id))
                module.exit_json(changed=True)
            module.exit_json(changed=False)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == '__main__':
    main()
