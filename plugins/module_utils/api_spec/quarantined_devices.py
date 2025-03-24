"""
API Spec for Quarantined Devices module.

This module contains the Ansible argument spec for quarantined devices management
in the Strata Cloud Manager (SCM).
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class QuarantinedDevicesSpec:
    """
    Defines the Ansible argument spec for quarantined devices module.

    This class specifies the parameters and structure for quarantined devices module
    in Ansible.
    """

    @staticmethod
    def spec():
        """
        Return the complete Ansible argument spec for the quarantined devices module.

        Returns:
            dict: Complete argument spec for quarantined devices module
        """
        return {
            "host_id": {"type": "str", "required": True},
            "serial_number": {"type": "str", "required": False},
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


class QuarantinedDevicesInfoSpec:
    """
    Defines the Ansible argument spec for quarantined devices info module.

    This class specifies the parameters and structure for quarantined devices info module
    in Ansible.
    """

    @staticmethod
    def spec():
        """
        Return the complete Ansible argument spec for the quarantined devices info module.

        Returns:
            dict: Complete argument spec for quarantined devices info module
        """
        return {
            "host_id": {"type": "str", "required": False},
            "serial_number": {"type": "str", "required": False},
            "gather_subset": {
                "type": "list",
                "elements": "str",
                "default": ["config"],
                "choices": ["all", "config"],
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
