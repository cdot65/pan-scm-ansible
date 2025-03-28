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
Ansible module for gathering information about syslog server profile objects in SCM.

This module provides functionality to retrieve information about syslog server profile objects
in the SCM (Strata Cloud Manager) system with various filtering options.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.syslog_server_profiles_info import (
    SyslogServerProfilesInfoSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError

DOCUMENTATION = r"""
---
module: syslog_server_profiles_info

short_description: Gather information about syslog server profile objects in SCM.

version_added: "0.1.0"

description:
    - Gather information about syslog server profile objects within Strata Cloud Manager (SCM).
    - Supports retrieving a specific syslog server profile by name or listing profiles with various filters.
    - Provides additional client-side filtering capabilities for exact matches, exclusions, and transport protocols.
    - Returns detailed information about each syslog server profile object.
    - This is an info module that only retrieves information and does not modify anything.

options:
    name:
        description: The name of a specific syslog server profile to retrieve.
        required: false
        type: str
    gather_subset:
        description:
            - Determines which information to gather about syslog server profiles.
            - C(all) gathers everything.
            - C(config) is the default which retrieves basic configuration.
        type: list
        elements: str
        default: ['config']
        choices: ['all', 'config']
    folder:
        description: Filter syslog server profiles by folder container.
        required: false
        type: str
    snippet:
        description: Filter syslog server profiles by snippet container.
        required: false
        type: str
    device:
        description: Filter syslog server profiles by device container.
        required: false
        type: str
    exact_match:
        description: When True, only return objects defined exactly in the specified container.
        required: false
        type: bool
        default: false
    exclude_folders:
        description: List of folder names to exclude from results.
        required: false
        type: list
        elements: str
    exclude_snippets:
        description: List of snippet values to exclude from results.
        required: false
        type: list
        elements: str
    exclude_devices:
        description: List of device values to exclude from results.
        required: false
        type: list
        elements: str
    transport:
        description: Filter by transport protocol used by the syslog servers.
        required: false
        type: list
        elements: str
        choices: ["UDP", "TCP"]
    format:
        description: Filter by syslog format used by the servers.
        required: false
        type: list
        elements: str
        choices: ["BSD", "IETF"]
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
- name: Gather Syslog Server Profile Information in Strata Cloud Manager
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

    - name: Get information about a specific syslog server profile
      cdot65.scm.syslog_server_profiles_info:
        provider: "{{ provider }}"
        name: "basic-syslog-profile"
        folder: "Shared"
      register: syslog_profile_info

    - name: List all syslog server profiles in a folder
      cdot65.scm.syslog_server_profiles_info:
        provider: "{{ provider }}"
        folder: "Shared"
      register: all_syslog_profiles

    - name: List only UDP syslog server profiles
      cdot65.scm.syslog_server_profiles_info:
        provider: "{{ provider }}"
        folder: "Shared"
        transport: ["UDP"]
      register: udp_syslog_profiles

    - name: List only IETF format syslog server profiles
      cdot65.scm.syslog_server_profiles_info:
        provider: "{{ provider }}"
        folder: "Shared"
        format: ["IETF"]
      register: ietf_syslog_profiles

    - name: List syslog server profiles with exact match and exclusions
      cdot65.scm.syslog_server_profiles_info:
        provider: "{{ provider }}"
        folder: "Shared"
        exact_match: true
        exclude_folders: ["Test"]
        exclude_snippets: ["default"]
      register: filtered_syslog_profiles
"""

RETURN = r"""
syslog_server_profiles:
    description: List of syslog server profile objects matching the filter criteria (returned when name is not specified).
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "basic-syslog-profile"
        servers:
          server1:
            name: "server1"
            server: "192.168.1.100"
            transport: "UDP"
            port: 514
            format: "BSD"
            facility: "LOG_USER"
        folder: "Shared"
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "advanced-syslog-profile"
        servers:
          primary:
            name: "primary"
            server: "logs.example.com"
            transport: "TCP"
            port: 1514
            format: "IETF"
            facility: "LOG_LOCAL0"
          backup:
            name: "backup"
            server: "backup-logs.example.com"
            transport: "TCP"
            port: 1514
            format: "IETF"
            facility: "LOG_LOCAL1"
        format:
          traffic: "hostname,$time,$src,$dst,$proto,$sport,$dport"
          threat: "hostname,$time,$src,$dst,$threatid,$severity"
          system: "hostname,$time,$severity,$result"
        folder: "Shared"
syslog_server_profile:
    description: Information about the requested syslog server profile (returned when name is specified).
    returned: success, when name is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "basic-syslog-profile"
        servers:
          server1:
            name: "server1"
            server: "192.168.1.100"
            transport: "UDP"
            port: 514
            format: "BSD"
            facility: "LOG_USER"
        folder: "Shared"
"""


def build_filter_params(module_params):
    """
    Build filter parameters dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        (dict, dict): Tuple containing:
            - dict: Container parameters (folder, snippet, device)
            - dict: Filter parameters for the list operation
    """
    # Container params
    container_params = {}
    for container in ["folder", "snippet", "device"]:
        if module_params.get(container) is not None:
            container_params[container] = module_params[container]

    # Filter params
    filter_params = {}
    for filter_param in ["exact_match", "exclude_folders", "exclude_snippets", "exclude_devices"]:
        if module_params.get(filter_param) is not None:
            filter_params[filter_param] = module_params[filter_param]

    # Add transport filter if provided
    if module_params.get("transport") is not None:
        filter_params["transport"] = module_params["transport"]

    # Add format filter if provided
    if module_params.get("format") is not None:
        filter_params["format"] = module_params["format"]

    return container_params, filter_params


def main():
    """
    Main execution path for the syslog_server_profiles_info module.

    This module provides functionality to gather information about syslog server profile objects
    in the SCM (Strata Cloud Manager) system with various filtering options.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=SyslogServerProfilesInfoSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        # Only require a container if we're not provided with a specific name
        required_if=[["name", None, ["folder", "snippet", "device"], True]],
    )

    result = {}

    try:
        client = get_scm_client(module)

        # Check if we're fetching a specific syslog server profile by name
        if module.params.get("name"):
            name = module.params["name"]
            container_params = {}

            # Get the container param
            for container in ["folder", "snippet", "device"]:
                if module.params.get(container):
                    container_params[container] = module.params[container]

            try:
                # Fetch a specific syslog server profile
                syslog_server_profile = client.syslog_server_profile.fetch(
                    name=name, **container_params
                )

                # Serialize response for Ansible output
                result["syslog_server_profile"] = serialize_response(syslog_server_profile)

            except ObjectNotPresentError:
                module.fail_json(
                    msg=f"Syslog server profile with name '{name}' not found in {list(container_params.keys())[0]} '{list(container_params.values())[0]}'"
                )
            except (MissingQueryParameterError, InvalidObjectError) as e:
                module.fail_json(msg=str(e))

        else:
            # List syslog server profiles with filtering
            container_params, filter_params = build_filter_params(module.params)

            try:
                syslog_server_profiles = client.syslog_server_profile.list(
                    **container_params, **filter_params
                )

                # Serialize response for Ansible output
                result["syslog_server_profiles"] = [
                    serialize_response(profile) for profile in syslog_server_profiles
                ]

            except MissingQueryParameterError as e:
                module.fail_json(msg=f"Missing required parameter: {str(e)}")
            except InvalidObjectError as e:
                module.fail_json(msg=f"Invalid filter parameters: {str(e)}")

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
