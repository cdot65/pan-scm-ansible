# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Ansible module utilities for host information profile (HIP) objects in SCM.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class HIPObjectSpec:
    """
    API spec for HIP objects in SCM.

    Provides validation and specification details for Host Information
    Profile (HIP) objects in Palo Alto Networks' Strata Cloud Manager.
    """

    @staticmethod
    def spec() -> dict:
        """
        Returns the module spec for HIP objects.

        Returns:
            dict: The module spec dictionary
        """
        return dict(
            name=dict(type="str", required=True),
            description=dict(type="str", required=False),
            host_info=dict(
                type="dict",
                required=False,
                options=dict(
                    criteria=dict(
                        type="dict",
                        required=True,
                        options=dict(
                            domain=dict(type="dict", required=False),
                            os=dict(type="dict", required=False),
                            client_version=dict(type="dict", required=False),
                            host_name=dict(type="dict", required=False),
                            host_id=dict(type="dict", required=False),
                            managed=dict(type="bool", required=False),
                            serial_number=dict(type="dict", required=False),
                        ),
                    ),
                ),
            ),
            network_info=dict(
                type="dict",
                required=False,
                options=dict(
                    criteria=dict(
                        type="dict",
                        required=True,
                        options=dict(
                            network=dict(type="dict", required=False),
                        ),
                    ),
                ),
            ),
            patch_management=dict(
                type="dict",
                required=False,
                options=dict(
                    criteria=dict(
                        type="dict",
                        required=True,
                        options=dict(
                            is_installed=dict(type="bool", required=False, default=True),
                            is_enabled=dict(
                                type="str", required=False, choices=["no", "yes", "not-available"]
                            ),
                            missing_patches=dict(
                                type="dict",
                                required=False,
                                options=dict(
                                    severity=dict(type="int", required=False),
                                    patches=dict(type="list", elements="str", required=False),
                                    check=dict(
                                        type="str",
                                        required=False,
                                        default="has-any",
                                        choices=["has-any", "has-none", "has-all"],
                                    ),
                                ),
                            ),
                        ),
                    ),
                    vendor=dict(
                        type="list",
                        elements="dict",
                        required=False,
                        options=dict(
                            name=dict(type="str", required=True),
                            product=dict(type="list", elements="str", required=False),
                        ),
                    ),
                    exclude_vendor=dict(type="bool", required=False, default=False),
                ),
            ),
            disk_encryption=dict(
                type="dict",
                required=False,
                options=dict(
                    criteria=dict(
                        type="dict",
                        required=True,
                        options=dict(
                            is_installed=dict(type="bool", required=False, default=True),
                            is_enabled=dict(
                                type="str", required=False, choices=["no", "yes", "not-available"]
                            ),
                            encrypted_locations=dict(
                                type="list",
                                elements="dict",
                                required=False,
                                options=dict(
                                    name=dict(type="str", required=True),
                                    encryption_state=dict(type="dict", required=True),
                                ),
                            ),
                        ),
                    ),
                    vendor=dict(
                        type="list",
                        elements="dict",
                        required=False,
                        options=dict(
                            name=dict(type="str", required=True),
                            product=dict(type="list", elements="str", required=False),
                        ),
                    ),
                    exclude_vendor=dict(type="bool", required=False, default=False),
                ),
            ),
            mobile_device=dict(
                type="dict",
                required=False,
                options=dict(
                    criteria=dict(
                        type="dict",
                        required=True,
                        options=dict(
                            jailbroken=dict(type="bool", required=False),
                            disk_encrypted=dict(type="bool", required=False),
                            passcode_set=dict(type="bool", required=False),
                            last_checkin_time=dict(type="dict", required=False),
                            applications=dict(
                                type="dict",
                                required=False,
                                options=dict(
                                    has_malware=dict(type="bool", required=False),
                                    has_unmanaged_app=dict(type="bool", required=False),
                                    includes=dict(
                                        type="list",
                                        elements="dict",
                                        required=False,
                                        options=dict(
                                            name=dict(type="str", required=True),
                                            package=dict(type="str", required=False),
                                            hash=dict(type="str", required=False),
                                        ),
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            certificate=dict(
                type="dict",
                required=False,
                options=dict(
                    criteria=dict(
                        type="dict",
                        required=True,
                        options=dict(
                            certificate_profile=dict(type="str", required=False),
                            certificate_attributes=dict(
                                type="list",
                                elements="dict",
                                required=False,
                                options=dict(
                                    name=dict(type="str", required=True),
                                    value=dict(type="str", required=True),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            folder=dict(type="str", required=False),
            snippet=dict(type="str", required=False),
            device=dict(type="str", required=False),
            provider=dict(
                type="dict",
                required=True,
                options=dict(
                    client_id=dict(type="str", required=True),
                    client_secret=dict(type="str", required=True, no_log=True),
                    tsg_id=dict(type="str", required=True),
                    log_level=dict(
                        type="str",
                        required=False,
                        default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                    ),
                ),
            ),
            state=dict(
                type="str",
                required=True,
                choices=["present", "absent"],
            ),
        )
