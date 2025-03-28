"""
API specification for the SCM agent versions module.

This module provides Ansible parameter specifications for agent versions management in SCM.
The agent versions API endpoint provides read-only access to available agent versions
for GlobalProtect, NGFWs, SD-WAN and CPE devices in Strata Cloud Manager.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class AgentVersionsSpec:
    """
    Class for defining the module parameter specifications for agent versions.

    This specification aligns with the SCM SDK's agent_versions module parameters
    and follows Ansible module parameter standards.
    """

    @classmethod
    def spec(cls):
        """
        Return the module parameter specification for agent versions.

        Returns:
            dict: The module spec for agent versions
        """
        return {
            # Basic query parameters
            "name": {
                "type": "str",
                "required": False,
                "description": "The name of a specific agent to filter by",
            },
            "version": {
                "type": "str",
                "required": False,
                "description": "The specific version to filter by",
            },
            # Core classification parameters
            "type": {
                "type": "str",
                "required": False,
                "choices": ["prisma_access", "ngfw", "sdwan", "cpe"],
                "description": "The type of agent to filter by",
            },
            "status": {
                "type": "str",
                "required": False,
                "choices": ["recommended", "current", "deprecated", "obsolete"],
                "description": "The status of agent versions to filter by",
            },
            # Additional filter parameters
            "platform": {
                "type": "str",
                "required": False,
                "description": "The platform to filter by (e.g., 'linux_x86_64')",
            },
            "features_enabled": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "List of features that must be enabled in the agent versions",
            },
            # Metadata parameters
            "release_date": {
                "type": "str",
                "required": False,
                "description": "Filter by release date (format: YYYY-MM-DD)",
            },
            "end_of_support_date": {
                "type": "str",
                "required": False,
                "description": "Filter by end of support date (format: YYYY-MM-DD)",
            },
            "release_notes_url": {
                "type": "str",
                "required": False,
                "description": "Release notes URL for the agent version",
            },
            # Provider authentication
            "provider": {
                "type": "dict",
                "required": True,
                "options": {
                    "client_id": {
                        "type": "str",
                        "required": True,
                        "description": "Client ID for authentication to SCM",
                    },
                    "client_secret": {
                        "type": "str",
                        "required": True,
                        "no_log": True,
                        "description": "Client secret for authentication to SCM",
                    },
                    "tsg_id": {
                        "type": "str",
                        "required": True,
                        "description": "Tenant Service Group ID for SCM",
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
            # Control parameters
            "gather_subset": {
                "type": "list",
                "elements": "str",
                "default": ["config"],
                "choices": ["all", "config"],
                "description": "Determines which information to gather about agent versions",
            },
            "exact_match": {
                "type": "bool",
                "required": False,
                "default": False,
                "description": "When True, require exact matches on filter criteria",
            },
            "exact_version": {
                "type": "bool",
                "required": False,
                "default": False,
                "description": "When True, require exact version match rather than prefix match",
            },
            # State parameter (required for CUD operations)
            "state": {
                "type": "str",
                "required": True,
                "choices": ["present", "absent"],
                "description": "Desired state of the agent version configuration",
            },
            # Test mode for CI/CD environments
            "testmode": {
                "type": "bool",
                "required": False,
                "default": False,
                "description": "Enable test mode for CI/CD environments (no API calls)",
            },
            # For test mode data generation
            "test_timestamp": {
                "type": "str",
                "required": False,
                "description": "Timestamp to use for test mode data generation",
            },
        }


class AgentVersionsInfoSpec:
    """
    Class for defining the module parameter specifications for agent versions info.

    This specification is designed for the info module variant which is focused
    on retrieving information about agent versions with various filtering options.
    """

    @classmethod
    def spec(cls):
        """
        Return the module parameter specification for agent versions info.

        Returns:
            dict: The module spec for agent versions info
        """
        return {
            # Basic query parameters
            "name": {
                "type": "str",
                "required": False,
                "description": "The name of a specific agent to retrieve information about",
            },
            "version": {
                "type": "str",
                "required": False,
                "description": "The specific version to retrieve information about",
            },
            # List filter parameters (note: using lists for multi-value filtering)
            "type": {
                "type": "list",
                "elements": "str",
                "required": False,
                "choices": ["prisma_access", "ngfw", "sdwan", "cpe"],
                "description": "Filter agent versions by their type",
            },
            "status": {
                "type": "list",
                "elements": "str",
                "required": False,
                "choices": ["recommended", "current", "deprecated", "obsolete"],
                "description": "Filter agent versions by their status",
            },
            "platform": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "Filter agent versions by platform compatibility",
            },
            "features": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "Filter agent versions by supported features",
            },
            # Information gathering control
            "gather_subset": {
                "type": "list",
                "elements": "str",
                "default": ["config"],
                "choices": ["all", "config"],
                "description": "Determines which information to gather about agent versions",
            },
            # Provider authentication
            "provider": {
                "type": "dict",
                "required": True,
                "options": {
                    "client_id": {
                        "type": "str",
                        "required": True,
                        "description": "Client ID for authentication to SCM",
                    },
                    "client_secret": {
                        "type": "str",
                        "required": True,
                        "no_log": True,
                        "description": "Client secret for authentication to SCM",
                    },
                    "tsg_id": {
                        "type": "str",
                        "required": True,
                        "description": "Tenant Service Group ID for SCM",
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
            # Additional filter behaviors
            "exact_match": {
                "type": "bool",
                "required": False,
                "default": False,
                "description": "When True, only return objects with exact matching criteria",
            },
            "exact_version": {
                "type": "bool",
                "required": False,
                "default": False,
                "description": "When True, require exact version match rather than prefix match",
            },
            # Test mode for CI/CD environments
            "testmode": {
                "type": "bool",
                "required": False,
                "default": False,
                "description": "Enable test mode for CI/CD environments (no API calls)",
            },
            # For test mode data generation
            "test_timestamp": {
                "type": "str",
                "required": False,
                "description": "Timestamp to use for test mode data generation",
            },
        }
