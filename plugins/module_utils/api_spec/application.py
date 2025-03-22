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


class ApplicationSpec:
    """
    API specifications for SCM Ansible modules.

    This class provides standardized specifications for SCM (Strata Cloud Manager)
    related Ansible modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def spec() -> Dict[str, Any]:
        """Returns Ansible module spec for application objects."""
        return dict(
            name=dict(
                type="str",
                required=True,
            ),
            category=dict(
                type="str",
                required=False,
            ),
            subcategory=dict(
                type="str",
                required=False,
            ),
            technology=dict(
                type="str",
                required=False,
            ),
            risk=dict(
                type="str",
                required=False,
            ),
            description=dict(
                type="str",
                required=False,
            ),
            default_timeout=dict(
                type="int",
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
            tag=dict(
                type="list",
                elements="str",
                required=False,
            ),
            ports=dict(
                type="list",
                elements="str",
                required=False,
            ),
            transfers_files=dict(
                type="bool",
                required=False,
            ),
            has_known_vulnerabilities=dict(
                type="bool",
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
