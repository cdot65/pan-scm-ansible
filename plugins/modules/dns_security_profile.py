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
Ansible module for managing DNS security profile objects in SCM.

This module provides functionality to create, update, and delete DNS security profile objects
in the SCM (Strata Cloud Manager) system. It handles security settings, botnet domains
configurations, and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.dns_security_profile import (
    DNSSecurityProfileSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.security import DNSSecurityProfileUpdateModel

DOCUMENTATION = r"""
---
module: dns_security_profile

short_description: Manage DNS security profile objects in SCM.

version_added: "0.1.0"

description:
    - Manage DNS security profile objects within Strata Cloud Manager (SCM).
    - Create, update, and delete DNS security profile objects.
    - Configure botnet domains, DNS security categories, and sinkhole settings.
    - Ensures that exactly one container type (folder, snippet, device) is provided.

options:
    name:
        description: The name of the DNS security profile (max 63 chars).
        required: true
        type: str
    description:
        description: Description of the DNS security profile.
        required: false
        type: str
    botnet_domains:
        description: Botnet domains configuration.
        required: false
        type: dict
        suboptions:
            dns_security_categories:
                description: List of DNS security categories configuration.
                required: false
                type: list
                elements: dict
                suboptions:
                    name:
                        description: DNS security category name.
                        required: true
                        type: str
                    action:
                        description: Action to take for the category.
                        required: true
                        type: str
                        choices: ["default", "allow", "block", "sinkhole"]
                    log_level:
                        description: Log level for the category.
                        required: false
                        type: str
                        choices: ["default", "none", "low", "informational", "medium", "high", "critical"]
                    packet_capture:
                        description: Packet capture option.
                        required: false
                        type: str
                        choices: ["disable", "single-packet", "extended-capture"]
            sinkhole:
                description: Sinkhole configuration for DNS security.
                required: false
                type: dict
                suboptions:
                    ipv4_address:
                        description: IPv4 address for the sinkhole.
                        required: true
                        type: str
                        choices: ["pan-sinkhole-default-ip", "127.0.0.1"]
                    ipv6_address:
                        description: IPv6 address for the sinkhole.
                        required: true
                        type: str
                        choices: ["::1"]
            whitelist:
                description: List of whitelisted domains.
                required: false
                type: list
                elements: dict
                suboptions:
                    name:
                        description: Name of the whitelisted domain.
                        required: true
                        type: str
                    description:
                        description: Description of the whitelisted domain.
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
        description: Desired state of the DNS security profile object.
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
- name: Manage DNS Security Profiles in Strata Cloud Manager
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

    - name: Create a basic DNS security profile
      cdot65.scm.dns_security_profile:
        provider: "{{ provider }}"
        name: "test-dns-security"
        description: "Test DNS security profile"
        folder: "Texas"
        state: "present"

    - name: Create a DNS security profile with botnet domain settings
      cdot65.scm.dns_security_profile:
        provider: "{{ provider }}"
        name: "botnet-protection"
        description: "DNS profile with botnet protection"
        botnet_domains:
          dns_security_categories:
            - name: "command-and-control"
              action: "block"
              log_level: "high"
              packet_capture: "single-packet"
            - name: "malware"
              action: "sinkhole"
              log_level: "critical"
            - name: "phishing"
              action: "block"
          sinkhole:
            ipv4_address: "pan-sinkhole-default-ip"
            ipv6_address: "::1"
          whitelist:
            - name: "trusted-domain.com"
              description: "Trusted internal domain"
        folder: "Texas"
        state: "present"

    - name: Update an existing DNS security profile
      cdot65.scm.dns_security_profile:
        provider: "{{ provider }}"
        name: "botnet-protection"
        description: "Updated DNS security profile"
        botnet_domains:
          dns_security_categories:
            - name: "command-and-control"
              action: "sinkhole"
              log_level: "critical"
            - name: "malware"
              action: "block"
            - name: "spyware"
              action: "block"
              log_level: "high"
          sinkhole:
            ipv4_address: "127.0.0.1"
            ipv6_address: "::1"
        folder: "Texas"
        state: "present"

    - name: Delete a DNS security profile
      cdot65.scm.dns_security_profile:
        provider: "{{ provider }}"
        name: "botnet-protection"
        folder: "Texas"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
dns_security_profile:
    description: Details about the DNS security profile.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "botnet-protection"
        description: "DNS profile with botnet protection"
        botnet_domains:
          dns_security_categories:
            - name: "command-and-control"
              action: "block"
              log_level: "high"
              packet_capture: "single-packet"
            - name: "malware"
              action: "sinkhole"
              log_level: "critical"
          sinkhole:
            ipv4_address: "pan-sinkhole-default-ip"
            ipv6_address: "::1"
          whitelist:
            - name: "trusted-domain.com"
              description: "Trusted internal domain"
        folder: "Texas"
"""


def build_dns_security_profile_data(module_params):
    """
    Build DNS security profile data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant DNS security profile parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(dns_security_profile_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        dns_security_profile_data (dict): DNS security profile parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [
        dns_security_profile_data.get(container) for container in ["folder", "snippet", "device"]
    ]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the DNS security profile object needs to be updated.

    Args:
        existing: Existing DNS security profile object from the SCM API
        params (dict): DNS security profile parameters with desired state from Ansible module

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

    # Check description update
    if "description" in params and params["description"] is not None:
        current_description = getattr(existing, "description", None)
        if current_description != params["description"]:
            update_data["description"] = params["description"]
            changed = True
        else:
            update_data["description"] = current_description
    else:
        # Keep existing description if available
        current_description = getattr(existing, "description", None)
        if current_description is not None:
            update_data["description"] = current_description

    # Check botnet_domains update
    if "botnet_domains" in params and params["botnet_domains"] is not None:
        existing_botnet = getattr(existing, "botnet_domains", None)

        # Only set update flag if existing and requested configs are different
        if existing_botnet != params["botnet_domains"]:
            update_data["botnet_domains"] = params["botnet_domains"]
            changed = True
        else:
            # Keep existing botnet_domains
            update_data["botnet_domains"] = existing_botnet
    else:
        # Keep existing botnet_domains if available
        existing_botnet = getattr(existing, "botnet_domains", None)
        if existing_botnet is not None:
            update_data["botnet_domains"] = existing_botnet

    return changed, update_data


def get_existing_dns_security_profile(client, dns_security_profile_data):
    """
    Attempt to fetch an existing DNS security profile object.

    Args:
        client: SCM client instance
        dns_security_profile_data (dict): DNS security profile parameters to search for

    Returns:
        tuple: (bool, object) indicating if DNS security profile exists and the DNS security profile object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if (
                container in dns_security_profile_data
                and dns_security_profile_data[container] is not None
            ):
                container_type = container
                break

        if container_type is None or "name" not in dns_security_profile_data:
            return False, None

        # Fetch the DNS security profile using the appropriate container
        existing = client.dns_security_profile.fetch(
            name=dns_security_profile_data["name"],
            **{container_type: dns_security_profile_data[container_type]},
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the DNS security profile object module.

    This module provides functionality to create, update, and delete DNS security profile objects
    in the SCM (Strata Cloud Manager) system. It handles botnet domains and DNS security categories,
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=DNSSecurityProfileSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet", "device"],
        ],
        required_one_of=[["folder", "snippet", "device"]],
    )

    result = {"changed": False, "dns_security_profile": None}

    try:
        client = get_scm_client(module)
        dns_security_profile_data = build_dns_security_profile_data(module.params)

        # Validate container is specified
        if not is_container_specified(dns_security_profile_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing DNS security profile
        exists, existing_dns_security_profile = get_existing_dns_security_profile(
            client, dns_security_profile_data
        )

        if module.params["state"] == "present":
            if not exists:
                # Create new DNS security profile
                if not module.check_mode:
                    try:
                        new_dns_security_profile = client.dns_security_profile.create(
                            data=dns_security_profile_data
                        )
                        result["dns_security_profile"] = serialize_response(
                            new_dns_security_profile
                        )
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"A DNS security profile with name '{dns_security_profile_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid DNS security profile data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(
                    existing_dns_security_profile, dns_security_profile_data
                )

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = DNSSecurityProfileUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_dns_security_profile = client.dns_security_profile.update(
                            update_model
                        )
                        result["dns_security_profile"] = serialize_response(
                            updated_dns_security_profile
                        )
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["dns_security_profile"] = serialize_response(
                        existing_dns_security_profile
                    )

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    try:
                        profile_id = str(existing_dns_security_profile.id)
                        client.dns_security_profile.delete(profile_id)
                        result["changed"] = True
                        result["msg"] = f"Deleted DNS security profile with ID: {profile_id}"
                    except Exception as e:
                        module.fail_json(msg=f"Failed to delete DNS security profile: {str(e)}")
                else:
                    result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
