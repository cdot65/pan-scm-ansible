"""
API Spec for HTTP Server Profiles Info module.

This module contains the Ansible argument spec for HTTP server profiles info
in the Strata Cloud Manager (SCM).
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class HTTPServerProfilesInfoSpec:
    """
    Defines the Ansible argument spec for HTTP server profiles info module.

    This class specifies the parameters and structure for HTTP server profiles info module
    in Ansible.
    """

    @staticmethod
    def spec():
        """
        Return the complete Ansible argument spec for the HTTP server profiles info module.

        Returns:
            dict: Complete argument spec for HTTP server profiles info module
        """
        return {
            "name": {"type": "str", "required": False},
            "gather_subset": {
                "type": "list",
                "elements": "str",
                "default": ["config"],
                "choices": ["all", "config"],
            },
            "folder": {"type": "str", "required": False},
            "snippet": {"type": "str", "required": False},
            "device": {"type": "str", "required": False},
            "exact_match": {"type": "bool", "required": False, "default": False},
            "exclude_folders": {"type": "list", "elements": "str", "required": False},
            "exclude_snippets": {"type": "list", "elements": "str", "required": False},
            "exclude_devices": {"type": "list", "elements": "str", "required": False},
            "protocol": {
                "type": "list",
                "elements": "str",
                "required": False,
                "choices": ["HTTP", "HTTPS"],
            },
            "tag_registration": {"type": "bool", "required": False},
            "provider": {
                "type": "dict",
                "required": True,
                "options": {
                    "client_id": {"type": "str", "required": True},
                    "client_secret": {"type": "str", "required": True, "no_log": True},
                    "tsg_id": {"type": "str", "required": True},
                    "log_level": {"type": "str", "required": False, "default": "INFO"},
                },
            },
        }