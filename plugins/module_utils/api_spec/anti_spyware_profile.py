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


class AntiSpywareProfileSpec:
    """
    API specifications for SCM Ansible modules.

    This class provides standardized specifications for SCM (Strata Cloud Manager)
    related Ansible modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def spec() -> Dict[str, Any]:
        """
        Returns Ansible module spec for anti-spyware profile objects.

        This method defines the structure and requirements for anti-spyware profile related
        parameters in SCM modules, aligning with the Pydantic models in the SCM SDK.

        Returns:
            Dict[str, Any]: A dictionary containing the module specification with
                         parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type="str",
                required=True,
                description="The name of the anti-spyware profile (max 63 chars, must match pattern: ^[a-zA-Z0-9][a-zA-Z0-9_\\-. ]*$).",
            ),
            description=dict(
                type="str",
                required=False,
                description="Description of the anti-spyware profile (max 1023 chars).",
            ),
            cloud_inline_analysis=dict(
                type="bool",
                required=False,
                default=False,
                description="Enable or disable cloud inline analysis capabilities.",
            ),
            inline_exception_edl_url=dict(
                type="list",
                elements="str",
                required=False,
                description="List of EDL URLs to be excluded from cloud inline analysis.",
            ),
            inline_exception_ip_address=dict(
                type="list",
                elements="str",
                required=False,
                description="List of IP addresses to be excluded from cloud inline analysis.",
            ),
            mica_engine_spyware_enabled=dict(
                type="list",
                elements="dict",
                required=False,
                description="List of MICA engine spyware detector configurations.",
                options=dict(
                    name=dict(
                        type="str",
                        required=True,
                        description="Name of the MICA engine spyware detector.",
                    ),
                    inline_policy_action=dict(
                        type="str",
                        required=False,
                        choices=[
                            "alert",
                            "allow",
                            "drop",
                            "reset-both",
                            "reset-client",
                            "reset-server",
                        ],
                        default="alert",
                        description="Action to take when the MICA engine detects spyware.",
                    ),
                ),
            ),
            rules=dict(
                type="list",
                elements="dict",
                required=True,
                description="List of anti-spyware rules to apply. At least one rule is required.",
                options=dict(
                    name=dict(
                        type="str",
                        required=True,
                        description="Name of the rule.",
                    ),
                    severity=dict(
                        type="list",
                        elements="str",
                        required=True,
                        choices=[
                            "critical",
                            "high",
                            "medium",
                            "low",
                            "informational",
                            "any",
                        ],
                        description="List of severity levels this rule applies to.",
                    ),
                    category=dict(
                        type="str",
                        required=True,
                        description="Category for the rule (e.g., spyware, dns-security, command-and-control).",
                    ),
                    threat_name=dict(
                        type="str",
                        required=True,
                        description="Specific threat name to match (min length: 4 chars).",
                    ),
                    packet_capture=dict(
                        type="str",
                        required=False,
                        choices=["disable", "single-packet", "extended-capture"],
                        description="Type of packet capture to perform when rule matches.",
                    ),
                    action=dict(
                        type="str",
                        required=True,
                        choices=[
                            "alert",
                            "allow",
                            "drop",
                            "reset-both",
                            "reset-client",
                            "reset-server",
                        ],
                        description="Action to take when the rule matches. This is converted to an action object in the API.",
                    ),
                ),
            ),
            threat_exception=dict(
                type="list",
                elements="dict",
                required=False,
                description="List of exceptions to the threat rules.",
                options=dict(
                    name=dict(
                        type="str",
                        required=True,
                        description="Name of the threat exception.",
                    ),
                    packet_capture=dict(
                        type="str",
                        required=True,
                        choices=["disable", "single-packet", "extended-capture"],
                        description="Type of packet capture to perform for this exception.",
                    ),
                    exempt_ip=dict(
                        type="list",
                        elements="dict",
                        required=False,
                        description="List of IP addresses to exempt from this rule.",
                        options=dict(
                            name=dict(
                                type="str",
                                required=True,
                                description="Exempt IP address or range.",
                            ),
                        ),
                    ),
                    notes=dict(
                        type="str",
                        required=False,
                        description="Additional notes for the threat exception.",
                    ),
                    action=dict(
                        type="str",
                        required=True,
                        choices=[
                            "alert",
                            "allow",
                            "drop",
                            "reset-both",
                            "reset-client",
                            "reset-server",
                        ],
                        description="Action to take for excepted traffic.",
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
                description="Desired state of the anti-spyware profile.",
            ),
        )
