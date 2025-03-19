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
Ansible module for managing anti-spyware profile objects in SCM.

This module provides functionality to create, update, and delete anti-spyware profile objects
in the SCM (Security Control Manager) system. It handles various profile attributes
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
from scm.config.security.anti_spyware_profile import AntiSpywareProfile
from scm.exceptions import NotFoundError
from scm.models.security.anti_spyware_profiles import (
    AntiSpywareProfileCreateModel,
    AntiSpywareProfileUpdateModel,
)

DOCUMENTATION = r'''
---
module: anti_spyware_profile

short_description: Manage anti-spyware profile objects in SCM.

version_added: "0.1.0"

description:
    - Manage anti-spyware profile objects within Strata Cloud Manager (SCM).
    - Supports creation, modification, and deletion of anti-spyware profiles.
    - Ensures proper validation of profile attributes.
    - Ensures that exactly one of 'folder', 'snippet', or 'device' is provided.

options:
    name:
        description: The name of the anti-spyware profile.
        required: true
        type: str
    description:
        description: Description of the profile.
        required: false
        type: str
    cloud_inline_analysis:
        description: Enable cloud inline analysis.
        required: false
        type: bool
        default: false
    inline_exception_edl_url:
        description: List of inline exception EDL URLs.
        required: false
        type: list
        elements: str
    inline_exception_ip_address:
        description: List of inline exception IP addresses.
        required: false
        type: list
        elements: str
    mica_engine_spyware_enabled:
        description: List of MICA engine spyware enabled entries.
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: Name of the MICA engine spyware detector.
                required: true
                type: str
            inline_policy_action:
                description: Inline policy action.
                required: false
                type: str
                choices: ['alert', 'allow', 'drop', 'reset-both', 'reset-client', 'reset-server']
                default: 'alert'
    rules:
        description: List of anti-spyware rules.
        required: true
        type: list
        elements: dict
        suboptions:
            name:
                description: Rule name.
                required: true
                type: str
            severity:
                description: List of severities.
                required: true
                type: list
                elements: str
                choices: ['critical', 'high', 'medium', 'low', 'informational', 'any']
            category:
                description: Rule category.
                required: true
                type: str
            threat_name:
                description: Threat name.
                required: false
                type: str
            packet_capture:
                description: Packet capture setting.
                required: false
                type: str
                choices: ['disable', 'single-packet', 'extended-capture']
    threat_exception:
        description: List of threat exceptions.
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: Threat exception name.
                required: true
                type: str
            packet_capture:
                description: Packet capture setting.
                required: true
                type: str
                choices: ['disable', 'single-packet', 'extended-capture']
            exempt_ip:
                description: List of exempt IP entries.
                required: false
                type: list
                elements: dict
                suboptions:
                    name:
                        description: Exempt IP name.
                        required: true
                        type: str
            notes:
                description: Notes for the threat exception.
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
        description: Desired state of the anti-spyware profile.
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
- name: Manage Anti-Spyware Profiles in Strata Cloud Manager
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
    - name: Create anti-spyware profile
      cdot65.scm.anti_spyware_profile:
        provider: "{{ provider }}"
        name: "Custom-Spyware-Profile"
        description: "Custom anti-spyware profile"
        cloud_inline_analysis: true
        rules:
          - name: "Block-Critical-Threats"
            severity: ["critical"]
            category: "spyware"
            packet_capture: "single-packet"
        folder: "Production"
        state: "present"

    - name: Update anti-spyware profile
      cdot65.scm.anti_spyware_profile:
        provider: "{{ provider }}"
        name: "Custom-Spyware-Profile"
        description: "Updated anti-spyware profile"
        rules:
          - name: "Block-Critical-Threats"
            severity: ["critical", "high"]
            category: "spyware"
            packet_capture: "extended-capture"
        folder: "Production"
        state: "present"

    - name: Remove anti-spyware profile
      cdot65.scm.anti_spyware_profile:
        provider: "{{ provider }}"
        name: "Custom-Spyware-Profile"
        folder: "Production"
        state: "absent"
'''

RETURN = r'''
anti_spyware_profile:
    description: Details about the anti-spyware profile object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Custom-Spyware-Profile"
        description: "Custom anti-spyware profile"
        cloud_inline_analysis: true
        rules:
          - name: "Block-Critical-Threats"
            severity: ["critical"]
            category: "spyware"
            packet_capture: "single-packet"
        folder: "Production"
'''


def build_profile_data(module_params):
    """
    Build profile data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant profile parameters
    """
    return {k: v for k, v in module_params.items() if k not in ['provider', 'state'] and v is not None}


def get_existing_profile(profile_api, profile_data):
    """
    Attempt to fetch an existing anti-spyware profile object.

    Args:
        profile_api: AntiSpywareProfile API instance
        profile_data (dict): Profile parameters to search for

    Returns:
        tuple: (bool, object) indicating if profile exists and the profile object if found
    """
    try:
        existing = profile_api.fetch(
            name=profile_data['name'],
            folder=profile_data.get('folder'),
            snippet=profile_data.get('snippet'),
            device=profile_data.get('device'),
        )
        return True, existing
    except NotFoundError:
        return False, None


def main():
    """
    Main execution path for the anti-spyware profile module.
    """
    module = AnsibleModule(
        argument_spec=ScmSpec.anti_spyware_profile_spec(),
        supports_check_mode=True,
        required_if=[
            ('state', 'present', ['rules']),
        ],
    )

    try:
        client = get_scm_client(module)
        profile_api = AntiSpywareProfile(client)

        profile_data = build_profile_data(module.params)
        exists, existing_profile = get_existing_profile(
            profile_api,
            profile_data,
        )

        if module.params['state'] == 'present':
            if not exists:
                # Validate using Pydantic
                try:
                    AntiSpywareProfileCreateModel(**profile_data)
                except ValidationError as e:
                    module.fail_json(msg=str(e))

                if not module.check_mode:
                    result = profile_api.create(data=profile_data)
                    module.exit_json(
                        changed=True,
                        anti_spyware_profile=serialize_response(result),
                    )
                module.exit_json(changed=True)
            else:
                # Compare and update if needed
                need_update = False
                for key, value in profile_data.items():
                    if hasattr(existing_profile, key) and getattr(existing_profile, key) != value:
                        need_update = True
                        break

                if need_update:
                    # Prepare update data
                    update_data = profile_data.copy()
                    update_data['id'] = str(existing_profile.id)

                    # Validate using Pydantic
                    try:
                        profile_update_model = AntiSpywareProfileUpdateModel(**update_data)
                    except ValidationError as e:
                        module.fail_json(msg=str(e))

                    if not module.check_mode:
                        result = profile_api.update(profile=profile_update_model)
                        module.exit_json(
                            changed=True,
                            anti_spyware_profile=serialize_response(result),
                        )
                    module.exit_json(changed=True)
                else:
                    module.exit_json(
                        changed=False,
                        anti_spyware_profile=serialize_response(existing_profile),
                    )

        elif module.params['state'] == 'absent':
            if exists:
                if not module.check_mode:
                    profile_api.delete(str(existing_profile.id))
                module.exit_json(changed=True)
            module.exit_json(changed=False)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == '__main__':
    main()
