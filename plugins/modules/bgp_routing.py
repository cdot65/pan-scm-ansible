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
Ansible module for managing BGP routing configuration in SCM.

This module provides functionality to create, update, and reset BGP routing configuration
in the SCM (Strata Cloud Manager) system. It handles various BGP routing settings
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.bgp_routing import BGPRoutingSpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, MissingQueryParameterError

DOCUMENTATION = r"""
---
module: bgp_routing

short_description: Manage BGP routing configuration in SCM.

version_added: "0.1.0"

description:
    - Manage BGP routing configuration within Strata Cloud Manager (SCM).
    - Create, update, and reset BGP routing settings for service connections.
    - Configure routing preferences, backbone routing options, and other BGP-related settings.
    - BGP routing is a singleton object in SCM, meaning there is only one global configuration.

options:
    backbone_routing:
        description: The backbone routing option to use.
        required: false
        type: str
        choices:
          - no-asymmetric-routing
          - asymmetric-routing-only
          - asymmetric-routing-with-load-share
    routing_preference:
        description: The routing preference configuration.
        required: false
        type: dict
        suboptions:
            default:
                description: Default routing configuration (empty dict).
                type: dict
                required: false
            hot_potato_routing:
                description: Hot potato routing configuration (empty dict).
                type: dict
                required: false
    accept_route_over_SC:
        description: Whether to accept routes over service connections.
        required: false
        type: bool
    outbound_routes_for_services:
        description: List of outbound routes for services in CIDR notation.
        required: false
        type: list
        elements: str
    add_host_route_to_ike_peer:
        description: Whether to add host route to IKE peer.
        required: false
        type: bool
    withdraw_static_route:
        description: Whether to withdraw static routes.
        required: false
        type: bool
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
        description: Desired state of the BGP routing configuration.
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
- name: Manage BGP Routing in Strata Cloud Manager
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

    - name: Configure BGP routing with default routing
      cdot65.scm.bgp_routing:
        provider: "{{ provider }}"
        backbone_routing: "no-asymmetric-routing"
        routing_preference:
          default: {}
        accept_route_over_SC: false
        outbound_routes_for_services: ["10.0.0.0/8", "172.16.0.0/12"]
        add_host_route_to_ike_peer: false
        withdraw_static_route: false
        state: "present"

    - name: Configure BGP routing with hot potato routing
      cdot65.scm.bgp_routing:
        provider: "{{ provider }}"
        backbone_routing: "asymmetric-routing-with-load-share"
        routing_preference:
          hot_potato_routing: {}
        accept_route_over_SC: true
        outbound_routes_for_services: ["192.168.0.0/16"]
        add_host_route_to_ike_peer: true
        withdraw_static_route: false
        state: "present"

    - name: Update only the backbone routing option
      cdot65.scm.bgp_routing:
        provider: "{{ provider }}"
        backbone_routing: "asymmetric-routing-only"
        state: "present"

    - name: Reset BGP routing to default configuration
      cdot65.scm.bgp_routing:
        provider: "{{ provider }}"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
bgp_routing:
    description: Details about the BGP routing configuration.
    returned: when state is present
    type: dict
    sample:
        backbone_routing: "no-asymmetric-routing"
        routing_preference:
            default: {}
        accept_route_over_SC: false
        outbound_routes_for_services: ["10.0.0.0/8"]
        add_host_route_to_ike_peer: false
        withdraw_static_route: false
"""


def build_bgp_routing_data(module_params):
    """
    Build BGP routing data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant BGP routing parameters
    """
    bgp_data = {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }

    # Ensure routing_preference has proper structure
    if "routing_preference" in bgp_data:
        routing_pref = bgp_data["routing_preference"]
        # Keep only non-empty parameter
        if "default" in routing_pref and not routing_pref["default"]:
            bgp_data["routing_preference"] = {"default": {}}
        elif "hot_potato_routing" in routing_pref and not routing_pref["hot_potato_routing"]:
            bgp_data["routing_preference"] = {"hot_potato_routing": {}}

    return bgp_data


