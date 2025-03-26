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


class ServiceSpec:
    """
    API specifications for SCM Ansible modules.

    This class provides standardized specifications for SCM (Strata Cloud Manager)
    related Ansible modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def spec() -> Dict[str, Any]:
        """
        Returns Ansible module spec for service objects.

        This method defines the structure and requirements for service related
        parameters in SCM modules, aligning with the Pydantic models in the SCM SDK.

        Returns:
            Dict[str, Any]: A dictionary containing the module specification with
                         parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type="str",
                required=True,
                description="The name of the service (max 63 chars, must match pattern: ^[a-zA-Z0-9_ \\.-]+$).",
            ),
            protocol=dict(
                type="dict",
                required=False,
                description="Protocol configuration (TCP or UDP). Exactly one of 'tcp' or 'udp' must be provided.",
                options=dict(
                    tcp=dict(
                        type="dict",
                        required=False,
                        description="TCP protocol configuration with port information.",
                        options=dict(
                            port=dict(
                                type="str",
                                required=True,
                                description="TCP port(s) for the service (e.g., '80' or '80,443,8080').",
                            ),
                            override=dict(
                                type="dict",
                                required=False,
                                description="Override settings for TCP timeouts.",
                                options=dict(
                                    timeout=dict(
                                        type="int",
                                        required=False,
                                        default=3600,
                                        description="Connection timeout in seconds.",
                                    ),
                                    halfclose_timeout=dict(
                                        type="int",
                                        required=False,
                                        default=120,
                                        description="Half-close timeout in seconds.",
                                    ),
                                    timewait_timeout=dict(
                                        type="int",
                                        required=False,
                                        default=15,
                                        description="Time-wait timeout in seconds.",
                                    ),
                                ),
                            ),
                        ),
                    ),
                    udp=dict(
                        type="dict",
                        required=False,
                        description="UDP protocol configuration with port information.",
                        options=dict(
                            port=dict(
                                type="str",
                                required=True,
                                description="UDP port(s) for the service (e.g., '53' or '67,68').",
                            ),
                            override=dict(
                                type="dict",
                                required=False,
                                description="Override settings for UDP timeouts.",
                                options=dict(
                                    timeout=dict(
                                        type="int",
                                        required=False,
                                        default=30,
                                        description="Connection timeout in seconds.",
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            description=dict(
                type="str",
                required=False,
                description="Description of the service (max 1023 chars).",
            ),
            tag=dict(
                type="list",
                elements="str",
                required=False,
                description="List of tags associated with the service (max 64 chars each).",
            ),
            folder=dict(
                type="str",
                required=False,
                description="The folder in which the service is defined (max 64 chars).",
            ),
            snippet=dict(
                type="str",
                required=False,
                description="The snippet in which the service is defined (max 64 chars).",
            ),
            device=dict(
                type="str",
                required=False,
                description="The device in which the service is defined (max 64 chars).",
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
                description="Desired state of the service object.",
            ),
        )
