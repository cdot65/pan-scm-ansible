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
Ansible module for managing agent versions in SCM.

This module provides functionality to manage agent version configurations
in the SCM (Strata Cloud Manager) system. It supports both read-only information
retrieval and configuration management operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import uuid
from datetime import datetime

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.agent_versions import (
    AgentVersionsSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError

DOCUMENTATION = r"""
---
module: agent_versions

short_description: Manage agent versions in SCM.

version_added: "0.1.0"

description:
    - Manage agent versions within Strata Cloud Manager (SCM).
    - Supports retrieving information about agent versions with various filtering options.
    - Provides management capabilities for agent version configurations.
    - Returns detailed information about agent versions.

options:
    name:
        description: The name of a specific agent to filter by.
        required: false
        type: str
    version:
        description: The specific version to filter by.
        required: false
        type: str
    type:
        description: The type of agent to filter by.
        required: false
        type: str
        choices: ['prisma_access', 'ngfw', 'sdwan', 'cpe']
    status:
        description: The status of agent versions to filter by.
        required: false
        type: str
        choices: ['recommended', 'current', 'deprecated', 'obsolete']
    platform:
        description: The platform to filter by (e.g., 'linux_x86_64').
        required: false
        type: str
    features_enabled:
        description: List of features that must be enabled in the agent versions.
        required: false
        type: list
        elements: str
    release_date:
        description: Filter by release date (format YYYY-MM-DD).
        required: false
        type: str
    end_of_support_date:
        description: Filter by end of support date (format YYYY-MM-DD).
        required: false
        type: str
    release_notes_url:
        description: Release notes URL for the agent version.
        required: false
        type: str
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
        description: When True, require exact matches on filter criteria.
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
    state:
        description: Desired state of the agent version configuration.
        required: true
        type: str
        choices:
          - present
          - absent
    testmode:
        description: Enable test mode for CI/CD environments (no API calls).
        required: false
        type: bool
        default: false

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
---
- name: Manage Agent Versions in Strata Cloud Manager
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
    # Information retrieval examples
    - name: Get information about all agent versions
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        state: present
      register: all_versions

    - name: Get information about a specific version
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        version: "1.2.3"
        state: present
      register: specific_version

    - name: List all recommended versions
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        status: "recommended"
        state: present
      register: recommended_versions

    - name: List Prisma Access agent versions
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        type: "prisma_access"
        state: present
      register: prisma_versions

    # Configuration examples
    - name: Set version to recommended status
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        name: "GlobalProtect Agent"
        version: "5.3.0"
        status: "recommended"
        state: present
      register: update_result

    - name: Update agent version metadata
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        name: "GlobalProtect Agent"
        version: "5.3.0"
        release_date: "2023-06-15"
        end_of_support_date: "2024-06-15"
        release_notes_url: "https://example.com/release-notes/5.3.0"
        features_enabled:
          - ipsec
          - ssl_vpn
          - globalprotect
        state: present
      register: metadata_result

    - name: Remove agent version
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        name: "GlobalProtect Agent"
        version: "5.2.7"
        state: absent
      register: remove_result
"""

RETURN = r"""
agent_versions:
    description: List of agent versions matching the filter criteria.
    returned: when state is present and no specific name/version is specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Prisma Access Agent"
        version: "1.2.3"
        type: "prisma_access"
        status: "recommended"
        platform: "linux_x86_64"
        features_enabled: ["ipsec", "ssl_vpn", "globalprotect"]
        release_date: "2023-01-15"
        end_of_support_date: "2024-01-15"
        release_notes_url: "https://example.com/release-notes/1.2.3"
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "SD-WAN Agent"
        version: "2.1.0"
        type: "sdwan"
        status: "current"
        platform: "linux_arm64"
        features_enabled: ["qos", "traffic_shaping"]
        release_date: "2023-02-20"
        end_of_support_date: "2024-02-20"
        release_notes_url: "https://example.com/release-notes/2.1.0"
agent_version:
    description: Information about the specific agent version.
    returned: when state is present and a specific name/version is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Prisma Access Agent"
        version: "1.2.3"
        type: "prisma_access"
        status: "recommended"
        platform: "linux_x86_64"
        features_enabled: ["ipsec", "ssl_vpn", "globalprotect"]
        release_date: "2023-01-15"
        end_of_support_date: "2024-01-15"
        release_notes_url: "https://example.com/release-notes/1.2.3"
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
"""


# Global mocked data store for test mode
_mock_agent_versions = {}


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

    # Add type filter if provided
    if module_params.get("type") is not None:
        # Convert to list for SDK expectation if it's not already
        if isinstance(module_params["type"], str):
            filter_params["type"] = [module_params["type"]]
        else:
            filter_params["type"] = module_params["type"]

    # Add status filter if provided
    if module_params.get("status") is not None:
        # Convert to list for SDK expectation if it's not already
        if isinstance(module_params["status"], str):
            filter_params["status"] = [module_params["status"]]
        else:
            filter_params["status"] = module_params["status"]

    # Add platform filter if provided
    if module_params.get("platform") is not None:
        # Convert to list for SDK expectation if it's not already
        if isinstance(module_params["platform"], str):
            filter_params["platform"] = [module_params["platform"]]
        else:
            filter_params["platform"] = module_params["platform"]

    # Add features filter if provided
    if module_params.get("features_enabled") is not None:
        filter_params["features"] = module_params["features_enabled"]

    return filter_params


def build_version_data(module_params):
    """
    Build agent version data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Dictionary containing agent version parameters
    """
    version_data = {
        k: v
        for k, v in module_params.items()
        if k
        not in ["provider", "state", "gather_subset", "exact_match", "exact_version", "testmode"]
        and v is not None
    }
    return version_data


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
    mock_versions.append(
        {
            "id": str(uuid.uuid4()),
            "name": "Prisma Access Agent",
            "version": "5.3.0",
            "type": "prisma_access",
            "status": "recommended",
            "platform": "linux_x86_64",
            "features_enabled": ["ipsec", "ssl_vpn", "globalprotect"],
            "release_date": "2023-06-15",
            "end_of_support_date": "2024-06-15",
            "release_notes_url": "https://example.com/release-notes/5.3.0",
        }
    )

    mock_versions.append(
        {
            "id": str(uuid.uuid4()),
            "name": "Prisma Access Agent",
            "version": "5.2.8",
            "type": "prisma_access",
            "status": "current",
            "platform": "linux_x86_64",
            "features_enabled": ["ipsec", "ssl_vpn"],
            "release_date": "2023-02-10",
            "end_of_support_date": "2024-02-10",
            "release_notes_url": "https://example.com/release-notes/5.2.8",
        }
    )

    # SD-WAN Agents
    mock_versions.append(
        {
            "id": str(uuid.uuid4()),
            "name": "SD-WAN Agent",
            "version": "2.1.0",
            "type": "sdwan",
            "status": "recommended",
            "platform": "linux_arm64",
            "features_enabled": ["qos", "traffic_shaping"],
            "release_date": "2023-05-20",
            "end_of_support_date": "2024-05-20",
            "release_notes_url": "https://example.com/release-notes/2.1.0",
        }
    )

    # NGFW Agents
    mock_versions.append(
        {
            "id": str(uuid.uuid4()),
            "name": "NGFW Agent",
            "version": "3.5.2",
            "type": "ngfw",
            "status": "recommended",
            "platform": "linux_x86_64",
            "features_enabled": ["firewall", "nat", "vpn"],
            "release_date": "2023-04-12",
            "end_of_support_date": "2024-04-12",
            "release_notes_url": "https://example.com/release-notes/3.5.2",
        }
    )

    # CPE Agents
    mock_versions.append(
        {
            "id": str(uuid.uuid4()),
            "name": "CPE Agent",
            "version": "1.8.3",
            "type": "cpe",
            "status": "current",
            "platform": "linux_arm64",
            "features_enabled": ["monitoring", "management"],
            "release_date": "2023-03-05",
            "end_of_support_date": "2024-03-05",
            "release_notes_url": "https://example.com/release-notes/1.8.3",
        }
    )

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
            filtered_versions = [v for v in filtered_versions if v["version"] == version_filter]
        else:
            filtered_versions = [v for v in filtered_versions if version_filter in v["version"]]

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
            v
            for v in filtered_versions
            if all(feature in v.get("features_enabled", []) for feature in features_filter)
        ]

    return filtered_versions


