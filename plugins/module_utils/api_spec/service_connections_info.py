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


class ServiceConnectionsInfoSpec:
    """
    Service Connections Info API specification for Ansible modules.

    This class provides a standard specification for service connection info-related parameters
    used in SCM Ansible modules. It ensures consistent parameter validation
    across the collection.
    """

    @staticmethod
    def spec():
        """
        Returns Ansible module spec for service connection info objects.

        This method defines the structure and requirements for service connection info-related
        parameters in SCM modules, including all the attributes for retrieving
        service connection information.

        Returns:
            Dict: A dictionary containing the module specification with
                parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type="str",
                required=False,
            ),
            testmode=dict(
                type="bool",
                required=False,
                default=False,
            ),
            test_timestamp=dict(
                type="str",
                required=False,
            ),
            gather_subset=dict(
                type="list",
                elements="str",
                default=["config"],
                choices=["all", "config"],
            ),
            folder=dict(
                type="str",
                required=False,
                default="Service Connections",
            ),
            snippet=dict(
                type="str",
                required=False,
            ),
            device=dict(
                type="str",
                required=False,
            ),
            exact_match=dict(
                type="bool",
                required=False,
                default=False,
            ),
            exclude_folders=dict(
                type="list",
                elements="str",
                required=False,
            ),
            exclude_snippets=dict(
                type="list",
                elements="str",
                required=False,
            ),
            exclude_devices=dict(
                type="list",
                elements="str",
                required=False,
            ),
            connection_types=dict(
                type="list",
                elements="str",
                required=False,
                choices=["sase", "prisma", "panorama"],
            ),
            status=dict(
                type="list",
                elements="str",
                required=False,
                choices=["enabled", "disabled"],
            ),
            tags=dict(
                type="list",
                elements="str",
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
        )
