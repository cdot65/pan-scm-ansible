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

from __future__ import absolute_import, division, print_function

__metaclass__ = type

try:
    from typing import Dict
except ImportError:
    # Define fallback for Python 2.7
    Dict = None


class BGPRoutingSpec:
    """
    BGP Routing API specification for Ansible modules interacting with SCM BGP routing configuration.

    This class provides a standard specification for BGP routing-related parameters 
    used in SCM Ansible modules. It ensures consistent parameter validation
    across the collection.
    """

    @staticmethod
    def spec():
        """
        Returns Ansible module spec for BGP routing configuration.

        This method defines the structure and requirements for BGP routing-related
        parameters in SCM modules, including all attributes for BGP routing
        configuration.

        Returns:
            Dict: A dictionary containing the module specification with
                parameter definitions and their requirements.
        """
        return dict(
            backbone_routing=dict(
                type="str",
                required=False,
                choices=[
                    "no-asymmetric-routing",
                    "asymmetric-routing-only",
                    "asymmetric-routing-with-load-share",
                ],
            ),
            routing_preference=dict(
                type="dict",
                required=False,
                options=dict(
                    default=dict(
                        type="dict",
                        required=False,
                    ),
                    hot_potato_routing=dict(
                        type="dict",
                        required=False,
                    ),
                ),
                mutually_exclusive=[["default", "hot_potato_routing"]],
                required_one_of=[["default", "hot_potato_routing"]],
            ),
            accept_route_over_SC=dict(
                type="bool",
                required=False,
            ),
            outbound_routes_for_services=dict(
                type="list",
                elements="str",
                required=False,
            ),
            add_host_route_to_ike_peer=dict(
                type="bool",
                required=False,
            ),
            withdraw_static_route=dict(
                type="bool",
                required=False,
            ),
            provider=dict(
                type="dict",
                required=True,
                options=dict(
                    client_id=dict(
                        type="str",
                        required=True,
                    ),
                    client_secret=dict(
                        type="str",
                        required=True,
                        no_log=True,
                    ),
                    tsg_id=dict(
                        type="str",
                        required=True,
                    ),
                    log_level=dict(
                        type="str",
                        required=False,
                        default="INFO",
                    ),
                ),
            ),
            state=dict(
                type="str",
                choices=["present", "absent"],
                required=True,
            ),
        )
