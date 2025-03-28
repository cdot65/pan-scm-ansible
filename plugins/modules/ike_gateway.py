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
Ansible module for managing IKE gateways in SCM.

This module provides functionality to create, update, and delete IKE gateway
configurations in the SCM (Strata Cloud Manager) system.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import uuid
from datetime import datetime

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.ike_gateway import IKEGatewaySpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError
from scm.models.network import IKEGatewayUpdateModel

DOCUMENTATION = r"""
---
module: ike_gateway

short_description: Manage IKE gateways in SCM.

version_added: "0.1.0"

description:
    - Manage IKE gateways within Strata Cloud Manager (SCM).
    - Create, update, and delete IKE gateway configurations.
    - Configure authentication methods, protocol versions, and peer settings.

options:
    name:
        description: The name of the IKE Gateway.
        required: true
        type: str
    authentication:
        description: Authentication configuration for the IKE Gateway.
        required: true
        type: dict
        suboptions:
            pre_shared_key:
                description: Pre-shared key authentication configuration.
                required: false
                type: dict
                suboptions:
                    key:
                        description: Pre-shared key for authentication.
                        required: true
                        type: str
            certificate:
                description: Certificate-based authentication configuration.
                required: false
                type: dict
                suboptions:
                    allow_id_payload_mismatch:
                        description: Allow ID payload mismatch.
                        required: false
                        type: bool
                    certificate_profile:
                        description: Certificate profile name.
                        required: false
                        type: str
                    local_certificate:
                        description: Local certificate configuration.
                        required: false
                        type: dict
                    strict_validation_revocation:
                        description: Enable strict validation revocation.
                        required: false
                        type: bool
                    use_management_as_source:
                        description: Use management interface as source.
                        required: false
                        type: bool
    peer_id:
        description: Peer identification settings.
        required: false
        type: dict
        suboptions:
            type:
                description: Type of peer ID.
                required: true
                type: str
                choices: ["ipaddr", "keyid", "fqdn", "ufqdn"]
            id:
                description: Peer ID string.
                required: true
                type: str
    local_id:
        description: Local identification settings.
        required: false
        type: dict
        suboptions:
            type:
                description: Type of local ID.
                required: true
                type: str
                choices: ["ipaddr", "keyid", "fqdn", "ufqdn"]
            id:
                description: Local ID string.
                required: true
                type: str
    protocol:
        description: IKE protocol configuration.
        required: true
        type: dict
        suboptions:
            version:
                description: IKE protocol version preference.
                required: false
                type: str
                choices: ["ikev2-preferred", "ikev1", "ikev2"]
                default: "ikev2-preferred"
            ikev1:
                description: IKEv1 protocol configuration.
                required: false
                type: dict
                suboptions:
                    ike_crypto_profile:
                        description: IKE Crypto Profile name for IKEv1.
                        required: false
                        type: str
                    dpd:
                        description: Dead Peer Detection configuration.
                        required: false
                        type: dict
                        suboptions:
                            enable:
                                description: Enable Dead Peer Detection.
                                required: false
                                type: bool
            ikev2:
                description: IKEv2 protocol configuration.
                required: false
                type: dict
                suboptions:
                    ike_crypto_profile:
                        description: IKE Crypto Profile name for IKEv2.
                        required: false
                        type: str
                    dpd:
                        description: Dead Peer Detection configuration.
                        required: false
                        type: dict
                        suboptions:
                            enable:
                                description: Enable Dead Peer Detection.
                                required: false
                                type: bool
    protocol_common:
        description: Common protocol configuration.
        required: false
        type: dict
        suboptions:
            nat_traversal:
                description: NAT traversal configuration.
                required: false
                type: dict
                suboptions:
                    enable:
                        description: Enable NAT traversal.
                        required: false
                        type: bool
            passive_mode:
                description: Enable passive mode.
                required: false
                type: bool
            fragmentation:
                description: IKE fragmentation configuration.
                required: false
                type: dict
                suboptions:
                    enable:
                        description: Enable IKE fragmentation.
                        required: false
                        type: bool
    peer_address:
        description: Peer address configuration.
        required: true
        type: dict
        suboptions:
            ip:
                description: Static IP address of peer gateway.
                required: false
                type: str
            fqdn:
                description: FQDN of peer gateway.
                required: false
                type: str
            dynamic:
                description: Dynamic peer address configuration.
                required: false
                type: dict
    folder:
        description: The folder in which the resource is defined.
        required: false
        type: str
    snippet:
        description: The snippet in which the resource is defined.
        required: false
        type: str
    device:
        description: The device in which the resource is defined.
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
        description: Desired state of the IKE gateway.
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
- name: Manage IKE Gateways in Strata Cloud Manager
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

    - name: Create an IKE Gateway with pre-shared key authentication
      cdot65.scm.ike_gateway:
        provider: "{{ provider }}"
        name: "ikev2-psk-gateway"
        authentication:
          pre_shared_key:
            key: "supersecretpsk"
        peer_id:
          type: "fqdn"
          id: "remote.example.com"
        local_id:
          type: "fqdn"
          id: "local.example.com"
        protocol:
          version: "ikev2"
          ikev2:
            ike_crypto_profile: "ikev2-aes256-sha256"
            dpd:
              enable: true
        protocol_common:
          nat_traversal:
            enable: true
          fragmentation:
            enable: true
        peer_address:
          ip: "198.51.100.1"
        folder: "SharedFolder"
        state: "present"

    - name: Create an IKE Gateway with certificate authentication
      cdot65.scm.ike_gateway:
        provider: "{{ provider }}"
        name: "ikev2-cert-gateway"
        authentication:
          certificate:
            certificate_profile: "my-cert-profile"
            allow_id_payload_mismatch: false
            strict_validation_revocation: true
        protocol:
          version: "ikev2-preferred"
          ikev1:
            ike_crypto_profile: "ikev1-default"
          ikev2:
            ike_crypto_profile: "ikev2-default"
        peer_address:
          fqdn: "remote-gateway.example.com"
        folder: "SharedFolder"
        state: "present"

    - name: Update an existing IKE Gateway
      cdot65.scm.ike_gateway:
        provider: "{{ provider }}"
        name: "ikev2-psk-gateway"
        authentication:
          pre_shared_key:
            key: "newsecretpsk"
        protocol:
          version: "ikev2"
          ikev2:
            ike_crypto_profile: "ikev2-updated-profile"
        folder: "SharedFolder"
        state: "present"

    - name: Delete an IKE Gateway
      cdot65.scm.ike_gateway:
        provider: "{{ provider }}"
        name: "ikev2-cert-gateway"
        folder: "SharedFolder"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Indicates if the resource has been changed.
    returned: always
    type: bool
    sample: true
gateway:
    description: The details of the IKE gateway.
    returned: when state is present
    type: complex
    contains:
        id:
            description: The UUID of the IKE gateway.
            returned: when state is present
            type: str
            sample: "123e4567-e89b-12d3-a456-426655440000"
        name:
            description: The name of the IKE gateway.
            returned: when state is present
            type: str
            sample: "ikev2-psk-gateway"
        authentication:
            description: Authentication configuration.
            returned: when state is present
            type: dict
        peer_id:
            description: Peer identification settings.
            returned: when state is present
            type: dict
        local_id:
            description: Local identification settings.
            returned: when state is present
            type: dict
        protocol:
            description: IKE protocol configuration.
            returned: when state is present
            type: dict
        protocol_common:
            description: Common protocol configuration.
            returned: when state is present
            type: dict
        peer_address:
            description: Peer address configuration.
            returned: when state is present
            type: dict
        folder:
            description: The folder in which the resource is defined.
            returned: when state is present
            type: str
            sample: "SharedFolder"
        snippet:
            description: The snippet in which the resource is defined.
            returned: when state is present
            type: str
            sample: null
        device:
            description: The device in which the resource is defined.
            returned: when state is present
            type: str
            sample: null
        created_at:
            description: The timestamp when the IKE gateway was created.
            returned: when state is present
            type: str
            sample: "2024-03-15T14:30:22.123456Z"
        created_by:
            description: The user who created the IKE gateway.
            returned: when state is present
            type: str
            sample: "admin@example.com"
        modified_at:
            description: The timestamp when the IKE gateway was last modified.
            returned: when state is present
            type: str
            sample: "2024-03-16T09:45:33.123456Z"
        modified_by:
            description: The user who last modified the IKE gateway.
            returned: when state is present
            type: str
            sample: "admin@example.com"
"""