def get_current_bgp_routing(client):
    """
    Get current BGP routing configuration.

    Args:
        client: SCM client instance

    Returns:
        object: Current BGP routing configuration or None if it doesn't exist
    """
    try:
        return client.bgp_routing.get()
    except Exception:
        # Return None if BGP routing configuration doesn't exist or there's an error
        return None


def needs_update(existing, params):
    """
    Determine if the BGP routing configuration needs to be updated.

    Args:
        existing: Existing BGP routing configuration from the SCM API
        params (dict): BGP routing parameters with desired state from Ansible module

    Returns:
        bool: Whether an update is needed
    """
    changed = False

    # Check backbone_routing parameter
    if "backbone_routing" in params and params["backbone_routing"] is not None:
        if existing.backbone_routing.value != params["backbone_routing"]:
            changed = True

    # Check routing_preference parameter
    if "routing_preference" in params and params["routing_preference"] is not None:
        routing_pref = params["routing_preference"]
        existing_is_default = hasattr(existing.routing_preference, "default")

        # If default in params but existing is hot_potato_routing
        if "default" in routing_pref and not existing_is_default:
            changed = True
        # If hot_potato_routing in params but existing is default
        elif "hot_potato_routing" in routing_pref and existing_is_default:
            changed = True

    # Check boolean parameters
    for bool_param in [
        "accept_route_over_SC",
        "add_host_route_to_ike_peer",
        "withdraw_static_route",
    ]:
        if bool_param in params and params[bool_param] is not None:
            if getattr(existing, bool_param) != params[bool_param]:
                changed = True

    # Check outbound_routes_for_services parameter
    if (
        "outbound_routes_for_services" in params
        and params["outbound_routes_for_services"] is not None
    ):
        # Convert string to list if needed
        routes = params["outbound_routes_for_services"]
        if isinstance(routes, str):
            routes = [routes]

        # Compare routes (order might not matter)
        if set(existing.outbound_routes_for_services) != set(routes):
            changed = True

    return changed


def main():
    """
    Main execution path for the BGP routing module.

    This module provides functionality to create, update, and reset BGP routing configuration
    in the SCM (Strata Cloud Manager) system. It supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=BGPRoutingSpec.spec(),
        supports_check_mode=True,
    )

    result = {"changed": False, "bgp_routing": None}

    try:
        client = get_scm_client(module)
        bgp_routing_data = build_bgp_routing_data(module.params)

        # Get existing BGP routing configuration
        existing_config = get_current_bgp_routing(client)

        if module.params["state"] == "present":
            if existing_config is None:
                # Create new BGP routing configuration
                if not module.check_mode:
                    try:
                        new_config = client.bgp_routing.create(bgp_routing_data)
                        result["bgp_routing"] = serialize_response(new_config)
                        result["changed"] = True
                    except (InvalidObjectError, MissingQueryParameterError) as e:
                        module.fail_json(
                            msg=f"Failed to create BGP routing configuration: {str(e)}"
                        )
                else:
                    result["changed"] = True
            else:
                # Check if update is needed
                need_update = needs_update(existing_config, bgp_routing_data)

                if need_update:
                    if not module.check_mode:
                        try:
                            # Perform update
                            updated_config = client.bgp_routing.update(bgp_routing_data)
                            result["bgp_routing"] = serialize_response(updated_config)
                            result["changed"] = True
                        except (InvalidObjectError, MissingQueryParameterError) as e:
                            module.fail_json(
                                msg=f"Failed to update BGP routing configuration: {str(e)}"
                            )
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["bgp_routing"] = serialize_response(existing_config)

        elif module.params["state"] == "absent":
            if existing_config is not None:
                # Only reset if configuration exists
                if not module.check_mode:
                    try:
                        client.bgp_routing.delete()
                        result["changed"] = True
                    except Exception as e:
                        module.fail_json(msg=f"Failed to reset BGP routing configuration: {str(e)}")
                else:
                    result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
