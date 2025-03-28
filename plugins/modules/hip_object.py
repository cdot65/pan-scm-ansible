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
Ansible module for managing Host Information Profile (HIP) objects in SCM.

This module provides functionality to create, update, and delete HIP objects
in the SCM (Strata Cloud Manager) system. It handles various HIP criteria types
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.hip_object import HIPObjectSpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.objects import HIPObjectUpdateModel

DOCUMENTATION = r"""
---
module: hip_object

short_description: Manage HIP objects in SCM.

version_added: "0.1.0"

description:
    - Manage Host Information Profile (HIP) objects within Strata Cloud Manager (SCM).
    - Create, update, and delete HIP objects for endpoint security posture assessment.
    - Support for various criteria types including host information, network information, patch management, disk encryption, mobile device, and certificate validation.
    - Ensures that exactly one container type (folder, snippet, device) is provided.

options:
    name:
        description: The name of the HIP object (max 31 chars).
        required: true
        type: str
    description:
        description: Description of the HIP object (max 255 chars).
        required: false
        type: str
    host_info:
        description: Host information criteria.
        required: false
        type: dict
        suboptions:
            criteria:
                description: Host information criteria specifications.
                required: true
                type: dict
                suboptions:
                    domain:
                        description: Domain criteria.
                        required: false
                        type: dict
                    os:
                        description: Operating system criteria.
                        required: false
                        type: dict
                    client_version:
                        description: Client version criteria.
                        required: false
                        type: dict
                    host_name:
                        description: Host name criteria.
                        required: false
                        type: dict
                    host_id:
                        description: Host ID criteria.
                        required: false
                        type: dict
                    managed:
                        description: Managed state criteria.
                        required: false
                        type: bool
                    serial_number:
                        description: Serial number criteria.
                        required: false
                        type: dict
    network_info:
        description: Network information criteria.
        required: false
        type: dict
        suboptions:
            criteria:
                description: Network information criteria specifications.
                required: true
                type: dict
                suboptions:
                    network:
                        description: Network criteria.
                        required: false
                        type: dict
    patch_management:
        description: Patch management criteria.
        required: false
        type: dict
        suboptions:
            criteria:
                description: Patch management criteria specifications.
                required: true
                type: dict
                suboptions:
                    is_installed:
                        description: Installation status.
                        required: false
                        type: bool
                        default: true
                    is_enabled:
                        description: Enabled status.
                        required: false
                        type: str
                        choices:
                            - "no"
                            - "yes"
                            - "not-available"
                    missing_patches:
                        description: Missing patches specification.
                        required: false
                        type: dict
                        suboptions:
                            severity:
                                description: Patch severity level.
                                required: false
                                type: int
                            patches:
                                description: List of patches.
                                required: false
                                type: list
                                elements: str
                            check:
                                description: Check type.
                                required: false
                                type: str
                                default: "has-any"
                                choices:
                                    - "has-any"
                                    - "has-none"
                                    - "has-all"
            vendor:
                description: Vendor information.
                required: false
                type: list
                elements: dict
                suboptions:
                    name:
                        description: Vendor name.
                        required: true
                        type: str
                    product:
                        description: List of vendor products.
                        required: false
                        type: list
                        elements: str
            exclude_vendor:
                description: Exclude vendor flag.
                required: false
                type: bool
                default: false
    disk_encryption:
        description: Disk encryption criteria.
        required: false
        type: dict
        suboptions:
            criteria:
                description: Disk encryption criteria specifications.
                required: true
                type: dict
                suboptions:
                    is_installed:
                        description: Installation status.
                        required: false
                        type: bool
                        default: true
                    is_enabled:
                        description: Enabled status.
                        required: false
                        type: str
                        choices:
                            - "no"
                            - "yes"
                            - "not-available"
                    encrypted_locations:
                        description: Encrypted locations.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            name:
                                description: Location name.
                                required: true
                                type: str
                            encryption_state:
                                description: Encryption state specification.
                                required: true
                                type: dict
            vendor:
                description: Vendor information.
                required: false
                type: list
                elements: dict
                suboptions:
                    name:
                        description: Vendor name.
                        required: true
                        type: str
                    product:
                        description: List of vendor products.
                        required: false
                        type: list
                        elements: str
            exclude_vendor:
                description: Exclude vendor flag.
                required: false
                type: bool
                default: false
    mobile_device:
        description: Mobile device criteria.
        required: false
        type: dict
        suboptions:
            criteria:
                description: Mobile device criteria specifications.
                required: true
                type: dict
                suboptions:
                    jailbroken:
                        description: Jailbroken status.
                        required: false
                        type: bool
                    disk_encrypted:
                        description: Disk encryption status.
                        required: false
                        type: bool
                    passcode_set:
                        description: Passcode status.
                        required: false
                        type: bool
                    last_checkin_time:
                        description: Last check-in time.
                        required: false
                        type: dict
                    applications:
                        description: Applications criteria.
                        required: false
                        type: dict
                        suboptions:
                            has_malware:
                                description: Malware presence flag.
                                required: false
                                type: bool
                            has_unmanaged_app:
                                description: Unmanaged apps presence flag.
                                required: false
                                type: bool
                            includes:
                                description: Included applications.
                                required: false
                                type: list
                                elements: dict
                                suboptions:
                                    name:
                                        description: Application name.
                                        required: true
                                        type: str
                                    package:
                                        description: Package name.
                                        required: false
                                        type: str
                                    hash:
                                        description: Application hash.
                                        required: false
                                        type: str
    certificate:
        description: Certificate criteria.
        required: false
        type: dict
        suboptions:
            criteria:
                description: Certificate criteria specifications.
                required: true
                type: dict
                suboptions:
                    certificate_profile:
                        description: Certificate profile name.
                        required: false
                        type: str
                    certificate_attributes:
                        description: Certificate attributes.
                        required: false
                        type: list
                        elements: dict
                        suboptions:
                            name:
                                description: Attribute name.
                                required: true
                                type: str
                            value:
                                description: Attribute value.
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
                choices:
                    - "DEBUG"
                    - "INFO"
                    - "WARNING"
                    - "ERROR"
                    - "CRITICAL"
    state:
        description: Desired state of the HIP object.
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
- name: Manage HIP Objects in Strata Cloud Manager
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

    - name: Create a basic HIP object with host information
      cdot65.scm.hip_object:
        provider: "{{ provider }}"
        name: "Windows_Workstation"
        description: "HIP object for Windows workstations"
        folder: "Texas"
        host_info:
          criteria:
            os:
              contains:
                Microsoft: "All"
            managed: true
        state: "present"

    - name: Create HIP object with patch management criteria
      cdot65.scm.hip_object:
        provider: "{{ provider }}"
        name: "Patched_Endpoints"
        description: "HIP object for patch management"
        folder: "Texas"
        patch_management:
          criteria:
            is_installed: true
            is_enabled: "yes"
            missing_patches:
              severity: 3
              check: "has-none"
          vendor:
            - name: "Microsoft"
              product: ["Windows Update"]
        state: "present"

    - name: Create HIP object with disk encryption requirements
      cdot65.scm.hip_object:
        provider: "{{ provider }}"
        name: "Encrypted_Drives"
        description: "HIP object for disk encryption"
        folder: "Texas"
        disk_encryption:
          criteria:
            is_installed: true
            encrypted_locations:
              - name: "C:"
                encryption_state:
                  is: "encrypted"
        state: "present"

    - name: Update an existing HIP object
      cdot65.scm.hip_object:
        provider: "{{ provider }}"
        name: "Windows_Workstation"
        description: "Updated Windows workstation requirements"
        folder: "Texas"
        host_info:
          criteria:
            os:
              contains:
                Microsoft: "All"
            managed: true
            domain:
              contains: "company.local"
        state: "present"

    - name: Delete a HIP object
      cdot65.scm.hip_object:
        provider: "{{ provider }}"
        name: "Encrypted_Drives"
        folder: "Texas"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
hip_object:
    description: Details about the HIP object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Windows_Workstation"
        description: "HIP object for Windows workstations"
        host_info:
          criteria:
            os:
              contains:
                Microsoft: "All"
            managed: true
        folder: "Texas"
"""