def build_gateway_data(module_params):
    """
    Build IKE gateway data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant gateway parameters
    """
    gateway_fields = [
        "name",
        "peer_id",
        "local_id",
        "folder",
        "snippet",
        "device",
    ]

    # Start with base fields
    gateway_data = {
        field: module_params.get(field)
        for field in gateway_fields
        if module_params.get(field) is not None
    }

    # Handle authentication - ensure only one auth type is included
    if module_params.get("authentication") is not None:
        auth = module_params["authentication"]
        gateway_data["authentication"] = {}

        if auth.get("pre_shared_key") is not None:
            gateway_data["authentication"]["pre_shared_key"] = auth["pre_shared_key"]
        elif auth.get("certificate") is not None:
            gateway_data["authentication"]["certificate"] = auth["certificate"]

    # Handle protocol - ensure proper structure based on version
    if module_params.get("protocol") is not None:
        protocol = module_params["protocol"]
        gateway_data["protocol"] = {"version": protocol.get("version", "ikev2-preferred")}

        if protocol.get("ikev1") is not None:
            gateway_data["protocol"]["ikev1"] = protocol["ikev1"]

        if protocol.get("ikev2") is not None:
            gateway_data["protocol"]["ikev2"] = protocol["ikev2"]

    # Handle peer_address - ensure only one address type is included
    if module_params.get("peer_address") is not None:
        addr = module_params["peer_address"]
        gateway_data["peer_address"] = {}

        if addr.get("ip") is not None:
            gateway_data["peer_address"]["ip"] = addr["ip"]
        elif addr.get("fqdn") is not None:
            gateway_data["peer_address"]["fqdn"] = addr["fqdn"]
        elif addr.get("dynamic") is not None:
            gateway_data["peer_address"]["dynamic"] = addr["dynamic"]

    # Handle protocol_common
    if module_params.get("protocol_common") is not None:
        gateway_data["protocol_common"] = module_params["protocol_common"]

    return gateway_data


