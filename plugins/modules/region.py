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
Ansible module for managing region objects in SCM.

This module provides functionality to create, update, and delete region objects
in the SCM (Strata Cloud Manager) system. It handles geo_location configuration
and associated addresses, and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.region import RegionSpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.objects import RegionUpdateModel

DOCUMENTATION = r"""
---
module: region

short_description: Manage region objects in SCM.

version_added: "0.1.0"

description:
    - Manage region objects within Strata Cloud Manager (SCM).
    - Create, update, and delete region objects defining geographic locations and associated networks.
    - Ensures that exactly one container type (folder, snippet, device) is provided.
    - "Note: Unlike other SCM objects, regions do not support 'description' or 'tag' fields.
      If these fields are provided in the module parameters, they will be ignored by the SCM API."

options:
    name:
        description: The name of the region (max 31 chars).
        required: true
        type: str
    geo_location:
        description: Geographic location of the region with latitude (-90 to 90) and longitude (-180 to 180).
        required: false
        type: dict
        suboptions:
            latitude:
                description: The latitudinal position (must be between -90 and 90 degrees).
                required: true
                type: float
            longitude:
                description: The longitudinal position (must be between -180 and 180 degrees).
                required: true
                type: float
    address:
        description: List of IP addresses or networks associated with the region.
        required: false
        type: list
        elements: str
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
        description: Desired state of the region object.
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
- name: Manage Region Objects in Strata Cloud Manager
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

    - name: Create a region with geo_location and addresses
      cdot65.scm.region:
        provider: "{{ provider }}"
        name: "us-west-region"
        geo_location:
          latitude: 37.7749
          longitude: -122.4194
        address:
          - "10.0.0.0/8"
          - "192.168.1.0/24"
        folder: "Global"
        state: "present"

    - name: Create a region with addresses only
      cdot65.scm.region:
        provider: "{{ provider }}"
        name: "internal-networks"
        address:
          - "172.16.0.0/16"
          - "192.168.0.0/16"
        folder: "Global"
        state: "present"

    - name: Update a region with new geo_location
      cdot65.scm.region:
        provider: "{{ provider }}"
        name: "us-west-region"
        geo_location:
          latitude: 40.7128
          longitude: -74.0060
        address:
          - "10.0.0.0/8"
          - "192.168.1.0/24"
          - "172.16.0.0/16"
        folder: "Global"
        state: "present"

    - name: Delete a region
      cdot65.scm.region:
        provider: "{{ provider }}"
        name: "internal-networks"
        folder: "Global"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
region:
    description: Details about the region object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "us-west-region"
        geo_location:
          latitude: 37.7749
          longitude: -122.4194
        address: ["10.0.0.0/8", "192.168.1.0/24"]
        folder: "Global"
"""


def build_region_data(module_params):
    """
    Build region data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant region parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(region_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        region_data (dict): Region parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [region_data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the region object needs to be updated.

    Args:
        existing: Existing region object from the SCM API
        params (dict): Region parameters with desired state from Ansible module

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

    # Check geo_location parameter
    if "geo_location" in params and params["geo_location"] is not None:
        # Convert existing geo_location to dict for comparison if it exists
        existing_geo = None
        if existing.geo_location is not None:
            existing_geo = {
                "latitude": existing.geo_location.latitude,
                "longitude": existing.geo_location.longitude,
            }

        # Compare with the new geo_location
        if existing_geo != params["geo_location"]:
            update_data["geo_location"] = params["geo_location"]
            changed = True
    elif hasattr(existing, "geo_location") and existing.geo_location is not None:
        # Keep existing geo_location if it exists
        update_data["geo_location"] = {
            "latitude": existing.geo_location.latitude,
            "longitude": existing.geo_location.longitude,
        }

    # Check address parameter
    if "address" in params and params["address"] is not None:
        existing_addresses = getattr(existing, "address", None) or []
        if set(existing_addresses) != set(params["address"]):
            update_data["address"] = params["address"]
            changed = True
    elif hasattr(existing, "address") and existing.address is not None:
        update_data["address"] = existing.address

    return changed, update_data


def get_existing_region(client, region_data):
    """
    Attempt to fetch an existing region object.

    Args:
        client: SCM client instance
        region_data (dict): Region parameters to search for

    Returns:
        tuple: (bool, object) indicating if region exists and the region object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if container in region_data and region_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in region_data:
            return False, None

        # Fetch the region using the appropriate container
        existing = client.region.fetch(
            name=region_data["name"], **{container_type: region_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the region object module.

    This module provides functionality to create, update, and delete region objects
    in the SCM (Strata Cloud Manager) system. It handles geo_location configuration
    and associated addresses, and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=RegionSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        required_one_of=[["folder", "snippet", "device"]],
    )

    result = {"changed": False, "region": None}

    try:
        client = get_scm_client(module)
        region_data = build_region_data(module.params)

        # Validate container is specified
        if not is_container_specified(region_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing region
        exists, existing_region = get_existing_region(client, region_data)

        if module.params["state"] == "present":
            if not exists:
                # Create new region
                if not module.check_mode:
                    try:
                        new_region = client.region.create(data=region_data)
                        result["region"] = serialize_response(new_region)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"A region with name '{region_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid region data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_region, region_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = RegionUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_region = client.region.update(update_model)
                        result["region"] = serialize_response(updated_region)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["region"] = serialize_response(existing_region)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.region.delete(str(existing_region.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
