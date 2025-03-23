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


class ServiceGroupSpec:
    """
    API specifications for SCM Ansible modules.

    This class provides standardized specifications for SCM (Strata Cloud Manager)
    related Ansible modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def spec() -> Dict[str, Any]:
        """
        Returns Ansible module spec for service group objects.

        This method defines the structure and requirements for service group-related
        parameters in SCM modules.

        Returns:
            Dict[str, Any]: A dictionary containing the module specification with
                           parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type="str",
                required=True,
                description="The name of the service group (max 63 chars).",
            ),
            members=dict(
                type="list",
                elements="str",
                required=False,
                description="List of service objects that are members of this group.",
            ),
            tag=dict(
                type="list",
                elements="str",
                required=False,
                description="List of tags associated with the service group. These must be references to existing tag objects in SCM, not just string labels.",
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
                options=dict(
                    client_id=dict(
                        type="str",
                        required=True,
                        description="Client ID for authentication.",
                    ),
                    client_secret=dict(
                        type="str",
                        required=True,
                        no_log=True,
                        description="Client secret for authentication.",
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
                        description="Log level for the SDK.",
                    ),
                ),
                description="Authentication credentials.",
            ),
            state=dict(
                type="str",
                choices=["present", "absent"],
                required=True,
                description="Desired state of the service group object.",
            ),
        )
