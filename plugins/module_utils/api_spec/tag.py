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


class TagSpec:
    """
    API specifications for SCM Ansible modules.

    This class provides standardized specifications for SCM (Strata Cloud Manager)
    related Ansible modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def spec() -> Dict[str, Any]:
        """
        Returns Ansible module spec for tag objects.

        This method defines the structure and requirements for tag-related
        parameters in SCM modules.

        Returns:
            Dict[str, Any]: A dictionary containing the module specification with
                           parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type="str",
                required=True,
                description="The name of the tag (max 63 chars)",
            ),
            color=dict(
                type="str",
                required=False,
                description="Color associated with the tag",
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
            comments=dict(
                type="str",
                required=False,
                description="Comments for the tag (max 1023 chars)",
            ),
            folder=dict(
                type="str",
                required=False,
                description="The folder where the tag is stored (max 64 chars)",
            ),
            snippet=dict(
                type="str",
                required=False,
                description="The configuration snippet for the tag (max 64 chars)",
            ),
            device=dict(
                type="str",
                required=False,
                description="The device where the tag is configured (max 64 chars)",
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
            state=dict(
                type="str",
                choices=["present", "absent"],
                required=True,
                description="Desired state of the tag object",
            ),
        )
