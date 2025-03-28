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
Ansible module for managing HTTP server profile objects in SCM.

This module provides functionality to create, update, and delete HTTP server profile objects
in the SCM (Strata Cloud Manager) system. It handles various server configurations
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.http_server_profiles import (
    HTTPServerProfilesSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.objects import HTTPServerProfileUpdateModel

DOCUMENTATION = r"""
---
module: http_server_profiles

short_description: Manage HTTP server profile objects in SCM.

version_added: "0.1.0"

description:
    - Manage HTTP server profile objects within Strata Cloud Manager (SCM).
    - Create, update, and delete HTTP server profile objects.
    - Configure HTTP and HTTPS servers with various settings.
    - Ensures that exactly one container type (folder, snippet, device) is provided.

options:
    name:
        description: The name of the HTTP server profile (max 63 chars).
        required: true
        type: str
    server:
        description: List of server configurations within the HTTP server profile. Required when state=present.
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: HTTP server name.
                required: true
                type: str
            address:
                description: HTTP server address.
                required: true
                type: str
            protocol:
                description: HTTP server protocol.
                required: true
                type: str
                choices: ["HTTP", "HTTPS"]
            port:
                description: HTTP server port.
                required: true
                type: int
            tls_version:
                description: HTTP server TLS version (only applies when protocol is HTTPS).
                required: false
                type: str
                choices: ["1.0", "1.1", "1.2", "1.3"]
            certificate_profile:
                description: HTTP server certificate profile (only applies when protocol is HTTPS).
                required: false
                type: str
            http_method:
                description: HTTP operation to perform.
                required: true
                type: str
                choices: ["GET", "POST", "PUT", "DELETE"]
    tag_registration:
        description: Whether to register tags on match.
        required: false
        type: bool
    description:
        description: Description of the HTTP server profile.
        required: false
        type: str
    format:
        description: Format settings for different log types.
        required: false
        type: dict
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
        description: Desired state of the HTTP server profile object.
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
- name: Manage HTTP Server Profiles in Strata Cloud Manager
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

    - name: Create an HTTP server profile with a single HTTP server
      cdot65.scm.http_server_profiles:
        provider: "{{ provider }}"
        name: "test-http-profile"
        description: "Test HTTP server profile"
        server:
          - name: "primary-server"
            address: "10.0.0.1"
            protocol: "HTTP"
            port: 8080
        folder: "Texas"
        state: "present"

    - name: Create an HTTPS server profile with TLS configuration
      cdot65.scm.http_server_profiles:
        provider: "{{ provider }}"
        name: "secure-profile"
        description: "Secure HTTPS server profile"
        server:
          - name: "secure-server"
            address: "logs.example.com"
            protocol: "HTTPS"
            port: 443
            tls_version: "1.2"
            certificate_profile: "default-cert-profile"
            http_method: "POST"
        tag_registration: true
        folder: "Texas"
        state: "present"

    - name: Update an existing HTTP server profile
      cdot65.scm.http_server_profiles:
        provider: "{{ provider }}"
        name: "test-http-profile"
        description: "Updated HTTP server profile"
        server:
          - name: "primary-server"
            address: "10.0.0.1"
            protocol: "HTTP"
            port: 8080
          - name: "backup-server"
            address: "10.0.0.2"
            protocol: "HTTP"
            port: 8080
        folder: "Texas"
        state: "present"

    - name: Delete an HTTP server profile
      cdot65.scm.http_server_profiles:
        provider: "{{ provider }}"
        name: "test-http-profile"
        folder: "Texas"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
http_server_profile:
    description: Details about the HTTP server profile.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "test-http-profile"
        description: "Test HTTP server profile"
        server:
          - name: "primary-server"
            address: "10.0.0.1"
            protocol: "HTTP"
            port: 8080
        folder: "Texas"
        tag_registration: false
"""


def build_http_server_profile_data(module_params):
    """
    Build HTTP server profile data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant HTTP server profile parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(http_server_profile_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        http_server_profile_data (dict): HTTP server profile parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [
        http_server_profile_data.get(container) for container in ["folder", "snippet", "device"]
    ]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the HTTP server profile object needs to be updated.

    Args:
        existing: Existing HTTP server profile object from the SCM API
        params (dict): HTTP server profile parameters with desired state from Ansible module

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
    for param in ["description", "tag_registration"]:
        # Set the current value as default
        current_value = getattr(existing, param, None)
        update_data[param] = current_value

        # If user provided a new value, use it and check if it's different
        if param in params and params[param] is not None:
            if current_value != params[param]:
                update_data[param] = params[param]
                changed = True

    # Check and update server configuration
    if "server" in params and params["server"] is not None:
        # Convert existing servers to comparable format
        existing_servers = []
        if hasattr(existing, "server") and existing.server is not None:
            for server in existing.server:
                server_dict = {
                    "name": server.name,
                    "address": server.address,
                    "protocol": server.protocol,
                    "port": server.port,
                }

                # Add optional fields if present
                if hasattr(server, "tls_version") and server.tls_version is not None:
                    server_dict["tls_version"] = server.tls_version
                if (
                    hasattr(server, "certificate_profile")
                    and server.certificate_profile is not None
                ):
                    server_dict["certificate_profile"] = server.certificate_profile
                if hasattr(server, "http_method") and server.http_method is not None:
                    server_dict["http_method"] = server.http_method

                existing_servers.append(server_dict)

        # Convert params servers to comparable format
        params_servers = []
        for server in params["server"]:
            server_dict = {
                "name": server["name"],
                "address": server["address"],
                "protocol": server["protocol"],
                "port": server["port"],
            }

            # Add optional fields if present
            if "tls_version" in server and server["tls_version"] is not None:
                server_dict["tls_version"] = server["tls_version"]
            if "certificate_profile" in server and server["certificate_profile"] is not None:
                server_dict["certificate_profile"] = server["certificate_profile"]
            if "http_method" in server and server["http_method"] is not None:
                server_dict["http_method"] = server["http_method"]

            params_servers.append(server_dict)

        # Compare server configurations
        # Normalize servers for comparison by sorting them and their keys
        def normalize_servers(servers):
            sorted_servers = sorted(servers, key=lambda x: x["name"])
            for server in sorted_servers:
                # Sort the keys in each server dict for consistent comparison
                server = {k: server[k] for k in sorted(server)}
            return sorted_servers

        normalized_existing = normalize_servers(existing_servers)
        normalized_params = normalize_servers(params_servers)

        if normalized_existing != normalized_params:
            update_data["server"] = params["server"]
            changed = True
        else:
            update_data["server"] = existing_servers

    # Check format configuration
    if "format" in params and params["format"] is not None:
        current_format = getattr(existing, "format", None)
        if current_format != params["format"]:
            update_data["format"] = params["format"]
            changed = True
        else:
            update_data["format"] = current_format

    return changed, update_data


def get_existing_http_server_profile(client, http_server_profile_data):
    """
    Attempt to fetch an existing HTTP server profile object.

    Args:
        client: SCM client instance
        http_server_profile_data (dict): HTTP server profile parameters to search for

    Returns:
        tuple: (bool, object) indicating if HTTP server profile exists and the HTTP server profile object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if (
                container in http_server_profile_data
                and http_server_profile_data[container] is not None
            ):
                container_type = container
                break

        if container_type is None or "name" not in http_server_profile_data:
            return False, None

        # Fetch the HTTP server profile using the appropriate container
        existing = client.http_server_profile.fetch(
            name=http_server_profile_data["name"],
            **{container_type: http_server_profile_data[container_type]},
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the HTTP server profile object module.

    This module provides functionality to create, update, and delete HTTP server profile objects
    in the SCM (Strata Cloud Manager) system. It handles various server configurations
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=HTTPServerProfilesSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet", "device"],
        ],
        required_one_of=[["folder", "snippet", "device"]],
        required_if=[
            ["state", "present", ["server"]],
        ],
    )

    result = {"changed": False, "http_server_profile": None}

    try:
        client = get_scm_client(module)
        http_server_profile_data = build_http_server_profile_data(module.params)

        # Validate container is specified
        if not is_container_specified(http_server_profile_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing HTTP server profile
        exists, existing_http_server_profile = get_existing_http_server_profile(
            client, http_server_profile_data
        )

        if module.params["state"] == "present":
            if not exists:
                # Create new HTTP server profile
                if not module.check_mode:
                    try:
                        new_http_server_profile = client.http_server_profile.create(
                            data=http_server_profile_data
                        )
                        result["http_server_profile"] = serialize_response(new_http_server_profile)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"An HTTP server profile with name '{http_server_profile_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid HTTP server profile data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(
                    existing_http_server_profile, http_server_profile_data
                )

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = HTTPServerProfileUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_http_server_profile = client.http_server_profile.update(
                            update_model
                        )
                        result["http_server_profile"] = serialize_response(
                            updated_http_server_profile
                        )
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["http_server_profile"] = serialize_response(existing_http_server_profile)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    try:
                        profile_id = str(existing_http_server_profile.id)
                        client.http_server_profile.delete(profile_id)
                        result["changed"] = True
                        result["msg"] = f"Deleted HTTP server profile with ID: {profile_id}"
                    except Exception as e:
                        module.fail_json(msg=f"Failed to delete HTTP server profile: {str(e)}")
                else:
                    result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
