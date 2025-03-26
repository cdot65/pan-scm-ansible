# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Ansible module utilities for host information profile (HIP) profiles in SCM.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class HIPProfileSpec:
    """
    API spec for HIP profiles in SCM.

    Provides validation and specification details for Host Information
    Profile (HIP) profiles in Palo Alto Networks' Strata Cloud Manager.
    """

    @staticmethod
    def spec() -> dict:
        """
        Returns the module spec for HIP profiles.

        Returns:
            dict: The module spec dictionary
        """
        return dict(
            name=dict(type="str", required=True),
            description=dict(type="str", required=False),
            match=dict(type="str", required=False),
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
