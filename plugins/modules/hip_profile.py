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
Ansible module for managing HIP profiles in SCM.

This module provides functionality to create, update, and delete HIP profiles
in the SCM (Strata Cloud Manager) system. It handles match expressions
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.hip_profile import HIPProfileSpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.objects import HIPProfileUpdateModel

DOCUMENTATION = r"""
---
module: hip_profile

short_description: Manage HIP profiles in SCM.

version_added: "0.1.0"

description:
    - Manage HIP profiles within Strata Cloud Manager (SCM).
    - Create, update, and delete HIP profiles with match expressions.
    - Ensures that exactly one container type (folder, snippet, device) is provided.
    - HIP profiles define match criteria expressions used to associate HIP objects with policy rules.

options:
    name:
        description: The name of the HIP profile (max 31 chars).
        required: true
        type: str
    description:
        description: Description of the HIP profile (max 255 chars).
        required: false
        type: str
    match:
        description: Match expression for the profile (max 2048 chars).
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
        description: Desired state of the HIP profile.
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
- name: Manage HIP Profiles in Strata Cloud Manager
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

    - name: Create a basic HIP profile with single match expression
      cdot65.scm.hip_profile:
        provider: "{{ provider }}"
        name: "windows-workstations"
        description: "Windows workstations basic profile"
        match: '"is-win"'
        folder: "Shared"
        state: "present"

    - name: Create a HIP profile with complex match expression
      cdot65.scm.hip_profile:
        provider: "{{ provider }}"
        name: "secure-workstations"
        description: "Secured workstations profile"
        match: '"is-win" and "is-firewall-enabled"'
        folder: "Shared"
        state: "present"

    - name: Update a HIP profile with new match expression
      cdot65.scm.hip_profile:
        provider: "{{ provider }}"
        name: "secure-workstations"
        description: "Enhanced secure workstations profile"
        match: '"is-win" and "is-firewall-enabled" and "is-disk-encrypted"'
        folder: "Shared"
        state: "present"

    - name: Delete a HIP profile
      cdot65.scm.hip_profile:
        provider: "{{ provider }}"
        name: "windows-workstations"
        folder: "Shared"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
hip_profile:
    description: Details about the HIP profile.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "secure-workstations"
        description: "Secured workstations profile"
        match: '"is-win" and "is-firewall-enabled"'
        folder: "Shared"
"""


def build_hip_profile_data(module_params):
    """
    Build HIP profile data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant HIP profile parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(hip_profile_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        hip_profile_data (dict): HIP profile parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [hip_profile_data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the HIP profile needs to be updated.

    Args:
        existing: Existing HIP profile object from the SCM API
        params (dict): HIP profile parameters with desired state from Ansible module

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
    for param in ["description", "match"]:
        # Set the current value as default
        current_value = getattr(existing, param, None)
        update_data[param] = current_value

        # If user provided a new value, use it and check if it's different
        if param in params and params[param] is not None:
            if current_value != params[param]:
                update_data[param] = params[param]
                changed = True

    return changed, update_data


def get_existing_hip_profile(client, hip_profile_data):
    """
    Attempt to fetch an existing HIP profile.

    Args:
        client: SCM client instance
        hip_profile_data (dict): HIP profile parameters to search for

    Returns:
        tuple: (bool, object) indicating if HIP profile exists and the HIP profile object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if container in hip_profile_data and hip_profile_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in hip_profile_data:
            return False, None

        # Fetch the HIP profile using the appropriate container
        existing = client.hip_profile.fetch(
            name=hip_profile_data["name"], **{container_type: hip_profile_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the HIP profile module.

    This module provides functionality to create, update, and delete HIP profiles
    in the SCM (Strata Cloud Manager) system. It handles match expressions
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=HIPProfileSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet", "device"],
        ],
        required_one_of=[["folder", "snippet", "device"]],
        required_if=[["state", "present", ["match"], False]],
    )

    result = {"changed": False, "hip_profile": None}

    try:
        client = get_scm_client(module)
        hip_profile_data = build_hip_profile_data(module.params)

        # Validate container is specified
        if not is_container_specified(hip_profile_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing HIP profile
        exists, existing_hip_profile = get_existing_hip_profile(client, hip_profile_data)

        if module.params["state"] == "present":
            if not exists:
                # Create new HIP profile
                if not module.check_mode:
                    try:
                        new_hip_profile = client.hip_profile.create(data=hip_profile_data)
                        result["hip_profile"] = serialize_response(new_hip_profile)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"A HIP profile with name '{hip_profile_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid HIP profile data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_hip_profile, hip_profile_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = HIPProfileUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_hip_profile = client.hip_profile.update(update_model)
                        result["hip_profile"] = serialize_response(updated_hip_profile)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["hip_profile"] = serialize_response(existing_hip_profile)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.hip_profile.delete(str(existing_hip_profile.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
