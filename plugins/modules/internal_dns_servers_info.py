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
Ansible module for gathering information about internal DNS servers in SCM.

This module provides functionality to retrieve information about internal DNS server objects
in the SCM (Strata Cloud Manager) system with various filtering options.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.internal_dns_servers_info import (
    InternalDnsServersInfoSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError

DOCUMENTATION = r"""
---
module: internal_dns_servers_info

short_description: Gather information about internal DNS servers in SCM.

version_added: "0.1.0"

description:
    - Gather information about internal DNS server objects within Strata Cloud Manager (SCM).
    - Supports retrieving a specific DNS server by name or listing all DNS servers.
    - Returns detailed information about each DNS server object including domain names,
      primary and secondary DNS server addresses.
    - This is an info module that only retrieves information and does not modify anything.

options:
    name:
        description: The name of a specific internal DNS server object to retrieve.
        required: false
        type: str
    gather_subset:
        description:
            - Determines which information to gather about DNS servers.
            - C(all) gathers everything.
            - C(config) is the default which retrieves basic configuration.
        type: list
        elements: str
        default: ['config']
        choices: ['all', 'config']
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

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
---
- name: Gather Internal DNS Server Information in Strata Cloud Manager
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

    - name: Get information about a specific DNS server
      cdot65.scm.internal_dns_servers_info:
        provider: "{{ provider }}"
        name: "main-dns-server"
      register: dns_server_info

    - name: List all internal DNS servers
      cdot65.scm.internal_dns_servers_info:
        provider: "{{ provider }}"
      register: all_dns_servers
"""

RETURN = r"""
internal_dns_servers:
    description: List of internal DNS server objects (returned when name is not specified).
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "main-dns-server"
        domain_name: ["example.com", "internal.example.com"]
        primary: "192.168.1.10"
        secondary: "192.168.1.11"
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "backup-dns-server"
        domain_name: ["backup.example.com"]
        primary: "192.168.2.10"
        secondary: "192.168.2.11"
internal_dns_server:
    description: Information about the requested internal DNS server (returned when name is specified).
    returned: success, when name is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "main-dns-server"
        domain_name: ["example.com", "internal.example.com"]
        primary: "192.168.1.10"
        secondary: "192.168.1.11"
"""


def main():
    """
    Main execution path for the internal_dns_servers_info module.

    This module provides functionality to gather information about internal DNS server objects
    in the SCM (Strata Cloud Manager) system.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=InternalDnsServersInfoSpec.spec(),
        supports_check_mode=True,
    )

    result = {}

    try:
        client = get_scm_client(module)

        # Check if we're fetching a specific DNS server by name
        if module.params.get("name"):
            name = module.params["name"]

            try:
                # Fetch a specific DNS server
                dns_server = client.internal_dns_server.fetch(name=name)

                # Serialize response for Ansible output
                result["internal_dns_server"] = serialize_response(dns_server)

            except ObjectNotPresentError:
                module.fail_json(msg=f"Internal DNS server with name '{name}' not found")
            except (MissingQueryParameterError, InvalidObjectError) as e:
                module.fail_json(msg=str(e))

        else:
            # List all DNS servers
            try:
                dns_servers = client.internal_dns_server.list()

                # Serialize response for Ansible output
                result["internal_dns_servers"] = [
                    serialize_response(dns_server) for dns_server in dns_servers
                ]

            except MissingQueryParameterError as e:
                module.fail_json(msg=f"Missing required parameter: {str(e)}")
            except InvalidObjectError as e:
                module.fail_json(msg=f"Invalid parameters: {str(e)}")

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
