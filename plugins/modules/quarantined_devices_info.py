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
Ansible module for gathering information about quarantined devices in SCM.

This module provides functionality to retrieve information about quarantined devices
in the SCM (Strata Cloud Manager) system with various filtering options.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.quarantined_devices import (
    QuarantinedDevicesInfoSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, MissingQueryParameterError

DOCUMENTATION = r"""
---
module: quarantined_devices_info

short_description: Gather information about quarantined devices in SCM.

version_added: "0.1.0"

description:
    - Gather information about quarantined devices within Strata Cloud Manager (SCM).
    - List quarantined devices with optional filtering.
    - The SCM API only supports listing and filtering (no direct fetch by ID).
    - This is an info module that only retrieves information and does not modify anything.

options:
    host_id:
        description: Filter quarantined devices by host ID.
        required: false
        type: str
    serial_number:
        description: Filter quarantined devices by serial number.
        required: false
        type: str
    gather_subset:
        description:
            - Determines which information to gather about quarantined devices.
            - C(all) gathers everything.
            - C(config) is the default which retrieves basic configuration.
        type: list
        elements: str
        default: ['config']
        choices: ['all', 'config']
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

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
---
- name: Gather Quarantined Devices Information in Strata Cloud Manager
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

    - name: List all quarantined devices
      cdot65.scm.quarantined_devices_info:
        provider: "{{ provider }}"
      register: all_devices

    - name: List quarantined devices by host ID
      cdot65.scm.quarantined_devices_info:
        provider: "{{ provider }}"
        host_id: "device-12345"
      register: filtered_by_host_id

    - name: List quarantined devices by serial number
      cdot65.scm.quarantined_devices_info:
        provider: "{{ provider }}"
        serial_number: "PA-987654321"
      register: filtered_by_serial
"""

RETURN = r"""
quarantined_devices:
    description: List of quarantined devices matching the filter criteria.
    returned: success
    type: list
    elements: dict
    sample:
      - host_id: "device-12345"
        serial_number: "PA-987654321"
      - host_id: "device-67890"
        serial_number: "PA-567890123"
"""


def build_filter_params(module_params):
    """
    Build filter parameters dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant filter parameters
    """
    filter_params = {}

    # Add filter parameters if provided
    for param in ["host_id", "serial_number"]:
        if module_params.get(param) is not None:
            filter_params[param] = module_params[param]

    return filter_params


def main():
    """
    Main execution path for the quarantined_devices_info module.

    This module provides functionality to gather information about quarantined devices
    in the SCM (Strata Cloud Manager) system with various filtering options.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=QuarantinedDevicesInfoSpec.spec(),
        supports_check_mode=True,
    )

    result = {"quarantined_devices": []}

    try:
        client = get_scm_client(module)

        # Build filter parameters from module parameters
        filter_params = build_filter_params(module.params)

        try:
            # List quarantined devices with filtering
            quarantined_devices = client.quarantined_device.list(**filter_params)

            # Serialize response for Ansible output
            result["quarantined_devices"] = [
                serialize_response(device) for device in quarantined_devices
            ]

        except MissingQueryParameterError as e:
            module.fail_json(msg=f"Missing required parameter: {str(e)}")
        except InvalidObjectError as e:
            module.fail_json(msg=f"Invalid filter parameters: {str(e)}")

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
