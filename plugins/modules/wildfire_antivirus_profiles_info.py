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
Ansible module for gathering information about WildFire antivirus profiles in SCM.

This module provides functionality to retrieve information about WildFire antivirus profiles
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
module: wildfire_antivirus_profiles_info

short_description: Gather information about WildFire antivirus profiles in SCM.

version_added: "0.1.0"

description:
    - Gather information about WildFire antivirus profiles within Strata Cloud Manager (SCM).
    - Supports retrieving a specific profile by name or listing profiles with various filters.
    - Provides additional client-side filtering capabilities for exact matches and exclusions.
    - Returns detailed information about each WildFire antivirus profile.
    - This is an info module that only retrieves information and does not modify anything.

options:
    name:
        description: The name of a specific WildFire antivirus profile to retrieve.
        required: false
        type: str
    gather_subset:
        description:
            - Determines which information to gather about profiles.
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
- name: Gather WildFire Antivirus Profile Information in Strata Cloud Manager
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

    - name: Get information about a specific WildFire antivirus profile
      cdot65.scm.wildfire_antivirus_profiles_info:
        provider: "{{ provider }}"
        name: "Basic-Wildfire-AV"
        folder: "Texas"
      register: profile_info

    - name: List all WildFire antivirus profiles in a folder
      cdot65.scm.wildfire_antivirus_profiles_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_profiles

    - name: List WildFire antivirus profiles by rule name
      cdot65.scm.wildfire_antivirus_profiles_info:
        provider: "{{ provider }}"
        folder: "Texas"
        rules: ["Default-Rule"]
      register: filtered_profiles

    - name: List profiles with exact match and exclusions
      cdot65.scm.wildfire_antivirus_profiles_info:
        provider: "{{ provider }}"
        folder: "Texas"
        exact_match: true
        exclude_folders: ["All"]
        exclude_snippets: ["default"]
      register: filtered_profiles
"""

RETURN = r"""
wildfire_antivirus_profiles:
    description: List of WildFire antivirus profile objects matching the filter criteria (returned when name is not specified).
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Basic-Wildfire-AV"
        description: "Basic WildFire antivirus profile"
        folder: "Texas"
        packet_capture: true
        rules:
          - name: "Default-Rule"
            direction: "both"
            analysis: "public-cloud"
            application: ["any"]
            file_type: ["any"]
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "Advanced-Wildfire-AV"
        description: "Advanced WildFire antivirus profile with exceptions"
        folder: "Texas"
        packet_capture: true
        rules:
          - name: "Web-Traffic-Rule"
            direction: "download"
            analysis: "public-cloud"
            application: ["web-browsing", "ssl"]
            file_type: ["pe", "pdf"]
wildfire_antivirus_profile:
    description: Information about the requested WildFire antivirus profile (returned when name is specified).
    returned: success, when name is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Basic-Wildfire-AV"
        description: "Basic WildFire antivirus profile"
        folder: "Texas"
        packet_capture: true
        rules:
          - name: "Default-Rule"
            direction: "both"
            analysis: "public-cloud"
            application: ["any"]
            file_type: ["any"]
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

    # Add other filter parameters
    for param in ["rules"]:
        if module_params.get(param) is not None:
            filter_params[param] = module_params[param]

    return container_params, filter_params


def main():
    """
    Main execution path for the wildfire_antivirus_profiles_info module.

    This module provides functionality to gather information about WildFire antivirus profiles
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
                profile = client.wildfire_antivirus_profile.fetch(name=name, **container_params)

                # Serialize response for Ansible output
                result["wildfire_antivirus_profile"] = serialize_response(profile)

            except ObjectNotPresentError:
                module.fail_json(
                    msg=f"WildFire antivirus profile with name '{name}' not found in {list(container_params.keys())[0]} '{list(container_params.values())[0]}'"
                )
            except (MissingQueryParameterError, InvalidObjectError) as e:
                module.fail_json(msg=str(e))

        else:
            # List profiles with filtering
            container_params, filter_params = build_filter_params(module.params)

            try:
                profiles = client.wildfire_antivirus_profile.list(
                    **container_params, **filter_params
                )

                # Serialize response for Ansible output
                result["wildfire_antivirus_profiles"] = [
                    serialize_response(profile) for profile in profiles
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
