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
Ansible module for gathering information about anti-spyware profile objects in SCM.

This module provides functionality to retrieve information about anti-spyware profile objects
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

from scm.config.security.anti_spyware_profile import AntiSpywareProfile
from scm.exceptions import InvalidObjectError, MissingQueryParameterError, NotFoundError

DOCUMENTATION = r"""
---
module: anti_spyware_profile_info

short_description: Gather information about anti-spyware profile objects in SCM.

version_added: "0.1.0"

description:
    - Gather information about anti-spyware profile objects within Strata Cloud Manager (SCM).
    - Supports retrieving a specific profile by name or listing profiles with various filters.
    - Provides additional client-side filtering capabilities for exact matches and exclusions.
    - Returns detailed information about each anti-spyware profile object.
    - This is an info module that only retrieves information and does not modify anything.

options:
    name:
        description: The name of a specific anti-spyware profile to retrieve.
        required: false
        type: str
    gather_subset:
        description: 
            - Determines which information to gather about anti-spyware profiles.
            - C(all) gathers everything.
            - C(config) is the default which retrieves basic configuration.
        type: list
        elements: str
        default: ['config']
        choices: ['all', 'config']
    folder:
        description: Filter profiles by folder container.
        required: false
        type: str
    snippet:
        description: Filter profiles by snippet container.
        required: false
        type: str
    device:
        description: Filter profiles by device container.
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
    cloud_inline_analysis:
        description: Filter by cloud inline analysis setting.
        required: false
        type: bool
    rules:
        description: Filter by rule names.
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
- name: Gather Anti-Spyware Profile Information in Strata Cloud Manager
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

    - name: Get information about a specific anti-spyware profile
      cdot65.scm.anti_spyware_profile_info:
        provider: "{{ provider }}"
        name: "Custom-Spyware-Profile"
        folder: "Production"
      register: profile_info

    - name: List all anti-spyware profiles in a folder
      cdot65.scm.anti_spyware_profile_info:
        provider: "{{ provider }}"
        folder: "Production"
      register: all_profiles

    - name: List profiles with specific rules
      cdot65.scm.anti_spyware_profile_info:
        provider: "{{ provider }}"
        folder: "Production"
        rules: ["Block-Critical-Threats"]
      register: rule_profiles

    - name: List profiles with cloud inline analysis enabled
      cdot65.scm.anti_spyware_profile_info:
        provider: "{{ provider }}"
        folder: "Production"
        cloud_inline_analysis: true
      register: cloud_enabled_profiles

    - name: List profiles with exact match and exclusions
      cdot65.scm.anti_spyware_profile_info:
        provider: "{{ provider }}"
        folder: "Production"
        exact_match: true
        exclude_folders: ["All"]
        exclude_snippets: ["default"]
      register: filtered_profiles
"""

RETURN = r"""
anti_spyware_profiles:
    description: List of anti-spyware profile objects matching the filter criteria (returned when name is not specified).
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Custom-Spyware-Profile"
        description: "Custom anti-spyware profile"
        cloud_inline_analysis: true
        rules:
          - name: "Block-Critical-Threats"
            severity: ["critical"]
            category: "spyware"
            packet_capture: "single-packet"
        folder: "Production"
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "Default-Spyware-Profile"
        description: "Default anti-spyware profile"
        cloud_inline_analysis: false
        rules:
          - name: "Block-All-Threats"
            severity: ["critical", "high", "medium"]
            category: "spyware"
            packet_capture: "extended-capture"
        folder: "Production"
anti_spyware_profile:
    description: Information about the requested anti-spyware profile (returned when name is specified).
    returned: success, when name is specified
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

    # Add specific filters for anti-spyware profiles
    for param in ["cloud_inline_analysis", "rules"]:
        if module_params.get(param) is not None:
            filter_params[param] = module_params[param]

    return container_params, filter_params


def main():
    """
    Main execution path for the anti_spyware_profile_info module.

    This module provides functionality to gather information about anti-spyware profile objects
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
            cloud_inline_analysis=dict(type="bool", required=False),
            rules=dict(type="list", elements="str", required=False),
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
        profile_api = AntiSpywareProfile(client)

        # Check if we're fetching a specific profile by name
        if module.params.get("name"):
            name = module.params["name"]
            container_params = {}

            # Get the container param
            for container in ["folder", "snippet", "device"]:
                if module.params.get(container):
                    container_params[container] = module.params[container]

            try:
                # Fetch a specific profile
                profile = profile_api.fetch(name=name, **container_params)

                # Serialize response for Ansible output
                profile_data = serialize_response(profile)

                # Ensure list fields are never None
                list_fields = [
                    "rules",
                    "threat_exception",
                    "inline_exception_edl_url",
                    "inline_exception_ip_address",
                    "mica_engine_spyware_enabled",
                ]
                for field in list_fields:
                    if field in profile_data and profile_data[field] is None:
                        profile_data[field] = []

                result["anti_spyware_profile"] = profile_data

            except NotFoundError:
                module.fail_json(
                    msg=f"Anti-spyware profile with name '{name}' not found in {list(container_params.keys())[0]} '{list(container_params.values())[0]}'"
                )
            except (MissingQueryParameterError, InvalidObjectError) as e:
                module.fail_json(msg=str(e))

        else:
            # List profiles with filtering
            container_params, filter_params = build_filter_params(module.params)

            try:
                profiles = profile_api.list(**container_params, **filter_params)

                # Serialize response for Ansible output and ensure list fields are never None
                serialized_profiles = []
                for profile in profiles:
                    profile_data = serialize_response(profile)

                    # Ensure list fields are never None
                    list_fields = [
                        "rules",
                        "threat_exception",
                        "inline_exception_edl_url",
                        "inline_exception_ip_address",
                        "mica_engine_spyware_enabled",
                    ]
                    for field in list_fields:
                        if field in profile_data and profile_data[field] is None:
                            profile_data[field] = []

                    serialized_profiles.append(profile_data)

                result["anti_spyware_profiles"] = serialized_profiles

            except MissingQueryParameterError as e:
                module.fail_json(msg=f"Missing required parameter: {str(e)}")
            except InvalidObjectError as e:
                module.fail_json(msg=f"Invalid filter parameters: {str(e)}")

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
