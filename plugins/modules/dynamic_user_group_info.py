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
Ansible module for gathering information about dynamic user group objects in SCM.

This module provides functionality to retrieve information about dynamic user group objects
in the SCM (Strata Cloud Manager) system with various filtering options.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.dynamic_user_group import (
    DynamicUserGroupInfoSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError

DOCUMENTATION = r"""
---
module: dynamic_user_group_info

short_description: Gather information about dynamic user group objects in SCM.

version_added: "0.1.0"

description:
    - Gather information about dynamic user group objects within Strata Cloud Manager (SCM).
    - Supports retrieving a specific dynamic user group by name or listing dynamic user groups with various filters.
    - Provides additional client-side filtering capabilities for exact matches and exclusions.
    - Returns detailed information about each dynamic user group object.
    - This is an info module that only retrieves information and does not modify anything.

options:
    name:
        description: The name of a specific dynamic user group object to retrieve.
        required: false
        type: str
    gather_subset:
        description:
            - Determines which information to gather about dynamic user groups.
            - C(all) gathers everything.
            - C(config) is the default which retrieves basic configuration.
        type: list
        elements: str
        default: ['config']
        choices: ['all', 'config']
    folder:
        description: Filter dynamic user groups by folder container.
        required: false
        type: str
    snippet:
        description: Filter dynamic user groups by snippet container.
        required: false
        type: str
    device:
        description: Filter dynamic user groups by device container.
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
    filters:
        description: Filter by filter expressions.
        required: false
        type: list
        elements: str
    tags:
        description: Filter by tags.
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
- name: Gather Dynamic User Group Information in Strata Cloud Manager
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

    - name: Get information about a specific dynamic user group
      cdot65.scm.dynamic_user_group_info:
        provider: "{{ provider }}"
        name: "high_risk_users"
        folder: "Security"
      register: dug_info

    - name: List all dynamic user group objects in a folder
      cdot65.scm.dynamic_user_group_info:
        provider: "{{ provider }}"
        folder: "Security"
      register: all_dugs

    - name: List dynamic user groups with specific tags
      cdot65.scm.dynamic_user_group_info:
        provider: "{{ provider }}"
        folder: "Security"
        tags: ["RiskManagement", "Security"]
      register: tagged_dugs

    - name: List dynamic user groups with specific filter expressions
      cdot65.scm.dynamic_user_group_info:
        provider: "{{ provider }}"
        folder: "Security"
        filters: ["tag.criticality.high"]
      register: filtered_dugs

    - name: List dynamic user groups with exact match and exclusions
      cdot65.scm.dynamic_user_group_info:
        provider: "{{ provider }}"
        folder: "Security"
        exact_match: true
        exclude_folders: ["All"]
        exclude_snippets: ["default"]
      register: filtered_dugs
"""

RETURN = r"""
dynamic_user_groups:
    description: List of dynamic user group objects matching the filter criteria (returned when name is not specified).
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "high_risk_users"
        description: "Users with high risk classification"
        filter: "tag.criticality.high"
        folder: "Security"
        tag: ["RiskManagement", "Security"]
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "risky_contractors"
        description: "High risk contractors"
        filter: "tag.user_type.contractor and (tag.criticality.high or tag.risk_score.gt.80)"
        folder: "Security"
        tag: ["RiskManagement", "Contractors"]
dynamic_user_group:
    description: Information about the requested dynamic user group (returned when name is specified).
    returned: success, when name is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "high_risk_users"
        description: "Users with high risk classification"
        filter: "tag.criticality.high"
        folder: "Security"
        tag: ["RiskManagement", "Security"]
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

    # Convert "tags" parameter to "tags" for SDK
    if module_params.get("tags") is not None:
        filter_params["tags"] = module_params["tags"]

    # Add "filters" parameter for filter expressions
    if module_params.get("filters") is not None:
        filter_params["filters"] = module_params["filters"]

    return container_params, filter_params


def main():
    """
    Main execution path for the dynamic_user_group_info module.

    This module provides functionality to gather information about dynamic user group objects
    in the SCM (Strata Cloud Manager) system with various filtering options.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=DynamicUserGroupInfoSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        # Only require a container if we're not provided with a specific name
        required_if=[["name", None, ["folder", "snippet", "device"], True]],
    )

    result = {}

    try:
        client = get_scm_client(module)

        # Check if we're fetching a specific dynamic user group by name
        if module.params.get("name"):
            name = module.params["name"]
            container_params = {}

            # Get the container param
            for container in ["folder", "snippet", "device"]:
                if module.params.get(container):
                    container_params[container] = module.params[container]

            try:
                # Fetch a specific dynamic user group
                dug = client.dynamic_user_group.fetch(name=name, **container_params)

                # Serialize response for Ansible output
                result["dynamic_user_group"] = serialize_response(dug)

            except ObjectNotPresentError:
                module.fail_json(
                    msg=f"Dynamic user group with name '{name}' not found in {list(container_params.keys())[0]} '{list(container_params.values())[0]}'"
                )
            except (MissingQueryParameterError, InvalidObjectError) as e:
                module.fail_json(msg=str(e))

        else:
            # List dynamic user groups with filtering
            container_params, filter_params = build_filter_params(module.params)

            try:
                dugs = client.dynamic_user_group.list(**container_params, **filter_params)

                # Serialize response for Ansible output
                result["dynamic_user_groups"] = [serialize_response(dug) for dug in dugs]

            except MissingQueryParameterError as e:
                module.fail_json(msg=f"Missing required parameter: {str(e)}")
            except InvalidObjectError as e:
                module.fail_json(msg=f"Invalid filter parameters: {str(e)}")

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
