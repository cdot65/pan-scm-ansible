# -*- coding: utf-8 -*-

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.


class AddressGroupSpec:
    """
    API specifications for SCM Ansible modules.

    This class provides standardized specifications for SCM (Strata Cloud Manager)
    related Ansible modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def spec():
        return dict(
            name=dict(
                type="str",
                required=True,
                description="The name of the address group (max 63 chars).",
            ),
            description=dict(
                type="str",
                required=False,
                description="Description of the address group (max 1023 chars).",
            ),
            tag=dict(
                type="list",
                elements="str",
                required=False,
                description="List of tags associated with the address group (max 64 chars each).",
            ),
            dynamic=dict(
                type="dict",
                required=False,
                options=dict(
                    filter=dict(
                        type="str",
                        required=True,
                        description="Tag-based filter defining group membership (e.g. \"'tag1' or 'tag2'\").",
                    ),
                ),
                description="Dynamic filter for group membership (mutually exclusive with 'static').",
            ),
            static=dict(
                type="list",
                elements="str",
                required=False,
                description="List of static addresses in the group (mutually exclusive with 'dynamic').",
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
                description="Desired state of the address group object.",
            ),
        )
