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
Ansible module for managing service objects in SCM.

This module provides functionality to create, update, and delete service objects
in the SCM (Security Control Manager) system. It handles TCP and UDP services
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
from scm.config.objects.service import Service
from scm.exceptions import NotFoundError
from scm.models.objects.service import ServiceCreateModel, ServiceUpdateModel

DOCUMENTATION = r'''
---
module: service

short_description: Manage service objects in SCM.

version_added: "0.1.0"

description:
    - Manage service objects within Strata Cloud Manager (SCM).
    - Supports both TCP and UDP services.
    - Ensures that exactly one protocol type is configured.
    - Ensures that exactly one of 'folder', 'snippet', or 'device' is provided.

options:
    name:
        description: The name of the service.
        required: true
        type: str
    protocol:
        description: Protocol configuration (TCP or UDP).
        required: true
        type: dict
        suboptions:
            tcp:
                description: TCP protocol configuration.
                type: dict
                suboptions:
                    port:
                        description: TCP port(s) for the service.
                        type: str
                        required: true
                    override:
                        description: Override settings for TCP.
                        type: dict
                        suboptions:
                            timeout:
                                description: Connection timeout in seconds.
                                type: int
                            halfclose_timeout:
                                description: Half-close timeout in seconds.
                                type: int
                            timewait_timeout:
                                description: Time-wait timeout in seconds.
                                type: int
            udp:
                description: UDP protocol configuration.
                type: dict
                suboptions:
                    port:
                        description: UDP port(s) for the service.
                        type: str
                        required: true
                    override:
                        description: Override settings for UDP.
                        type: dict
                        suboptions:
                            timeout:
                                description: Connection timeout in seconds.
                                type: int
    description:
        description: Description of the service.
        required: false
        type: str
    tag:
        description: List of tags associated with the service.
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
        description: Desired state of the service object.
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
- name: Manage Service Objects in Strata Cloud Manager
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
    - name: Create TCP service
      cdot65.scm.service:
        provider: "{{ provider }}"
        name: "web-service"
        protocol:
          tcp:
            port: "80,443"
            override:
              timeout: 30
        description: "Web service ports"
        folder: "Texas"
        state: "present"

    - name: Create UDP service
      cdot65.scm.service:
        provider: "{{ provider }}"
        name: "dns-service"
        protocol:
          udp:
            port: "53"
        description: "DNS service"
        folder: "Texas"
        state: "present"

    - name: Update service
      cdot65.scm.service:
        provider: "{{ provider }}"
        name: "web-service"
        protocol:
          tcp:
            port: "80,443,8080"
        folder: "Texas"
        state: "present"

    - name: Remove service
      cdot65.scm.service:
        provider: "{{ provider }}"
        name: "web-service"
        folder: "Texas"
        state: "absent"
'''

RETURN = r'''
service:
    description: Details about the service object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "web-service"
        protocol:
          tcp:
            port: "80,443"
            override:
              timeout: 30
        folder: "Texas"
'''


def build_service_data(module_params):
    """
    Build service data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant service parameters
    """
    service_data = {k: v for k, v in module_params.items() if k not in ['provider', 'state', 'protocol'] and v is not None}

    # Handle protocol separately to ensure proper structure
    if 'protocol' in module_params and module_params['protocol']:
        protocol_data = {}

        # Handle TCP protocol
        if 'tcp' in module_params['protocol'] and module_params['protocol']['tcp'] is not None and module_params['protocol']['tcp'].get('port'):

            tcp_data = module_params['protocol']['tcp'].copy()
            if 'override' in tcp_data and tcp_data['override']:
                tcp_data['override'] = {
                    'timeout': tcp_data['override'].get('timeout', 3600),
                    'halfclose_timeout': tcp_data['override'].get('halfclose_timeout', 120),
                    'timewait_timeout': tcp_data['override'].get('timewait_timeout', 15),
                }
            protocol_data['tcp'] = tcp_data

        # Handle UDP protocol
        elif 'udp' in module_params['protocol'] and module_params['protocol']['udp'] is not None and module_params['protocol']['udp'].get('port'):

            udp_data = module_params['protocol']['udp'].copy()
            if 'override' in udp_data and udp_data['override']:
                udp_data['override'] = {'timeout': udp_data['override'].get('timeout', 30)}
            protocol_data['udp'] = udp_data

        # Only add protocol if we have valid data
        if protocol_data:
            service_data['protocol'] = protocol_data

    return service_data


def get_existing_service(service_api, service_data):
    """
    Attempt to fetch an existing service object.

    Args:
        service_api: Service API instance
        service_data (dict): Service parameters to search for

    Returns:
        tuple: (bool, object) indicating if service exists and the service object if found
    """
    try:
        existing = service_api.fetch(
            name=service_data['name'],
            folder=service_data.get('folder'),
            snippet=service_data.get('snippet'),
            device=service_data.get('device'),
        )
        return True, existing
    except NotFoundError:
        return False, None


def main():
    """
    Main execution path for the service object module.
    """
    module = AnsibleModule(
        argument_spec=ScmSpec.service_spec(),
        supports_check_mode=True,
        required_if=[
            ('state', 'present', ['protocol']),
        ],
        required_one_of=[['folder', 'snippet', 'device']],
    )

    try:
        client = get_scm_client(module)
        service_api = Service(client)

        # Build service data
        service_data = build_service_data(module.params)

        exists, existing_service = get_existing_service(
            service_api,
            service_data,
        )

        if module.params['state'] == 'present':
            if not exists:
                try:
                    ServiceCreateModel(**service_data)
                except ValidationError as e:
                    module.fail_json(msg=str(e))

                if not module.check_mode:
                    result = service_api.create(data=service_data)
                    module.exit_json(
                        changed=True,
                        service=serialize_response(result),
                    )
                module.exit_json(changed=True)
            else:
                # For updates, start with the existing service data
                update_data = existing_service.model_dump(exclude_unset=True)
                need_update = False

                # Update only the fields that are explicitly provided
                if 'protocol' in service_data:
                    protocol = service_data['protocol']
                    if 'tcp' in protocol and protocol['tcp']:
                        if 'port' in protocol['tcp']:
                            if update_data['protocol']['tcp']['port'] != protocol['tcp']['port']:
                                update_data['protocol']['tcp']['port'] = protocol['tcp']['port']
                                need_update = True
                    elif 'udp' in protocol and protocol['udp']:
                        if 'port' in protocol['udp']:
                            if update_data['protocol']['udp']['port'] != protocol['udp']['port']:
                                update_data['protocol']['udp']['port'] = protocol['udp']['port']
                                need_update = True

                # Handle other fields
                for field in ['description', 'tag']:
                    if field in service_data and service_data[field] != getattr(existing_service, field):
                        update_data[field] = service_data[field]
                        need_update = True

                if need_update:
                    try:
                        service_update_model = ServiceUpdateModel(**update_data)
                    except ValidationError as e:
                        module.fail_json(msg=str(e))

                    if not module.check_mode:
                        result = service_api.update(service=service_update_model)
                        module.exit_json(
                            changed=True,
                            service=serialize_response(result),
                        )
                    module.exit_json(changed=True)
                else:
                    module.exit_json(
                        changed=False,
                        service=serialize_response(existing_service),
                    )

        elif module.params['state'] == 'absent':
            if exists:
                if not module.check_mode:
                    service_api.delete(str(existing_service.id))
                module.exit_json(changed=True)
            module.exit_json(changed=False)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == '__main__':
    main()
