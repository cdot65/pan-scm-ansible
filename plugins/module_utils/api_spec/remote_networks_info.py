"""
API specification for remote networks information in Strata Cloud Manager (SCM).

This module provides the argument specification for the remote_networks_info Ansible module,
which retrieves information about remote networks in the SCM system.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class RemoteNetworksInfoSpec:
    """
    API specification for remote networks information in Strata Cloud Manager.

    This class defines the argument specification for the remote_networks_info Ansible module.
    """

    @staticmethod
    def spec():
        """
        Return the argument specification for the remote_networks_info module.

        Returns:
            dict: Argument specification for the remote_networks_info module.
        """
        return dict(
            name=dict(type="str", required=False),
            gather_subset=dict(
                type="list", elements="str", default=["config"], choices=["all", "config"]
            ),
            folder=dict(type="str", required=False),
            regions=dict(type="list", elements="str", required=False),
            license_types=dict(
                type="list",
                elements="str",
                required=False,
                choices=["FWAAS-AGGREGATE", "FWAAS-BYOL", "CN-SERIES", "FWAAS-PAYG"],
            ),
            subnets=dict(type="list", elements="str", required=False),
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
        )