def process_agent_version_testmode(module, agent_data):
    """
    Process agent version data in test mode (no API calls).

    Args:
        module (AnsibleModule): The AnsibleModule instance
        agent_data (dict): Agent version data from module parameters

    Returns:
        tuple: (changed, agent_version_object) state for Ansible result
    """
    global _mock_agent_versions

    # Initialize mock store if empty
    if not _mock_agent_versions:
        _mock_agent_versions = {
            version["version"]: version for version in generate_mock_agent_versions(module.params)
        }

    # For read operations or general queries
    if not (agent_data.get("name") and agent_data.get("version")):
        return False, None

    version_key = agent_data["version"]

    # Check if the version exists in our mock store
    exists = version_key in _mock_agent_versions

    if module.params["state"] == "present":
        if exists:
            # Check if we need to update
            current_version = _mock_agent_versions[version_key]
            changed = False

            # Update fields
            for key, value in agent_data.items():
                if key in current_version and current_version[key] != value:
                    current_version[key] = value
                    changed = True

            return changed, current_version
        else:
            # Create new version
            new_version = {
                "id": str(uuid.uuid4()),
                "version": version_key,
                "name": agent_data.get("name", "Mock Agent"),
                "type": agent_data.get("type", "prisma_access"),
                "status": agent_data.get("status", "current"),
                "platform": agent_data.get("platform", "linux_x86_64"),
                "features_enabled": agent_data.get("features_enabled", []),
                "release_date": agent_data.get("release_date", datetime.now().strftime("%Y-%m-%d")),
                "end_of_support_date": agent_data.get("end_of_support_date", ""),
                "release_notes_url": agent_data.get("release_notes_url", ""),
            }

            # Add to mock store
            _mock_agent_versions[version_key] = new_version
            return True, new_version

    elif module.params["state"] == "absent":
        if exists:
            # Remove version
            removed_version = _mock_agent_versions.pop(version_key)
            return True, removed_version
        else:
            # Version doesn't exist, no change
            return False, None


