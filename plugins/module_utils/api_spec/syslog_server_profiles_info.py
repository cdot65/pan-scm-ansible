#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Calvin Remsburg (@cdot65)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
API spec for syslog_server_profiles_info module.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class SyslogServerProfilesInfoSpec:
    """
    API specification for the syslog_server_profiles_info module.

    This class defines the parameters accepted by the syslog_server_profiles_info module.
    """

    @staticmethod
    def spec():
        """
        Return the specification for the syslog_server_profiles_info module.

        :return: Module specification dictionary
        :rtype: dict
        """
        return {
            "name": {
                "type": "str",
                "required": False,
                "description": "The name of a specific syslog server profile to retrieve."
            },
            "gather_subset": {
                "type": "list",
                "elements": "str",
                "default": ["config"],
                "choices": ["all", "config"],
                "description": (
                    "Determines which information to gather about syslog server profiles. "
                    "C(all) gathers everything. "
                    "C(config) is the default which retrieves basic configuration."
                )
            },
            "folder": {
                "type": "str",
                "required": False,
                "description": "Filter syslog server profiles by folder container."
            },
            "snippet": {
                "type": "str",
                "required": False,
                "description": "Filter syslog server profiles by snippet container."
            },
            "device": {
                "type": "str",
                "required": False,
                "description": "Filter syslog server profiles by device container."
            },
            "exact_match": {
                "type": "bool",
                "required": False,
                "default": False,
                "description": "When True, only return objects defined exactly in the specified container."
            },
            "exclude_folders": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "List of folder names to exclude from results."
            },
            "exclude_snippets": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "List of snippet values to exclude from results."
            },
            "exclude_devices": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "List of device values to exclude from results."
            },
            "transport": {
                "type": "list",
                "elements": "str",
                "required": False,
                "choices": ["UDP", "TCP"],
                "description": "Filter by transport protocol used by the syslog servers."
            },
            "format": {
                "type": "list",
                "elements": "str",
                "required": False,
                "choices": ["BSD", "IETF"],
                "description": "Filter by syslog format used by the servers."
            },
            "provider": {
                "type": "dict",
                "required": True,
                "description": "Authentication credentials.",
                "options": {
                    "client_id": {
                        "type": "str",
                        "required": True,
                        "description": "Client ID for authentication."
                    },
                    "client_secret": {
                        "type": "str",
                        "required": True,
                        "no_log": True,
                        "description": "Client secret for authentication."
                    },
                    "tsg_id": {
                        "type": "str",
                        "required": True,
                        "description": "Tenant Service Group ID."
                    },
                    "log_level": {
                        "type": "str",
                        "required": False,
                        "default": "INFO",
                        "description": "Log level for the SDK."
                    }
                }
            }
        }