# -*- coding: utf-8 -*-

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.


class ApplicationSpec:
    """
    API specifications for SCM Ansible modules.

    This class provides standardized specifications for SCM (Strata Cloud Manager)
    related Ansible modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def spec():
        """Returns Ansible module spec for application objects."""
        return dict(
            name=dict(
                type="str",
                required=True,
                description="The name of the application (max 63 chars).",
            ),
            category=dict(
                type="str",
                required=False,
                description="High-level category to which the application belongs (max 50 chars).",
            ),
            subcategory=dict(
                type="str",
                required=False,
                description="Specific sub-category within the high-level category (max 50 chars).",
            ),
            technology=dict(
                type="str",
                required=False,
                description="The underlying technology utilized by the application (max 50 chars).",
            ),
            risk=dict(
                type="int",
                required=False,
                description="The risk level associated with the application (1-5).",
            ),
            description=dict(
                type="str",
                required=False,
                description="Description for the application (max 1023 chars).",
            ),
            ports=dict(
                type="list",
                elements="str",
                required=False,
                description="List of TCP/UDP ports associated with the application.",
            ),
            folder=dict(
                type="str",
                required=False,
                description="The folder where the application configuration is stored (max 64 chars).",
            ),
            snippet=dict(
                type="str",
                required=False,
                description="The configuration snippet for the application (max 64 chars).",
            ),
            evasive=dict(
                type="bool",
                required=False,
                default=False,
                description="Indicates if the application uses evasive techniques.",
            ),
            pervasive=dict(
                type="bool",
                required=False,
                default=False,
                description="Indicates if the application is widely used.",
            ),
            excessive_bandwidth_use=dict(
                type="bool",
                required=False,
                default=False,
                description="Indicates if the application uses excessive bandwidth.",
            ),
            used_by_malware=dict(
                type="bool",
                required=False,
                default=False,
                description="Indicates if the application is commonly used by malware.",
            ),
            transfers_files=dict(
                type="bool",
                required=False,
                default=False,
                description="Indicates if the application transfers files.",
            ),
            has_known_vulnerabilities=dict(
                type="bool",
                required=False,
                default=False,
                description="Indicates if the application has known vulnerabilities.",
            ),
            tunnels_other_apps=dict(
                type="bool",
                required=False,
                default=False,
                description="Indicates if the application tunnels other applications.",
            ),
            prone_to_misuse=dict(
                type="bool",
                required=False,
                default=False,
                description="Indicates if the application is prone to misuse.",
            ),
            no_certifications=dict(
                type="bool",
                required=False,
                default=False,
                description="Indicates if the application lacks certifications.",
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
                description="Authentication credentials for SCM API.",
            ),
            state=dict(
                type="str",
                choices=["present", "absent"],
                required=True,
                description="Desired state of the application object.",
            ),
        )