def is_container_specified(data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        data (dict): Gateway parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    container_fields = ["folder", "snippet", "device"]
    container_count = sum(1 for field in container_fields if data.get(field) is not None)
    return container_count == 1


def get_existing_gateway(client, gateway_data):
    """
    Attempt to fetch an existing IKE gateway.

    Args:
        client: SCM client instance
        gateway_data (dict): Gateway parameters to search for

    Returns:
        tuple: (bool, object) indicating if gateway exists and the gateway object if found
    """
    try:
        # Determine which container to use
        container_type = None
        container_value = None
        for field in ["folder", "snippet", "device"]:
            if gateway_data.get(field) is not None:
                container_type = field
                container_value = gateway_data[field]
                break

        if not container_type or not container_value:
            return False, None

        # Fetch the gateway by name and container
        gateway = client.ike_gateway.fetch(
            name=gateway_data["name"], **{container_type: container_value}
        )
        return True, gateway
    except (MissingQueryParameterError, ObjectNotPresentError):
        return False, None
    except Exception as e:
        return False, e


def needs_update(existing, params):
    """
    Determine if the IKE gateway needs to be updated.

    Args:
        existing: Existing IKE gateway object from the SCM API
        params (dict): Gateway parameters with desired state from Ansible module

    Returns:
        (bool, dict): Tuple containing:
            - bool: Whether an update is needed
            - dict: Complete object data for update including all fields from the existing
                   object with any modifications from the params
    """
    # Convert existing object to a dictionary for comparison
    existing_dict = serialize_response(existing)
    update_needed = False
    update_data = {}

    # Start with all fields from the existing gateway
    update_data["id"] = str(existing.id)

    # Always include name in the update data
    update_data["name"] = existing.name

    # Check which fields to update based on provided parameters
    gateway_fields = [
        "name",
        "authentication",
        "peer_id",
        "local_id",
        "protocol",
        "protocol_common",
        "peer_address",
    ]

    # Include container field in update data (only one of these should be set)
    for container in ["folder", "snippet", "device"]:
        if getattr(existing, container) is not None:
            update_data[container] = getattr(existing, container)

    # Check each field for changes
    for field in gateway_fields:
        if field in params and params[field] is not None:
            if field == "authentication" and "pre_shared_key" in params[field]:
                # Always update if pre_shared_key is provided (can't compare PSK)
                update_needed = True
                update_data[field] = params[field]
            elif field in existing_dict and params[field] != existing_dict[field]:
                update_needed = True
                update_data[field] = params[field]
            else:
                # Include existing field value if no update needed
                update_data[field] = existing_dict.get(field)
        elif field in existing_dict:
            # Include existing field value if not provided in params
            update_data[field] = existing_dict.get(field)

    return update_needed, update_data


def main():
    """
    Main execution path for the ike_gateway module.

    This module provides functionality to create, update, and delete IKE gateways
    in the SCM (Strata Cloud Manager) system.

    :return: Ansible module exit data
    :rtype: dict
    """
    # Create AnsibleModule instance with params from IKEGatewaySpec
    module = AnsibleModule(
        argument_spec=IKEGatewaySpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet", "device"],
        ],
        required_one_of=[
            ["folder", "snippet", "device"],
        ],
    )

    # Configure parameters from module
    state = module.params.get("state")
    gateway_data = build_gateway_data(module.params)

    # Initialize result
    result = {"changed": False, "gateway": {}}

    # Check if container specified
    if not is_container_specified(gateway_data):
        module.fail_json(msg="Exactly one of folder, snippet, or device must be specified.")

    try:
        # Get the SCM client
        client = get_scm_client(module)  # Pass the module object, not just the provider dictionary

        # Check if client is properly initialized
        if not client:
            module.fail_json(msg="Failed to initialize SCM client")

        # Check if the gateway exists
        gateway_exists, existing_gateway = get_existing_gateway(client, gateway_data)

        # Handle errors from get_existing_gateway
        if isinstance(existing_gateway, Exception):
            module.fail_json(msg=f"Error fetching existing gateway: {str(existing_gateway)}")

        # Handle state=present (create or update)
        if state == "present":
            if gateway_exists and existing_gateway:
                # Check if gateway needs update
                update_needed, update_data = needs_update(existing_gateway, gateway_data)

                if update_needed:
                    if not module.check_mode:
                        try:
                            # Create update model
                            gateway = IKEGatewayUpdateModel(**update_data)
                            # Validate client has ike_gateway attribute
                            if not hasattr(client, "ike_gateway"):
                                module.fail_json(
                                    msg="SCM client does not have ike_gateway service initialized"
                                )
                            # Update the gateway
                            updated_gateway = client.ike_gateway.update(gateway)
                            result["gateway"] = serialize_response(updated_gateway)
                        except Exception as e:
                            module.fail_json(msg=f"Error updating gateway: {str(e)}")
                    result["changed"] = True
                else:
                    # No update needed
                    result["gateway"] = serialize_response(existing_gateway)
            else:
                # Create new gateway
                if not module.check_mode:
                    try:
                        # Validate client has ike_gateway attribute
                        if not hasattr(client, "ike_gateway"):
                            module.fail_json(
                                msg="SCM client does not have ike_gateway service initialized"
                            )
                        created_gateway = client.ike_gateway.create(data=gateway_data)
                        result["gateway"] = serialize_response(created_gateway)
                    except Exception as e:
                        module.fail_json(msg=f"Error creating gateway: {str(e)}")
                result["changed"] = True

        # Handle state=absent (delete)
        elif state == "absent":
            if gateway_exists and existing_gateway:
                if not module.check_mode:
                    try:
                        # Validate client has ike_gateway attribute
                        if not hasattr(client, "ike_gateway"):
                            module.fail_json(
                                msg="SCM client does not have ike_gateway service initialized"
                            )
                        # Ensure existing_gateway has an id attribute
                        if not hasattr(existing_gateway, "id"):
                            module.fail_json(msg="Gateway object does not have an ID attribute")
                        # Delete the gateway
                        client.ike_gateway.delete(object_id=str(existing_gateway.id))
                    except Exception as e:
                        module.fail_json(msg=f"Error deleting gateway: {str(e)}")
                result["changed"] = True

    except Exception as e:
        module.fail_json(msg=f"Error: {str(e)}")

    module.exit_json(**result)


if __name__ == "__main__":
    main()
