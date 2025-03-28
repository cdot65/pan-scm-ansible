"""
API specification for the SCM IKE Gateway modules.

This module provides Ansible parameter specifications for IKE Gateway management
in Strata Cloud Manager.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class IKEGatewaySpec:
    """
    Class for defining the module parameter specifications for IKE Gateways.
    
    This specification aligns with the SCM SDK's IKE Gateway module parameters
    and follows Ansible module parameter standards.
    """

    @classmethod
    def spec(cls):
        """
        Return the module parameter specification for IKE Gateway.

        Returns:
            dict: The module spec for IKE Gateway
        """
        return {
            # Name for the gateway
            "name": {
                "type": "str",
                "required": True,
                "description": "The name of the IKE Gateway",
            },
            
            # Authentication configuration
            "authentication": {
                "type": "dict",
                "required": True,
                "description": "Authentication configuration for the IKE Gateway",
                "options": {
                    "pre_shared_key": {
                        "type": "dict",
                        "required": False,
                        "description": "Pre-shared key authentication configuration",
                        "options": {
                            "key": {
                                "type": "str",
                                "required": True, 
                                "no_log": True,
                                "description": "Pre-shared key for authentication",
                            },
                        },
                    },
                    "certificate": {
                        "type": "dict",
                        "required": False,
                        "description": "Certificate-based authentication configuration",
                        "options": {
                            "allow_id_payload_mismatch": {
                                "type": "bool",
                                "required": False,
                                "description": "Allow ID payload mismatch",
                            },
                            "certificate_profile": {
                                "type": "str",
                                "required": False,
                                "description": "Certificate profile name",
                            },
                            "local_certificate": {
                                "type": "dict",
                                "required": False,
                                "description": "Local certificate configuration",
                            },
                            "strict_validation_revocation": {
                                "type": "bool",
                                "required": False,
                                "description": "Enable strict validation revocation",
                            },
                            "use_management_as_source": {
                                "type": "bool",
                                "required": False,
                                "description": "Use management interface as source",
                            },
                        },
                    },
                },
            },
            
            # Peer identification
            "peer_id": {
                "type": "dict",
                "required": False,
                "description": "Peer identification settings",
                "options": {
                    "type": {
                        "type": "str",
                        "required": True,
                        "choices": ["ipaddr", "keyid", "fqdn", "ufqdn"],
                        "description": "Type of peer ID",
                    },
                    "id": {
                        "type": "str",
                        "required": True,
                        "description": "Peer ID string",
                    },
                },
            },
            
            # Local identification
            "local_id": {
                "type": "dict",
                "required": False,
                "description": "Local identification settings",
                "options": {
                    "type": {
                        "type": "str",
                        "required": True,
                        "choices": ["ipaddr", "keyid", "fqdn", "ufqdn"],
                        "description": "Type of local ID",
                    },
                    "id": {
                        "type": "str",
                        "required": True,
                        "description": "Local ID string",
                    },
                },
            },
            
            # Protocol configuration
            "protocol": {
                "type": "dict",
                "required": True,
                "description": "IKE protocol configuration",
                "options": {
                    "version": {
                        "type": "str",
                        "required": False,
                        "choices": ["ikev2-preferred", "ikev1", "ikev2"],
                        "default": "ikev2-preferred",
                        "description": "IKE protocol version preference",
                    },
                    "ikev1": {
                        "type": "dict",
                        "required": False,
                        "description": "IKEv1 protocol configuration",
                        "options": {
                            "ike_crypto_profile": {
                                "type": "str",
                                "required": False,
                                "description": "IKE Crypto Profile name for IKEv1",
                            },
                            "dpd": {
                                "type": "dict",
                                "required": False,
                                "description": "Dead Peer Detection configuration",
                                "options": {
                                    "enable": {
                                        "type": "bool",
                                        "required": False,
                                        "description": "Enable Dead Peer Detection",
                                    },
                                },
                            },
                        },
                    },
                    "ikev2": {
                        "type": "dict",
                        "required": False,
                        "description": "IKEv2 protocol configuration",
                        "options": {
                            "ike_crypto_profile": {
                                "type": "str",
                                "required": False,
                                "description": "IKE Crypto Profile name for IKEv2",
                            },
                            "dpd": {
                                "type": "dict",
                                "required": False,
                                "description": "Dead Peer Detection configuration",
                                "options": {
                                    "enable": {
                                        "type": "bool",
                                        "required": False,
                                        "description": "Enable Dead Peer Detection",
                                    },
                                },
                            },
                        },
                    },
                },
            },
            
            # Protocol common settings
            "protocol_common": {
                "type": "dict",
                "required": False,
                "description": "Common protocol configuration",
                "options": {
                    "nat_traversal": {
                        "type": "dict",
                        "required": False,
                        "description": "NAT traversal configuration",
                        "options": {
                            "enable": {
                                "type": "bool",
                                "required": False,
                                "description": "Enable NAT traversal",
                            },
                        },
                    },
                    "passive_mode": {
                        "type": "bool",
                        "required": False,
                        "description": "Enable passive mode",
                    },
                    "fragmentation": {
                        "type": "dict",
                        "required": False,
                        "description": "IKE fragmentation configuration",
                        "options": {
                            "enable": {
                                "type": "bool",
                                "required": False,
                                "description": "Enable IKE fragmentation",
                            },
                        },
                    },
                },
            },
            
            # Peer address configuration
            "peer_address": {
                "type": "dict",
                "required": True,
                "description": "Peer address configuration",
                "options": {
                    "ip": {
                        "type": "str",
                        "required": False,
                        "description": "Static IP address of peer gateway",
                    },
                    "fqdn": {
                        "type": "str",
                        "required": False,
                        "description": "FQDN of peer gateway",
                    },
                    "dynamic": {
                        "type": "dict",
                        "required": False,
                        "description": "Dynamic peer address configuration",
                    },
                },
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
                "description": "Desired state of the IKE Gateway",
            },
        }


class IKEGatewayInfoSpec:
    """
    Class for defining the module parameter specifications for IKE Gateway info.
    
    This specification is designed for the info module that retrieves information about
    IKE Gateways.
    """

    @classmethod
    def spec(cls):
        """
        Return the module parameter specification for IKE Gateway info.

        Returns:
            dict: The module spec for IKE Gateway info
        """
        return {
            # Name parameter (optional for info module)
            "name": {
                "type": "str",
                "required": False,
                "description": "The name of the IKE Gateway to retrieve",
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
                "description": "Filter gateways by folder container",
            },
            "snippet": {
                "type": "str",
                "required": False,
                "description": "Filter gateways by snippet container",
            },
            "device": {
                "type": "str",
                "required": False,
                "description": "Filter gateways by device container",
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