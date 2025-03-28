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
Ansible module for managing log forwarding profile objects in SCM.

This module provides functionality to create, update, and delete log forwarding profile objects
in the SCM (Strata Cloud Manager) system. It handles various log forwarding configurations
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.log_forwarding_profile import (
    LogForwardingProfileSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.objects import LogForwardingProfileUpdateModel

DOCUMENTATION = r"""
---
module: log_forwarding_profile

short_description: Manage log forwarding profile objects in SCM.

version_added: "0.1.0"

description:
    - Manage log forwarding profile objects within Strata Cloud Manager (SCM).
    - Create, update, and delete log forwarding profile objects.
    - Configure log filtering and forwarding behavior.
    - Ensures that exactly one container type (folder, snippet, device) is provided.

options:
    name:
        description: The name of the log forwarding profile (max 63 chars).
        required: true
        type: str
    description:
        description: Description of the log forwarding profile.
        required: false
        type: str
    match_list:
        description: List of match list configurations within the log forwarding profile. Required when state=present.
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: Match list entry name.
                required: true
                type: str
            action:
                description: Match list action.
                required: true
                type: str
                choices: ["tagging", "forwarding"]
            send_http:
                description: List of HTTP server profiles to use for forwarding.
                required: false
                type: list
                elements: str
            filter:
                description: Filter to apply to this match list.
                required: false
                type: str
            action_desc:
                description: Description of this match list entry.
                required: false
                type: str
            log_type:
                description: Type of logs to forward.
                required: true
                type: str
                choices: ["traffic", "threat", "wildfire", "url", "data", "tunnel", "auth", "decryption"]
            send_to_panorama:
                description: Whether to send logs to Panorama.
                required: false
                type: bool
            snmp_profiles:
                description: List of SNMP profiles to use.
                required: false
                type: list
                elements: str
            email_profiles:
                description: List of email profiles to use.
                required: false
                type: list
                elements: str
            send_syslog:
                description: List of syslog profiles to use.
                required: false
                type: list
                elements: str
            tag:
                description: List of tags to apply.
                required: false
                type: list
                elements: str
    filter:
        description: List of filter configurations within the log forwarding profile.
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: Filter name.
                required: true
                type: str
            filter:
                description: Filter expression.
                required: true
                type: str
    folder:
        description: The folder in which the resource is defined (max 64 chars).
        required: false
        type: str
    snippet:
        description: The snippet in which the resource is defined (max 64 chars).
        required: false
        type: str
    device:
        description: The device in which the resource is defined (max 64 chars).
        required: false
        type: str
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
    state:
        description: Desired state of the log forwarding profile object.
        required: true
        type: str
        choices:
          - present
          - absent

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
---
- name: Manage Log Forwarding Profiles in Strata Cloud Manager
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

    - name: Create a log forwarding profile with filter and match list
      cdot65.scm.log_forwarding_profile:
        provider: "{{ provider }}"
        name: "test-log-profile"
        description: "Test log forwarding profile"
        folder: "Texas"
        filter:
          - name: "critical-events"
            filter: "severity eq critical"
        match_list:
          - name: "forward-critical-threats"
            action: "forwarding"
            send_http: ["secure-profile"]  # You can also use http_profile as an alias
            log_type: "threat"
            filter: "critical-events"
            send_to_panorama: true
        state: "present"

    - name: Update an existing log forwarding profile
      cdot65.scm.log_forwarding_profile:
        provider: "{{ provider }}"
        name: "test-log-profile"
        description: "Updated log forwarding profile"
        folder: "Texas"
        filter:
          - name: "critical-events"
            filter: "severity eq critical"
          - name: "warning-events"
            filter: "severity eq warning"
        match_list:
          - name: "forward-critical-threats"
            action: "forwarding"
            send_http: ["secure-profile"]
            log_type: "threat"
            filter: "critical-events"
            send_to_panorama: true
          - name: "tag-warning-events"
            action: "tagging"
            filter: "warning-events"
            tag: ["warning", "review"]
        state: "present"

    - name: Create a profile with both syslog and HTTP forwarding
      cdot65.scm.log_forwarding_profile:
        provider: "{{ provider }}"
        name: "multi-destination-profile"
        description: "Forward logs to multiple destinations"
        folder: "Texas"
        filter:
          - name: "threat-events"
            filter: "severity eq critical or severity eq high"
        match_list:
          - name: "forward-threat-logs"
            action: "forwarding"
            send_http: ["http-server1", "http-server2"]
            send_syslog: ["syslog-profile1"]  # You can also use syslog_profiles as an alias
            log_type: "threat"
            filter: "threat-events"
            send_to_panorama: true
            action_desc: "Forward critical and high threats"  # You can also use description as an alias
        state: "present"

    - name: Delete a log forwarding profile
      cdot65.scm.log_forwarding_profile:
        provider: "{{ provider }}"
        name: "test-log-profile"
        folder: "Texas"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
log_forwarding_profile:
    description: Details about the log forwarding profile.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "test-log-profile"
        description: "Test log forwarding profile"
        filter:
          - name: "critical-events"
            filter: "severity eq critical"
        match_list:
          - name: "forward-critical-threats"
            action: "forwarding"
            send_http: ["secure-profile"] 
            log_type: "threat"
            filter: "critical-events"
            send_to_panorama: true
        folder: "Texas"
"""


def normalize_match_list_fields(match_list):
    """
    Normalize match_list fields to align with API expectations.

    - Handle both send_http and http_profile (preferring send_http)
    - Handle both send_syslog and syslog_profiles (preferring send_syslog)
    - Handle both action_desc and description (preferring action_desc)

    Args:
        match_list (list): List of match_list dictionaries from user input

    Returns:
        list: Normalized match_list with consistent field names
    """
    if not match_list:
        return match_list

    normalized_list = []

    for item in match_list:
        normalized_item = item.copy()

        # Handle http_profile -> send_http conversion
        if "http_profile" in normalized_item and "send_http" not in normalized_item:
            normalized_item["send_http"] = normalized_item.pop("http_profile")

        # Handle syslog_profiles -> send_syslog conversion
        if "syslog_profiles" in normalized_item and "send_syslog" not in normalized_item:
            normalized_item["send_syslog"] = normalized_item.pop("syslog_profiles")

        # Handle description -> action_desc conversion
        if "description" in normalized_item and "action_desc" not in normalized_item:
            normalized_item["action_desc"] = normalized_item.pop("description")

        normalized_list.append(normalized_item)

    return normalized_list


def build_log_forwarding_profile_data(module_params):
    """
    Build log forwarding profile data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant log forwarding profile parameters
    """
    data = {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }

    # Normalize match_list fields if present
    if "match_list" in data and data["match_list"]:
        data["match_list"] = normalize_match_list_fields(data["match_list"])

    return data


def is_container_specified(log_forwarding_profile_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        log_forwarding_profile_data (dict): Log forwarding profile parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [
        log_forwarding_profile_data.get(container) for container in ["folder", "snippet", "device"]
    ]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the log forwarding profile object needs to be updated.

    Args:
        existing: Existing log forwarding profile object from the SCM API
        params (dict): Log forwarding profile parameters with desired state from Ansible module

    Returns:
        (bool, dict): Tuple containing:
            - bool: Whether an update is needed
            - dict: Complete object data for update including all fields from the existing
                   object with any modifications from the params
    """
    changed = False

    # Start with a fresh update model using all fields from existing object
    update_data = {
        "id": str(existing.id),  # Convert UUID to string for Pydantic
        "name": existing.name,
    }

    # Add the container field (folder, snippet, or device)
    for container in ["folder", "snippet", "device"]:
        container_value = getattr(existing, container, None)
        if container_value is not None:
            update_data[container] = container_value

    # Check each parameter that can be updated
    for param in ["description"]:
        # Set the current value as default
        current_value = getattr(existing, param, None)
        update_data[param] = current_value

        # If user provided a new value, use it and check if it's different
        if param in params and params[param] is not None:
            if current_value != params[param]:
                update_data[param] = params[param]
                changed = True

    # Check and update match_list configuration
    if "match_list" in params and params["match_list"] is not None:
        # Convert existing match_list to comparable format
        existing_match_list = []
        if hasattr(existing, "match_list") and existing.match_list is not None:
            for match in existing.match_list:
                match_dict = {
                    "name": match.name,
                    "action": match.action,
                }

                # Add optional fields if present
                for field in [
                    "send_http",
                    "send_syslog",
                    "filter",
                    "action_desc",
                    "log_type",
                    "send_to_panorama",
                    "quarantine",
                    "tag",
                ]:
                    field_value = getattr(match, field, None)
                    if field_value is not None:
                        match_dict[field] = field_value

                existing_match_list.append(match_dict)

        # Compare match_list configurations
        # Normalize match_list for comparison by sorting
        def normalize_match_list(match_list):
            return sorted(match_list, key=lambda x: x["name"])

        if normalize_match_list(existing_match_list) != normalize_match_list(params["match_list"]):
            update_data["match_list"] = params["match_list"]
            changed = True
        else:
            update_data["match_list"] = existing_match_list

    # Check and update filter configuration
    if "filter" in params and params["filter"] is not None:
        # Convert existing filter to comparable format
        existing_filter = []
        if hasattr(existing, "filter") and existing.filter is not None:
            for filter_item in existing.filter:
                filter_dict = {
                    "name": filter_item.name,
                    "filter": filter_item.filter,
                }
                existing_filter.append(filter_dict)

        # Compare filter configurations
        # Normalize filter for comparison by sorting
        def normalize_filter(filter_list):
            return sorted(filter_list, key=lambda x: x["name"])

        if normalize_filter(existing_filter) != normalize_filter(params["filter"]):
            update_data["filter"] = params["filter"]
            changed = True
        else:
            update_data["filter"] = existing_filter

    return changed, update_data


def get_existing_log_forwarding_profile(client, log_forwarding_profile_data):
    """
    Attempt to fetch an existing log forwarding profile object.

    Args:
        client: SCM client instance
        log_forwarding_profile_data (dict): Log forwarding profile parameters to search for

    Returns:
        tuple: (bool, object) indicating if log forwarding profile exists and the log forwarding profile object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if (
                container in log_forwarding_profile_data
                and log_forwarding_profile_data[container] is not None
            ):
                container_type = container
                break

        if container_type is None or "name" not in log_forwarding_profile_data:
            return False, None

        # Fetch the log forwarding profile using the appropriate container
        existing = client.log_forwarding_profile.fetch(
            name=log_forwarding_profile_data["name"],
            **{container_type: log_forwarding_profile_data[container_type]},
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the log forwarding profile object module.

    This module provides functionality to create, update, and delete log forwarding profile objects
    in the SCM (Strata Cloud Manager) system. It handles various log forwarding configurations
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=LogForwardingProfileSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet", "device"],
        ],
        required_one_of=[["folder", "snippet", "device"]],
        required_if=[
            ["state", "present", ["match_list"], True],
        ],
    )

    result = {"changed": False, "log_forwarding_profile": None}

    try:
        client = get_scm_client(module)
        log_forwarding_profile_data = build_log_forwarding_profile_data(module.params)

        # Validate container is specified
        if not is_container_specified(log_forwarding_profile_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing log forwarding profile
        exists, existing_log_forwarding_profile = get_existing_log_forwarding_profile(
            client, log_forwarding_profile_data
        )

        if module.params["state"] == "present":
            if not exists:
                # Create new log forwarding profile
                if not module.check_mode:
                    try:
                        new_log_forwarding_profile = client.log_forwarding_profile.create(
                            data=log_forwarding_profile_data
                        )
                        result["log_forwarding_profile"] = serialize_response(
                            new_log_forwarding_profile
                        )
                        result["changed"] = True
                    except NameNotUniqueError:
                        # If profile already exists, let's just fetch it and return it
                        container_type = None
                        for container in ["folder", "snippet", "device"]:
                            if (
                                container in log_forwarding_profile_data
                                and log_forwarding_profile_data[container] is not None
                            ):
                                container_type = container
                                break

                        existing = client.log_forwarding_profile.fetch(
                            name=log_forwarding_profile_data["name"],
                            **{container_type: log_forwarding_profile_data[container_type]},
                        )
                        result["log_forwarding_profile"] = serialize_response(existing)
                        result["changed"] = False
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid log forwarding profile data: {str(e)}")
                    except Exception as e:
                        # This is to handle unexpected errors like 500 errors during idempotence testing
                        # First try to check if the profile already exists (which it might in case of a race condition or API error)
                        try:
                            container_type = None
                            for container in ["folder", "snippet", "device"]:
                                if (
                                    container in log_forwarding_profile_data
                                    and log_forwarding_profile_data[container] is not None
                                ):
                                    container_type = container
                                    break

                            existing = client.log_forwarding_profile.fetch(
                                name=log_forwarding_profile_data["name"],
                                **{container_type: log_forwarding_profile_data[container_type]},
                            )
                            # If we get here, the profile exists despite the earlier error
                            result["log_forwarding_profile"] = serialize_response(existing)
                            result["changed"] = False
                            module.warn(f"Creation failed but profile exists already: {str(e)}")
                        except Exception:
                            # If we can't fetch the profile after the error, it probably doesn't exist
                            # so re-raise the original error
                            module.fail_json(msg=f"Error creating log forwarding profile: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(
                    existing_log_forwarding_profile, log_forwarding_profile_data
                )

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = LogForwardingProfileUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_log_forwarding_profile = client.log_forwarding_profile.update(
                            update_model
                        )
                        result["log_forwarding_profile"] = serialize_response(
                            updated_log_forwarding_profile
                        )
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["log_forwarding_profile"] = serialize_response(
                        existing_log_forwarding_profile
                    )

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    profile_id = str(existing_log_forwarding_profile.id)
                    client.log_forwarding_profile.delete(profile_id)
                    result["changed"] = True
                    result["msg"] = f"Deleted log forwarding profile with ID: {profile_id}"
                else:
                    result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
