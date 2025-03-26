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


class URLCategoriesSpec:
    """
    URL Categories API specification for Ansible modules interacting with SCM URL category objects.

    This class provides a standard specification for URL categories-related parameters
    used in SCM Ansible modules. It ensures consistent parameter validation
    across the collection.
    """

    @staticmethod
    def spec():
        """
        Returns Ansible module spec for URL category objects.

        This method defines the structure and requirements for URL category-related
        parameters in SCM modules, including all the attributes for creating,
        updating, and deleting URL category objects.

        Returns:
            Dict: A dictionary containing the module specification with
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
            list=dict(
                type="list",
                elements="str",
                required=False,
            ),
            type=dict(
                type="str",
                required=False,
                choices=["URL List", "Category Match"],
                default="URL List",
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
