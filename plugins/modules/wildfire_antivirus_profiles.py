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
Ansible module for managing WildFire antivirus profiles in SCM.

This module provides functionality to create, update, and delete WildFire antivirus profiles
in the SCM (Strata Cloud Manager) system. It handles various profile configurations
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.wildfire_antivirus_profiles import (
    WildfireAntivirusProfileSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.security.wildfire_antivirus_profiles import (
    WildfireAvProfileUpdateModel,
)

DOCUMENTATION = r"""
---
module: wildfire_antivirus_profiles

short_description: Manage WildFire antivirus profiles in SCM.

version_added: "0.1.0"

description:
    - Manage WildFire antivirus profiles within Strata Cloud Manager (SCM).
    - Create, update, and delete WildFire antivirus profiles for malware analysis using either public or private cloud infrastructure.
    - Configure rules based on traffic direction, application types, and file types.
    - Add exceptions for specific scenarios.
    - Enables packet capture capabilities when needed.
    - Ensures that at least one rule is provided for create/update operations.
    - Ensures that exactly one container type (folder, snippet, device) is provided.

options:
    name:
        description: The name of the WildFire antivirus profile (max 63 chars).
        required: true
        type: str
    description:
        description: Description of the WildFire antivirus profile (max 1023 chars).
        required: false
        type: str
    packet_capture:
        description: Whether packet capture is enabled.
        required: false
        type: bool
        default: false
    rules:
        description: List of WildFire antivirus protection rules to apply. At least one rule is required.
        required: true
        type: list
        elements: dict
        suboptions:
            name:
                description: Name of the rule.
                required: true
                type: str
            direction:
                description: Direction of traffic to inspect.
                required: true
                type: str
                choices: ["download", "upload", "both"]
            analysis:
                description: Analysis type for malware detection.
                required: false
                type: str
                choices: ["public-cloud", "private-cloud"]
            application:
                description: List of applications this rule applies to.
                required: false
                type: list
                elements: str
                default: ["any"]
            file_type:
                description: List of file types this rule applies to.
                required: false
                type: list
                elements: str
                default: ["any"]
    mlav_exception:
        description: List of Machine Learning Anti-Virus exceptions.
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: Name of the MLAV exception.
                required: true
                type: str
            description:
                description: Description of the MLAV exception.
                required: false
                type: str
            filename:
                description: Filename to exempt from scanning.
                required: true
                type: str
    threat_exception:
        description: List of threat exceptions.
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: Name of the threat exception.
                required: true
                type: str
            notes:
                description: Additional notes for the threat exception.
                required: false
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
        description: Desired state of the WildFire antivirus profile.
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
- name: Manage WildFire Antivirus Profiles in Strata Cloud Manager
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

    - name: Create a basic WildFire antivirus profile
      cdot65.scm.wildfire_antivirus_profiles:
        provider: "{{ provider }}"
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
        state: "present"

    - name: Create a comprehensive WildFire antivirus profile
      cdot65.scm.wildfire_antivirus_profiles:
        provider: "{{ provider }}"
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
          - name: "FTP-Upload-Rule"
            direction: "upload"
            analysis: "private-cloud"
            application: ["ftp"]
            file_type: ["exe", "dll"]
        mlav_exception:
          - name: "Exception1"
            description: "Test exception"
            filename: "legitimate.exe"
        threat_exception:
          - name: "ThreatEx1"
            notes: "Known false positive"
        state: "present"

    - name: Update a WildFire antivirus profile
      cdot65.scm.wildfire_antivirus_profiles:
        provider: "{{ provider }}"
        name: "Basic-Wildfire-AV"
        description: "Updated WildFire antivirus profile"
        folder: "Texas"
        packet_capture: false
        rules:
          - name: "Updated-Rule"
            direction: "download"
            analysis: "public-cloud"
            application: ["web-browsing"]
            file_type: ["pe"]
        state: "present"

    - name: Delete a WildFire antivirus profile
      cdot65.scm.wildfire_antivirus_profiles:
        provider: "{{ provider }}"
        name: "Basic-Wildfire-AV"
        folder: "Texas"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
wildfire_antivirus_profile:
    description: Details about the WildFire antivirus profile.
    returned: when state is present
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


def build_profile_data(module_params):
    """
    Build WildFire antivirus profile data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant profile parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(profile_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        profile_data (dict): Profile parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [profile_data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the WildFire antivirus profile needs to be updated.

    Args:
        existing: Existing profile object from the SCM API
        params (dict): Profile parameters with desired state from Ansible module

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
    for param in ["description", "packet_capture"]:
        # Set the current value as default
        current_value = getattr(existing, param, None)
        update_data[param] = current_value

        # If user provided a new value, use it and check if it's different
        if param in params and params[param] is not None:
            if current_value != params[param]:
                update_data[param] = params[param]
                changed = True

    # Check rules for changes
    current_rules = getattr(existing, "rules", [])
    # Deep comparison would be complex, so for simplicity we'll assume rules have changed
    # if the user provides them in the parameters
    if "rules" in params and params["rules"] is not None:
        if params["rules"] != current_rules:
            update_data["rules"] = params["rules"]
            changed = True
    else:
        update_data["rules"] = current_rules

    # Check mlav_exception for changes
    current_mlav_exceptions = getattr(existing, "mlav_exception", [])
    if "mlav_exception" in params and params["mlav_exception"] is not None:
        if params["mlav_exception"] != current_mlav_exceptions:
            update_data["mlav_exception"] = params["mlav_exception"]
            changed = True
    else:
        if current_mlav_exceptions:
            update_data["mlav_exception"] = current_mlav_exceptions

    # Check threat_exception for changes
    current_threat_exceptions = getattr(existing, "threat_exception", [])
    if "threat_exception" in params and params["threat_exception"] is not None:
        if params["threat_exception"] != current_threat_exceptions:
            update_data["threat_exception"] = params["threat_exception"]
            changed = True
    else:
        if current_threat_exceptions:
            update_data["threat_exception"] = current_threat_exceptions

    return changed, update_data


def get_existing_profile(client, profile_data):
    """
    Attempt to fetch an existing WildFire antivirus profile object.

    Args:
        client: SCM client instance
        profile_data (dict): Profile parameters to search for

    Returns:
        tuple: (bool, object) indicating if profile exists and the profile object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if container in profile_data and profile_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in profile_data:
            return False, None

        # Fetch the profile using the appropriate container
        existing = client.wildfire_antivirus_profile.fetch(
            name=profile_data["name"], **{container_type: profile_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the WildFire antivirus profiles module.

    This module provides functionality to create, update, and delete WildFire antivirus profile objects
    in the SCM (Strata Cloud Manager) system. It handles various profile configurations
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=WildfireAntivirusProfileSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet", "device"],
        ],
        required_one_of=[["folder", "snippet", "device"]],
        required_if=[],
        required_together=[],
    )

    result = {"changed": False, "wildfire_antivirus_profile": None}

    try:
        client = get_scm_client(module)
        profile_data = build_profile_data(module.params)

        # Validate container is specified
        if not is_container_specified(profile_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing profile
        exists, existing_profile = get_existing_profile(client, profile_data)

        if module.params["state"] == "present":
            # Check if rules parameter is provided for create/update
            if "rules" not in module.params or not module.params["rules"]:
                module.fail_json(msg="Rules parameter is required when state is present")

            if not exists:
                # Create new profile
                if not module.check_mode:
                    try:
                        new_profile = client.wildfire_antivirus_profile.create(data=profile_data)
                        result["wildfire_antivirus_profile"] = serialize_response(new_profile)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"A WildFire antivirus profile with name '{profile_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid WildFire antivirus profile data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_profile, profile_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = WildfireAvProfileUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_profile = client.wildfire_antivirus_profile.update(update_model)
                        result["wildfire_antivirus_profile"] = serialize_response(updated_profile)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["wildfire_antivirus_profile"] = serialize_response(existing_profile)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.wildfire_antivirus_profile.delete(str(existing_profile.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
