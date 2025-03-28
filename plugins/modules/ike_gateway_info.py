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
Ansible module for gathering information about IKE gateways in SCM.

This module provides functionality to retrieve information about IKE gateways
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
module: ike_gateway_info

short_description: Gather information about IKE gateways in SCM.

version_added: "0.2.0"

description:
    - Gather information about IKE gateways within Strata Cloud Manager (SCM).
    - Supports retrieving a specific gateway by name or listing gateways with various filters.
    - Provides additional client-side filtering capabilities for exact matches and exclusions.
    - Returns detailed information about each IKE gateway including authentication, protocol, and peer details.
    - This is an info module that only retrieves information and does not modify anything.

options:
    name:
        description: The name of a specific IKE gateway to retrieve.
        required: false
        type: str
    gather_subset:
        description:
            - Determines which information to gather about IKE gateways.
            - C(all) gathers everything.
            - C(config) is the default which retrieves basic configuration.
        type: list
        elements: str
        default: ['config']
        choices: ['all', 'config']
    folder:
        description: Filter IKE gateways by folder container.
        required: false
        type: str
    snippet:
        description: Filter IKE gateways by snippet container.
        required: false
        type: str
    device:
        description: Filter IKE gateways by device container.
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
- name: Gather IKE Gateway Information in Strata Cloud Manager
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

    - name: Get information about a specific IKE gateway
      cdot65.scm.ike_gateway_info:
        provider: "{{ provider }}"
        name: "branch-office-gateway"
        folder: "Service Connections"
      register: gateway_info

    - name: List all IKE gateways in a folder
      cdot65.scm.ike_gateway_info:
        provider: "{{ provider }}"
        folder: "Service Connections"
      register: all_gateways

    - name: List gateways with exact match and exclusions
      cdot65.scm.ike_gateway_info:
        provider: "{{ provider }}"
        folder: "Service Connections"
        exact_match: true
        exclude_folders: ["All"]
        exclude_snippets: ["default"]
      register: filtered_gateways
"""

RETURN = r"""
gateways:
    description: List of IKE gateway objects matching the filter criteria (returned when name is not specified).
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "branch-office-gateway"
        folder: "Service Connections"
        authentication:
          pre_shared_key: {}
        peer_id:
          type: "fqdn"
          id: "peer.example.com"
        protocol:
          version: "ikev2"
          ikev2:
            ike_crypto_profile: "default-profile"
        peer_address:
          ip: "198.51.100.1"
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "hq-gateway"
        folder: "Service Connections"
        authentication:
          pre_shared_key: {}
        protocol:
          version: "ikev2-preferred"
        peer_address:
          fqdn: "hq.example.com"
gateway:
    description: Information about the requested IKE gateway (returned when name is specified).
    returned: success, when name is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "branch-office-gateway"
        folder: "Service Connections"
        authentication:
          pre_shared_key: {}
        peer_id:
          type: "fqdn"
          id: "peer.example.com"
        protocol:
          version: "ikev2"
          ikev2:
            ike_crypto_profile: "default-profile"
        peer_address:
          ip: "198.51.100.1"
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

    return container_params, filter_params


def main():
    """
    Main execution path for the ike_gateway_info module.

    This module provides functionality to gather information about IKE gateways
    in the SCM (Strata Cloud Manager) system with various filtering options.

    :return: Ansible module exit data
    :rtype: dict
    """
    # Define module parameters
    argument_spec = {
        "name": dict(type="str", required=False),
        "gather_subset": dict(
            type="list",
            elements="str",
            default=["config"],
            choices=["all", "config"],
        ),
        "folder": dict(type="str", required=False),
        "snippet": dict(type="str", required=False),
        "device": dict(type="str", required=False),
        "exact_match": dict(type="bool", required=False, default=False),
        "exclude_folders": dict(type="list", elements="str", required=False),
        "exclude_snippets": dict(type="list", elements="str", required=False),
        "exclude_devices": dict(type="list", elements="str", required=False),
        "provider": dict(
            type="dict",
            required=True,
            options=dict(
                client_id=dict(type="str", required=True),
                client_secret=dict(type="str", required=True, no_log=True),
                tsg_id=dict(type="str", required=True),
                log_level=dict(type="str", required=False, default="INFO"),
            ),
        ),
    }

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet", "device"],
        ],
        # Only require a container if we're not provided with a specific name
        required_if=[["name", None, ["folder", "snippet", "device"], True]],
    )

    # Initialize result with changed=False and no gateway info yet
    result = {"changed": False}

    try:
        client = get_scm_client(module)

        # Check if we're fetching a specific gateway by name
        if module.params.get("name"):
            name = module.params["name"]
            container_params = {}

            # Get the container param
            for container in ["folder", "snippet", "device"]:
                if module.params.get(container):
                    container_params[container] = module.params[container]

            # If no container param is specified, try to find the gateway without container filters
            try:
                gateway = client.ike_gateway.fetch(
                    name=name, **container_params
                )
                # Add gateway to result dictionary as a separate key
                result["gateway"] = serialize_response(gateway)
            except ObjectNotPresentError:
                module.fail_json(
                    msg=f"IKE gateway with name '{name}' not found"
                    + (f" in {list(container_params.keys())[0]} '{list(container_params.values())[0]}'" if container_params else "")
                )
            except Exception as e:
                module.fail_json(msg=f"Error retrieving IKE gateway information: {str(e)}")
        else:
            # Check if at least one container filter is provided when listing gateways
            container_params, filter_params = build_filter_params(module.params)
            if not any(
                key in container_params for key in ["folder", "snippet", "device"]
            ):
                module.fail_json(
                    msg="One of 'folder', 'snippet', or 'device' must be provided when 'name' is not specified."
                )

            # List gateways with filters
            try:
                # Call the list method with filter params
                gateways = client.ike_gateway.list(**container_params, **filter_params)
                
                # Add gateways list to result dictionary as a separate key
                result["gateways"] = [serialize_response(gateway) for gateway in gateways]
            except Exception as e:
                module.fail_json(msg=f"Error listing IKE gateways: {str(e)}")

        module.exit_json(**result)
    except Exception as e:
        module.fail_json(msg=f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":
    main()