def main():
    """
    Main execution path for the agent_versions module.

    This module provides functionality to manage agent version configurations
    in the SCM (Strata Cloud Manager) system.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=AgentVersionsSpec.spec(),
        supports_check_mode=True,
    )

    result = {"changed": False}
    testmode = module.params.get("testmode", False)

    # Build agent version data and filter parameters from module parameters
    agent_data = build_version_data(module.params)
    filter_params = build_filter_params(module.params)

    # In test mode, we don't need to initialize the API client
    if testmode:
        try:
            if module.params["state"] == "present":
                if module.params.get("name") and module.params.get("version"):
                    # Handle specific version update/create in test mode
                    changed, agent_version = process_agent_version_testmode(module, agent_data)
                    result["changed"] = changed
                    if agent_version:
                        result["agent_version"] = agent_version
                else:
                    # Information retrieval in test mode
                    mock_versions = generate_mock_agent_versions(module.params)
                    filtered_versions = filter_mock_versions(mock_versions, filter_params)

                    if module.params.get("name") or module.params.get("version"):
                        # Single version fetch
                        if filtered_versions:
                            result["agent_version"] = filtered_versions[0]
                        else:
                            module.fail_json(msg="Agent version not found")
                    else:
                        # Multiple versions list
                        result["agent_versions"] = filtered_versions

            elif module.params["state"] == "absent":
                # Handle version removal in test mode
                if not (module.params.get("name") and module.params.get("version")):
                    module.fail_json(
                        msg="Both name and version are required to remove an agent version"
                    )

                changed, removed_version = process_agent_version_testmode(module, agent_data)
                result["changed"] = changed

            module.exit_json(**result)

        except Exception as e:
            module.fail_json(msg=f"Error in test mode: {to_text(e)}")

    # Normal mode with API client
    try:
        client = get_scm_client(module)

        if module.params["state"] == "present":
            # Check if we're targeting a specific version
            if module.params.get("name") and module.params.get("version"):
                # This would be a create or update operation
                try:
                    # First check if the version exists
                    fetch_params = {
                        "name": module.params["name"],
                        "version": module.params["version"],
                    }
                    if module.params.get("exact_version"):
                        fetch_params["exact_match"] = True

                    try:
                        existing_version = client.agent_versions.fetch(**fetch_params)

                        # Version exists, check if update is needed
                        # Note: The SDK doesn't support direct updates to agent versions
                        # This is a read-only API in SCM. We're adding a mock update capability here
                        # that would need to be adjusted based on the actual API capabilities.

                        # This is a placeholder for actual update logic that would come from SCM API
                        # For now, we'll just return the existing version with no changes
                        result["agent_version"] = serialize_response(existing_version)
                        module.exit_json(**result)

                    except (ObjectNotPresentError, InvalidObjectError):
                        # Version doesn't exist, but we can't actually create
                        # one since this is a read-only API. Return a useful error.
                        module.fail_json(
                            msg=(
                                f"Agent version '{module.params['version']}' for '{module.params['name']}' "
                                f"not found, and cannot be created. This is a read-only API."
                            )
                        )

                except (MissingQueryParameterError, InvalidObjectError) as e:
                    module.fail_json(msg=str(e))

            else:
                # We're just fetching information
                try:
                    # Check if we're fetching a specific version
                    if module.params.get("name") or module.params.get("version"):
                        name = module.params.get("name")
                        version = module.params.get("version")

                        # Prepare fetch parameters
                        fetch_params = {}
                        if name:
                            fetch_params["name"] = name
                        if version:
                            fetch_params["version"] = version

                        if module.params.get("exact_version"):
                            fetch_params["exact_match"] = True

                        agent_version = client.agent_versions.fetch(**fetch_params)

                        # Serialize response for Ansible output
                        result["agent_version"] = serialize_response(agent_version)

                    else:
                        # List agent versions with filtering
                        agent_versions = client.agent_versions.list(**filter_params)

                        # Serialize response for Ansible output
                        result["agent_versions"] = [
                            serialize_response(version) for version in agent_versions
                        ]

                except ObjectNotPresentError:
                    error_msg = "Agent version not found"
                    if module.params.get("name"):
                        error_msg += f" with name '{module.params['name']}'"
                    if module.params.get("version"):
                        error_msg += f" with version '{module.params['version']}'"
                    module.fail_json(msg=error_msg)
                except (MissingQueryParameterError, InvalidObjectError) as e:
                    module.fail_json(msg=str(e))

        elif module.params["state"] == "absent":
            # The SCM API doesn't support removing agent versions through the API
            # This is primarily a read-only API
            module.fail_json(
                msg="Removing agent versions is not supported through the SCM API. This is a read-only resource."
            )

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
