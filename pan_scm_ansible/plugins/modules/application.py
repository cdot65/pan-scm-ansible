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
Ansible module for managing application objects in SCM.

This module provides functionality to create, update, and delete application objects
in the SCM (Security Control Manager) system. It handles various application attributes
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
from scm.config.objects.application import Application
from scm.exceptions import NotFoundError
from scm.models.objects.application import ApplicationCreateModel, ApplicationUpdateModel

DOCUMENTATION = r'''
---
module: application

short_description: Manage application objects in SCM.

version_added: "0.1.0"

description:
    - Manage application objects within Strata Cloud Manager (SCM).
    - Supports creation, modification, and deletion of application objects.
    - Ensures proper validation of application attributes.
    - Ensures that exactly one of 'folder' or 'snippet' is provided.

options:
    name:
        description: The name of the application.
        required: true
        type: str
    category:
        description: High-level category to which the application belongs.
        required: true
        type: str
    subcategory:
        description: Specific sub-category within the high-level category.
        required: true
        type: str
    technology:
        description: The underlying technology utilized by the application.
        required: true
        type: str
    risk:
        description: The risk level associated with the application (1-5).
        required: true
        type: int
    description:
        description: Description for the application.
        required: false
        type: str
    ports:
        description: List of TCP/UDP ports associated with the application.
        required: false
        type: list
        elements: str
    folder:
        description: The folder where the application configuration is stored.
        required: false
        type: str
    snippet:
        description: The configuration snippet for the application.
        required: false
        type: str
    evasive:
        description: Indicates if the application uses evasive techniques.
        required: false
        type: bool
        default: false
    pervasive:
        description: Indicates if the application is widely used.
        required: false
        type: bool
        default: false
    excessive_bandwidth_use:
        description: Indicates if the application uses excessive bandwidth.
        required: false
        type: bool
        default: false
    used_by_malware:
        description: Indicates if the application is commonly used by malware.
        required: false
        type: bool
        default: false
    transfers_files:
        description: Indicates if the application transfers files.
        required: false
        type: bool
        default: false
    has_known_vulnerabilities:
        description: Indicates if the application has known vulnerabilities.
        required: false
        type: bool
        default: false
    tunnels_other_apps:
        description: Indicates if the application tunnels other applications.
        required: false
        type: bool
        default: false
    prone_to_misuse:
        description: Indicates if the application is prone to misuse.
        required: false
        type: bool
        default: false
    no_certifications:
        description: Indicates if the application lacks certifications.
        required: false
        type: bool
        default: false
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
        description: Desired state of the application object.
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
- name: Manage Application Objects in Strata Cloud Manager
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
    - name: Create a custom application
      cdot65.scm.application:
        provider: "{{ provider }}"
        name: "custom-app"
        category: "business-systems"
        subcategory: "database"
        technology: "client-server"
        risk: 3
        description: "Custom database application"
        ports: 
          - "tcp/1521"
        folder: "Texas"
        transfers_files: true
        state: "present"

    - name: Update application risk level
      cdot65.scm.application:
        provider: "{{ provider }}"
        name: "custom-app"
        category: "business-systems"
        subcategory: "database"
        technology: "client-server"
        risk: 4
        folder: "Texas"
        has_known_vulnerabilities: true
        state: "present"

    - name: Remove application
      cdot65.scm.application:
        provider: "{{ provider }}"
        name: "custom-app"
        folder: "Texas"
        state: "absent"
'''

RETURN = r'''
application:
    description: Details about the application object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "custom-app"
        category: "business-systems"
        subcategory: "database"
        technology: "client-server"
        risk: 3
        folder: "Texas"
'''


def build_application_data(module_params):
    """
    Build application data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant application parameters
    """
    return {k: v for k, v in module_params.items() if k not in ['provider', 'state'] and v is not None}


def get_existing_application(application_api, application_data):
    """
    Attempt to fetch an existing application object.

    Args:
        application_api: Application API instance
        application_data (dict): Application parameters to search for

    Returns:
        tuple: (bool, object) indicating if application exists and the application object if found
    """
    try:
        existing = application_api.fetch(
            name=application_data['name'],
            folder=application_data.get('folder'),
            snippet=application_data.get('snippet'),
        )
        return True, existing
    except NotFoundError:
        return False, None


def main():
    """
    Main execution path for the application object module.
    """
    module = AnsibleModule(
        argument_spec=ScmSpec.application_spec(),
        supports_check_mode=True,
        required_if=[
            ('state', 'present', ['category', 'subcategory', 'technology', 'risk']),
        ],
    )

    try:
        client = get_scm_client(module)
        application_api = Application(client)

        application_data = build_application_data(module.params)
        exists, existing_application = get_existing_application(
            application_api,
            application_data,
        )

        if module.params['state'] == 'present':
            if not exists:
                # Validate using Pydantic
                try:
                    ApplicationCreateModel(**application_data)
                except ValidationError as e:
                    module.fail_json(msg=str(e))

                if not module.check_mode:
                    result = application_api.create(data=application_data)
                    module.exit_json(
                        changed=True,
                        application=serialize_response(result),
                    )
                module.exit_json(changed=True)
            else:
                # Compare and update if needed
                need_update = False
                for key, value in application_data.items():
                    if hasattr(existing_application, key) and getattr(existing_application, key) != value:
                        need_update = True
                        break

                if need_update:
                    # Prepare update data
                    update_data = application_data.copy()
                    update_data['id'] = str(existing_application.id)

                    # Validate using Pydantic
                    try:
                        application_update_model = ApplicationUpdateModel(**update_data)
                    except ValidationError as e:
                        module.fail_json(msg=str(e))

                    if not module.check_mode:
                        result = application_api.update(application=application_update_model)
                        module.exit_json(
                            changed=True,
                            application=serialize_response(result),
                        )
                    module.exit_json(changed=True)
                else:
                    module.exit_json(
                        changed=False,
                        application=serialize_response(existing_application),
                    )

        elif module.params['state'] == 'absent':
            if exists:
                if not module.check_mode:
                    application_api.delete(str(existing_application.id))
                module.exit_json(changed=True)
            module.exit_json(changed=False)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == '__main__':
    main()
