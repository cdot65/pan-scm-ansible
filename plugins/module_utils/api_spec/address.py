# -*- coding: utf-8 -*-

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.

from typing import Any, Dict


class AddressSpec:
    """
    Address API specification for Ansible modules interacting with SCM address objects.
    
    This class provides a standard specification for address-related parameters
    used in SCM Ansible modules. It ensures consistent parameter validation
    across the collection.
    """

    @staticmethod
    def spec() -> Dict[str, Any]:
        """
        Returns Ansible module spec for address objects.

        This method defines the structure and requirements for address-related
        parameters in SCM modules, including all the attributes for creating,
        updating, and deleting address objects.

        Returns:
            Dict[str, Any]: A dictionary containing the module specification with
                           parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type="str",
                required=True,
            ),
            description=dict(
                type="str",
                required=False,
            ),
            tag=dict(
                type="list",
                elements="str",
                required=False,
            ),
            ip_netmask=dict(
                type="str",
                required=False,
            ),
            ip_range=dict(
                type="str",
                required=False,
            ),
            ip_wildcard=dict(
                type="str",
                required=False,
            ),
            fqdn=dict(
                type="str",
                required=False,
            ),
            folder=dict(
                type="str",
                required=False,
            ),
            snippet=dict(
                type="str",
                required=False,
            ),
            device=dict(
                type="str",
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
