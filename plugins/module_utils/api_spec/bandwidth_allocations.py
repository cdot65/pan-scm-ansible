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


class BandwidthAllocationsSpec:
    """
    Bandwidth Allocations API specification for Ansible modules interacting with SCM bandwidth allocation objects.

    This class provides a standard specification for bandwidth allocation-related parameters 
    used in SCM Ansible modules. It ensures consistent parameter validation
    across the collection.
    """

    @staticmethod
    def spec():
        """
        Returns Ansible module spec for bandwidth allocation objects.

        This method defines the structure and requirements for bandwidth allocation-related
        parameters in SCM modules, including all the attributes for creating,
        updating, and deleting bandwidth allocation objects.

        Returns:
            Dict: A dictionary containing the module specification with
                parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type="str",
                required=True,
            ),
            allocated_bandwidth=dict(
                type="float",
                required=False,
            ),
            spn_name_list=dict(
                type="list",
                elements="str",
                required=False,
            ),
            qos=dict(
                type="dict",
                required=False,
                options=dict(
                    enabled=dict(
                        type="bool",
                        required=False,
                    ),
                    customized=dict(
                        type="bool",
                        required=False,
                    ),
                    profile=dict(
                        type="str",
                        required=False,
                    ),
                    guaranteed_ratio=dict(
                        type="float",
                        required=False,
                    ),
                ),
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