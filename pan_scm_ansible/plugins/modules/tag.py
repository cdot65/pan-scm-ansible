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
Ansible module for managing tag objects in SCM.

This module provides functionality to create, update, and delete tag objects
in the SCM (Security Control Manager) system. It handles tag attributes
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
from scm.config.objects.tag import Tag
from scm.exceptions import NotFoundError
from scm.models.objects.tag import TagCreateModel, TagUpdateModel

DOCUMENTATION = r'''
---
module: tag

short_description: Manage tag objects in SCM.

version_added: "0.1.0"

description:
    - Manage tag objects within Strata Cloud Manager (SCM).
    - Supports creation, modification, and deletion of tag objects.
    - Ensures proper validation of tag attributes including color values.
    - Ensures that exactly one of 'folder', 'snippet', or 'device' is provided.

options:
    name:
        description: The name of the tag.
        required: true
        type: str
    color:
        description: Color associated with the tag.
        required: false
        type: str
        choices:
            - Azure Blue
            - Black
            - Blue
            - Blue Gray
            # ... (list all colors from the Colors enum)
    comments:
        description: Comments for the tag.
        required: false
        type: str
    folder:
        description: The folder where the tag is stored.
        required: false
        type: str
    snippet:
        description: The configuration snippet for the tag.
        required: false
        type: str
    device:
        description: The device where the tag is configured.
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
        description: Desired state of the tag object.
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
- name: Manage Tag Objects in Strata Cloud Manager
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
    - name: Create a new tag
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "Production"
        color: "Blue"
        comments: "Production environment tag"
        folder: "Texas"
        state: "present"

    - name: Update tag color
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "Production"
        color: "Red"
        folder: "Texas"
        state: "present"

    - name: Remove tag
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "Production"
        folder: "Texas"
        state: "absent"
'''

RETURN = r'''
tag:
    description: Details about the tag object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Production"
        color: "Blue"
        folder: "Texas"
'''


def build_tag_data(module_params):
    """
    Build tag data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant tag parameters
    """
    return {k: v for k, v in module_params.items() if k not in ['provider', 'state'] and v is not None}


def get_existing_tag(tag_api, tag_data):
    """
    Attempt to fetch an existing tag object.

    Args:
        tag_api: Tag API instance
        tag_data (dict): Tag parameters to search for

    Returns:
        tuple: (bool, object) indicating if tag exists and the tag object if found
    """
    try:
        existing = tag_api.fetch(
            name=tag_data['name'],
            folder=tag_data.get('folder'),
            snippet=tag_data.get('snippet'),
            device=tag_data.get('device'),
        )
        return True, existing
    except NotFoundError:
        return False, None


def main():
    """
    Main execution path for the tag object module.
    """
    module = AnsibleModule(
        argument_spec=ScmSpec.tag_spec(),
        supports_check_mode=True,
    )

    try:
        client = get_scm_client(module)
        tag_api = Tag(client)

        tag_data = build_tag_data(module.params)
        exists, existing_tag = get_existing_tag(
            tag_api,
            tag_data,
        )

        if module.params['state'] == 'present':
            if not exists:
                # Validate using Pydantic
                try:
                    TagCreateModel(**tag_data)
                except ValidationError as e:
                    module.fail_json(msg=str(e))

                if not module.check_mode:
                    result = tag_api.create(data=tag_data)
                    module.exit_json(
                        changed=True,
                        tag=serialize_response(result),
                    )
                module.exit_json(changed=True)
            else:
                # Compare and update if needed
                need_update = False
                for key, value in tag_data.items():
                    if hasattr(existing_tag, key) and getattr(existing_tag, key) != value:
                        need_update = True
                        break

                if need_update:
                    # Prepare update data
                    update_data = tag_data.copy()
                    update_data['id'] = str(existing_tag.id)

                    # Validate using Pydantic
                    try:
                        tag_update_model = TagUpdateModel(**update_data)
                    except ValidationError as e:
                        module.fail_json(msg=str(e))

                    if not module.check_mode:
                        result = tag_api.update(tag=tag_update_model)
                        module.exit_json(
                            changed=True,
                            tag=serialize_response(result),
                        )
                    module.exit_json(changed=True)
                else:
                    module.exit_json(
                        changed=False,
                        tag=serialize_response(existing_tag),
                    )

        elif module.params['state'] == 'absent':
            if exists:
                if not module.check_mode:
                    tag_api.delete(str(existing_tag.id))
                module.exit_json(changed=True)
            module.exit_json(changed=False)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == '__main__':
    main()
