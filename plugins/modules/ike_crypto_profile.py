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
Ansible module for managing IKE crypto profiles in SCM.

This module provides functionality to create, update, and delete IKE crypto profiles
in the SCM (Strata Cloud Manager) system.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import uuid
from datetime import datetime

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.ike_crypto_profile import (
    IKECryptoProfileSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError
from scm.models.network import IKECryptoProfileUpdateModel

DOCUMENTATION = r"""
---
module: ike_crypto_profile

short_description: Manage IKE crypto profiles in SCM.

version_added: "0.1.0"

description:
    - Manage IKE crypto profiles within Strata Cloud Manager (SCM).
    - Create, update, and delete IKE crypto profile objects.
    - Configure hash algorithms, encryption algorithms, and DH groups.
    - Set lifetime parameters and authentication settings.

options:
    name:
        description: The name of the IKE crypto profile.
        required: true
        type: str
    description:
        description: Description of the IKE crypto profile.
        required: false
        type: str
    hash:
        description: List of hash algorithms to use.
        required: false
        type: list
        elements: str
        choices: ["md5", "sha1", "sha256", "sha384", "sha512"]
    encryption:
        description: List of encryption algorithms to use.
        required: false
        type: list
        elements: str
        choices: ["des", "3des", "aes-128-cbc", "aes-192-cbc", "aes-256-cbc", "aes-128-gcm", "aes-256-gcm"]
    dh_group:
        description: List of Diffie-Hellman groups to use.
        required: false
        type: list
        elements: str
        choices: ["group1", "group2", "group5", "group14", "group19", "group20"]
    lifetime_seconds:
        description: Lifetime in seconds (180-65535).
        required: false
        type: int
    lifetime_minutes:
        description: Lifetime in minutes (3-65535).
        required: false
        type: int
    lifetime_hours:
        description: Lifetime in hours (1-65535).
        required: false
        type: int
    lifetime_days:
        description: Lifetime in days (1-365).
        required: false
        type: int
    authentication_multiple:
        description: IKEv2 SA reauthentication interval equals authentication-multiple * rekey-lifetime; 0 means reauthentication disabled.
        required: false
        type: int
        default: 0
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
        description: Desired state of the IKE crypto profile.
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
- name: Manage IKE Crypto Profiles in Strata Cloud Manager
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

    - name: Create an IKE crypto profile with AES-256 and SHA-256
      cdot65.scm.ike_crypto_profile:
        provider: "{{ provider }}"
        name: "ikev2-aes256-sha256"
        description: "IKEv2 AES-256 SHA-256 profile"
        hash:
          - "sha256"
        encryption:
          - "aes-256-cbc"
        dh_group:
          - "group14"
        lifetime_hours: 8
        authentication_multiple: 0
        folder: "SharedFolder"
        state: "present"

    - name: Create an IKE crypto profile with multiple algorithms
      cdot65.scm.ike_crypto_profile:
        provider: "{{ provider }}"
        name: "ikev2-multi-algo"
        description: "IKEv2 with multiple algorithm options"
        hash:
          - "sha256"
          - "sha384"
          - "sha512"
        encryption:
          - "aes-256-cbc"
          - "aes-256-gcm"
        dh_group:
          - "group14"
          - "group19"
          - "group20"
        lifetime_days: 1
        folder: "SharedFolder"
        state: "present"

    - name: Update an IKE crypto profile
      cdot65.scm.ike_crypto_profile:
        provider: "{{ provider }}"
        name: "ikev2-aes256-sha256"
        description: "Updated IKEv2 AES-256 SHA-256 profile"
        hash:
          - "sha256"
        encryption:
          - "aes-256-cbc"
        dh_group:
          - "group14"
          - "group19"  # Added a new DH group
        lifetime_hours: 24  # Changed lifetime
        folder: "SharedFolder"
        state: "present"

    - name: Delete an IKE crypto profile
      cdot65.scm.ike_crypto_profile:
        provider: "{{ provider }}"
        name: "ikev2-multi-algo"
        folder: "SharedFolder"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
profile:
    description: Details about the IKE crypto profile.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "ikev2-aes256-sha256"
        description: "IKEv2 AES-256 SHA-256 profile"
        folder: "SharedFolder"
        hash: ["sha256"]
        encryption: ["aes-256-cbc"]
        dh_group: ["group14"]
        authentication_multiple: 0
"""

# Storage for tracking changes during module execution
changed_records = {}


def build_profile_data(module_params):
    """
    Build IKE crypto profile data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant profile parameters
    """
    profile_data = {}

    # Copy basic parameters
    for param in ["name", "description"]:
        if module_params.get(param) is not None:
            profile_data[param] = module_params[param]

    # Copy algorithm parameters
    for param in ["hash", "encryption", "dh_group"]:
        if module_params.get(param) is not None:
            profile_data[param] = module_params[param]

    # Copy authentication_multiple if provided
    if module_params.get("authentication_multiple") is not None:
        profile_data["authentication_multiple"] = module_params["authentication_multiple"]

    # Handle lifetime parameter (only one can be set)
    lifetime_params = ["lifetime_seconds", "lifetime_minutes", "lifetime_hours", "lifetime_days"]
    for lifetime_param in lifetime_params:
        if module_params.get(lifetime_param) is not None:
            # Extract the unit from the parameter name (after "lifetime_")
            unit = lifetime_param.split("_")[1]
            # Create the lifetime object with the appropriate unit key
            profile_data["lifetime"] = {unit: module_params[lifetime_param]}
            break  # Only use the first lifetime parameter found

    # Copy container parameters
    for container in ["folder", "snippet", "device"]:
        if module_params.get(container) is not None:
            profile_data[container] = module_params[container]

    return profile_data


def is_container_specified(data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        data (dict): Profile parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def get_existing_profile(client, profile_data):
    """
    Attempt to fetch an existing IKE crypto profile.

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
        existing = client.ike_crypto_profile.fetch(
            name=profile_data["name"], **{container_type: profile_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def needs_update(existing, params):
    """
    Determine if the IKE crypto profile needs to be updated.

    Args:
        existing: Existing IKE crypto profile object from the SCM API
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

    # Check parameters that can be updated
    for param in ["description", "hash", "encryption", "dh_group", "authentication_multiple"]:
        # Set the current value as default
        current_value = getattr(existing, param, None)
        update_data[param] = current_value

        # If user provided a new value, check if it's different
        if param in params and params[param] is not None:
            if current_value != params[param]:
                update_data[param] = params[param]
                changed = True

    # Handle lifetime parameter differently
    if "lifetime" in params and params["lifetime"] is not None:
        # Existing lifetime might be None or a specific time unit
        existing_lifetime = getattr(existing, "lifetime", None)

        if existing_lifetime != params["lifetime"]:
            update_data["lifetime"] = params["lifetime"]
            changed = True
    else:
        # Include existing lifetime in update data if it exists
        existing_lifetime = getattr(existing, "lifetime", None)
        if existing_lifetime is not None:
            update_data["lifetime"] = existing_lifetime

    return changed, update_data


def main():
    """
    Main execution path for the ike_crypto_profile module.

    This module provides functionality to create, update, and delete IKE crypto profiles
    in the SCM (Strata Cloud Manager) system.

    :return: Ansible module exit data
    :rtype: dict
    """
    spec = IKECryptoProfileSpec.spec()

    module = AnsibleModule(
        argument_spec=spec,
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet", "device"],
            ["lifetime_seconds", "lifetime_minutes", "lifetime_hours", "lifetime_days"],
        ],
        required_one_of=[["folder", "snippet", "device"]],
        required_if=[["state", "present", ["hash", "encryption", "dh_group"], True]],
    )

    result = {"changed": False, "profile": None}

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
            # Algorithm parameters are required for create (handled by required_if)

            if not exists:
                # Create new profile
                if not module.check_mode:
                    try:
                        new_profile = client.ike_crypto_profile.create(data=profile_data)
                        result["profile"] = serialize_response(new_profile)
                        result["changed"] = True
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid profile data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_profile, profile_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = IKECryptoProfileUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_profile = client.ike_crypto_profile.update(update_model)
                        result["profile"] = serialize_response(updated_profile)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["profile"] = serialize_response(existing_profile)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.ike_crypto_profile.delete(str(existing_profile.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
