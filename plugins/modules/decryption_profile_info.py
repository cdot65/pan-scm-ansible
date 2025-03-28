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
Ansible module for gathering information about decryption profile objects in SCM.

This module provides functionality to retrieve information about decryption profile objects
in the SCM (Strata Cloud Manager) system with various filtering options.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils._text import to_text
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.decryption_profile_info import (  # noqa: F401
    DecryptionProfileInfoSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import (  # noqa: F401
    get_scm_client,
)
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (  # noqa: F401
    serialize_response,
)

from scm.config.security.decryption_profile import DecryptionProfile
from scm.exceptions import NotFoundError

DOCUMENTATION = r"""
---
module: decryption_profile_info

short_description: Gather information about decryption profile objects in SCM.

version_added: "0.1.0"

description:
    - Gather information about decryption profile objects within Strata Cloud Manager (SCM).
    - Supports retrieving a specific decryption profile by name or listing decryption profiles with various filters.
    - Provides additional client-side filtering capabilities for exact matches and exclusions.
    - Returns detailed information about each decryption profile object.
    - This is an info module that only retrieves information and does not modify anything.

options:
    name:
        description: The name of a specific decryption profile to retrieve.
        required: false
        type: str
    gather_subset:
        description:
            - Determines which information to gather about decryption profiles.
            - C(all) gathers everything.
            - C(config) is the default which retrieves basic configuration.
        type: list
        elements: str
        default: ['config']
        choices: ['all', 'config']
    folder:
        description: Filter decryption profiles by folder container.
        required: false
        type: str
    snippet:
        description: Filter decryption profiles by snippet container.
        required: false
        type: str
    device:
        description: Filter decryption profiles by device container.
        required: false
        type: str
    exact_match:
        description: When True, only return objects defined exactly in the specified container.
        required: false
        type: bool
        default: false
    exclude_folders:
        description: List of folder names to exclude from results.
        required: false
        type: list
        elements: str
    exclude_snippets:
        description: List of snippet values to exclude from results.
        required: false
        type: list
        elements: str
    exclude_devices:
        description: List of device values to exclude from results.
        required: false
        type: list
        elements: str
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

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
---
- name: Gather Decryption Profile Information in Strata Cloud Manager
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

    - name: Get information about a specific decryption profile
      cdot65.scm.decryption_profile_info:
        provider: "{{ provider }}"
        name: "Custom-Decryption-Profile"
        folder: "Production"
      register: profile_info

    - name: List all decryption profiles in a folder
      cdot65.scm.decryption_profile_info:
        provider: "{{ provider }}"
        folder: "Production"
      register: all_profiles

    - name: List profiles with exact match and exclusions
      cdot65.scm.decryption_profile_info:
        provider: "{{ provider }}"
        folder: "Production"
        exact_match: true
        exclude_folders: ["Shared"]
      register: filtered_profiles
"""

RETURN = r"""
profiles:
    description: List of decryption profile objects matching the filter criteria (returned when name is not specified).
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Custom-Decryption-Profile"
        description: "Custom decryption profile for forward proxy"
        ssl_forward_proxy:
          enabled: true
          block_expired_cert: true
          block_untrusted_issuer: true
        folder: "Production"
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "Inbound-Inspection-Profile"
        description: "Decryption profile for inbound inspection"
        ssl_inbound_inspection:
          enabled: true
        folder: "Production"
profile:
    description: Information about the requested decryption profile (returned when name is specified).
    returned: success, when name is specified
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


def build_filter_params(module_params):
    """
    Build filter parameters dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant filter parameters
    """
    # Container params
    container_params = {}
    for container in ["folder", "snippet", "device"]:
        if module_params.get(container) is not None:
            container_params[container] = module_params[container]

    # Filter params
    filter_params = {}
    for filter_param in ["exact_match", "exclude_folders", "exclude_snippets", "exclude_devices"]:
        if module_params.get(filter_param) is not None:
            filter_params[filter_param] = module_params[filter_param]

    return container_params, filter_params


def main():
    """
    Main execution path for the decryption_profile_info module.

    This module provides functionality to gather information about decryption profile objects
    in the SCM (Strata Cloud Manager) system with various filtering options.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=DecryptionProfileInfoSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        # Only require a container if we're not provided with a specific name
        required_if=[["name", None, ["folder", "snippet", "device"], True]],
    )

    result = {}

    try:
        client = get_scm_client(module)
        profile_api = DecryptionProfile(client)

        # Check if we're fetching a specific profile by name
        if module.params.get("name"):
            name = module.params["name"]
            container_params = {}

            # Get the container param
            for container in ["folder", "snippet", "device"]:
                if module.params.get(container):
                    container_params[container] = module.params[container]

            try:
                # Fetch a specific profile
                profile = profile_api.fetch(name=name, **container_params)

                # Serialize response for Ansible output
                result["profile"] = serialize_response(profile)

            except NotFoundError:
                module.fail_json(
                    msg=f"Decryption profile with name '{name}' not found in {list(container_params.keys())[0]} '{list(container_params.values())[0]}'"
                )
            except Exception as e:
                module.fail_json(msg=str(e))

        else:
            # List profiles with filtering
            container_params, filter_params = build_filter_params(module.params)

            try:
                profiles = profile_api.list(**container_params, **filter_params)

                # Serialize response for Ansible output
                result["profiles"] = [serialize_response(profile) for profile in profiles]

            except Exception as e:
                module.fail_json(msg=f"Failed to list profiles: {str(e)}")

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
