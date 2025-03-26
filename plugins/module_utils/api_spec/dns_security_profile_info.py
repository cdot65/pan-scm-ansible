"""
API Spec for DNS Security Profile Info module.

This module contains the Ansible argument spec for DNS security profile info
in the Strata Cloud Manager (SCM).
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class DNSSecurityProfileInfoSpec:
    """
    Defines the Ansible argument spec for DNS security profile info module.

    This class specifies the parameters and structure for DNS security profile info module
    in Ansible.
    """

    @staticmethod
    def spec():
        """
        Return the complete Ansible argument spec for the DNS security profile info module.

        Returns:
            dict: Complete argument spec for DNS security profile info module
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
            "dns_security_categories": {
                "type": "list",
                "elements": "str",
                "required": False,
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
