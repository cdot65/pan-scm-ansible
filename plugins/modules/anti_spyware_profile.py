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
Ansible module for managing anti-spyware profile objects in SCM.

This module provides functionality to create, update, and delete anti-spyware profile objects
in the SCM (Strata Cloud Manager) system. It handles various profile attributes
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.anti_spyware_profile import \
    AntiSpywareProfileSpec  # noqa: F401
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import (  # noqa: F401
    get_scm_client,
)
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (  # noqa: F401
    serialize_response,
)
from pydantic import ValidationError

from scm.config.security.anti_spyware_profile import AntiSpywareProfile
from scm.exceptions import NotFoundError
from scm.models.security.anti_spyware_profiles import (
    AntiSpywareProfileCreateModel,
    AntiSpywareProfileUpdateModel,
)

DOCUMENTATION = r"""
---
module: anti_spyware_profile

short_description: Manage anti-spyware profile objects in SCM.

version_added: "0.1.0"

description:
    - Manage anti-spyware profile objects within Strata Cloud Manager (SCM).
    - Supports creation, modification, and deletion of anti-spyware profiles.
    - Ensures proper validation of profile attributes.
    - Ensures that exactly one of 'folder', 'snippet', or 'device' is provided.

options:
    name:
        description: The name of the anti-spyware profile.
        required: true
        type: str
    description:
        description: Description of the profile.
        required: false
        type: str
    cloud_inline_analysis:
        description: Enable cloud inline analysis.
        required: false
        type: bool
        default: false
    inline_exception_edl_url:
        description: List of inline exception EDL URLs.
        required: false
        type: list
        elements: str
    inline_exception_ip_address:
        description: List of inline exception IP addresses.
        required: false
        type: list
        elements: str
    mica_engine_spyware_enabled:
        description: List of MICA engine spyware enabled entries.
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: Name of the MICA engine spyware detector.
                required: true
                type: str
            inline_policy_action:
                description: Inline policy action.
                required: false
                type: str
                choices: ['alert', 'allow', 'drop', 'reset-both', 'reset-client', 'reset-server']
                default: 'alert'
    rules:
        description: List of anti-spyware rules.
        required: true
        type: list
        elements: dict
        suboptions:
            name:
                description: Rule name.
                required: true
                type: str
            severity:
                description: List of severities.
                required: true
                type: list
                elements: str
                choices: ['critical', 'high', 'medium', 'low', 'informational', 'any']
            category:
                description: Rule category.
                required: true
                type: str
            threat_name:
                description: Threat name.
                required: false
                type: str
            packet_capture:
                description: Packet capture setting.
                required: false
                type: str
                choices: ['disable', 'single-packet', 'extended-capture']
    threat_exception:
        description: List of threat exceptions.
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: Threat exception name.
                required: true
                type: str
            packet_capture:
                description: Packet capture setting.
                required: true
                type: str
                choices: ['disable', 'single-packet', 'extended-capture']
            exempt_ip:
                description: List of exempt IP entries.
                required: false
                type: list
                elements: dict
                suboptions:
                    name:
                        description: Exempt IP name.
                        required: true
                        type: str
            notes:
                description: Notes for the threat exception.
                required: false
                type: str
    folder:
        description: The folder in which the resource is defined.
        required: false
        type: str
    snippet:
        description: The snippet in which the resource is defined.
        required: false
        type: str
    device:
        description: The device in which the resource is defined.
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
                no_log: true
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
        description: Desired state of the anti-spyware profile.
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
- name: Manage Anti-Spyware Profiles in Strata Cloud Manager
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
    - name: Create anti-spyware profile
      cdot65.scm.anti_spyware_profile:
        provider: "{{ provider }}"
        name: "Custom-Spyware-Profile"
        description: "Custom anti-spyware profile"
        cloud_inline_analysis: true
        rules:
          - name: "Block-Critical-Threats"
            severity: ["critical"]
            category: "spyware"
            packet_capture: "single-packet"
        folder: "Production"
        state: "present"

    - name: Update anti-spyware profile
      cdot65.scm.anti_spyware_profile:
        provider: "{{ provider }}"
        name: "Custom-Spyware-Profile"
        description: "Updated anti-spyware profile"
        rules:
          - name: "Block-Critical-Threats"
            severity: ["critical", "high"]
            category: "spyware"
            packet_capture: "extended-capture"
        folder: "Production"
        state: "present"

    - name: Remove anti-spyware profile
      cdot65.scm.anti_spyware_profile:
        provider: "{{ provider }}"
        name: "Custom-Spyware-Profile"
        folder: "Production"
        state: "absent"
"""

