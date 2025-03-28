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
Ansible module for gathering information about agent versions in SCM.

This module provides functionality to retrieve information about agent versions
in the SCM (Strata Cloud Manager) system with various filtering options.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import uuid
from datetime import datetime

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.agent_versions import AgentVersionsInfoSpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError

DOCUMENTATION = r"""
---
module: agent_versions_info

short_description: Gather information about agent versions in SCM.

version_added: "0.1.0"

description:
    - Gather information about agent versions within Strata Cloud Manager (SCM).
    - Supports retrieving a specific agent version by name/version or listing agent versions with various filters.
    - Provides additional client-side filtering capabilities.
    - Returns detailed information about each agent version.
    - This is an info module that only retrieves information and does not modify anything.

options:
    name:
        description: The name of a specific agent to retrieve information about.
        required: false
        type: str
    version:
        description: The specific version to retrieve information about.
        required: false
        type: str
    type:
        description: Filter agent versions by their type.
        required: false
        type: list
        elements: str
        choices: ['prisma_access', 'ngfw', 'sdwan', 'cpe']
    status:
        description: Filter agent versions by their status.
        required: false
        type: list
        elements: str
        choices: ['recommended', 'current', 'deprecated', 'obsolete']
    platform:
        description: Filter agent versions by platform compatibility.
        required: false
        type: list
        elements: str
    features:
        description: Filter agent versions by supported features.
        required: false
        type: list
        elements: str
    gather_subset:
        description:
            - Determines which information to gather about agent versions.
            - C(all) gathers everything.
            - C(config) is the default which retrieves basic configuration.
        type: list
        elements: str
        default: ['config']
        choices: ['all', 'config']
    exact_match:
        description: When True, only return objects with exact matching criteria.
        required: false
        type: bool
        default: false
    exact_version:
        description: When True, require exact version match rather than prefix match.
        required: false
        type: bool
        default: false
    provider:
        description: Authentication credentials for SCM.
        required: true
        type: dict
        suboptions:
            client_id:
                description: Client ID for authentication to SCM.
                required: true
                type: str
            client_secret:
                description: Client secret for authentication to SCM.
                required: true
                type: str
                no_log: true
            tsg_id:
                description: Tenant Service Group ID for SCM.
                required: true
                type: str
            log_level:
                description: Log level for the SDK.
                required: false
                type: str
                default: "INFO"
    testmode:
        description: Enable test mode for CI/CD environments (no API calls).
        required: false
        type: bool
        default: false
    test_timestamp:
        description: Timestamp to use for test mode data generation.
        required: false
        type: str

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
---
- name: Gather Agent Version Information in Strata Cloud Manager
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
    - name: Get information about all agent versions
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
      register: all_versions

    - name: Get information about a specific version
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
        version: "5.3.0"
      register: specific_version

    - name: List all recommended versions
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
        status: ["recommended"]
      register: recommended_versions

    - name: List Prisma Access agent versions
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
        type: ["prisma_access"]
      register: prisma_versions

    - name: List versions with exact matching
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
        version: "5.3.0"
        exact_match: true
        exact_version: true
      register: exact_versions

    - name: List versions by platform
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
        platform: ["linux_x86_64"]
      register: platform_versions

    - name: List versions supporting specific features
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
        features: ["ipsec", "ssl_vpn"]
      register: feature_versions
"""

RETURN = r"""
agent_versions:
    description: List of agent versions matching the filter criteria (returned when version is not specified).
    returned: success, when version is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Prisma Access Agent"
        version: "5.3.0"
        type: "prisma_access"
        status: "recommended"
        platform: "linux_x86_64"
        features_enabled: ["ipsec", "ssl_vpn", "globalprotect"]
        release_date: "2023-06-15"
        end_of_support_date: "2024-06-15"
        release_notes_url: "https://example.com/release-notes/5.3.0"
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "SD-WAN Agent"
        version: "2.1.0"
        type: "sdwan"
        status: "current"
        platform: "linux_arm64"
        features_enabled: ["qos", "traffic_shaping"]
        release_date: "2023-05-20"
        end_of_support_date: "2024-05-20"
        release_notes_url: "https://example.com/release-notes/2.1.0"
agent_version:
    description: Information about the requested agent version (returned when version is specified).
    returned: success, when version is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Prisma Access Agent"
        version: "5.3.0"
        type: "prisma_access"
        status: "recommended"
        platform: "linux_x86_64"
        features_enabled: ["ipsec", "ssl_vpn", "globalprotect"]
        release_date: "2023-06-15"
        end_of_support_date: "2024-06-15"
        release_notes_url: "https://example.com/release-notes/5.3.0"
"""


