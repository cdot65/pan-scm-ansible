"""
API specification for remote networks in Strata Cloud Manager (SCM).

This module provides the argument specification for the remote_networks Ansible module,
which manages remote networks in the SCM system.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class RemoteNetworksSpec:
    """
    API specification for remote networks in Strata Cloud Manager.

    This class defines the argument specification for the remote_networks Ansible module.
    """

    @staticmethod
    def spec():
        """
        Return the argument specification for the remote_networks module.

        Returns:
            dict: Argument specification for the remote_networks module.
        """
        return dict(
            name=dict(type="str", required=True),
            description=dict(type="str", required=False),
            region=dict(type="str", required=True),
            license_type=dict(
                type="str",
                default="FWAAS-AGGREGATE",
                choices=["FWAAS-AGGREGATE", "FWAAS-BYOL", "CN-SERIES", "FWAAS-PAYG"],
            ),
            spn_name=dict(type="str", required=False),
            subnets=dict(type="list", elements="str", required=False),
            folder=dict(type="str", required=False),
            # ECMP configuration
            ecmp_load_balancing=dict(type="str", required=True, choices=["enable", "disable"]),
            ecmp_tunnels=dict(
                type="list",
                elements="dict",
                required=False,
                options=dict(
                    name=dict(type="str", required=True),
                    ipsec_tunnel=dict(type="str", required=True),
                    local_ip_address=dict(type="str", required=True),
                    peer_ip_address=dict(type="str", required=True),
                    peer_as=dict(type="str", required=True),
                ),
            ),
            # Standard tunnel configuration
            ipsec_tunnel=dict(type="str", required=False),
            # Protocol configuration (BGP)
            protocol=dict(
                type="dict",
                required=False,
                options=dict(
                    bgp=dict(
                        type="dict",
                        required=False,
                        options=dict(
                            enable=dict(type="bool", required=False),
                            local_ip_address=dict(type="str", required=False),
                            peer_ip_address=dict(type="str", required=False),
                            peer_as=dict(type="str", required=False),
                            local_as=dict(type="str", required=False),
                            secret=dict(type="str", required=False, no_log=True),
                        ),
                    ),
                ),
            ),
            # Authentication and state parameters
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
            state=dict(type="str", required=True, choices=["present", "absent"]),
        )
