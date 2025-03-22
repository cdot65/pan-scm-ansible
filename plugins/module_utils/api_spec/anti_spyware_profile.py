# -*- coding: utf-8 -*-

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
        """Returns Ansible module spec for anti-spyware profile objects."""
        return dict(
            name=dict(
                type="str",
                required=True,
            ),
            description=dict(
                type="str",
                required=False,
            ),
            cloud_inline_analysis=dict(
                type="bool",
                required=False,
                default=False,
            ),
            inline_exception_edl_url=dict(
                type="list",
                elements="str",
                required=False,
            ),
            inline_exception_ip_address=dict(
                type="list",
                elements="str",
                required=False,
            ),
            mica_engine_spyware_enabled=dict(
                type="list",
                elements="dict",
                required=False,
                options=dict(
                    name=dict(
                        type="str",
                        required=True,
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
                    ),
                ),
            ),
            rules=dict(
                type="list",
                elements="dict",
                required=True,
                options=dict(
                    name=dict(
                        type="str",
                        required=True,
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
                    ),
                    category=dict(
                        type="str",
                        required=True,
                    ),
                    threat_name=dict(
                        type="str",
                        required=False,
                    ),
                    packet_capture=dict(
                        type="str",
                        required=False,
                        choices=["disable", "single-packet", "extended-capture"],
                    ),
                ),
            ),
            threat_exception=dict(
                type="list",
                elements="dict",
                required=False,
                options=dict(
                    name=dict(
                        type="str",
                        required=True,
                    ),
                    packet_capture=dict(
                        type="str",
                        required=True,
                        choices=["disable", "single-packet", "extended-capture"],
                    ),
                    exempt_ip=dict(
                        type="list",
                        elements="dict",
                        required=False,
                        options=dict(
                            name=dict(
                                type="str",
                                required=True,
                            ),
                        ),
                    ),
                    notes=dict(
                        type="str",
                        required=False,
                    ),
                ),
            ),
            folder=dict(
                type="str",
                required=False,
            ),
            snippet=dict(
                type="str",
                required=False,
            ),
            device=dict(
                type="str",
                required=False,
            ),
            provider=dict(
                type="dict",
                required=True,
                options=dict(
                    client_id=dict(
                        type="str",
                        required=True,
                    ),
                    client_secret=dict(
                        type="str",
                        required=True,
                        no_log=True,
                    ),
                    tsg_id=dict(
                        type="str",
                        required=True,
                    ),
                    log_level=dict(
                        type="str",
                        required=False,
                        default="INFO",
                    ),
                ),
            ),
            state=dict(
                type="str",
                choices=["present", "absent"],
                required=True,
            ),
        )
