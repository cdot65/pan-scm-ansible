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


class TagInfoSpec:
    """
    API specifications for SCM Ansible info modules.

    This class provides standardized specifications for SCM (Strata Cloud Manager)
    related Ansible info modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def spec() -> Dict[str, Any]:
        """
        Returns Ansible module spec for tag info objects.

        This method defines the structure and requirements for tag-related
        parameters in SCM info modules.

        Returns:
            Dict[str, Any]: A dictionary containing the module specification with
                           parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type="str",
                required=False,
                description="The name of a specific tag object to retrieve",
            ),
            gather_subset=dict(
                type="list",
                elements="str",
                default=["config"],
                choices=["all", "config"],
                description="Determines which information to gather about tags",
            ),
            folder=dict(
                type="str",
                required=False,
                description="Filter tags by folder container",
            ),
            snippet=dict(
                type="str",
                required=False,
                description="Filter tags by snippet container",
            ),
            device=dict(
                type="str",
                required=False,
                description="Filter tags by device container",
            ),
            exact_match=dict(
                type="bool",
                required=False,
                default=False,
                description="When True, only return objects defined exactly in the specified container",
            ),
            exclude_folders=dict(
                type="list",
                elements="str",
                required=False,
                description="List of folder names to exclude from results",
            ),
            exclude_snippets=dict(
                type="list",
                elements="str",
                required=False,
                description="List of snippet values to exclude from results",
            ),
            exclude_devices=dict(
                type="list",
                elements="str",
                required=False,
                description="List of device values to exclude from results",
            ),
            colors=dict(
                type="list",
                elements="str",
                required=False,
                description="Filter by tag colors",
                choices=[
                    "Azure Blue",
                    "Black",
                    "Blue",
                    "Blue Gray",
                    "Blue Violet",
                    "Brown",
                    "Burnt Sienna",
                    "Cerulean Blue",
                    "Chestnut",
                    "Cobalt Blue",
                    "Copper",
                    "Cyan",
                    "Forest Green",
                    "Gold",
                    "Gray",
                    "Green",
                    "Lavender",
                    "Light Gray",
                    "Light Green",
                    "Lime",
                    "Magenta",
                    "Mahogany",
                    "Maroon",
                    "Medium Blue",
                    "Medium Rose",
                    "Medium Violet",
                    "Midnight Blue",
                    "Olive",
                    "Orange",
                    "Orchid",
                    "Peach",
                    "Purple",
                    "Red",
                    "Red Violet",
                    "Red-Orange",
                    "Salmon",
                    "Thistle",
                    "Turquoise Blue",
                    "Violet Blue",
                    "Yellow",
                    "Yellow-Orange",
                ],
            ),
            provider=dict(
                type="dict",
                required=True,
                options=dict(
                    client_id=dict(
                        type="str",
                        required=True,
                        description="Client ID for authentication",
                    ),
                    client_secret=dict(
                        type="str",
                        required=True,
                        no_log=True,
                        description="Client secret for authentication",
                    ),
                    tsg_id=dict(
                        type="str",
                        required=True,
                        description="Tenant Service Group ID",
                    ),
                    log_level=dict(
                        type="str",
                        required=False,
                        default="INFO",
                        description="Log level for the SDK",
                    ),
                ),
            ),
        )
