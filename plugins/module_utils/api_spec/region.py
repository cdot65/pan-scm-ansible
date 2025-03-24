"""
API Spec for Region module.

This module contains the Ansible argument spec for region management
in the Strata Cloud Manager (SCM).
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class RegionSpec:
    """
    Defines the Ansible argument spec for region module.

    This class specifies the parameters and structure for region module
    in Ansible.
    """

    @staticmethod
    def spec():
        """
        Return the complete Ansible argument spec for the region module.

        Returns:
            dict: Complete argument spec for region module
        """
        return {
            "name": {
                "type": "str",
                "required": True,
                "description": "The name of the region (max 31 chars).",
            },
            "geo_location": {
                "type": "dict",
                "required": False,
                "options": {
                    "latitude": {
                        "type": "float", 
                        "required": True,
                        "description": "The latitudinal position (must be between -90 and 90 degrees)."
                    },
                    "longitude": {
                        "type": "float", 
                        "required": True,
                        "description": "The longitudinal position (must be between -180 and 180 degrees)."
                    },
                },
                "description": "Geographic location of the region with latitude (-90 to 90) and longitude (-180 to 180).",
            },
            "address": {
                "type": "list",
                "elements": "str",
                "required": False,
                "description": "List of IP addresses or networks associated with the region.",
            },
            "folder": {
                "type": "str",
                "required": False,
                "description": "The folder in which the resource is defined (max 64 chars).",
            },
            "snippet": {
                "type": "str",
                "required": False,
                "description": "The snippet in which the resource is defined (max 64 chars).",
            },
            "device": {
                "type": "str",
                "required": False,
                "description": "The device in which the resource is defined (max 64 chars).",
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
            "state": {
                "type": "str",
                "required": True,
                "choices": ["present", "absent"],
            },
        }