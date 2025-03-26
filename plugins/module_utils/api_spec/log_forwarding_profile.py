"""
API Spec for Log Forwarding Profiles module.

This module contains the Ansible argument spec for log forwarding profiles management
in the Strata Cloud Manager (SCM).
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class LogForwardingProfileSpec:
    """
    Defines the Ansible argument spec for log forwarding profiles module.

    This class specifies the parameters and structure for log forwarding profiles module
    in Ansible.
    """

    @staticmethod
    def filter_fields():
        """
        Define the fields for a filter configuration in a log forwarding profile.

        Returns:
            dict: Dictionary containing the filter fields specification
        """
        return {
            "name": {"type": "str", "required": True},
            "filter": {"type": "str", "required": True},
        }

    @staticmethod
    def match_list_fields():
        """
        Define the fields for match list configuration in a log forwarding profile.

        Returns:
            dict: Dictionary containing the match list fields specification
        """
        return {
            "name": {"type": "str", "required": True},
            "action": {
                "type": "str",
                "required": True,
                "choices": ["tagging", "forwarding"],
            },
            "send_http": {"type": "list", "elements": "str", "required": False},
            "send_syslog": {"type": "list", "elements": "str", "required": False},
            "filter": {"type": "str", "required": False},
            "action_desc": {"type": "str", "required": False},
            "log_type": {
                "type": "str",
                "required": True,
                "choices": [
                    "traffic",
                    "threat",
                    "wildfire",
                    "url",
                    "data",
                    "tunnel",
                    "auth",
                    "decryption",
                ],
            },
            "send_to_panorama": {"type": "bool", "required": False},
            "quarantine": {"type": "bool", "required": False},
            "tag": {"type": "list", "elements": "str", "required": False},
        }

    @staticmethod
    def spec():
        """
        Return the complete Ansible argument spec for the log forwarding profiles module.

        Returns:
            dict: Complete argument spec for log forwarding profiles module
        """
        return {
            "name": {"type": "str", "required": True},
            "description": {"type": "str", "required": False},
            "match_list": {
                "type": "list",
                "elements": "dict",
                "required": False,
                "options": LogForwardingProfileSpec.match_list_fields(),
            },
            "enhanced_application_logging": {"type": "bool", "required": False},
            "filter": {
                "type": "list",
                "elements": "dict",
                "required": False,
                "options": LogForwardingProfileSpec.filter_fields(),
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
