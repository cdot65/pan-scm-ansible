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
Ansible module for gathering information about external dynamic lists in SCM.

This module provides functionality to retrieve information about external dynamic lists
in the SCM (Strata Cloud Manager) system with various filtering options.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError

DOCUMENTATION = r"""
---
module: external_dynamic_lists_info

short_description: Gather information about external dynamic lists in SCM.

version_added: "0.1.0"

description:
    - Gather information about external dynamic lists within Strata Cloud Manager (SCM).
    - Supports retrieving a specific list by name or listing external dynamic lists with various filters.
    - Provides additional client-side filtering capabilities for exact matches and exclusions.
    - Returns detailed information about each external dynamic list.
    - This is an info module that only retrieves information and does not modify anything.

options:
    name:
        description: The name of a specific external dynamic list to retrieve.
        required: false
        type: str
    gather_subset:
        description:
            - Determines which information to gather about external dynamic lists.
            - C(all) gathers everything.
            - C(config) is the default which retrieves basic configuration.
        type: list
        elements: str
        default: ['config']
        choices: ['all', 'config']
    folder:
        description: Filter external dynamic lists by folder container.
        required: false
        type: str
    snippet:
        description: Filter external dynamic lists by snippet container.
        required: false
        type: str
    device:
        description: Filter external dynamic lists by device container.
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
    types:
        description: Filter by external dynamic list types.
        required: false
        type: list
        elements: str
        choices: ["ip", "domain", "url", "imsi", "imei", "predefined_ip", "predefined_url"]
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
- name: Gather External Dynamic Lists Information in Strata Cloud Manager
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

    - name: Get information about a specific external dynamic list
      cdot65.scm.external_dynamic_lists_info:
        provider: "{{ provider }}"
        name: "malicious-ips"
        folder: "Texas"
      register: edl_info

    - name: List all external dynamic lists in a folder
      cdot65.scm.external_dynamic_lists_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_edls

    - name: List only IP-based external dynamic lists
      cdot65.scm.external_dynamic_lists_info:
        provider: "{{ provider }}"
        folder: "Texas"
        types: ["ip"]
      register: ip_edls

    - name: List external dynamic lists with exact match and exclusions
      cdot65.scm.external_dynamic_lists_info:
        provider: "{{ provider }}"
        folder: "Texas"
        exact_match: true
        exclude_folders: ["All"]
        exclude_snippets: ["default"]
      register: filtered_edls
"""

RETURN = r"""
external_dynamic_lists:
    description: List of external dynamic list objects matching the filter criteria (returned when name is not specified).
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "malicious-ips"
        type:
          ip:
            url: "https://threatfeeds.example.com/ips.txt"
            description: "Known malicious IPs"
            recurring:
              hourly: {}
        folder: "Texas"
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "blocked-domains"
        type:
          domain:
            url: "https://threatfeeds.example.com/domains.txt"
            description: "Blocked domains list"
            recurring:
              daily:
                at: "03"
            expand_domain: true
        folder: "Texas"
external_dynamic_list:
    description: Information about the requested external dynamic list (returned when name is specified).
    returned: success, when name is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "malicious-ips"
        type:
          ip:
            url: "https://threatfeeds.example.com/ips.txt"
            description: "Known malicious IPs"
            recurring:
              hourly: {}
        folder: "Texas"
"""


def build_filter_params(module_params):
    """
    Build filter parameters dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant filter parameters
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

    # Add types parameter
    if module_params.get("types") is not None:
        filter_params["types"] = module_params["types"]

    return container_params, filter_params


def main():
    """
    Main execution path for the external_dynamic_lists_info module.

    This module provides functionality to gather information about external dynamic lists
    in the SCM (Strata Cloud Manager) system with various filtering options.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=False),
            gather_subset=dict(
                type="list", elements="str", default=["config"], choices=["all", "config"]
            ),
            folder=dict(type="str", required=False),
            snippet=dict(type="str", required=False),
            device=dict(type="str", required=False),
            exact_match=dict(type="bool", required=False, default=False),
            exclude_folders=dict(type="list", elements="str", required=False),
            exclude_snippets=dict(type="list", elements="str", required=False),
            exclude_devices=dict(type="list", elements="str", required=False),
            types=dict(
                type="list",
                elements="str",
                required=False,
                choices=["ip", "domain", "url", "imsi", "imei", "predefined_ip", "predefined_url"],
            ),
            provider=dict(
                type="dict",
                required=True,
                options=dict(
                    client_id=dict(type="str", required=True),
                    client_secret=dict(type="str", required=True, no_log=True),
                    tsg_id=dict(type="str", required=True),
                    log_level=dict(type="str", required=False, default="INFO"),
                ),
            ),
        ),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        # Only require a container if we're not provided with a specific name
        required_if=[["name", None, ["folder", "snippet", "device"], True]],
    )

    result = {}

    try:
        client = get_scm_client(module)

        # Check if we're fetching a specific external dynamic list by name
        if module.params.get("name"):
            name = module.params["name"]
            container_params = {}

            # Get the container param
            for container in ["folder", "snippet", "device"]:
                if module.params.get(container):
                    container_params[container] = module.params[container]

            try:
                # Fetch a specific external dynamic list
                edl = client.external_dynamic_list.fetch(name=name, **container_params)

                # Serialize response for Ansible output
                result["external_dynamic_list"] = serialize_response(edl)

            except ObjectNotPresentError:
                module.fail_json(
                    msg=f"External dynamic list with name '{name}' not found in {list(container_params.keys())[0]} '{list(container_params.values())[0]}'"
                )
            except (MissingQueryParameterError, InvalidObjectError) as e:
                module.fail_json(msg=str(e))

        else:
            # List external dynamic lists with filtering
            container_params, filter_params = build_filter_params(module.params)

            try:
                edls = client.external_dynamic_list.list(**container_params, **filter_params)

                # Serialize response for Ansible output
                result["external_dynamic_lists"] = [serialize_response(edl) for edl in edls]

            except MissingQueryParameterError as e:
                module.fail_json(msg=f"Missing required parameter: {str(e)}")
            except InvalidObjectError as e:
                module.fail_json(msg=f"Invalid filter parameters: {str(e)}")

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
