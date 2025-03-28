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
Ansible module for managing bandwidth allocation objects in SCM.

This module provides functionality to create, update, and delete bandwidth allocation
objects in the SCM (Strata Cloud Manager) system. It handles bandwidth allocation
configuration and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.bandwidth_allocations import (
    BandwidthAllocationsSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError

DOCUMENTATION = r"""
---
module: bandwidth_allocations

short_description: Manage bandwidth allocation objects in SCM.

version_added: "0.1.0"

description:
    - Manage bandwidth allocation objects within Strata Cloud Manager (SCM).
    - Create, update, and delete bandwidth allocation objects.
    - Configure allocated bandwidth and QoS settings for Service Provider Networks (SPNs).

options:
    name:
        description: Name of the aggregated bandwidth region (max 63 chars).
        required: true
        type: str
    allocated_bandwidth:
        description: Bandwidth to allocate in Mbps (must be greater than 0).
        required: false
        type: float
    spn_name_list:
        description: List of SPN names for this region.
        required: false
        type: list
        elements: str
    qos:
        description: QoS configuration for bandwidth allocation.
        required: false
        type: dict
        suboptions:
            enabled:
                description: Enable QoS for bandwidth allocation.
                required: false
                type: bool
            customized:
                description: Use customized QoS settings.
                required: false
                type: bool
            profile:
                description: QoS profile name.
                required: false
                type: str
            guaranteed_ratio:
                description: Guaranteed ratio for bandwidth.
                required: false
                type: float
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
        description: Desired state of the bandwidth allocation object.
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
- name: Manage Bandwidth Allocations in Strata Cloud Manager
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

    - name: Create a basic bandwidth allocation
      cdot65.scm.bandwidth_allocations:
        provider: "{{ provider }}"
        name: "East_Region"
        allocated_bandwidth: 500.0
        spn_name_list:
          - "SPN1"
          - "SPN2"
        state: "present"

    - name: Create a bandwidth allocation with QoS enabled
      cdot65.scm.bandwidth_allocations:
        provider: "{{ provider }}"
        name: "West_Region"
        allocated_bandwidth: 750.0
        spn_name_list:
          - "SPN3"
          - "SPN4"
        qos:
          enabled: true
          customized: false
        state: "present"

    - name: Create a bandwidth allocation with customized QoS
      cdot65.scm.bandwidth_allocations:
        provider: "{{ provider }}"
        name: "Central_Region"
        allocated_bandwidth: 1000.0
        spn_name_list:
          - "SPN5"
          - "SPN6"
        qos:
          enabled: true
          customized: true
          profile: "High_Priority"
          guaranteed_ratio: 0.75
        state: "present"

    - name: Update a bandwidth allocation with increased bandwidth
      cdot65.scm.bandwidth_allocations:
        provider: "{{ provider }}"
        name: "East_Region"
        allocated_bandwidth: 800.0
        spn_name_list:
          - "SPN1"
          - "SPN2"
        state: "present"

    - name: Delete a bandwidth allocation
      cdot65.scm.bandwidth_allocations:
        provider: "{{ provider }}"
        name: "Central_Region"
        spn_name_list:
          - "SPN5"
          - "SPN6"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
bandwidth_allocation:
    description: Details about the bandwidth allocation object.
    returned: when state is present
    type: dict
    sample:
        name: "East_Region"
        allocated_bandwidth: 500.0
        spn_name_list: ["SPN1", "SPN2"]
        qos:
            enabled: false
            customized: false
            profile: null
            guaranteed_ratio: null
"""


def build_bandwidth_allocation_data(module_params):
    """
    Build bandwidth allocation data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant bandwidth allocation parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def needs_update(existing, params):
    """
    Determine if the bandwidth allocation object needs to be updated.

    Args:
        existing: Existing bandwidth allocation object from the SCM API
        params (dict): Bandwidth allocation parameters with desired state from Ansible module

    Returns:
        (bool, dict): Tuple containing:
            - bool: Whether an update is needed
            - dict: Complete object data for update including all fields from the existing
                   object with any modifications from the params
    """
    changed = False

    # Start with a fresh update model using all fields from existing object
    update_data = {
        "name": existing.name,
    }

    # Check and update allocated_bandwidth
    if "allocated_bandwidth" in params and params["allocated_bandwidth"] is not None:
        if existing.allocated_bandwidth != params["allocated_bandwidth"]:
            update_data["allocated_bandwidth"] = params["allocated_bandwidth"]
            changed = True
        else:
            update_data["allocated_bandwidth"] = existing.allocated_bandwidth
    else:
        update_data["allocated_bandwidth"] = existing.allocated_bandwidth

    # Check and update spn_name_list
    if "spn_name_list" in params and params["spn_name_list"] is not None:
        if existing.spn_name_list != params["spn_name_list"]:
            update_data["spn_name_list"] = params["spn_name_list"]
            changed = True
        else:
            update_data["spn_name_list"] = existing.spn_name_list
    elif getattr(existing, "spn_name_list", None) is not None:
        update_data["spn_name_list"] = existing.spn_name_list

    # Check and update QoS settings
    existing_qos = getattr(existing, "qos", None)
    params_qos = params.get("qos")

    # If neither exists, no QoS data to include
    if existing_qos is None and params_qos is None:
        pass
    # If only params QoS exists, use that
    elif existing_qos is None and params_qos is not None:
        update_data["qos"] = params_qos
        changed = True
    # If only existing QoS exists, include it
    elif existing_qos is not None and params_qos is None:
        update_data["qos"] = {
            "enabled": getattr(existing_qos, "enabled", None),
            "customized": getattr(existing_qos, "customized", None),
            "profile": getattr(existing_qos, "profile", None),
            "guaranteed_ratio": getattr(existing_qos, "guaranteed_ratio", None),
        }
    # If both exist, compare and update
    else:
        update_qos = {}
        qos_changed = False

        # Compare and set QoS enabled status
        if "enabled" in params_qos and params_qos["enabled"] is not None:
            if getattr(existing_qos, "enabled", None) != params_qos["enabled"]:
                update_qos["enabled"] = params_qos["enabled"]
                qos_changed = True
            else:
                update_qos["enabled"] = getattr(existing_qos, "enabled", None)
        elif getattr(existing_qos, "enabled", None) is not None:
            update_qos["enabled"] = getattr(existing_qos, "enabled", None)

        # Compare and set QoS customized flag
        if "customized" in params_qos and params_qos["customized"] is not None:
            if getattr(existing_qos, "customized", None) != params_qos["customized"]:
                update_qos["customized"] = params_qos["customized"]
                qos_changed = True
            else:
                update_qos["customized"] = getattr(existing_qos, "customized", None)
        elif getattr(existing_qos, "customized", None) is not None:
            update_qos["customized"] = getattr(existing_qos, "customized", None)

        # Compare and set QoS profile
        if "profile" in params_qos and params_qos["profile"] is not None:
            if getattr(existing_qos, "profile", None) != params_qos["profile"]:
                update_qos["profile"] = params_qos["profile"]
                qos_changed = True
            else:
                update_qos["profile"] = getattr(existing_qos, "profile", None)
        elif getattr(existing_qos, "profile", None) is not None:
            update_qos["profile"] = getattr(existing_qos, "profile", None)

        # Compare and set QoS guaranteed ratio
        if "guaranteed_ratio" in params_qos and params_qos["guaranteed_ratio"] is not None:
            if getattr(existing_qos, "guaranteed_ratio", None) != params_qos["guaranteed_ratio"]:
                update_qos["guaranteed_ratio"] = params_qos["guaranteed_ratio"]
                qos_changed = True
            else:
                update_qos["guaranteed_ratio"] = getattr(existing_qos, "guaranteed_ratio", None)
        elif getattr(existing_qos, "guaranteed_ratio", None) is not None:
            update_qos["guaranteed_ratio"] = getattr(existing_qos, "guaranteed_ratio", None)

        # Only update QoS if there are changes
        if qos_changed:
            update_data["qos"] = update_qos
            changed = True
        elif update_qos:  # Include original QoS data if no changes
            update_data["qos"] = update_qos

    return changed, update_data


def get_existing_bandwidth_allocation(client, params):
    """
    Attempt to fetch an existing bandwidth allocation object.

    Args:
        client: SCM client instance
        params (dict): Bandwidth allocation parameters to search for

    Returns:
        tuple: (bool, object) indicating if bandwidth allocation exists and the object if found
    """
    try:
        if "name" not in params:
            return False, None

        existing = client.bandwidth_allocation.get(name=params["name"])
        return existing is not None, existing
    except Exception:
        # Handle any error as "object not found" during the get operation
        return False, None


def main():
    """
    Main execution path for the bandwidth allocations module.

    This module provides functionality to create, update, and delete bandwidth allocation
    objects in the SCM (Strata Cloud Manager) system. It supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=BandwidthAllocationsSpec.spec(),
        supports_check_mode=True,
        required_if=[
            ["state", "present", ["allocated_bandwidth"], True],
            ["state", "absent", ["spn_name_list"], True],
        ],
    )

    result = {"changed": False, "bandwidth_allocation": None}

    try:
        client = get_scm_client(module)
        bandwidth_allocation_data = build_bandwidth_allocation_data(module.params)

        # Get existing bandwidth allocation
        exists, existing_allocation = get_existing_bandwidth_allocation(
            client, bandwidth_allocation_data
        )

        if module.params["state"] == "present":
            if not exists:
                # Create new bandwidth allocation
                if not module.check_mode:
                    try:
                        new_allocation = client.bandwidth_allocation.create(
                            data=bandwidth_allocation_data
                        )
                        result["bandwidth_allocation"] = serialize_response(new_allocation)
                        result["changed"] = True
                    except Exception as e:
                        # Add detailed error information
                        error_details = {
                            "error_message": str(e),
                            "error_type": type(e).__name__,
                            "request_data": bandwidth_allocation_data,
                        }
                        module.fail_json(
                            msg=f"Failed to create bandwidth allocation: {str(e)}",
                            error_details=error_details,
                        )
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(
                    existing_allocation, bandwidth_allocation_data
                )

                if need_update:
                    if not module.check_mode:
                        # Perform update with complete object data
                        updated_allocation = client.bandwidth_allocation.update(data=update_data)
                        result["bandwidth_allocation"] = serialize_response(updated_allocation)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["bandwidth_allocation"] = serialize_response(existing_allocation)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    # For delete, we need name and spn_name_list
                    name = bandwidth_allocation_data["name"]
                    spn_name_list = bandwidth_allocation_data["spn_name_list"]

                    # Convert list to comma-separated string as required by the API
                    spn_name_string = ",".join(spn_name_list)

                    try:
                        client.bandwidth_allocation.delete(name=name, spn_name_list=spn_name_string)
                    except Exception as e:
                        # If we get an error that suggests the object doesn't exist, we can ignore it
                        if "Object Not Present" in str(e) or "not found" in str(e).lower():
                            module.warn(
                                f"Bandwidth allocation '{name}' may already be deleted or doesn't exist"
                            )
                        else:
                            # For other errors, we should raise them
                            raise e
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
