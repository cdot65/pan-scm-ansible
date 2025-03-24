"""
API Spec for DNS Security Profile module.

This module contains the Ansible argument spec for DNS security profile management
in the Strata Cloud Manager (SCM).
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class DNSSecurityProfileSpec:
    """
    Defines the Ansible argument spec for DNS security profile module.

    This class specifies the parameters and structure for DNS security profile module
    in Ansible.
    """

    @staticmethod
    def dns_security_category_fields():
        """
        Define the fields for a DNS security category configuration.

        Returns:
            dict: Dictionary containing the DNS security category fields specification
        """
        return {
            "name": {"type": "str", "required": True},
            "action": {
                "type": "str",
                "required": True,
                "choices": ["default", "allow", "block", "sinkhole"],
            },
            "log_level": {
                "type": "str",
                "required": False,
                "choices": [
                    "default",
                    "none",
                    "low",
                    "informational",
                    "medium",
                    "high",
                    "critical",
                ],
            },
            "packet_capture": {
                "type": "str",
                "required": False,
                "choices": ["disable", "single-packet", "extended-capture"],
            },
        }

    @staticmethod
    def botnet_domains_fields():
        """
        Define the fields for botnet domains configuration.

        Returns:
            dict: Dictionary containing the botnet domains fields specification
        """
        return {
            "dns_security_categories": {
                "type": "list",
                "elements": "dict",
                "required": False,
                "options": DNSSecurityProfileSpec.dns_security_category_fields(),
            },
            "sinkhole": {
                "type": "dict",
                "required": False,
                "options": {
                    "ipv4_address": {
                        "type": "str", 
                        "required": True,
                        "choices": ["pan-sinkhole-default-ip", "127.0.0.1"],
                    },
                    "ipv6_address": {
                        "type": "str", 
                        "required": True,
                        "choices": ["::1"],
                    },
                },
            },
            "whitelist": {
                "type": "list",
                "elements": "dict",
                "required": False,
                "options": {
                    "name": {"type": "str", "required": True},
                    "description": {"type": "str", "required": False},
                },
            },
        }

    @staticmethod
    def spec():
        """
        Return the complete Ansible argument spec for the DNS security profile module.

        Returns:
            dict: Complete argument spec for DNS security profile module
        """
        return {
            "name": {"type": "str", "required": True},
            "description": {"type": "str", "required": False},
            "botnet_domains": {
                "type": "dict",
                "required": False,
                "options": DNSSecurityProfileSpec.botnet_domains_fields(),
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