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


class WildfireAntivirusProfileSpec:
    """
    API specifications for Strata Cloud Manager wildfire antivirus profile Ansible modules.

    This class provides standardized specifications for SCM (Strata Cloud Manager)
    related Ansible modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def spec() -> Dict[str, Any]:
        """
        Returns Ansible module spec for wildfire antivirus profile objects.

        This method defines the structure and requirements for wildfire antivirus profile
        related parameters in SCM modules, aligning with the Pydantic models in the SCM SDK.

        Returns:
            Dict[str, Any]: A dictionary containing the module specification with
                         parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type="str",
                required=True,
                description="The name of the wildfire antivirus profile (max 63 chars, must match pattern: ^[a-zA-Z0-9._-]+$).",
            ),
            description=dict(
                type="str",
                required=False,
                description="Description of the wildfire antivirus profile (max 1023 chars).",
            ),
            packet_capture=dict(
                type="bool",
                required=False,
                default=False,
                description="Whether packet capture is enabled.",
            ),
            rules=dict(
                type="list",
                elements="dict",
                required=True,
                description="List of wildfire antivirus protection rules to apply. At least one rule is required.",
                options=dict(
                    name=dict(
                        type="str",
                        required=True,
                        description="Name of the rule.",
                    ),
                    direction=dict(
                        type="str",
                        required=True,
                        choices=["download", "upload", "both"],
                        description="Direction of traffic to inspect.",
                    ),
                    analysis=dict(
                        type="str",
                        required=False,
                        choices=["public-cloud", "private-cloud"],
                        description="Analysis type for malware detection.",
                    ),
                    application=dict(
                        type="list",
                        elements="str",
                        required=False,
                        default=["any"],
                        description="List of applications this rule applies to.",
                    ),
                    file_type=dict(
                        type="list",
                        elements="str",
                        required=False,
                        default=["any"],
                        description="List of file types this rule applies to.",
                    ),
                ),
            ),
            mlav_exception=dict(
                type="list",
                elements="dict",
                required=False,
                description="List of Machine Learning Anti-Virus exceptions.",
                options=dict(
                    name=dict(
                        type="str",
                        required=True,
                        description="Name of the MLAV exception.",
                    ),
                    description=dict(
                        type="str",
                        required=False,
                        description="Description of the MLAV exception.",
                    ),
                    filename=dict(
                        type="str",
                        required=True,
                        description="Filename to exempt from scanning.",
                    ),
                ),
            ),
            threat_exception=dict(
                type="list",
                elements="dict",
                required=False,
                description="List of threat exceptions.",
                options=dict(
                    name=dict(
                        type="str",
                        required=True,
                        description="Name of the threat exception.",
                    ),
                    notes=dict(
                        type="str",
                        required=False,
                        description="Additional notes for the threat exception.",
                    ),
                ),
            ),
            folder=dict(
                type="str",
                required=False,
                description="The folder in which the resource is defined (max 64 chars).",
            ),
            snippet=dict(
                type="str",
                required=False,
                description="The snippet in which the resource is defined (max 64 chars).",
            ),
            device=dict(
                type="str",
                required=False,
                description="The device in which the resource is defined (max 64 chars).",
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
                description="Desired state of the wildfire antivirus profile.",
            ),
        )
