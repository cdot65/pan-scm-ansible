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
Ansible module for managing application group objects in SCM.

This module provides functionality to create, update, and delete application group objects
in the SCM (Security Control Manager) system. It handles application group membership
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
from scm.config.objects.application_group import ApplicationGroup
from scm.exceptions import NotFoundError
from scm.models.objects.application_group import ApplicationGroupCreateModel, ApplicationGroupUpdateModel

DOCUMENTATION = r'''
---
module: application_group

short_description: Manage application group objects in SCM.

version_added: "0.1.0"

description:
    - Manage application group objects within Strata Cloud Manager (SCM).
    - Supports creation, modification, and deletion of application groups.
    - Ensures proper validation of group membership.
    - Ensures that exactly one of 'folder', 'snippet', or 'device' is provided.

options:
    name:
        description: The name of the application group.
        required: true
        type: str
    members:
        description: List of application / group / filter names.
        required: true
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
        description: Desired state of the application group object.
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
- name: Manage Application Groups in Strata Cloud Manager
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
    - name: Create web applications group
      cdot65.scm.application_group:
        provider: "{{ provider }}"
        name: "web-apps"
        members:
          - "ssl"
          - "web-browsing"
        folder: "Texas"
        state: "present"

    - name: Update web applications group membership
      cdot65.scm.application_group:
        provider: "{{ provider }}"
        name: "web-apps"
        members:
          - "ssl"
          - "web-browsing"
          - "dns-base"
        folder: "Texas"
        state: "present"

    - name: Remove application group
      cdot65.scm.application_group:
        provider: "{{ provider }}"
        name: "web-apps"
        folder: "Texas"
        state: "absent"
'''

RETURN = r'''
application_group:
    description: Details about the application group object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "web-apps"
        members:
          - "ssl"
          - "web-browsing"
        folder: "Texas"
'''


def build_application_group_data(module_params):
    """
    Build application group data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant application group parameters
    """
    return {k: v for k, v in module_params.items() if k not in ['provider', 'state'] and v is not None}


def get_existing_application_group(application_group_api, application_group_data):
    """
    Attempt to fetch an existing application group object.

    Args:
        application_group_api: ApplicationGroup API instance
        application_group_data (dict): Application group parameters to search for

    Returns:
        tuple: (bool, object) indicating if application group exists and the group object if found
    """
    try:
        existing = application_group_api.fetch(
            name=application_group_data['name'],
            folder=application_group_data.get('folder'),
            snippet=application_group_data.get('snippet'),
            device=application_group_data.get('device'),
        )
        return True, existing
    except NotFoundError:
        return False, None


def main():
    """
    Main execution path for the application group object module.
    """
    module = AnsibleModule(
        argument_spec=ScmSpec.application_group_spec(),
        supports_check_mode=True,
        required_if=[('state', 'present', ['members'])],
    )

    try:
        client = get_scm_client(module)
        application_group_api = ApplicationGroup(client)

        application_group_data = build_application_group_data(module.params)
        exists, existing_group = get_existing_application_group(
            application_group_api,
            application_group_data,
        )

        if module.params['state'] == 'present':
            if not exists:
                # Validate using Pydantic
                try:
                    ApplicationGroupCreateModel(**application_group_data)
                except ValidationError as e:
                    module.fail_json(msg=str(e))

                if not module.check_mode:
                    result = application_group_api.create(data=application_group_data)
                    module.exit_json(
                        changed=True,
                        application_group=serialize_response(result),
                    )
                module.exit_json(changed=True)
            else:
                # Compare and update if needed
                need_update = False
                if sorted(existing_group.members) != sorted(application_group_data.get('members', [])):
                    need_update = True

                if need_update:
                    # Prepare update data
                    update_data = application_group_data.copy()
                    update_data['id'] = str(existing_group.id)

                    # Validate using Pydantic
                    try:
                        application_group_update_model = ApplicationGroupUpdateModel(**update_data)
                    except ValidationError as e:
                        module.fail_json(msg=str(e))

                    if not module.check_mode:
                        result = application_group_api.update(app_group=application_group_update_model)
                        module.exit_json(
                            changed=True,
                            application_group=serialize_response(result),
                        )
                    module.exit_json(changed=True)
                else:
                    module.exit_json(
                        changed=False,
                        application_group=serialize_response(existing_group),
                    )

        elif module.params['state'] == 'absent':
            if exists:
                if not module.check_mode:
                    application_group_api.delete(str(existing_group.id))
                module.exit_json(changed=True)
            module.exit_json(changed=False)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == '__main__':
    main()
