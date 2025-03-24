"""
API Spec for HTTP Server Profiles module.

This module contains the Ansible argument spec for HTTP server profiles management
in the Strata Cloud Manager (SCM).
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class HTTPServerProfilesSpec:
    """
    Defines the Ansible argument spec for HTTP server profiles module.

    This class specifies the parameters and structure for HTTP server profiles module
    in Ansible.
    """

    @staticmethod
    def server_fields():
        """
        Define the fields for a server configuration in an HTTP server profile.

        Returns:
            dict: Dictionary containing the server fields specification
        """
        return {
            "name": {"type": "str", "required": True},
            "address": {"type": "str", "required": True},
            "protocol": {
                "type": "str",
                "required": True,
                "choices": ["HTTP", "HTTPS"],
            },
            "port": {"type": "int", "required": True},
            "tls_version": {
                "type": "str",
                "required": False,
                "choices": ["1.0", "1.1", "1.2", "1.3"],
            },
            "certificate_profile": {"type": "str", "required": False},
            "http_method": {
                "type": "str",
                "required": True,
                "choices": ["GET", "POST", "PUT", "DELETE"],
            },
        }

    @staticmethod
    def format_fields():
        """
        Define the fields for payload format configuration in an HTTP server profile.

        Returns:
            dict: Dictionary containing the format fields specification
        """
        # The exact fields in the payload format model are not fully specified in SDK
        # This is a simple placeholder that allows any dictionary structure
        return {"type": "dict", "required": False}

    @staticmethod
    def spec():
        """
        Return the complete Ansible argument spec for the HTTP server profiles module.

        Returns:
            dict: Complete argument spec for HTTP server profiles module
        """
        return {
            "name": {"type": "str", "required": True},
            "server": {
                "type": "list",
                "elements": "dict",
                "required": False,
                "options": HTTPServerProfilesSpec.server_fields(),
            },
            "tag_registration": {"type": "bool", "required": False},
            "description": {"type": "str", "required": False},
            "format": {
                "type": "dict",
                "required": False,
            },
            "folder": {"type": "str", "required": False},
            "snippet": {"type": "str", "required": False},
            "device": {"type": "str", "required": False},
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
            "state": {
                "type": "str",
                "required": True,
                "choices": ["present", "absent"],
            },
        }
