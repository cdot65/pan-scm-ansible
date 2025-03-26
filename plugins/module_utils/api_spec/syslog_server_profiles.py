#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Calvin Remsburg (@cdot65)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
API spec for syslog_server_profiles module.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class SyslogServerProfilesSpec:
    """
    API specification for the syslog_server_profiles module.

    This class defines the parameters accepted by the syslog_server_profiles module.
    """

    @staticmethod
    def spec():
        """
        Return the specification for the syslog_server_profiles module.

        :return: Module specification dictionary
        :rtype: dict
        """
        return {
            "name": {
                "type": "str",
                "required": True,
                "description": "The name of the syslog server profile (max 31 chars).",
            },
            "servers": {
                "type": "dict",
                "required": True,
                "description": "Dictionary of server configurations.",
                "options": {
                    "name": {"type": "str", "required": True, "description": "Syslog server name."},
                    "server": {
                        "type": "str",
                        "required": True,
                        "description": "Syslog server address.",
                    },
                    "transport": {
                        "type": "str",
                        "required": True,
                        "choices": ["UDP", "TCP"],
                        "description": "Transport protocol for the syslog server.",
                    },
                    "port": {
                        "type": "int",
                        "required": True,
                        "description": "Syslog server port (1-65535).",
                    },
                    "format": {
                        "type": "str",
                        "required": True,
                        "choices": ["BSD", "IETF"],
                        "description": "Syslog format.",
                    },
                    "facility": {
                        "type": "str",
                        "required": True,
                        "choices": [
                            "LOG_USER",
                            "LOG_LOCAL0",
                            "LOG_LOCAL1",
                            "LOG_LOCAL2",
                            "LOG_LOCAL3",
                            "LOG_LOCAL4",
                            "LOG_LOCAL5",
                            "LOG_LOCAL6",
                            "LOG_LOCAL7",
                        ],
                        "description": "Syslog facility.",
                    },
                },
            },
            "format": {
                "type": "dict",
                "required": False,
                "description": "Format settings for different log types.",
                "options": {
                    "escaping": {
                        "type": "dict",
                        "required": False,
                        "description": "Character escaping configuration.",
                        "options": {
                            "escape_character": {
                                "type": "str",
                                "required": False,
                                "description": "Escape sequence delimiter (max length: 1).",
                            },
                            "escaped_characters": {
                                "type": "str",
                                "required": False,
                                "description": "Characters to be escaped without spaces (max length: 255).",
                            },
                        },
                    },
                    "traffic": {
                        "type": "str",
                        "required": False,
                        "description": "Format for traffic logs.",
                    },
                    "threat": {
                        "type": "str",
                        "required": False,
                        "description": "Format for threat logs.",
                    },
                    "wildfire": {
                        "type": "str",
                        "required": False,
                        "description": "Format for wildfire logs.",
                    },
                    "url": {
                        "type": "str",
                        "required": False,
                        "description": "Format for URL logs.",
                    },
                    "data": {
                        "type": "str",
                        "required": False,
                        "description": "Format for data logs.",
                    },
                    "gtp": {
                        "type": "str",
                        "required": False,
                        "description": "Format for GTP logs.",
                    },
                    "sctp": {
                        "type": "str",
                        "required": False,
                        "description": "Format for SCTP logs.",
                    },
                    "tunnel": {
                        "type": "str",
                        "required": False,
                        "description": "Format for tunnel logs.",
                    },
                    "auth": {
                        "type": "str",
                        "required": False,
                        "description": "Format for authentication logs.",
                    },
                    "userid": {
                        "type": "str",
                        "required": False,
                        "description": "Format for user ID logs.",
                    },
                    "iptag": {
                        "type": "str",
                        "required": False,
                        "description": "Format for IP tag logs.",
                    },
                    "decryption": {
                        "type": "str",
                        "required": False,
                        "description": "Format for decryption logs.",
                    },
                    "config": {
                        "type": "str",
                        "required": False,
                        "description": "Format for configuration logs.",
                    },
                    "system": {
                        "type": "str",
                        "required": False,
                        "description": "Format for system logs.",
                    },
                    "globalprotect": {
                        "type": "str",
                        "required": False,
                        "description": "Format for GlobalProtect logs.",
                    },
                    "hip_match": {
                        "type": "str",
                        "required": False,
                        "description": "Format for HIP match logs.",
                    },
                    "correlation": {
                        "type": "str",
                        "required": False,
                        "description": "Format for correlation logs.",
                    },
                },
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
                "description": "Authentication credentials.",
                "options": {
                    "client_id": {
                        "type": "str",
                        "required": True,
                        "description": "Client ID for authentication.",
                    },
                    "client_secret": {
                        "type": "str",
                        "required": True,
                        "no_log": True,
                        "description": "Client secret for authentication.",
                    },
                    "tsg_id": {
                        "type": "str",
                        "required": True,
                        "description": "Tenant Service Group ID.",
                    },
                    "log_level": {
                        "type": "str",
                        "required": False,
                        "default": "INFO",
                        "description": "Log level for the SDK.",
                    },
                },
            },
            "state": {
                "type": "str",
                "required": True,
                "choices": ["present", "absent"],
                "description": "Desired state of the syslog server profile.",
            },
        }
