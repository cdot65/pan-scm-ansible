# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.

from typing import Any, Dict


class DecryptionProfileSpec:
    """
    API specifications for SCM Ansible modules.

    This class provides standardized specifications for SCM (Strata Cloud Manager)
    related Ansible modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def spec() -> Dict[str, Any]:
        """
        Returns Ansible module spec for decryption profile objects.

        This method defines the structure and requirements for decryption profile related
        parameters in SCM modules, aligning with the Pydantic models in the SCM SDK.

        Returns:
            Dict[str, Any]: A dictionary containing the module specification with
                        parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type="str",
                required=True,
                description="The name of the decryption profile (max 63 chars, must match pattern: ^[a-zA-Z0-9][a-zA-Z0-9_\\-. ]*$).",
            ),
            description=dict(
                type="str",
                required=False,
                description="Description of the decryption profile (max 1023 chars).",
            ),
            ssl_forward_proxy=dict(
                type="dict",
                required=False,
                description="SSL Forward Proxy settings.",
                options=dict(
                    enabled=dict(
                        type="bool",
                        required=False,
                        default=False,
                        description="Enable SSL Forward Proxy.",
                    ),
                    block_unsupported_cipher=dict(
                        type="bool",
                        required=False,
                        default=False,
                        description="Block sessions with unsupported ciphers.",
                    ),
                    block_unknown_cert=dict(
                        type="bool",
                        required=False,
                        default=False,
                        description="Block sessions with unknown certificates.",
                    ),
                    block_expired_cert=dict(
                        type="bool",
                        required=False,
                        default=False,
                        description="Block sessions with expired certificates.",
                    ),
                    block_timeoff_cert=dict(
                        type="bool",
                        required=False,
                        default=False,
                        description="Block sessions with certificates not yet valid.",
                    ),
                    block_untrusted_issuer=dict(
                        type="bool",
                        required=False,
                        default=False,
                        description="Block sessions with untrusted issuer certificates.",
                    ),
                    block_unknown_status=dict(
                        type="bool",
                        required=False,
                        default=False,
                        description="Block sessions with certificates that have unknown status.",
                    ),
                ),
            ),
            ssl_inbound_inspection=dict(
                type="dict",
                required=False,
                description="SSL Inbound Inspection settings.",
                options=dict(
                    enabled=dict(
                        type="bool",
                        required=False,
                        default=False,
                        description="Enable SSL Inbound Inspection.",
                    ),
                ),
            ),
            ssl_no_proxy=dict(
                type="dict",
                required=False,
                description="SSL No Proxy settings.",
                options=dict(
                    enabled=dict(
                        type="bool",
                        required=False,
                        default=False,
                        description="Enable SSL No Proxy.",
                    ),
                    block_session_expired_cert=dict(
                        type="bool",
                        required=False,
                        default=False,
                        description="Block sessions with expired certificates.",
                    ),
                    block_session_untrusted_issuer=dict(
                        type="bool",
                        required=False,
                        default=False,
                        description="Block sessions with untrusted issuer certificates.",
                    ),
                ),
            ),
            ssl_protocol_settings=dict(
                type="dict",
                required=False,
                description="SSL Protocol settings.",
                options=dict(
                    min_version=dict(
                        type="str",
                        required=False,
                        choices=["tls1-0", "tls1-1", "tls1-2", "tls1-3"],
                        default="tls1-0",
                        description="Minimum TLS version to support.",
                    ),
                    max_version=dict(
                        type="str",
                        required=False,
                        choices=["tls1-0", "tls1-1", "tls1-2", "tls1-3"],
                        default="tls1-3",
                        description="Maximum TLS version to support.",
                    ),
                    keyxchg_algorithm=dict(
                        type="list",
                        elements="str",
                        required=False,
                        choices=["dhe", "ecdhe"],
                        description="Key exchange algorithms to allow.",
                    ),
                    encrypt_algorithm=dict(
                        type="list",
                        elements="str",
                        required=False,
                        choices=[
                            "rc4",
                            "rc4-md5",
                            "aes-128-cbc",
                            "aes-128-gcm",
                            "aes-256-cbc",
                            "aes-256-gcm",
                            "3des",
                        ],
                        description="Encryption algorithms to allow.",
                    ),
                    auth_algorithm=dict(
                        type="list",
                        elements="str",
                        required=False,
                        choices=["sha1", "sha256", "sha384"],
                        description="Authentication algorithms to allow.",
                    ),
                ),
            ),
            folder=dict(
                type="str",
                required=False,
                description="The folder in which the profile is defined (max 64 chars).",
            ),
            snippet=dict(
                type="str",
                required=False,
                description="The snippet in which the profile is defined (max 64 chars).",
            ),
            device=dict(
                type="str",
                required=False,
                description="The device in which the profile is defined (max 64 chars).",
            ),
            provider=dict(
                type="dict",
                required=True,
                description="Authentication credentials for connecting to SCM.",
                options=dict(
                    client_id=dict(
                        type="str",
                        required=True,
                        description="Client ID for authentication with SCM.",
                    ),
                    client_secret=dict(
                        type="str",
                        required=True,
                        no_log=True,
                        description="Client secret for authentication with SCM.",
                    ),
                    tsg_id=dict(
                        type="str",
                        required=True,
                        description="Tenant Service Group ID.",
                    ),
                    log_level=dict(
                        type="str",
                        required=False,
                        default="INFO",
                        description="Log level for the SDK (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
                    ),
                ),
            ),
            state=dict(
                type="str",
                choices=["present", "absent"],
                required=True,
                description="Desired state of the decryption profile.",
            ),
        )