def build_filter_params(module_params):
    """
    Build filter parameters dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant filter parameters
    """
    filter_params = {}
    
    # Add standard filters
    for filter_param in ["exact_match", "exact_version"]:
        if module_params.get(filter_param) is not None:
            filter_params[filter_param] = module_params[filter_param]
    
    # Add version filter if provided
    if module_params.get("version") is not None:
        if module_params.get("exact_version", False):
            # For exact version match, we'll need to use the fetch method
            filter_params["version"] = module_params["version"]
        else:
            # For prefix match or contains match, we'll use it in list filtering
            # In the SDK, `version` in list() is for substring matching
            filter_params["version"] = module_params["version"]
    
    # Add type filter if provided
    if module_params.get("type") is not None:
        filter_params["type"] = module_params["type"]
    
    # Add status filter if provided
    if module_params.get("status") is not None:
        filter_params["status"] = module_params["status"]
    
    # Add platform filter if provided
    if module_params.get("platform") is not None:
        filter_params["platform"] = module_params["platform"]
    
    # Add features filter if provided
    if module_params.get("features") is not None:
        filter_params["features"] = module_params["features"]
    
    return filter_params


def generate_mock_agent_versions(module_params):
    """
    Generate mock agent versions for test mode.

    Args:
        module_params (dict): Module parameters

    Returns:
        list: List of mock agent version dictionaries
    """
    mock_versions = []
    
    # Prisma Access Agents
    mock_versions.append({
        "id": str(uuid.uuid4()),
        "name": "Prisma Access Agent",
        "version": "5.3.0",
        "type": "prisma_access",
        "status": "recommended",
        "platform": "linux_x86_64",
        "features_enabled": ["ipsec", "ssl_vpn", "globalprotect"],
        "release_date": "2023-06-15",
        "end_of_support_date": "2024-06-15",
        "release_notes_url": "https://example.com/release-notes/5.3.0"
    })
    
    mock_versions.append({
        "id": str(uuid.uuid4()),
        "name": "Prisma Access Agent",
        "version": "5.2.8",
        "type": "prisma_access",
        "status": "current",
        "platform": "linux_x86_64",
        "features_enabled": ["ipsec", "ssl_vpn"],
        "release_date": "2023-02-10",
        "end_of_support_date": "2024-02-10",
        "release_notes_url": "https://example.com/release-notes/5.2.8"
    })
    
    # SD-WAN Agents
    mock_versions.append({
        "id": str(uuid.uuid4()),
        "name": "SD-WAN Agent",
        "version": "2.1.0",
        "type": "sdwan",
        "status": "recommended",
        "platform": "linux_arm64",
        "features_enabled": ["qos", "traffic_shaping"],
        "release_date": "2023-05-20",
        "end_of_support_date": "2024-05-20",
        "release_notes_url": "https://example.com/release-notes/2.1.0"
    })
    
    # NGFW Agents
    mock_versions.append({
        "id": str(uuid.uuid4()),
        "name": "NGFW Agent",
        "version": "3.5.2",
        "type": "ngfw",
        "status": "recommended",
        "platform": "linux_x86_64",
        "features_enabled": ["firewall", "nat", "vpn"],
        "release_date": "2023-04-12",
        "end_of_support_date": "2024-04-12",
        "release_notes_url": "https://example.com/release-notes/3.5.2"
    })
    
    # CPE Agents
    mock_versions.append({
        "id": str(uuid.uuid4()),
        "name": "CPE Agent",
        "version": "1.8.3",
        "type": "cpe",
        "status": "current",
        "platform": "linux_arm64",
        "features_enabled": ["monitoring", "management"],
        "release_date": "2023-03-05",
        "end_of_support_date": "2024-03-05",
        "release_notes_url": "https://example.com/release-notes/1.8.3"
    })
    
    # Include the timestamp if provided for test repeatability
    if module_params.get("test_timestamp"):
        for version in mock_versions:
            version["test_timestamp"] = module_params["test_timestamp"]
    
    return mock_versions


