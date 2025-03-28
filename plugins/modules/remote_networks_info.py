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
Ansible module for gathering information about remote networks in SCM.

This module provides functionality to retrieve information about remote networks
in the SCM (Strata Cloud Manager) system with various filtering options.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.remote_networks_info import (
    RemoteNetworksInfoSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError

DOCUMENTATION = r"""
---
module: remote_networks_info

short_description: Gather information about remote networks in SCM.

version_added: "0.1.0"

description:
    - Gather information about remote networks within Strata Cloud Manager (SCM).
    - Supports retrieving a specific remote network by name or listing networks with various filters.
    - Provides additional client-side filtering capabilities by regions, license types, and subnets.
    - Returns detailed information about each remote network.
    - This is an info module that only retrieves information and does not modify anything.

options:
    name:
        description: The name of a specific remote network to retrieve.
        required: false
        type: str
    gather_subset:
        description:
            - Determines which information to gather about remote networks.
            - C(all) gathers everything.
            - C(config) is the default which retrieves basic configuration.
        type: list
        elements: str
        default: ['config']
        choices: ['all', 'config']
    folder:
        description: Filter remote networks by folder.
        required: false
        type: str
    regions:
        description: Filter remote networks by regions.
        required: false
        type: list
        elements: str
    license_types:
        description: Filter remote networks by license types.
        required: false
        type: list
        elements: str
        choices: ["FWAAS-AGGREGATE", "FWAAS-BYOL", "CN-SERIES", "FWAAS-PAYG"]
    subnets:
        description: Filter remote networks by subnets.
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
- name: Gather Remote Network Information in Strata Cloud Manager
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

    - name: Get information about a specific remote network
      cdot65.scm.remote_networks_info:
        provider: "{{ provider }}"
        name: "Branch-Office-1"
        folder: "Remote-Sites"
      register: network_info

    - name: List all remote networks in a folder
      cdot65.scm.remote_networks_info:
        provider: "{{ provider }}"
        folder: "Remote-Sites"
      register: all_networks

    - name: List remote networks in a specific region
      cdot65.scm.remote_networks_info:
        provider: "{{ provider }}"
        folder: "Remote-Sites"
        regions: ["us-east-1"]
      register: region_networks

    - name: List remote networks with specific license types
      cdot65.scm.remote_networks_info:
        provider: "{{ provider }}"
        folder: "Remote-Sites"
        license_types: ["FWAAS-AGGREGATE"]
      register: license_networks

    - name: List remote networks with specific subnets
      cdot65.scm.remote_networks_info:
        provider: "{{ provider }}"
        folder: "Remote-Sites"
        subnets: ["10.1.0.0/16"]
      register: subnet_networks
"""

RETURN = r"""
remote_networks:
    description: List of remote network objects matching the filter criteria (returned when name is not specified).
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Branch-Office-1"
        description: "Remote network for Branch Office 1"
        region: "us-east-1"
        license_type: "FWAAS-AGGREGATE"
        spn_name: "main-spn"
        folder: "Remote-Sites"
        ecmp_load_balancing: "disable"
        ipsec_tunnel: "tunnel-to-branch1"
        subnets: ["10.1.0.0/16", "10.2.0.0/16"]
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "Branch-Office-2"
        description: "Remote network for Branch Office 2"
        region: "us-west-1"
        license_type: "FWAAS-AGGREGATE"
        spn_name: "west-spn"
        folder: "Remote-Sites"
        ecmp_load_balancing: "enable"
        subnets: ["10.3.0.0/16", "10.4.0.0/16"]
remote_network:
    description: Information about the requested remote network (returned when name is specified).
    returned: success, when name is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Branch-Office-1"
        description: "Remote network for Branch Office 1"
        region: "us-east-1"
        license_type: "FWAAS-AGGREGATE"
        spn_name: "main-spn"
        folder: "Remote-Sites"
        ecmp_load_balancing: "disable"
        ipsec_tunnel: "tunnel-to-branch1"
        subnets: ["10.1.0.0/16", "10.2.0.0/16"]
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
    if module_params.get("folder") is not None:
        container_params["folder"] = module_params["folder"]

    # Filter params
    filter_params = {}
    for filter_param in ["regions", "license_types", "subnets"]:
        if module_params.get(filter_param) is not None:
            filter_params[filter_param] = module_params[filter_param]

    return container_params, filter_params


def main():
    """
    Main execution path for the remote_networks_info module.

    This module provides functionality to gather information about remote networks
    in the SCM (Strata Cloud Manager) system with various filtering options.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=RemoteNetworksInfoSpec.spec(),
        supports_check_mode=True,
    )

    result = {}

    try:
        client = get_scm_client(module)

        # Check if we're fetching a specific remote network by name
        if module.params.get("name"):
            name = module.params["name"]

            # Ensure folder is provided
            if not module.params.get("folder"):
                module.fail_json(msg="folder parameter is required when specifying name")

            folder = module.params["folder"]

            try:
                # Fetch a specific remote network
                remote_network = client.remote_network.fetch(name=name, folder=folder)

                # Serialize response for Ansible output
                result["remote_network"] = serialize_response(remote_network)

            except ObjectNotPresentError:
                module.fail_json(
                    msg=f"Remote network with name '{name}' not found in folder '{folder}'"
                )
            except (MissingQueryParameterError, InvalidObjectError) as e:
                module.fail_json(msg=str(e))

        else:
            # List remote networks with filtering
            container_params, filter_params = build_filter_params(module.params)

            # Ensure folder is provided for list operation
            if not container_params.get("folder"):
                module.fail_json(msg="folder parameter is required")

            try:
                remote_networks = client.remote_network.list(**container_params, **filter_params)

                # Serialize response for Ansible output
                result["remote_networks"] = [
                    serialize_response(network) for network in remote_networks
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
