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
Ansible module for managing decryption profile objects in SCM.

This module provides functionality to create, update, and delete decryption profile objects
in the SCM (Strata Cloud Manager) system. It handles various profile attributes
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from pydantic import ValidationError

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.decryption_profile import (  # noqa: F401
    DecryptionProfileSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import (  # noqa: F401
    get_scm_client,
)
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (  # noqa: F401
    serialize_response,
)
from scm.config.security.decryption_profile import DecryptionProfile
from scm.exceptions import NotFoundError
from scm.models.security.decryption_profiles import (
    DecryptionProfileCreateModel,
    DecryptionProfileUpdateModel,
)

DOCUMENTATION = r"""
---
module: decryption_profile

short_description: Manage decryption profile objects in SCM.

version_added: "0.1.0"

description:
    - Manage decryption profile objects within Strata Cloud Manager (SCM).
    - Supports creation, modification, and deletion of decryption profiles.
    - Configure SSL Forward Proxy, SSL Inbound Inspection, and SSL No Proxy settings.
    - Customize SSL protocol settings including version, algorithms, and ciphers.
    - Ensures proper validation of profile attributes.
    - Ensures that exactly one of 'folder', 'snippet', or 'device' is provided.

options:
    name:
        description: The name of the decryption profile.
        required: true
        type: str
    description:
        description: Description of the profile.
        required: false
        type: str
    ssl_forward_proxy:
        description: SSL Forward Proxy settings.
        required: false
        type: dict
        suboptions:
            enabled:
                description: Enable SSL Forward Proxy.
                required: false
                type: bool
                default: false
            block_unsupported_cipher:
                description: Block sessions with unsupported ciphers.
                required: false
                type: bool
                default: false
            block_unknown_cert:
                description: Block sessions with unknown certificates.
                required: false
                type: bool
                default: false
            block_expired_cert:
                description: Block sessions with expired certificates.
                required: false
                type: bool
                default: false
            block_timeoff_cert:
                description: Block sessions with certificates not yet valid.
                required: false
                type: bool
                default: false
            block_untrusted_issuer:
                description: Block sessions with untrusted issuer certificates.
                required: false
                type: bool
                default: false
            block_unknown_status:
                description: Block sessions with certificates that have unknown status.
                required: false
                type: bool
                default: false
    ssl_inbound_inspection:
        description: SSL Inbound Inspection settings.
        required: false
        type: dict
        suboptions:
            enabled:
                description: Enable SSL Inbound Inspection.
                required: false
                type: bool
                default: false
    ssl_no_proxy:
        description: SSL No Proxy settings.
        required: false
        type: dict
        suboptions:
            enabled:
                description: Enable SSL No Proxy.
                required: false
                type: bool
                default: false
            block_session_expired_cert:
                description: Block sessions with expired certificates.
                required: false
                type: bool
                default: false
            block_session_untrusted_issuer:
                description: Block sessions with untrusted issuer certificates.
                required: false
                type: bool
                default: false
    ssl_protocol_settings:
        description: SSL Protocol settings.
        required: false
        type: dict
        suboptions:
            min_version:
                description: Minimum TLS version to support.
                required: false
                type: str
                choices: ['tls1-0', 'tls1-1', 'tls1-2', 'tls1-3']
                default: "tls1-0"
            max_version:
                description: Maximum TLS version to support.
                required: false
                type: str
                choices: ['tls1-0', 'tls1-1', 'tls1-2', 'tls1-3']
                default: "tls1-3"
            keyxchg_algorithm:
                description: Key exchange algorithms to allow.
                required: false
                type: list
                elements: str
                choices: ['dhe', 'ecdhe']
            encrypt_algorithm:
                description: Encryption algorithms to allow.
                required: false
                type: list
                elements: str
                choices: ['rc4', 'rc4-md5', 'aes-128-cbc', 'aes-128-gcm', 'aes-256-cbc', 'aes-256-gcm', '3des']
            auth_algorithm:
                description: Authentication algorithms to allow.
                required: false
                type: list
                elements: str
                choices: ['sha1', 'sha256', 'sha384']
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
                no_log: True
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
        description: Desired state of the decryption profile.
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
- name: Manage Decryption Profiles in Strata Cloud Manager
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
    - name: Create decryption profile with SSL Forward Proxy enabled
      cdot65.scm.decryption_profile:
        provider: "{{ provider }}"
        name: "Custom-Decryption-Profile"
        description: "Custom decryption profile for forward proxy"
        ssl_forward_proxy:
          enabled: true
          block_expired_cert: true
          block_untrusted_issuer: true
        ssl_protocol_settings:
          min_version: "tls1-2"
          max_version: "tls1-3"
          keyxchg_algorithm: ["ecdhe"]
          encrypt_algorithm: ["aes-128-gcm", "aes-256-gcm"]
          auth_algorithm: ["sha256", "sha384"]
        folder: "Production"
        state: "present"

    - name: Update decryption profile with additional settings
      cdot65.scm.decryption_profile:
        provider: "{{ provider }}"
        name: "Custom-Decryption-Profile"
        description: "Updated decryption profile with additional settings"
        ssl_forward_proxy:
          enabled: true
          block_expired_cert: true
          block_untrusted_issuer: true
          block_unknown_cert: true
        ssl_no_proxy:
          enabled: true
          block_session_expired_cert: true
        ssl_protocol_settings:
          min_version: "tls1-2"
          max_version: "tls1-3"
          keyxchg_algorithm: ["ecdhe"]
          encrypt_algorithm: ["aes-128-gcm", "aes-256-gcm"]
          auth_algorithm: ["sha256", "sha384"]
        folder: "Production"
        state: "present"

    - name: Remove decryption profile
      cdot65.scm.decryption_profile:
        provider: "{{ provider }}"
        name: "Custom-Decryption-Profile"
        folder: "Production"
        state: "absent"
"""

RETURN = r"""
decryption_profile:
    description: Details about the decryption profile object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Custom-Decryption-Profile"
        description: "Custom decryption profile for forward proxy"
        ssl_forward_proxy:
          enabled: true
          block_expired_cert: true
          block_untrusted_issuer: true
        ssl_protocol_settings:
          min_version: "tls1-2"
          max_version: "tls1-3"
          keyxchg_algorithm: ["ecdhe"]
          encrypt_algorithm: ["aes-128-gcm", "aes-256-gcm"]
          auth_algorithm: ["sha256", "sha384"]
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
    # Create a copy of the parameters to avoid modifying the original
    profile_data = {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }

    return profile_data


def get_existing_profile(profile_api, profile_data):
    """
    Attempt to fetch an existing decryption profile object.

    Args:
        profile_api: DecryptionProfile API instance
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
    Determine if the decryption profile needs to be updated.

    Args:
        existing: Existing decryption profile object from the SCM API
        params (dict): Decryption profile parameters with desired state from Ansible module

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

    # Add description if it exists
    if hasattr(existing, "description") and existing.description is not None:
        update_data["description"] = existing.description
        if "description" in params and params["description"] is not None:
            if existing.description != params["description"]:
                update_data["description"] = params["description"]
                changed = True

    # Handle nested dict fields
    dict_fields = [
        "ssl_forward_proxy",
        "ssl_inbound_inspection",
        "ssl_no_proxy",
        "ssl_protocol_settings",
    ]

    for field in dict_fields:
        current_value = getattr(existing, field, None)
        # If current value is None, initialize as empty dict
        update_data[field] = {} if current_value is None else current_value

        # If user provided this field, check for changes
        if field in params and params[field] is not None:
            # For each field, determine if we need to update
            if current_value != params[field]:
                update_data[field] = params[field]
                changed = True

    return changed, update_data


def is_container_specified(profile_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        profile_data (dict): Decryption profile parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [profile_data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def main():
    """
    Main execution path for the decryption profile module.

    This module provides functionality to create, update, and delete decryption profile objects
    in the SCM (Strata Cloud Manager) system. It handles various profile attributes
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=DecryptionProfileSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        required_one_of=[["folder", "snippet", "device"]],
    )

    result = {"changed": False, "decryption_profile": None}

    try:
        client = get_scm_client(module)
        profile_api = DecryptionProfile(client)
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
                        DecryptionProfileCreateModel(**profile_data)

                        # Create profile
                        new_profile = profile_api.create(data=profile_data)
                        result["decryption_profile"] = serialize_response(new_profile)
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
                            profile_update_model = DecryptionProfileUpdateModel(**update_data)

                            # Perform update
                            updated_profile = profile_api.update(profile=profile_update_model)
                            result["decryption_profile"] = serialize_response(updated_profile)
                            result["changed"] = True
                        except ValidationError as e:
                            module.fail_json(msg=f"Invalid update data: {str(e)}")
                        except Exception as e:
                            module.fail_json(msg=f"Failed to update profile: {str(e)}")
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["decryption_profile"] = serialize_response(existing_profile)

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