def filter_mock_versions(mock_versions, filter_params):
    """
    Apply filters to mock versions for test mode.

    Args:
        mock_versions (list): List of mock version dictionaries
        filter_params (dict): Filter parameters

    Returns:
        list: Filtered list of mock version dictionaries
    """
    filtered_versions = mock_versions.copy()
    
    # Filter by name
    if "name" in filter_params and filter_params["name"]:
        name_filter = filter_params["name"]
        filtered_versions = [v for v in filtered_versions if v["name"] == name_filter]
    
    # Filter by version
    if "version" in filter_params and filter_params["version"]:
        version_filter = filter_params["version"]
        if filter_params.get("exact_version", False):
            filtered_versions = [v for v in filtered_versions if v["version"].lower() == version_filter.lower()]
        else:
            filtered_versions = [v for v in filtered_versions if version_filter.lower() in v["version"].lower()]
    
    # Filter by type
    if "type" in filter_params and filter_params["type"]:
        type_filter = filter_params["type"]
        if isinstance(type_filter, list):
            filtered_versions = [v for v in filtered_versions if v["type"] in type_filter]
        else:
            filtered_versions = [v for v in filtered_versions if v["type"] == type_filter]
    
    # Filter by status
    if "status" in filter_params and filter_params["status"]:
        status_filter = filter_params["status"]
        if isinstance(status_filter, list):
            filtered_versions = [v for v in filtered_versions if v["status"] in status_filter]
        else:
            filtered_versions = [v for v in filtered_versions if v["status"] == status_filter]
    
    # Filter by platform
    if "platform" in filter_params and filter_params["platform"]:
        platform_filter = filter_params["platform"]
        if isinstance(platform_filter, list):
            filtered_versions = [v for v in filtered_versions if v["platform"] in platform_filter]
        else:
            filtered_versions = [v for v in filtered_versions if v["platform"] == platform_filter]
    
    # Filter by features
    if "features" in filter_params and filter_params["features"]:
        features_filter = filter_params["features"]
        filtered_versions = [
            v for v in filtered_versions 
            if all(feature in v.get("features_enabled", []) for feature in features_filter)
        ]
    
    return filtered_versions


def main():
    """
    Main execution path for the agent_versions_info module.

    This module provides functionality to gather information about agent versions
    in the SCM (Strata Cloud Manager) system with various filtering options.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=AgentVersionsInfoSpec.spec(),
        supports_check_mode=True,
    )

    result = {}
    testmode = module.params.get("testmode", False)

    # Build filter parameters from module parameters
    filter_params = build_filter_params(module.params)

    # In test mode, we don't need to initialize the API client
    if testmode:
        try:
            # Generate and filter mock versions
            mock_versions = generate_mock_agent_versions(module.params)
            filtered_versions = filter_mock_versions(mock_versions, filter_params)
            
            # Check if we're looking for a specific version
            if module.params.get("version") and filter_params.get("exact_version", False):
                # Return a specific version
                if filtered_versions:
                    result["agent_version"] = filtered_versions[0]
                else:
                    module.fail_json(msg=f"Agent version '{module.params['version']}' not found")
            else:
                # Return a list of versions
                result["agent_versions"] = filtered_versions
                
            module.exit_json(**result)
            
        except Exception as e:
            module.fail_json(msg=f"Error in test mode: {to_text(e)}")
    
    # Normal mode with API client
    try:
        client = get_scm_client(module)
        
        # Check if we're fetching a specific version
        if module.params.get("version") and filter_params.get("exact_version", False):
            try:
                # Fetch a specific version
                version = module.params["version"]
                agent_version = client.agent_versions.fetch(version=version)
                
                # Serialize response for Ansible output
                result["agent_version"] = serialize_response(agent_version)
                
            except ObjectNotPresentError:
                module.fail_json(msg=f"Agent version '{version}' not found")
            except (MissingQueryParameterError, InvalidObjectError) as e:
                module.fail_json(msg=str(e))
        
        else:
            # List agent versions with filtering
            try:
                # In the SDK, if version is provided, it's used for substring filtering
                agent_versions = client.agent_versions.list(**filter_params)
                
                # Serialize response for Ansible output
                result["agent_versions"] = [serialize_response(ver) for ver in agent_versions]
                
            except (MissingQueryParameterError, InvalidObjectError) as e:
                module.fail_json(msg=f"Invalid filter parameters: {str(e)}")

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()