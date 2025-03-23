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


class AntiSpywareProfileInfoSpec:
    """
    API specifications for SCM Ansible info modules.

    This class provides standardized specifications for SCM (Strata Cloud Manager)
    related Ansible info modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def spec() -> Dict[str, Any]:
        """
        Returns Ansible module spec for anti-spyware profile info objects.

        This method defines the structure and requirements for anti-spyware profile info related
        parameters in SCM modules, aligning with the Pydantic models in the SCM SDK.

        Returns:
            Dict[str, Any]: A dictionary containing the module specification with
                         parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type="str",
                required=False,
                description="The name of a specific anti-spyware profile to retrieve.",
            ),
            gather_subset=dict(
                type="list",
                elements="str",
                default=["config"],
                choices=["all", "config"],
                description="Determines which information to gather about anti-spyware profiles.",
            ),
            folder=dict(
                type="str",
                required=False,
                description="Filter profiles by folder container (max 64 chars).",
            ),
            snippet=dict(
                type="str",
                required=False,
                description="Filter profiles by snippet container (max 64 chars).",
            ),
            device=dict(
                type="str",
                required=False,
                description="Filter profiles by device container (max 64 chars).",
            ),
            exact_match=dict(
                type="bool",
                required=False,
                default=False,
                description="When True, only return objects defined exactly in the specified container.",
            ),
            exclude_folders=dict(
                type="list",
                elements="str",
                required=False,
                description="List of folder names to exclude from results.",
            ),
            exclude_snippets=dict(
                type="list",
                elements="str",
                required=False,
                description="List of snippet values to exclude from results.",
            ),
            exclude_devices=dict(
                type="list",
                elements="str",
                required=False,
                description="List of device values to exclude from results.",
            ),
            cloud_inline_analysis=dict(
                type="bool",
                required=False,
                description="Filter by cloud inline analysis setting (True/False).",
            ),
            rules=dict(
                type="list",
                elements="str",
                required=False,
                description="Filter by rule names contained in the profiles.",
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
        )
