"""
API spec for external dynamic lists info module in SCM.

This module defines the Ansible arguments specifications for the external dynamic lists info module
used to retrieve information about external dynamic lists in Strata Cloud Manager (SCM).
"""

from ansible.module_utils.basic import env_fallback


class ExternalDynamicListsInfoSpec:
    """
    Specification for External Dynamic Lists Info module parameters.

    This class provides standardized parameter specifications for the
    external_dynamic_lists_info Ansible module, including options for filtering
    and retrieving external dynamic lists.
    """

    @staticmethod
    def spec():
        """
        Generate the module specification dictionary.

        Returns:
            dict: A dictionary containing all module parameters with their specs.
        """
        return dict(
            name=dict(type="str", required=False),
            gather_subset=dict(
                type="list",
                elements="str",
                default=["config"],
                choices=["all", "config"],
            ),
            folder=dict(type="str", required=False),
            snippet=dict(type="str", required=False),
            device=dict(type="str", required=False),
            exact_match=dict(type="bool", required=False, default=False),
            exclude_folders=dict(type="list", elements="str", required=False),
            exclude_snippets=dict(type="list", elements="str", required=False),
            exclude_devices=dict(type="list", elements="str", required=False),
            types=dict(
                type="list",
                elements="str",
                required=False,
                choices=["ip", "domain", "url", "imsi", "imei", "predefined_ip", "predefined_url"],
            ),
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
        )