RETURN = r"""
anti_spyware_profile:
    description: Details about the anti-spyware profile object.
    returned: when state is present
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


def build_profile_data(module_params):
    """
    Build profile data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant profile parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def get_existing_profile(profile_api, profile_data):
    """
    Attempt to fetch an existing anti-spyware profile object.

    Args:
        profile_api: AntiSpywareProfile API instance
        profile_data (dict): Profile parameters to search for

    Returns:
        tuple: (bool, object) indicating if profile exists and the profile object if found
    """
    try:
        existing = profile_api.fetch(
            name=profile_data["name"],
            folder=profile_data.get("folder"),
            snippet=profile_data.get("snippet"),
            device=profile_data.get("device"),
        )
        return True, existing
    except NotFoundError:
        return False, None


def needs_update(existing, params):
    """
    Determine if the anti-spyware profile needs to be updated.

    Args:
        existing: Existing anti-spyware profile object from the SCM API
        params (dict): Anti-spyware profile parameters with desired state from Ansible module

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
        "name": existing.name
    }
    
    # Add the container field (folder, snippet, or device)
    for container in ["folder", "snippet", "device"]:
        container_value = getattr(existing, container, None)
        if container_value is not None:
            update_data[container] = container_value
    
    # Add description if it exists
    if hasattr(existing, "description") and existing.description is not None:
        update_data["description"] = existing.description
        if "description" in params and params["description"] is not None:
            if existing.description != params["description"]:
                update_data["description"] = params["description"]
                changed = True
    
    # Add boolean fields
    if hasattr(existing, "cloud_inline_analysis"):
        update_data["cloud_inline_analysis"] = existing.cloud_inline_analysis
        if "cloud_inline_analysis" in params and params["cloud_inline_analysis"] is not None:
            if existing.cloud_inline_analysis != params["cloud_inline_analysis"]:
                update_data["cloud_inline_analysis"] = params["cloud_inline_analysis"]
                changed = True
    
    # Add list fields
    list_fields = [
        "inline_exception_edl_url",
        "inline_exception_ip_address",
        "mica_engine_spyware_enabled",
        "rules",
        "threat_exception"
    ]
    
    for field in list_fields:
        current_value = getattr(existing, field, None)
        # If current value is None, use empty list for Pydantic validation
        update_data[field] = current_value if current_value is not None else []
        
        if field in params and params[field] is not None:
            if current_value != params[field]:
                update_data[field] = params[field]
                changed = True
    
    return changed, update_data


def is_container_specified(profile_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        profile_data (dict): Anti-spyware profile parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [profile_data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def main():
    """
    Main execution path for the anti-spyware profile module.

    This module provides functionality to create, update, and delete anti-spyware profile objects
    in the SCM (Strata Cloud Manager) system. It handles various profile attributes
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=AntiSpywareProfileSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet", "device"]
        ],
        required_one_of=[
            ["folder", "snippet", "device"]
        ],
        required_if=[
            ["state", "present", ["rules"]],
        ],
    )

    result = {
        "changed": False,
        "anti_spyware_profile": None
    }

    try:
        client = get_scm_client(module)
        profile_api = AntiSpywareProfile(client)
        profile_data = build_profile_data(module.params)

        # Validate container is specified
        if not is_container_specified(profile_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing profile
        exists, existing_profile = get_existing_profile(
            profile_api,
            profile_data,
        )

        if module.params["state"] == "present":
            if not exists:
                # Create new profile
                if not module.check_mode:
                    try:
                        # Validate using Pydantic
                        AntiSpywareProfileCreateModel(**profile_data)
                        
                        # Create profile
                        new_profile = profile_api.create(data=profile_data)
                        result["anti_spyware_profile"] = serialize_response(new_profile)
                        result["changed"] = True
                    except ValidationError as e:
                        module.fail_json(msg=f"Invalid profile data: {str(e)}")
                    except Exception as e:
                        module.fail_json(msg=f"Failed to create profile: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_profile, profile_data)

                if need_update:
                    if not module.check_mode:
                        try:
                            # Validate using Pydantic
                            profile_update_model = AntiSpywareProfileUpdateModel(**update_data)
                            
                            # Perform update
                            updated_profile = profile_api.update(profile=profile_update_model)
                            result["anti_spyware_profile"] = serialize_response(updated_profile)
                            result["changed"] = True
                        except ValidationError as e:
                            module.fail_json(msg=f"Invalid update data: {str(e)}")
                        except Exception as e:
                            module.fail_json(msg=f"Failed to update profile: {str(e)}")
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["anti_spyware_profile"] = serialize_response(existing_profile)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    profile_api.delete(str(existing_profile.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
