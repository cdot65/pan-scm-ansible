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
Ansible module for gathering information about BGP routing configuration in SCM.

This module provides functionality to retrieve information about BGP routing configuration
in the SCM (Strata Cloud Manager) system.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError

DOCUMENTATION = r"""
---
module: bgp_routing_info

short_description: Gather information about BGP routing configuration in SCM.

version_added: "0.1.0"

description:
    - Gather information about BGP routing configuration within Strata Cloud Manager (SCM).
    - Retrieve details about backbone routing, routing preferences, and other BGP-related settings.
    - BGP routing is a singleton object in SCM, meaning there is only one global configuration.
    - This is an info module that only retrieves information and does not modify anything.

options:
    gather_subset:
        description:
            - Determines which information to gather about BGP routing.
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
- name: Gather BGP Routing Information in Strata Cloud Manager
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

    - name: Get information about BGP routing configuration
      cdot65.scm.bgp_routing_info:
        provider: "{{ provider }}"
      register: bgp_routing_info

    - name: Display BGP routing information
      debug:
        var: bgp_routing_info.bgp_routing

    - name: Check backbone routing configuration
      debug:
        msg: "Backbone routing is set to {{ bgp_routing_info.bgp_routing.backbone_routing }}"

    - name: Check routing preference type
      debug:
        msg: >
          Routing preference type is
          {% if bgp_routing_info.bgp_routing.routing_preference.default is defined %}
          default routing
          {% elif bgp_routing_info.bgp_routing.routing_preference.hot_potato_routing is defined %}
          hot potato routing
          {% else %}
          unknown
          {% endif %}

    - name: Display outbound routes
      debug:
        msg: "Outbound routes: {{ bgp_routing_info.bgp_routing.outbound_routes_for_services }}"
      when: bgp_routing_info.bgp_routing.outbound_routes_for_services | length > 0
"""

RETURN = r"""
bgp_routing:
    description: Information about the BGP routing configuration.
    returned: success
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


def main():
    """
    Main execution path for the bgp_routing_info module.

    This module provides functionality to gather information about BGP routing configuration
    in the SCM (Strata Cloud Manager) system.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=dict(
            gather_subset=dict(
                type="list", elements="str", default=["config"], choices=["all", "config"]
            ),
            provider=dict(
                type="dict",
                required=True,
                options=dict(
                    client_id=dict(type="str", required=True),
                    client_secret=dict(type="str", required=True, no_log=True),
                    tsg_id=dict(type="str", required=True),
                    log_level=dict(type="str", required=False, default="INFO"),
                ),
            ),
        ),
        supports_check_mode=True,
    )

    result = {}

    try:
        client = get_scm_client(module)

        try:
            # Get BGP routing configuration
            bgp_routing = client.bgp_routing.get()
            
            # Serialize response for Ansible output
            result["bgp_routing"] = serialize_response(bgp_routing)
            
        except InvalidObjectError as e:
            module.fail_json(msg=f"Failed to retrieve BGP routing configuration: {str(e)}")
        except Exception as e:
            module.fail_json(msg=f"Error fetching BGP routing: {str(e)}")

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
