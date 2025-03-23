"""
API spec for external dynamic lists module in SCM.

This module defines the Ansible arguments specifications for the external dynamic lists module
used to manage external dynamic lists in Strata Cloud Manager (SCM).
"""

from ansible.module_utils.basic import env_fallback


class ExternalDynamicListsSpec:
    """
    Specification for External Dynamic Lists module parameters.

    This class provides standardized parameter specifications for the
    external_dynamic_lists Ansible module, including options for different list
    types, container locations, and authentication.
    """

    @staticmethod
    def spec():
        """
        Generate the module specification dictionary.

        Returns:
            dict: A dictionary containing all module parameters with their specs.
        """
        return dict(
            name=dict(type="str", required=True),
            description=dict(type="str", required=False),
            # Container parameters (mutually exclusive)
            folder=dict(type="str", required=False),
            snippet=dict(type="str", required=False),
            device=dict(type="str", required=False),
            # Type parameters (only one should be provided)
            ip_list=dict(
                type="dict",
                required=False,
                options=dict(
                    url=dict(type="str", required=True),
                    exception_list=dict(type="list", elements="str", required=False),
                    certificate_profile=dict(type="str", required=False),
                    auth=dict(
                        type="dict",
                        required=False,
                        no_log=True,
                        options=dict(
                            username=dict(type="str", required=True),
                            password=dict(type="str", required=True, no_log=True),
                        ),
                    ),
                ),
            ),
            domain_list=dict(
                type="dict",
                required=False,
                options=dict(
                    url=dict(type="str", required=True),
                    exception_list=dict(type="list", elements="str", required=False),
                    certificate_profile=dict(type="str", required=False),
                    expand_domain=dict(type="bool", required=False, default=False),
                    auth=dict(
                        type="dict",
                        required=False,
                        no_log=True,
                        options=dict(
                            username=dict(type="str", required=True),
                            password=dict(type="str", required=True, no_log=True),
                        ),
                    ),
                ),
            ),
            url_list=dict(
                type="dict",
                required=False,
                options=dict(
                    url=dict(type="str", required=True),
                    exception_list=dict(type="list", elements="str", required=False),
                    certificate_profile=dict(type="str", required=False),
                    auth=dict(
                        type="dict",
                        required=False,
                        no_log=True,
                        options=dict(
                            username=dict(type="str", required=True),
                            password=dict(type="str", required=True, no_log=True),
                        ),
                    ),
                ),
            ),
            imsi_list=dict(
                type="dict",
                required=False,
                options=dict(
                    url=dict(type="str", required=True),
                    exception_list=dict(type="list", elements="str", required=False),
                    certificate_profile=dict(type="str", required=False),
                    auth=dict(
                        type="dict",
                        required=False,
                        no_log=True,
                        options=dict(
                            username=dict(type="str", required=True),
                            password=dict(type="str", required=True, no_log=True),
                        ),
                    ),
                ),
            ),
            imei_list=dict(
                type="dict",
                required=False,
                options=dict(
                    url=dict(type="str", required=True),
                    exception_list=dict(type="list", elements="str", required=False),
                    certificate_profile=dict(type="str", required=False),
                    auth=dict(
                        type="dict",
                        required=False,
                        no_log=True,
                        options=dict(
                            username=dict(type="str", required=True),
                            password=dict(type="str", required=True, no_log=True),
                        ),
                    ),
                ),
            ),
            # Update interval parameters (exactly one should be provided)
            five_minute=dict(type="bool", required=False),
            hourly=dict(type="bool", required=False),
            daily=dict(
                type="dict",
                required=False,
                options=dict(
                    at=dict(type="str", required=False, default="00"),
                ),
            ),
            weekly=dict(
                type="dict",
                required=False,
                options=dict(
                    day_of_week=dict(
                        type="str",
                        required=True,
                        choices=[
                            "sunday",
                            "monday",
                            "tuesday",
                            "wednesday",
                            "thursday",
                            "friday",
                            "saturday",
                        ],
                    ),
                    at=dict(type="str", required=False, default="00"),
                ),
            ),
            monthly=dict(
                type="dict",
                required=False,
                options=dict(
                    day_of_month=dict(type="int", required=True, min=1, max=31),
                    at=dict(type="str", required=False, default="00"),
                ),
            ),
            # Common parameters for all modules
            provider=dict(
                type="dict",
                required=True,
                options=dict(
                    client_id=dict(
                        type="str",
                        required=True,
                        fallback=(env_fallback, ["SCM_CLIENT_ID"]),
                    ),
                    client_secret=dict(
                        type="str",
                        required=True,
                        no_log=True,
                        fallback=(env_fallback, ["SCM_CLIENT_SECRET"]),
                    ),
                    tsg_id=dict(
                        type="str",
                        required=True,
                        fallback=(env_fallback, ["SCM_TSG_ID"]),
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
                required=True,
                choices=["present", "absent"],
            ),
        )
