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


class ApplicationGroupSpec:
    """
    API specifications for SCM Ansible modules.

    This class provides standardized specifications for SCM (Strata Cloud Manager)
    related Ansible modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def spec() -> Dict[str, Any]:
        """
        Returns Ansible module spec for application group objects.

        This method defines the structure and requirements for application group-related
        parameters in SCM modules.

        Returns:
            Dict[str, Any]: A dictionary containing the module specification with
                           parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type="str",
                required=True,
            ),
            members=dict(
                type="list",
                elements="str",
                required=False,
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
