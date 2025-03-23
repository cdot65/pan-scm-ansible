# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
API spec for dynamic_user_group module.

This module defines the specs for the dynamic_user_group module used in Ansible modules
to interact with dynamic user group objects in SCM.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class DynamicUserGroupSpec:
    """
    API spec for the dynamic_user_group module.

    This class provides the specs for the dynamic_user_group module and all parameters
    available in the SCM API for dynamic user groups.
    """

    @staticmethod
    def spec():
        """
        Returns the spec for the dynamic_user_group API.

        Returns:
            dict: A dictionary containing the spec for the dynamic_user_group API.
        """
        return dict(
            # Required parameters
            name=dict(
                type="str",
                required=True,
                # Max length: 63 chars, must match pattern: ^[a-zA-Z\d\-_. ]+$
            ),
            # Required for state=present
            filter=dict(
                type="str",
                required=False,
                # Max length: 2047 chars
            ),
            # Optional parameters
            description=dict(
                type="str",
                required=False,
                # Max length: 1023 chars
            ),
            tag=dict(
                type="list",
                elements="str",
                required=False,
                # Each tag max length: 127 chars
            ),
            # Container types (exactly one required)
            folder=dict(
                type="str",
                required=False,
                # Max length: 64 chars
            ),
            snippet=dict(
                type="str",
                required=False,
                # Max length: 64 chars
            ),
            device=dict(
                type="str",
                required=False,
                # Max length: 64 chars
            ),
            # Authentication credentials
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
            # State parameter
            state=dict(
                type="str",
                required=True,
                choices=["present", "absent"],
            ),
        )


class DynamicUserGroupInfoSpec:
    """
    API spec for the dynamic_user_group_info module.

    This class provides the specs for the dynamic_user_group_info module and all parameters
    available in the SCM API for retrieving dynamic user group information.
    """

    @staticmethod
    def spec():
        """
        Returns the spec for the dynamic_user_group_info API.

        Returns:
            dict: A dictionary containing the spec for the dynamic_user_group_info API.
        """
        return dict(
            # Optional parameters for fetching specific dynamic user group
            name=dict(
                type="str",
                required=False,
            ),
            # Information gathering options
            gather_subset=dict(
                type="list",
                elements="str",
                default=["config"],
                choices=["all", "config"],
            ),
            # Container types (exactly one required if name not specified)
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
            # Filtering options
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
            # Filter expression filtering
            filters=dict(
                type="list",
                elements="str",
                required=False,
            ),
            # Tag filtering
            tags=dict(
                type="list",
                elements="str",
                required=False,
            ),
            # Authentication credentials
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