def build_hip_object_data(module_params):
    """
    Build HIP object data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant HIP object parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(hip_object_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        hip_object_data (dict): HIP object parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [hip_object_data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def is_criteria_type_specified(hip_object_data):
    """
    Check if at least one criteria type is specified.

    Args:
        hip_object_data (dict): HIP object parameters

    Returns:
        bool: True if at least one criteria type is specified, False otherwise
    """
    criteria_types = [
        hip_object_data.get(criteria_type)
        for criteria_type in [
            "host_info",
            "network_info",
            "patch_management",
            "disk_encryption",
            "mobile_device",
            "certificate",
        ]
    ]
    return any(criteria_type is not None for criteria_type in criteria_types)


def needs_update(existing, params):
    """
    Determine if the HIP object needs to be updated.

    Args:
        existing: Existing HIP object from the SCM API
        params (dict): HIP object parameters with desired state from Ansible module

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

    # Check description parameter
    current_description = getattr(existing, "description", None)
    update_data["description"] = current_description

    if "description" in params and params["description"] is not None:
        if current_description != params["description"]:
            update_data["description"] = params["description"]
            changed = True

    # Process criteria type fields
    for criteria_type in [
        "host_info",
        "network_info",
        "patch_management",
        "disk_encryption",
        "mobile_device",
        "certificate",
    ]:
        current_value = getattr(existing, criteria_type, None)

        # If the existing object has this criteria type
        if current_value is not None:
            update_data[criteria_type] = current_value

        # If user provided this criteria type in params
        if criteria_type in params and params[criteria_type] is not None:
            # Simple comparison - in real world this would need a deeper comparison
            # of nested structures, but for this implementation we'll assume if the
            # field is provided, it needs updating
            if current_value != params[criteria_type]:
                update_data[criteria_type] = params[criteria_type]
                changed = True

    return changed, update_data


