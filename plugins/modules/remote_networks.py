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
Ansible module for managing remote networks in SCM.

This module provides functionality to create, update, and delete remote networks
in the SCM (Strata Cloud Manager) system. It manages site-to-site VPN 
connections between Strata Cloud Manager and external networks.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.remote_networks import RemoteNetworksSpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.deployment import RemoteNetworkUpdateModel

DOCUMENTATION = r"""
---
module: remote_networks

short_description: Manage remote networks in SCM.

version_added: "0.1.0"

description:
    - Manage remote networks within Strata Cloud Manager (SCM).
    - Create, update, and delete remote networks that establish site-to-site VPN connections.
    - Configure remote networks with various settings including ECMP load balancing and BGP.
    - Support for different license types (FWAAS-AGGREGATE, FWAAS-BYOL, CN-SERIES, FWAAS-PAYG).

options:
    name:
        description: The name of the remote network.
        required: true
        type: str
    description:
        description: Description of the remote network.
        required: false
        type: str
    region:
        description: The AWS region where the remote network is located.
        required: true
        type: str
    license_type:
        description: The license type for the remote network.
        required: false
        type: str
        default: "FWAAS-AGGREGATE"
        choices: ["FWAAS-AGGREGATE", "FWAAS-BYOL", "CN-SERIES", "FWAAS-PAYG"]
    spn_name:
        description: The SPN name, required when license_type is FWAAS-AGGREGATE.
        required: false
        type: str
    subnets:
        description: List of subnet CIDR ranges for the remote network.
        required: false
        type: list
        elements: str
    folder:
        description: The folder in which the resource is defined.
        required: false
        type: str
    ecmp_load_balancing:
        description: Enable or disable ECMP load balancing for the remote network.
        required: true
        type: str
        choices: ["enable", "disable"]
    ecmp_tunnels:
        description: List of ECMP tunnels when ecmp_load_balancing is enabled.
        required: false
        type: list
        elements: dict
        suboptions:
            name:
                description: Name of the ECMP tunnel.
                required: true
                type: str
            ipsec_tunnel:
                description: The IPsec tunnel name for this ECMP tunnel.
                required: true
                type: str
            local_ip_address:
                description: The local IP address for this tunnel.
                required: true
                type: str
            peer_ip_address:
                description: The peer IP address for this tunnel.
                required: true
                type: str
            peer_as:
                description: The peer AS number for BGP.
                required: true
                type: str
    ipsec_tunnel:
        description: The IPsec tunnel name when ecmp_load_balancing is disabled.
        required: false
        type: str
    protocol:
        description: Protocol configuration for the remote network.
        required: false
        type: dict
        suboptions:
            bgp:
                description: BGP configuration for the remote network.
                required: false
                type: dict
                suboptions:
                    enable:
                        description: Enable or disable BGP.
                        required: false
                        type: bool
                    local_ip_address:
                        description: The local IP address for BGP.
                        required: false
                        type: str
                    peer_ip_address:
                        description: The peer IP address for BGP.
                        required: false
                        type: str
                    peer_as:
                        description: The peer AS number for BGP.
                        required: false
                        type: str
                    local_as:
                        description: The local AS number for BGP.
                        required: false
                        type: str
                    secret:
                        description: The BGP authentication secret.
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
        description: Desired state of the remote network.
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
- name: Manage Remote Networks in Strata Cloud Manager
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

    - name: Create a remote network with standard IPsec tunnel
      cdot65.scm.remote_networks:
        provider: "{{ provider }}"
        name: "Branch-Office-1"
        description: "Remote network for Branch Office 1"
        region: "us-east-1"
        license_type: "FWAAS-AGGREGATE"
        spn_name: "main-spn"
        folder: "Remote-Sites"
        ecmp_load_balancing: "disable"
        ipsec_tunnel: "tunnel-to-branch1"
        subnets: ["10.1.0.0/16", "10.2.0.0/16"]
        protocol:
          bgp:
            enable: true
            local_ip_address: "10.0.0.1"
            peer_ip_address: "10.0.0.2"
            local_as: "65000"
            peer_as: "65001"
            secret: "bgp-auth-key"
        state: "present"

    - name: Create a remote network with ECMP load balancing
      cdot65.scm.remote_networks:
        provider: "{{ provider }}"
        name: "Branch-Office-2"
        description: "Remote network for Branch Office 2 with ECMP"
        region: "us-west-1"
        license_type: "FWAAS-AGGREGATE"
        spn_name: "west-spn"
        folder: "Remote-Sites"
        ecmp_load_balancing: "enable"
        ecmp_tunnels:
          - name: "tunnel1"
            ipsec_tunnel: "tunnel-to-branch2-1"
            local_ip_address: "10.0.1.1"
            peer_ip_address: "10.0.1.2"
            peer_as: "65002"
          - name: "tunnel2"
            ipsec_tunnel: "tunnel-to-branch2-2"
            local_ip_address: "10.0.2.1"
            peer_ip_address: "10.0.2.2"
            peer_as: "65002"
        subnets: ["10.3.0.0/16", "10.4.0.0/16"]
        state: "present"

    - name: Update a remote network
      cdot65.scm.remote_networks:
        provider: "{{ provider }}"
        name: "Branch-Office-1"
        description: "Updated description for Branch Office 1"
        region: "us-east-1"
        folder: "Remote-Sites"
        ecmp_load_balancing: "disable"
        ipsec_tunnel: "updated-tunnel-to-branch1"
        subnets: ["10.1.0.0/16", "10.2.0.0/16", "10.5.0.0/16"]
        state: "present"

    - name: Delete a remote network
      cdot65.scm.remote_networks:
        provider: "{{ provider }}"
        name: "Branch-Office-2"
        folder: "Remote-Sites"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
remote_network:
    description: Details about the remote network.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Branch-Office-1"
        description: "Remote network for Branch Office 1"
        region: "us-east-1"
        license_type: "FWAAS-AGGREGATE"
        spn_name: "main-spn"
        folder: "Remote-Sites"
        ecmp_load_balancing: "disable"
        ipsec_tunnel: "tunnel-to-branch1"
        subnets: ["10.1.0.0/16", "10.2.0.0/16"]
"""


