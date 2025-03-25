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


class SecurityRuleSpec:
    """
    SecurityRule API specification for Ansible modules interacting with SCM security rule objects.

    This class provides a standard specification for security rule-related parameters
    used in SCM Ansible modules. It ensures consistent parameter validation
    across the collection.
    """

    @staticmethod
    def spec():
        """
        Returns Ansible module spec for security rule objects.

        This method defines the structure and requirements for security rule-related
        parameters in SCM modules, including all the attributes for creating,
        updating, and deleting security rule objects.

        Returns:
            Dict: A dictionary containing the module specification with
                parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type="str",
                required=True,
            ),
            disabled=dict(
                type="bool",
                required=False,
                default=False,
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
            from_=dict(
                type="list",
                elements="str",
                required=False,
                default=["any"],
            ),
            source=dict(
                type="list",
                elements="str",
                required=False,
                default=["any"],
            ),
            negate_source=dict(
                type="bool",
                required=False,
                default=False,
            ),
            source_user=dict(
                type="list",
                elements="str",
                required=False,
                default=["any"],
            ),
            source_hip=dict(
                type="list",
                elements="str",
                required=False,
                default=["any"],
            ),
            to_=dict(
                type="list",
                elements="str",
                required=False,
                default=["any"],
            ),
            destination=dict(
                type="list",
                elements="str",
                required=False,
                default=["any"],
            ),
            negate_destination=dict(
                type="bool",
                required=False,
                default=False,
            ),
            destination_hip=dict(
                type="list",
                elements="str",
                required=False,
                default=["any"],
            ),
            application=dict(
                type="list",
                elements="str",
                required=False,
                default=["any"],
            ),
            service=dict(
                type="list",
                elements="str",
                required=False,
                default=["any"],
            ),
            category=dict(
                type="list",
                elements="str",
                required=False,
                default=["any"],
            ),
            action=dict(
                type="str",
                required=False,
                default="allow",
                choices=["allow", "deny", "drop", "reset-client", "reset-server", "reset-both"],
            ),
            profile_setting=dict(
                type="dict",
                required=False,
                options=dict(
                    group=dict(
                        type="list",
                        elements="str",
                        required=False,
                        default=["best-practice"],
                    ),
                ),
            ),
            log_setting=dict(
                type="str",
                required=False,
            ),
            schedule=dict(
                type="str",
                required=False,
            ),
            log_start=dict(
                type="bool",
                required=False,
            ),
            log_end=dict(
                type="bool",
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
            rulebase=dict(
                type="str",
                required=False,
                default="pre",
                choices=["pre", "post"],
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