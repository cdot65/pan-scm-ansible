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
Ansible module for managing syslog server profile objects in SCM.

This module provides functionality to create, update, and delete syslog server profile objects
in the SCM (Strata Cloud Manager) system. It handles server configurations and format settings,
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.syslog_server_profiles import (
    SyslogServerProfilesSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.objects import SyslogServerProfileUpdateModel

DOCUMENTATION = r"""
---
module: syslog_server_profiles

short_description: Manage syslog server profile objects in SCM.

version_added: "0.1.0"

description:
    - Manage syslog server profile objects within Strata Cloud Manager (SCM).
    - Create, update, and delete syslog server profile objects that define configurations for syslog servers.
    - Configure transport protocol, port, format, and facility for each syslog server.
    - Set up format settings for different log types.
    - Ensures that exactly one container type (folder, snippet, device) is provided.

options:
    name:
        description: The name of the syslog server profile (max 31 chars).
        required: true
        type: str
    servers:
        description: Dictionary of server configurations.
        required: true
        type: dict
        suboptions:
            name:
                description: Syslog server name.
                required: true
                type: str
            server:
                description: Syslog server address.
                required: true
                type: str
            transport:
                description: Transport protocol for the syslog server.
                required: true
                type: str
                choices: ["UDP", "TCP"]
            port:
                description: Syslog server port (1-65535).
                required: true
                type: int
            format:
                description: Syslog format.
                required: true
                type: str
                choices: ["BSD", "IETF"]
            facility:
                description: Syslog facility.
                required: true
                type: str
                choices: 
                  - "LOG_USER"
                  - "LOG_LOCAL0"
                  - "LOG_LOCAL1"
                  - "LOG_LOCAL2"
                  - "LOG_LOCAL3"
                  - "LOG_LOCAL4"
                  - "LOG_LOCAL5"
                  - "LOG_LOCAL6"
                  - "LOG_LOCAL7"
    format:
        description: Format settings for different log types.
        required: false
        type: dict
        suboptions:
            escaping:
                description: Character escaping configuration.
                required: false
                type: dict
                suboptions:
                    escape_character:
                        description: Escape sequence delimiter (max length 1).
                        required: false
                        type: str
                    escaped_characters:
                        description: Characters to be escaped without spaces (max length 255).
                        required: false
                        type: str
            traffic:
                description: Format for traffic logs.
                required: false
                type: str
            threat:
                description: Format for threat logs.
                required: false
                type: str
            wildfire:
                description: Format for wildfire logs.
                required: false
                type: str
            url:
                description: Format for URL logs.
                required: false
                type: str
            data:
                description: Format for data logs.
                required: false
                type: str
            gtp:
                description: Format for GTP logs.
                required: false
                type: str
            sctp:
                description: Format for SCTP logs.
                required: false
                type: str
            tunnel:
                description: Format for tunnel logs.
                required: false
                type: str
            auth:
                description: Format for authentication logs.
                required: false
                type: str
            userid:
                description: Format for user ID logs.
                required: false
                type: str
            iptag:
                description: Format for IP tag logs.
                required: false
                type: str
            decryption:
                description: Format for decryption logs.
                required: false
                type: str
            config:
                description: Format for configuration logs.
                required: false
                type: str
            system:
                description: Format for system logs.
                required: false
                type: str
            globalprotect:
                description: Format for GlobalProtect logs.
                required: false
                type: str
            hip_match:
                description: Format for HIP match logs.
                required: false
                type: str
            correlation:
                description: Format for correlation logs.
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
        description: Desired state of the syslog server profile.
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
- name: Manage Syslog Server Profiles in Strata Cloud Manager
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

    - name: Create a basic syslog server profile with UDP server
      cdot65.scm.syslog_server_profiles:
        provider: "{{ provider }}"
        name: "basic-syslog-profile"
        servers:
          server1:
            name: "server1"
            server: "192.168.1.100"
            transport: "UDP"
            port: 514
            format: "BSD"
            facility: "LOG_USER"
        folder: "Shared"
        state: "present"

    - name: Create a comprehensive syslog server profile with TCP servers and format settings
      cdot65.scm.syslog_server_profiles:
        provider: "{{ provider }}"
        name: "advanced-syslog-profile"
        servers:
          primary:
            name: "primary"
            server: "logs.example.com"
            transport: "TCP"
            port: 1514
            format: "IETF"
            facility: "LOG_LOCAL0"
          backup:
            name: "backup"
            server: "backup-logs.example.com"
            transport: "TCP"
            port: 1514
            format: "IETF"
            facility: "LOG_LOCAL1"
        format:
          escaping:
            escape_character: "\\"
            escaped_characters: ",\""
          traffic: "hostname,$time,$src,$dst,$proto,$sport,$dport"
          threat: "hostname,$time,$src,$dst,$threatid,$severity"
          system: "hostname,$time,$severity,$result"
        folder: "Shared"
        state: "present"

    - name: Update an existing syslog server profile
      cdot65.scm.syslog_server_profiles:
        provider: "{{ provider }}"
        name: "basic-syslog-profile"
        servers:
          server1:
            name: "server1"
            server: "new-logs.example.com"  # Updated server address
            transport: "UDP"
            port: 514
            format: "BSD"
            facility: "LOG_USER"
        folder: "Shared"
        state: "present"

    - name: Delete a syslog server profile
      cdot65.scm.syslog_server_profiles:
        provider: "{{ provider }}"
        name: "basic-syslog-profile"
        folder: "Shared"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
syslog_server_profile:
    description: Details about the syslog server profile.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "basic-syslog-profile"
        servers:
          server1:
            name: "server1"
            server: "192.168.1.100"
            transport: "UDP"
            port: 514
            format: "BSD"
            facility: "LOG_USER"
        folder: "Shared"
"""


def build_syslog_server_profile_data(module_params):
    """
    Build syslog server profile data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant syslog server profile parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(syslog_server_profile_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        syslog_server_profile_data (dict): Syslog server profile parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [
        syslog_server_profile_data.get(container) for container in ["folder", "snippet", "device"]
    ]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the syslog server profile needs to be updated.

    Args:
        existing: Existing syslog server profile object from the SCM API
        params (dict): Syslog server profile parameters with desired state from Ansible module

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

    # Check servers parameter
    if "servers" in params and params["servers"] is not None:
        existing_servers = getattr(existing, "servers", {})
        if existing_servers != params["servers"]:
            update_data["servers"] = params["servers"]
            changed = True
    else:
        # Preserve existing servers if not updating
        update_data["servers"] = getattr(existing, "servers", {})

    # Check format parameter
    if "format" in params and params["format"] is not None:
        existing_format = getattr(existing, "format", None)
        # Need to compare format structures, which may be nested
        if existing_format != params["format"]:
            update_data["format"] = params["format"]
            changed = True
    elif hasattr(existing, "format") and existing.format is not None:
        update_data["format"] = existing.format

    return changed, update_data


def get_existing_syslog_server_profile(client, syslog_server_profile_data):
    """
    Attempt to fetch an existing syslog server profile object.

    Args:
        client: SCM client instance
        syslog_server_profile_data (dict): Syslog server profile parameters to search for

    Returns:
        tuple: (bool, object) indicating if profile exists and the profile object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if (
                container in syslog_server_profile_data
                and syslog_server_profile_data[container] is not None
            ):
                container_type = container
                break

        if container_type is None or "name" not in syslog_server_profile_data:
            return False, None

        # Fetch the syslog server profile using the appropriate container
        existing = client.syslog_server_profile.fetch(
            name=syslog_server_profile_data["name"],
            **{container_type: syslog_server_profile_data[container_type]},
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the syslog server profile module.

    This module provides functionality to create, update, and delete syslog server profile objects
    in the SCM (Strata Cloud Manager) system. It handles server configurations and format settings,
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=SyslogServerProfilesSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        required_one_of=[["folder", "snippet", "device"]],
    )

    result = {"changed": False, "syslog_server_profile": None}

    try:
        client = get_scm_client(module)
        syslog_server_profile_data = build_syslog_server_profile_data(module.params)

        # Validate container is specified
        if not is_container_specified(syslog_server_profile_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing syslog server profile
        exists, existing_profile = get_existing_syslog_server_profile(
            client, syslog_server_profile_data
        )

        if module.params["state"] == "present":
            if not exists:
                # Create new syslog server profile
                if not module.check_mode:
                    try:
                        new_profile = client.syslog_server_profile.create(
                            data=syslog_server_profile_data
                        )
                        result["syslog_server_profile"] = serialize_response(new_profile)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"A syslog server profile with name '{syslog_server_profile_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid syslog server profile data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(
                    existing_profile, syslog_server_profile_data
                )

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = SyslogServerProfileUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_profile = client.syslog_server_profile.update(update_model)
                        result["syslog_server_profile"] = serialize_response(updated_profile)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["syslog_server_profile"] = serialize_response(existing_profile)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.syslog_server_profile.delete(str(existing_profile.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
