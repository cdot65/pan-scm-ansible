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
Ansible module for managing quarantined devices in SCM.

This module provides functionality to create and delete quarantined devices
in the SCM (Strata Cloud Manager) system. It supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.quarantined_devices import (
    QuarantinedDevicesSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, ObjectNotPresentError

DOCUMENTATION = r"""
---
module: quarantined_devices

short_description: Manage quarantined devices in SCM.

version_added: "0.1.0"

description:
    - Manage quarantined devices within Strata Cloud Manager (SCM).
    - Create and delete quarantined devices.
    - Note that this module only supports limited operations (create, list, delete) as defined by the SCM API.

options:
    host_id:
        description: The host ID of the device to quarantine.
        required: true
        type: str
    serial_number:
        description: The serial number of the device to quarantine.
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
        description: Desired state of the quarantined device.
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
- name: Manage Quarantined Devices in Strata Cloud Manager
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

    - name: Quarantine a device
      cdot65.scm.quarantined_devices:
        provider: "{{ provider }}"
        host_id: "device-12345"
        serial_number: "PA-987654321"
        state: "present"

    - name: Remove a device from quarantine
      cdot65.scm.quarantined_devices:
        provider: "{{ provider }}"
        host_id: "device-12345"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
quarantined_device:
    description: Details about the quarantined device.
    returned: when state is present
    type: dict
    sample:
        host_id: "device-12345"
        serial_number: "PA-987654321"
"""


def build_quarantined_device_data(module_params):
    """
    Build quarantined device data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant quarantined device parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def device_exists(client, host_id):
    """
    Check if a quarantined device with the given host_id exists.

    Args:
        client: SCM client instance
        host_id (str): Host ID to check

    Returns:
        tuple: (bool, object) indicating if device exists and the device object if found
    """
    try:
        # Use the list method with a filter to check if the device exists
        devices = client.quarantined_device.list(host_id=host_id)

        # If we found any devices matching this host_id
        if devices and len(devices) > 0:
            return True, devices[0]
        return False, None
    except Exception:
        return False, None


def main():
    """
    Main execution path for the quarantined devices module.

    This module provides functionality to create and delete quarantined devices
    in the SCM (Strata Cloud Manager) system.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=QuarantinedDevicesSpec.spec(),
        supports_check_mode=True,
    )

    result = {"changed": False, "quarantined_device": None}

    try:
        client = get_scm_client(module)
        quarantined_device_data = build_quarantined_device_data(module.params)
        host_id = module.params["host_id"]

        # Check if device is already quarantined
        exists, existing_device = device_exists(client, host_id)

        if module.params["state"] == "present":
            if not exists:
                # Create new quarantined device
                if not module.check_mode:
                    try:
                        new_device = client.quarantined_device.create(data=quarantined_device_data)
                        result["quarantined_device"] = serialize_response(new_device)
                        result["changed"] = True
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid quarantined device data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Device already exists, no changes needed
                # Note: The SCM API does not support updating quarantined devices
                result["quarantined_device"] = serialize_response(existing_device)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.quarantined_device.delete(host_id)
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