def get_existing_hip_object(client, hip_object_data):
    """
    Attempt to fetch an existing HIP object.

    Args:
        client: SCM client instance
        hip_object_data (dict): HIP object parameters to search for

    Returns:
        tuple: (bool, object) indicating if HIP object exists and the HIP object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if container in hip_object_data and hip_object_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in hip_object_data:
            return False, None

        # Fetch the HIP object using the appropriate container
        existing = client.hip_object.fetch(
            name=hip_object_data["name"], **{container_type: hip_object_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the HIP object module.

    This module provides functionality to create, update, and delete HIP objects
    in the SCM (Strata Cloud Manager) system. It supports various criteria types
    and container specifications.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=HIPObjectSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet", "device"],
        ],
        required_one_of=[["folder", "snippet", "device"]],
    )

    result = {"changed": False, "hip_object": None}

    try:
        client = get_scm_client(module)
        hip_object_data = build_hip_object_data(module.params)

        # Validate container is specified
        if not is_container_specified(hip_object_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing HIP object
        exists, existing_hip_object = get_existing_hip_object(client, hip_object_data)

        if module.params["state"] == "present":
            # Validate at least one criteria type is specified for creation
            if not exists and not is_criteria_type_specified(hip_object_data):
                module.fail_json(
                    msg="At least one of 'host_info', 'network_info', 'patch_management', 'disk_encryption', 'mobile_device', or 'certificate' must be provided when creating a HIP object."
                )

            if not exists:
                # Create new HIP object
                if not module.check_mode:
                    try:
                        new_hip_object = client.hip_object.create(data=hip_object_data)
                        result["hip_object"] = serialize_response(new_hip_object)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"A HIP object with name '{hip_object_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid HIP object data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_hip_object, hip_object_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = HIPObjectUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_hip_object = client.hip_object.update(update_model)
                        result["hip_object"] = serialize_response(updated_hip_object)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["hip_object"] = serialize_response(existing_hip_object)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.hip_object.delete(str(existing_hip_object.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
