"""
API specification for the SCM IKE crypto profile modules.

This module provides Ansible parameter specifications for IKE crypto profile management
in Strata Cloud Manager.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class IKECryptoProfileSpec:
    """
    Class for defining the module parameter specifications for IKE crypto profiles.

    This specification aligns with the SCM SDK's IKE crypto profile module parameters
    and follows Ansible module parameter standards.
    """

    @classmethod
    def spec(cls):
        """
        Return the module parameter specification for IKE crypto profile.

        Returns:
            dict: The module spec for IKE crypto profile
        """
        return {
            # Name and description
            "name": {
                "type": "str",
                "required": True,
                "description": "The name of the IKE crypto profile",
            },
            "description": {
                "type": "str",
                "required": False,
                "description": "Description of the IKE crypto profile",
            },
            # Algorithm parameters
            "hash": {
                "type": "list",
                "elements": "str",
                "required": False,
                "choices": ["md5", "sha1", "sha256", "sha384", "sha512"],
                "description": "List of hash algorithms to use",
            },
            "encryption": {
                "type": "list",
                "elements": "str",
                "required": False,
                "choices": [
                    "des",
                    "3des",
                    "aes-128-cbc",
                    "aes-192-cbc",
                    "aes-256-cbc",
                    "aes-128-gcm",
                    "aes-256-gcm",
                ],
                "description": "List of encryption algorithms to use",
            },
            "dh_group": {
                "type": "list",
                "elements": "str",
                "required": False,
                "choices": ["group1", "group2", "group5", "group14", "group19", "group20"],
                "description": "List of Diffie-Hellman groups to use",
            },
            # Lifetime configuration
            "lifetime_seconds": {
                "type": "int",
                "required": False,
                "description": "Lifetime in seconds (180-65535)",
            },
            "lifetime_minutes": {
                "type": "int",
                "required": False,
                "description": "Lifetime in minutes (3-65535)",
            },
            "lifetime_hours": {
                "type": "int",
                "required": False,
                "description": "Lifetime in hours (1-65535)",
            },
            "lifetime_days": {
                "type": "int",
                "required": False,
                "description": "Lifetime in days (1-365)",
            },
            # Authentication multiple (reauthentication interval)
            "authentication_multiple": {
                "type": "int",
                "required": False,
                "default": 0,
                "description": "IKEv2 SA reauthentication interval equals authentication-multiple * rekey-lifetime; 0 means reauthentication disabled",
            },
            # Container parameters (mutually exclusive)
            "folder": {
                "type": "str",
                "required": False,
                "description": "The folder in which the resource is defined",
            },
            "snippet": {
                "type": "str",
                "required": False,
                "description": "The snippet in which the resource is defined",
            },
            "device": {
                "type": "str",
                "required": False,
                "description": "The device in which the resource is defined",
            },
            # Provider authentication
            "provider": {
                "type": "dict",
                "required": True,
                "options": {
                    "client_id": {
                        "type": "str",
                        "required": True,
                        "description": "Client ID for authentication",
                    },
                    "client_secret": {
                        "type": "str",
                        "required": True,
                        "no_log": True,
                        "description": "Client secret for authentication",
                    },
                    "tsg_id": {
                        "type": "str",
                        "required": True,
                        "description": "Tenant Service Group ID",
                    },
                    "log_level": {
                        "type": "str",
                        "required": False,
                        "default": "INFO",
                        "description": "Log level for the SDK",
                    },
                },
                "description": "Authentication credentials for SCM",
            },
            # State parameter
            "state": {
                "type": "str",
                "required": True,
                "choices": ["present", "absent"],
                "description": "Desired state of the IKE crypto profile",
            },
        }


class IKECryptoProfileInfoSpec:
    """
    Class for defining the module parameter specifications for IKE crypto profile info.

    This specification is designed for the info module that retrieves information about
    IKE crypto profiles.
    """

    @classmethod
    def spec(cls):
        """
        Return the module parameter specification for IKE crypto profile info.

        Returns:
            dict: The module spec for IKE crypto profile info
        """
        return {
            # Name parameter (optional for info module)
            "name": {
                "type": "str",
                "required": False,
                "description": "The name of the IKE crypto profile to retrieve",
            },
            # Information gathering control
            "gather_subset": {
                "type": "list",
                "elements": "str",
                "default": ["config"],
                "choices": ["all", "config"],
                "description": "Determines which information to gather",
            },
            # Container parameters (mutually exclusive)
            "folder": {
                "type": "str",
                "required": False,
                "description": "Filter profiles by folder container",
            },
            "snippet": {
                "type": "str",
                "required": False,
                "description": "Filter profiles by snippet container",
            },
            "device": {
                "type": "str",
                "required": False,
                "description": "Filter profiles by device container",
            },
            # Filter parameters
            "exact_match": {
                "type": "bool",
                "required": False,
                "default": False,
                "description": "When True, only return objects defined exactly in the specified container",
            },
            "exclude_folders": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "List of folder names to exclude from results",
            },
            "exclude_snippets": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "List of snippet values to exclude from results",
            },
            "exclude_devices": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "List of device values to exclude from results",
            },
            # Provider authentication
            "provider": {
                "type": "dict",
                "required": True,
                "options": {
                    "client_id": {
                        "type": "str",
                        "required": True,
                        "description": "Client ID for authentication",
                    },
                    "client_secret": {
                        "type": "str",
                        "required": True,
                        "no_log": True,
                        "description": "Client secret for authentication",
                    },
                    "tsg_id": {
                        "type": "str",
                        "required": True,
                        "description": "Tenant Service Group ID",
                    },
                    "log_level": {
                        "type": "str",
                        "required": False,
                        "default": "INFO",
                        "description": "Log level for the SDK",
                    },
                },
                "description": "Authentication credentials for SCM",
            },
        }
