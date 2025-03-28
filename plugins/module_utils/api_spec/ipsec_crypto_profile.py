"""
API specification for the SCM IPsec crypto profile modules.

This module provides Ansible parameter specifications for IPsec crypto profile management
in Strata Cloud Manager.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class IPsecCryptoProfileSpec:
    """
    Class for defining the module parameter specifications for IPsec crypto profiles.
    
    This specification aligns with the SCM SDK's IPsec crypto profile module parameters
    and follows Ansible module parameter standards.
    """

    @classmethod
    def spec(cls):
        """
        Return the module parameter specification for IPsec crypto profile.

        Returns:
            dict: The module spec for IPsec crypto profile
        """
        return {
            # Name and description
            "name": {
                "type": "str",
                "required": True,
                "description": "The name of the IPsec crypto profile",
                "pattern": r"^[0-9a-zA-Z._\-]+$",
                "max_length": 31,
            },
            "description": {
                "type": "str",
                "required": False,
                "description": "Description of the IPsec crypto profile",
            },

            # ESP parameters
            "esp": {
                "type": "dict",
                "required": False,
                "options": {
                    "encryption": {
                        "type": "list",
                        "elements": "str",
                        "required": False,
                        "choices": ["des", "3des", "aes-128-cbc", "aes-192-cbc", "aes-256-cbc", "aes-128-gcm", "aes-256-gcm", "null"],
                        "description": "List of ESP encryption algorithms to use",
                    },
                    "authentication": {
                        "type": "list",
                        "elements": "str",
                        "required": False,
                        "choices": ["md5", "sha1", "sha256", "sha384", "sha512", "none"],
                        "description": "List of ESP authentication algorithms to use",
                    },
                },
                "description": "ESP protocol configuration",
            },
            
            # AH parameters
            "ah": {
                "type": "dict",
                "required": False,
                "options": {
                    "authentication": {
                        "type": "list",
                        "elements": "str",
                        "required": False,
                        "choices": ["md5", "sha1", "sha256", "sha384", "sha512"],
                        "description": "List of AH authentication algorithms to use",
                    },
                },
                "description": "AH protocol configuration",
            },
            
            # DH group
            "dh_group": {
                "type": "str",
                "required": False,
                "default": "group2",  # Default value to match the SDK
                "choices": ["no-pfs", "group1", "group2", "group5", "group14", "group19", "group20"],
                "description": "Diffie-Hellman group to use for PFS (default: group2)",
            },

            # Lifetime configuration
            "lifetime": {
                "type": "dict",
                "required": False,
                "options": {
                    "seconds": {
                        "type": "int",
                        "required": False,
                        "description": "Lifetime in seconds (180-65535)",
                        "min_value": 180,
                        "max_value": 65535,
                    },
                    "minutes": {
                        "type": "int",
                        "required": False,
                        "description": "Lifetime in minutes (3-65535)",
                        "min_value": 3,
                        "max_value": 65535,
                    },
                    "hours": {
                        "type": "int",
                        "required": False,
                        "description": "Lifetime in hours (1-65535)",
                        "min_value": 1,
                        "max_value": 65535,
                    },
                    "days": {
                        "type": "int",
                        "required": False,
                        "description": "Lifetime in days (1-365)",
                        "min_value": 1,
                        "max_value": 365,
                    },
                },
                "description": "SA lifetime configuration",
            },

            # Lifesize configuration
            "lifesize": {
                "type": "dict",
                "required": False,
                "options": {
                    "kb": {
                        "type": "int",
                        "required": False,
                        "description": "Lifesize limit in kilobytes",
                        "min_value": 1,
                        "max_value": 65535,
                    },
                    "mb": {
                        "type": "int",
                        "required": False,
                        "description": "Lifesize limit in megabytes",
                        "min_value": 1,
                        "max_value": 65535,
                    },
                    "gb": {
                        "type": "int",
                        "required": False,
                        "description": "Lifesize limit in gigabytes",
                        "min_value": 1,
                        "max_value": 65535,
                    },
                    "tb": {
                        "type": "int",
                        "required": False,
                        "description": "Lifesize limit in terabytes",
                        "min_value": 1,
                        "max_value": 65535,
                    },
                },
                "description": "SA lifesize configuration",
            },

            # Container parameters (mutually exclusive)
            "folder": {
                "type": "str",
                "required": False,
                "description": "The folder in which the resource is defined",
                "pattern": r"^[a-zA-Z\d\-_. ]+$",
                "max_length": 64,
            },
            "snippet": {
                "type": "str",
                "required": False,
                "description": "The snippet in which the resource is defined",
                "pattern": r"^[a-zA-Z\d\-_. ]+$",
                "max_length": 64,
            },
            "device": {
                "type": "str",
                "required": False,
                "description": "The device in which the resource is defined",
                "pattern": r"^[a-zA-Z\d\-_. ]+$",
                "max_length": 64,
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
                "description": "Desired state of the IPsec crypto profile",
            },
        }


class IPsecCryptoProfileInfoSpec:
    """
    Class for defining the module parameter specifications for IPsec crypto profile info.
    
    This specification is designed for the info module that retrieves information about
    IPsec crypto profiles.
    """

    @classmethod
    def spec(cls):
        """
        Return the module parameter specification for IPsec crypto profile info.

        Returns:
            dict: The module spec for IPsec crypto profile info
        """
        return {
            # Filter parameters
            "name": {
                "type": "str",
                "required": False,
                "description": "Name of the IPsec crypto profile to retrieve",
                "pattern": r"^[0-9a-zA-Z._\-]+$",
            },
            "id": {
                "type": "str",
                "required": False,
                "description": "ID of the IPsec crypto profile to retrieve",
            },
            "folder": {
                "type": "str",
                "required": False,
                "description": "The folder in which the resource is defined",
                "pattern": r"^[a-zA-Z\d\-_. ]+$",
            },
            "snippet": {
                "type": "str",
                "required": False,
                "description": "The snippet in which the resource is defined",
                "pattern": r"^[a-zA-Z\d\-_. ]+$",
            },
            "device": {
                "type": "str",
                "required": False,
                "description": "The device in which the resource is defined",
                "pattern": r"^[a-zA-Z\d\-_. ]+$",
            },
            "exact_match": {
                "type": "bool",
                "required": False,
                "default": False,
                "description": "Whether to perform an exact match on container parameters",
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