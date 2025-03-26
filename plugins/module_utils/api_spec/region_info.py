"""
API Spec for Region Info module.

This module contains the Ansible argument spec for region information retrieval
in the Strata Cloud Manager (SCM).
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class RegionInfoSpec:
    """
    Defines the Ansible argument spec for region info module.

    This class specifies the parameters and structure for region info module
    in Ansible.
    """

    @staticmethod
    def spec():
        """
        Return the complete Ansible argument spec for the region info module.

        Returns:
            dict: Complete argument spec for region info module
        """
        return {
            "name": {
                "type": "str",
                "required": False,
                "description": "The name of a specific region to retrieve.",
            },
            "gather_subset": {
                "type": "list",
                "elements": "str",
                "default": ["config"],
                "choices": ["all", "config"],
                "description": "Determines which information to gather about regions.",
            },
            "folder": {
                "type": "str",
                "required": False,
                "description": "Filter regions by folder container.",
            },
            "snippet": {
                "type": "str",
                "required": False,
                "description": "Filter regions by snippet container.",
            },
            "device": {
                "type": "str",
                "required": False,
                "description": "Filter regions by device container.",
            },
            "exact_match": {
                "type": "bool",
                "required": False,
                "default": False,
                "description": "When True, only return objects defined exactly in the specified container.",
            },
            "exclude_folders": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "List of folder names to exclude from results.",
            },
            "exclude_snippets": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "List of snippet values to exclude from results.",
            },
            "exclude_devices": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "List of device values to exclude from results.",
            },
            "geo_location": {
                "type": "dict",
                "required": False,
                "options": {
                    "latitude": {
                        "type": "dict",
                        "required": False,
                        "options": {
                            "min": {
                                "type": "float",
                                "required": True,
                                "description": "Minimum latitude value (range: -90 to 90).",
                            },
                            "max": {
                                "type": "float",
                                "required": True,
                                "description": "Maximum latitude value (range: -90 to 90).",
                            },
                        },
                    },
                    "longitude": {
                        "type": "dict",
                        "required": False,
                        "options": {
                            "min": {
                                "type": "float",
                                "required": True,
                                "description": "Minimum longitude value (range: -180 to 180).",
                            },
                            "max": {
                                "type": "float",
                                "required": True,
                                "description": "Maximum longitude value (range: -180 to 180).",
                            },
                        },
                    },
                },
                "description": "Filter by geographic location range.",
            },
            "addresses": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "Filter by addresses included in regions (e.g., ['10.0.0.0/8']).",
            },
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