def build_remote_network_data(module_params):
    """
    Build remote network data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant remote network parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def validate_remote_network_data(module, remote_network_data):
    """
    Validate remote network data.

    Args:
        module (AnsibleModule): Ansible module instance
        remote_network_data (dict): Remote network data to validate

    Returns:
        None
    """
    # Validate that FWAAS-AGGREGATE license type requires spn_name
    if remote_network_data.get("license_type") == "FWAAS-AGGREGATE" and not remote_network_data.get("spn_name"):
        module.fail_json(msg="spn_name is required when license_type is FWAAS-AGGREGATE")

    # Validate that ECMP load balancing configuration is correct
    if remote_network_data.get("ecmp_load_balancing") == "enable":
        if not remote_network_data.get("ecmp_tunnels"):
            module.fail_json(msg="ecmp_tunnels is required when ecmp_load_balancing is enabled")
    else:  # ecmp_load_balancing == "disable"
        if not remote_network_data.get("ipsec_tunnel"):
            module.fail_json(msg="ipsec_tunnel is required when ecmp_load_balancing is disabled")


def get_existing_remote_network(client, remote_network_data):
    """
    Attempt to fetch an existing remote network.

    Args:
        client: SCM client instance
        remote_network_data (dict): Remote network parameters to search for

    Returns:
        tuple: (bool, object) indicating if remote network exists and the object if found
    """
    try:
        if "folder" not in remote_network_data or "name" not in remote_network_data:
            return False, None

        existing = client.remote_network.fetch(
            name=remote_network_data["name"], folder=remote_network_data["folder"]
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def needs_update(existing, params):
    """
    Determine if the remote network needs to be updated.

    Args:
        existing: Existing remote network object from the SCM API
        params (dict): Remote network parameters with desired state from Ansible module

    Returns:
        (bool, dict): Tuple containing:
            - bool: Whether an update is needed
            - dict: Complete object data for update
    """
    changed = False

    # Start with a fresh update model using required fields from existing object
    update_data = {
        "id": str(existing.id),
        "name": existing.name,
        "region": existing.region,
        "folder": existing.folder,
        "ecmp_load_balancing": existing.ecmp_load_balancing,
    }

    # Add license_type and spn_name
    update_data["license_type"] = existing.license_type
    if hasattr(existing, "spn_name") and existing.spn_name is not None:
        update_data["spn_name"] = existing.spn_name

    # Check standard parameters that can be updated
    for param in ["description"]:
        current_value = getattr(existing, param, None)
        update_data[param] = current_value

        if param in params and params[param] is not None:
            if current_value != params[param]:
                update_data[param] = params[param]
                changed = True

    # Check subnets
    current_subnets = getattr(existing, "subnets", [])
    update_data["subnets"] = current_subnets or []

    if "subnets" in params and params["subnets"] is not None:
        if set(current_subnets or []) != set(params["subnets"]):
            update_data["subnets"] = params["subnets"]
            changed = True

    # Check ECMP configuration
    if existing.ecmp_load_balancing == "enable":
        # ECMP is enabled, check tunnels
        update_data["ecmp_tunnels"] = getattr(existing, "ecmp_tunnels", [])
        
        if "ecmp_tunnels" in params and params["ecmp_tunnels"] is not None:
            # Compare tunnels by converting to a comparable format
            existing_tunnels = [
                {k: str(v) for k, v in tunnel.dict().items()}
                for tunnel in (existing.ecmp_tunnels or [])
            ]
            new_tunnels = params["ecmp_tunnels"]
            
            if existing_tunnels != new_tunnels:
                update_data["ecmp_tunnels"] = new_tunnels
                changed = True
                
        # Check if ecmp_load_balancing is being changed to disable
        if "ecmp_load_balancing" in params and params["ecmp_load_balancing"] == "disable":
            update_data["ecmp_load_balancing"] = "disable"
            # Remove ecmp_tunnels and add ipsec_tunnel
            if "ecmp_tunnels" in update_data:
                del update_data["ecmp_tunnels"]
            if "ipsec_tunnel" in params and params["ipsec_tunnel"] is not None:
                update_data["ipsec_tunnel"] = params["ipsec_tunnel"]
            changed = True
    else:
        # ECMP is disabled, check ipsec_tunnel
        update_data["ipsec_tunnel"] = getattr(existing, "ipsec_tunnel", None)
        
        if "ipsec_tunnel" in params and params["ipsec_tunnel"] is not None:
            if update_data["ipsec_tunnel"] != params["ipsec_tunnel"]:
                update_data["ipsec_tunnel"] = params["ipsec_tunnel"]
                changed = True
                
        # Check if ecmp_load_balancing is being changed to enable
        if "ecmp_load_balancing" in params and params["ecmp_load_balancing"] == "enable":
            update_data["ecmp_load_balancing"] = "enable"
            # Remove ipsec_tunnel and add ecmp_tunnels
            if "ipsec_tunnel" in update_data:
                del update_data["ipsec_tunnel"]
            if "ecmp_tunnels" in params and params["ecmp_tunnels"] is not None:
                update_data["ecmp_tunnels"] = params["ecmp_tunnels"]
            changed = True

    # Check protocol configuration (BGP)
    current_protocol = getattr(existing, "protocol", None)
    if current_protocol is not None:
        update_data["protocol"] = current_protocol.dict()
    
    if "protocol" in params and params["protocol"] is not None:
        if current_protocol is None or current_protocol.dict() != params["protocol"]:
            update_data["protocol"] = params["protocol"]
            changed = True

    return changed, update_data


def main():
    """
    Main execution path for the remote networks module.

    This module provides functionality to create, update, and delete remote networks
    in the SCM (Strata Cloud Manager) system. It handles various network configurations
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=RemoteNetworksSpec.spec(),
        supports_check_mode=True,
        required_if=[
            ["state", "present", ["name", "folder", "region", "ecmp_load_balancing"]],
            ["state", "absent", ["name", "folder"]]
        ],
    )

    result = {"changed": False, "remote_network": None}

    try:
        client = get_scm_client(module)
        remote_network_data = build_remote_network_data(module.params)

        # Validate folder is specified
        if not remote_network_data.get("folder"):
            module.fail_json(msg="folder parameter is required")

        # Get existing remote network
        exists, existing_remote_network = get_existing_remote_network(client, remote_network_data)

        if module.params["state"] == "present":
            # Validate the remote network data
            validate_remote_network_data(module, remote_network_data)

            if not exists:
                # Create new remote network
                if not module.check_mode:
                    try:
                        new_remote_network = client.remote_network.create(data=remote_network_data)
                        result["remote_network"] = serialize_response(new_remote_network)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"A remote network with name '{remote_network_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid remote network data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_remote_network, remote_network_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = RemoteNetworkUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_remote_network = client.remote_network.update(update_model)
                        result["remote_network"] = serialize_response(updated_remote_network)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["remote_network"] = serialize_response(existing_remote_network)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    try:
                        client.remote_network.delete(str(existing_remote_network.id))
                        result["changed"] = True
                    except ObjectNotPresentError:
                        # Object already deleted, which is fine
                        pass
                else:
                    result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()