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
Ansible module for managing internal DNS servers in SCM.

This module provides functionality to create, update, and delete internal DNS server objects
in the SCM (Strata Cloud Manager) system. It supports configuring domain names,
primary and secondary DNS servers.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.internal_dns_servers import (
    InternalDnsServersSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.deployment import InternalDnsServersUpdateModel

DOCUMENTATION = r"""
---
module: internal_dns_servers

short_description: Manage internal DNS servers in SCM.

version_added: "0.1.0"

description:
    - Manage internal DNS server objects within Strata Cloud Manager (SCM).
    - Create, update, and delete internal DNS server configurations.
    - Configure domain names, primary and secondary DNS servers.

options:
    name:
        description: The name of the internal DNS server object (max 63 chars).
        required: true
        type: str
    domain_name:
        description: List of domain names to be resolved by these DNS servers.
        required: false
        type: list
        elements: str
    primary:
        description: IP address of the primary DNS server.
        required: false
        type: str
    secondary:
        description: IP address of the secondary DNS server.
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
        description: Desired state of the internal DNS server object.
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
- name: Manage Internal DNS Servers in Strata Cloud Manager
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

    - name: Create a DNS server configuration
      cdot65.scm.internal_dns_servers:
        provider: "{{ provider }}"
        name: "main-dns-server"
        domain_name: ["example.com", "internal.example.com"]
        primary: "192.168.1.10"
        secondary: "192.168.1.11"
        state: "present"
      register: dns_server

    - name: Update DNS server configuration with additional domain
      cdot65.scm.internal_dns_servers:
        provider: "{{ provider }}"
        name: "main-dns-server"
        domain_name: ["example.com", "internal.example.com", "new-domain.example.com"]
        primary: "192.168.1.10"
        secondary: "192.168.1.12"
        state: "present"
      register: updated_dns_server

    - name: Remove DNS server configuration
      cdot65.scm.internal_dns_servers:
        provider: "{{ provider }}"
        name: "main-dns-server"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
internal_dns_server:
    description: Details about the internal DNS server object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "main-dns-server"
        domain_name: ["example.com", "internal.example.com"]
        primary: "192.168.1.10"
        secondary: "192.168.1.11"
"""


def build_dns_server_data(module_params):
    """
    Build DNS server data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant DNS server parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def needs_update(existing, params):
    """
    Determine if the DNS server object needs to be updated.

    Args:
        existing: Existing DNS server object from the SCM API
        params (dict): DNS server parameters with desired state from Ansible module

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

    # Check each parameter that can be updated
    for param in ["domain_name", "primary", "secondary"]:
        # Set the current value as default
        current_value = getattr(existing, param, None)
        update_data[param] = current_value

        # If user provided a new value, use it and check if it's different
        if param in params and params[param] is not None:
            if param == "domain_name":
                # Compare lists for domain_name
                if sorted(current_value) != sorted(params[param]):
                    update_data[param] = params[param]
                    changed = True
            elif param in ["primary", "secondary"]:
                # Convert both to strings for comparison (handles IPvAnyAddress objects)
                if str(current_value) != str(params[param]):
                    update_data[param] = params[param]
                    changed = True
            elif current_value != params[param]:
                update_data[param] = params[param]
                changed = True

    return changed, update_data


def get_existing_dns_server(client, dns_server_data):
    """
    Attempt to fetch an existing DNS server object.

    Args:
        client: SCM client instance
        dns_server_data (dict): DNS server parameters to search for

    Returns:
        tuple: (bool, object) indicating if DNS server exists and the DNS server object if found
    """
    try:
        if "name" not in dns_server_data:
            return False, None

        # Fetch the DNS server by name
        existing = client.internal_dns_server.fetch(name=dns_server_data["name"])
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the internal DNS server module.

    This module provides functionality to create, update, and delete internal DNS server objects
    in the SCM (Strata Cloud Manager) system. It supports configuring domain names,
    primary and secondary DNS servers.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=InternalDnsServersSpec.spec(),
        supports_check_mode=True,
        required_if=[["state", "present", ["domain_name", "primary"], True]],
    )

    result = {"changed": False, "internal_dns_server": None}

    try:
        client = get_scm_client(module)
        dns_server_data = build_dns_server_data(module.params)

        # Get existing DNS server
        exists, existing_dns_server = get_existing_dns_server(client, dns_server_data)

        if module.params["state"] == "present":
            if not exists:
                # Create new DNS server
                if not module.check_mode:
                    try:
                        new_dns_server = client.internal_dns_server.create(data=dns_server_data)
                        result["internal_dns_server"] = serialize_response(new_dns_server)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"An internal DNS server with name '{dns_server_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid internal DNS server data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_dns_server, dns_server_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = InternalDnsServersUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_dns_server = client.internal_dns_server.update(update_model)
                        result["internal_dns_server"] = serialize_response(updated_dns_server)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["internal_dns_server"] = serialize_response(existing_dns_server)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.internal_dns_server.delete(str(existing_dns_server.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
