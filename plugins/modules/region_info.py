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
Ansible module for gathering information about region objects in SCM.

This module provides functionality to retrieve information about region objects
in the SCM (Strata Cloud Manager) system with various filtering options.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.region_info import RegionInfoSpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError

DOCUMENTATION = r"""
---
module: region_info

short_description: Gather information about region objects in SCM.

version_added: "0.1.0"

description:
  - Gather information about region objects within Strata Cloud Manager (SCM).
  - Supports retrieving a specific region by name or listing regions with various filters.
  - Provides additional client-side filtering capabilities for exact matches, exclusions, and geographical areas.
  - Returns detailed information about each region object.
  - This is an info module that only retrieves information and does not modify anything.

options:
  name:
    description: The name of a specific region to retrieve.
    required: false
    type: str
  gather_subset:
    description:
      - Determines which information to gather about regions.
      - C(all) gathers everything.
      - C(config) is the default which retrieves basic configuration.
    type: list
    elements: str
    default: ['config']
    choices: ['all', 'config']
  folder:
    description: Filter regions by folder container.
    required: false
    type: str
  snippet:
    description: Filter regions by snippet container.
    required: false
    type: str
  device:
    description: Filter regions by device container.
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
  geo_location:
    description: Filter by geographic location range.
    required: false
    type: dict
    suboptions:
      latitude:
        description: Latitude range for filtering (values must be between -90 and 90 degrees).
        required: false
        type: dict
        suboptions:
          min:
            description: Minimum latitude value (range -90 to 90).
            required: true
            type: float
          max:
            description: Maximum latitude value (range -90 to 90).
            required: true
            type: float
      longitude:
        description: Longitude range for filtering (values must be between -180 and 180 degrees).
        required: false
        type: dict
        suboptions:
          min:
            description: Minimum longitude value (range -180 to 180).
            required: true
            type: float
          max:
            description: Maximum longitude value (range -180 to 180).
            required: true
            type: float
  addresses:
    description: Filter by addresses included in regions (e.g., ['10.0.0.0/8']). Matches regions containing any of the specified addresses.
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
- name: Gather Region Information in Strata Cloud Manager
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

    - name: Get information about a specific region
      cdot65.scm.region_info:
        provider: "{{ provider }}"
        name: "us-west-region"
        folder: "Global"
      register: region_info

    - name: List all region objects in a folder
      cdot65.scm.region_info:
        provider: "{{ provider }}"
        folder: "Global"
      register: all_regions

    - name: List regions with geographic filtering (west coast US)
      cdot65.scm.region_info:
        provider: "{{ provider }}"
        folder: "Global"
        geo_location:
          latitude:
            min: 30
            max: 50
          longitude:
            min: -130
            max: -110
      register: west_coast_regions

    - name: List regions with specific addresses
      cdot65.scm.region_info:
        provider: "{{ provider }}"
        folder: "Global"
        addresses: ["10.0.0.0/8"]
      register: network_regions

    - name: List regions with exact match and exclusions
      cdot65.scm.region_info:
        provider: "{{ provider }}"
        folder: "Global"
        exact_match: true
        exclude_folders: ["Test", "Development"]
      register: filtered_regions
"""

RETURN = r"""
regions:
  description: List of region objects matching the filter criteria (returned when name is not specified).
  returned: success, when name is not specified
  type: list
  elements: dict
  sample:
    - id: "123e4567-e89b-12d3-a456-426655440000"
      name: "us-west-region"
      geo_location:
        latitude: 37.7749
        longitude: -122.4194
      address:
        - "10.0.0.0/8"
        - "192.168.1.0/24"
      folder: "Global"
    - id: "234e5678-e89b-12d3-a456-426655440001"
      name: "internal-networks"
      address:
        - "172.16.0.0/16"
        - "192.168.0.0/16"
      folder: "Global"
region:
  description: Information about the requested region (returned when name is specified).
  returned: success, when name is specified
  type: dict
  sample:
    id: "123e4567-e89b-12d3-a456-426655440000"
    name: "us-west-region"
    geo_location:
      latitude: 37.7749
      longitude: -122.4194
    address:
      - "10.0.0.0/8"
      - "192.168.1.0/24"
    folder: "Global"
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

    # Add geo_location filter if provided
    if module_params.get("geo_location") is not None:
        filter_params["geo_location"] = module_params["geo_location"]

    # Add addresses filter if provided
    if module_params.get("addresses") is not None:
        filter_params["addresses"] = module_params["addresses"]

    return container_params, filter_params


def main():
    """
    Main execution path for the region_info module.

    This module provides functionality to gather information about region objects
    in the SCM (Strata Cloud Manager) system with various filtering options.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=RegionInfoSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        # Only require a container if we're not provided with a specific name
        required_if=[["name", None, ["folder", "snippet", "device"], True]],
    )

    result = {}

    try:
        client = get_scm_client(module)

        # Check if we're fetching a specific region by name
        if module.params.get("name"):
            name = module.params["name"]
            container_params = {}

            # Get the container param
            for container in ["folder", "snippet", "device"]:
                if module.params.get(container):
                    container_params[container] = module.params[container]

            try:
                # Fetch a specific region
                region = client.region.fetch(name=name, **container_params)

                # Serialize response for Ansible output
                result["region"] = serialize_response(region)

            except ObjectNotPresentError:
                module.fail_json(
                    msg=f"Region with name '{name}' not found in {list(container_params.keys())[0]} '{list(container_params.values())[0]}'"
                )
            except (MissingQueryParameterError, InvalidObjectError) as e:
                module.fail_json(msg=str(e))

        else:
            # List regions with filtering
            container_params, filter_params = build_filter_params(module.params)

            try:
                regions = client.region.list(**container_params, **filter_params)

                # Serialize response for Ansible output
                result["regions"] = [serialize_response(region) for region in regions]

            except MissingQueryParameterError as e:
                module.fail_json(msg=f"Missing required parameter: {str(e)}")
            except InvalidObjectError as e:
                module.fail_json(msg=f"Invalid filter parameters: {str(e)}")

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()