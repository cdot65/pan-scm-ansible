# -*- coding: utf-8 -*-

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.

from typing import Dict, Any


class ScmSpec:
    """
    API specifications for SCM Ansible modules.

    This class provides standardized specifications for SCM (Source Control Management)
    related Ansible modules, ensuring consistent parameter definitions and validation
    across the module collection.
    """

    @staticmethod
    def address_spec() -> Dict[str, Any]:
        """
        Returns Ansible module spec for address objects.

        This method defines the structure and requirements for address-related
        parameters in SCM modules.

        Returns:
            Dict[str, Any]: A dictionary containing the module specification with
                           parameter definitions and their requirements.
        """
        return dict(
            name=dict(
                type='str',
                required=True,
            ),
            description=dict(
                type='str',
                required=False,
            ),
            tag=dict(
                type='list',
                elements='str',
                required=False,
            ),
            ip_netmask=dict(
                type='str',
                required=False,
            ),
            ip_range=dict(
                type='str',
                required=False,
            ),
            ip_wildcard=dict(
                type='str',
                required=False,
            ),
            fqdn=dict(
                type='str',
                required=False,
            ),
            folder=dict(
                type='str',
                required=False,
            ),
            snippet=dict(
                type='str',
                required=False,
            ),
            device=dict(
                type='str',
                required=False,
            ),
            provider=dict(
                type='dict',
                required=True,
                options=dict(
                    client_id=dict(
                        type='str',
                        required=True,
                    ),
                    client_secret=dict(
                        type='str',
                        required=True,
                        no_log=True,
                    ),
                    tsg_id=dict(
                        type='str',
                        required=True,
                    ),
                    log_level=dict(
                        type='str',
                        required=False,
                        default='INFO',
                    ),
                ),
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                required=True,
            ),
        )

    @staticmethod
    def address_group_spec():
        return dict(
            name=dict(
                type='str',
                required=True,
            ),
            description=dict(
                type='str',
                required=False,
            ),
            tag=dict(
                type='list',
                elements='str',
                required=False,
            ),
            dynamic=dict(
                type='dict',
                required=False,
                options=dict(
                    filter=dict(
                        type='str',
                        required=True,
                    ),
                ),
            ),
            static=dict(
                type='list',
                elements='str',
                required=False,
            ),
            folder=dict(
                type='str',
                required=False,
            ),
            snippet=dict(
                type='str',
                required=False,
            ),
            device=dict(
                type='str',
                required=False,
            ),
            provider=dict(
                type='dict',
                required=True,
                options=dict(
                    client_id=dict(
                        type='str',
                        required=True,
                    ),
                    client_secret=dict(
                        type='str',
                        required=True,
                    ),
                    tsg_id=dict(
                        type='str',
                        required=True,
                    ),
                    log_level=dict(
                        type='str',
                        required=False,
                        default='INFO',
                    ),
                ),
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                required=True,
            ),
        )

    @staticmethod
    def anti_spyware_profile_spec() -> Dict[str, Any]:
        """Returns Ansible module spec for anti-spyware profile objects."""
        return dict(
            name=dict(
                type='str',
                required=True,
            ),
            description=dict(
                type='str',
                required=False,
            ),
            cloud_inline_analysis=dict(
                type='bool',
                required=False,
                default=False,
            ),
            inline_exception_edl_url=dict(
                type='list',
                elements='str',
                required=False,
            ),
            inline_exception_ip_address=dict(
                type='list',
                elements='str',
                required=False,
            ),
            mica_engine_spyware_enabled=dict(
                type='list',
                elements='dict',
                required=False,
                options=dict(
                    name=dict(
                        type='str',
                        required=True,
                    ),
                    inline_policy_action=dict(
                        type='str',
                        required=False,
                        choices=['alert', 'allow', 'drop', 'reset-both', 'reset-client', 'reset-server'],
                        default='alert',
                    ),
                ),
            ),
            rules=dict(
                type='list',
                elements='dict',
                required=True,
                options=dict(
                    name=dict(
                        type='str',
                        required=True,
                    ),
                    severity=dict(
                        type='list',
                        elements='str',
                        required=True,
                        choices=['critical', 'high', 'medium', 'low', 'informational', 'any'],
                    ),
                    category=dict(
                        type='str',
                        required=True,
                    ),
                    threat_name=dict(
                        type='str',
                        required=False,
                    ),
                    packet_capture=dict(
                        type='str',
                        required=False,
                        choices=['disable', 'single-packet', 'extended-capture'],
                    ),
                ),
            ),
            threat_exception=dict(
                type='list',
                elements='dict',
                required=False,
                options=dict(
                    name=dict(
                        type='str',
                        required=True,
                    ),
                    packet_capture=dict(
                        type='str',
                        required=True,
                        choices=['disable', 'single-packet', 'extended-capture'],
                    ),
                    exempt_ip=dict(
                        type='list',
                        elements='dict',
                        required=False,
                        options=dict(
                            name=dict(
                                type='str',
                                required=True,
                            ),
                        ),
                    ),
                    notes=dict(
                        type='str',
                        required=False,
                    ),
                ),
            ),
            folder=dict(
                type='str',
                required=False,
            ),
            snippet=dict(
                type='str',
                required=False,
            ),
            device=dict(
                type='str',
                required=False,
            ),
            provider=dict(
                type='dict',
                required=True,
                options=dict(
                    client_id=dict(
                        type='str',
                        required=True,
                    ),
                    client_secret=dict(
                        type='str',
                        required=True,
                        no_log=True,
                    ),
                    tsg_id=dict(
                        type='str',
                        required=True,
                    ),
                    log_level=dict(
                        type='str',
                        required=False,
                        default='INFO',
                    ),
                ),
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                required=True,
            ),
        )

    @staticmethod
    def application_spec() -> Dict[str, Any]:
        """Returns Ansible module spec for application objects."""
        return dict(
            name=dict(
                type='str',
                required=True,
            ),
            category=dict(
                type='str',
                required=False,
            ),
            subcategory=dict(
                type='str',
                required=False,
            ),
            technology=dict(
                type='str',
                required=False,
            ),
            risk=dict(
                type='str',
                required=False,
            ),
            description=dict(
                type='str',
                required=False,
            ),
            default_timeout=dict(
                type='int',
                required=False,
            ),
            folder=dict(
                type='str',
                required=False,
            ),
            snippet=dict(
                type='str',
                required=False,
            ),
            tag=dict(
                type='list',
                elements='str',
                required=False,
            ),
            ports=dict(
                type='list',
                elements='str',
                required=False,
            ),
            transfers_files=dict(
                type='bool',
                required=False,
            ),
            has_known_vulnerabilities=dict(
                type='bool',
                required=False,
            ),
            provider=dict(
                type='dict',
                required=True,
                options=dict(
                    client_id=dict(
                        type='str',
                        required=True,
                    ),
                    client_secret=dict(
                        type='str',
                        required=True,
                        no_log=True,
                    ),
                    tsg_id=dict(
                        type='str',
                        required=True,
                    ),
                    log_level=dict(
                        type='str',
                        required=False,
                        default='INFO',
                    ),
                ),
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                required=True,
            ),
        )

    @staticmethod
    def application_group_spec() -> Dict[str, Any]:
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
                type='str',
                required=True,
            ),
            members=dict(
                type='list',
                elements='str',
                required=False,
            ),
            folder=dict(
                type='str',
                required=False,
            ),
            snippet=dict(
                type='str',
                required=False,
            ),
            device=dict(
                type='str',
                required=False,
            ),
            provider=dict(
                type='dict',
                required=True,
                options=dict(
                    client_id=dict(
                        type='str',
                        required=True,
                    ),
                    client_secret=dict(
                        type='str',
                        required=True,
                        no_log=True,
                    ),
                    tsg_id=dict(
                        type='str',
                        required=True,
                    ),
                    log_level=dict(
                        type='str',
                        required=False,
                        default='INFO',
                    ),
                ),
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                required=True,
            ),
        )

    @staticmethod
    def service_spec() -> Dict[str, Any]:
        """Returns Ansible module spec for service objects."""
        return dict(
            name=dict(
                type='str',
                required=True,
            ),
            protocol=dict(
                type='dict',
                required=False,
                options=dict(
                    tcp=dict(
                        type='dict',
                        required=False,
                        options=dict(
                            port=dict(
                                type='str',
                                required=True,
                            ),
                            override=dict(
                                type='dict',
                                required=False,
                                options=dict(
                                    timeout=dict(
                                        type='int',
                                        required=False,
                                        default=3600,
                                    ),
                                    halfclose_timeout=dict(
                                        type='int',
                                        required=False,
                                        default=120,
                                    ),
                                    timewait_timeout=dict(
                                        type='int',
                                        required=False,
                                        default=15,
                                    ),
                                ),
                            ),
                        ),
                    ),
                    udp=dict(
                        type='dict',
                        required=False,
                        options=dict(
                            port=dict(
                                type='str',
                                required=True,
                            ),
                            override=dict(
                                type='dict',
                                required=False,
                                options=dict(
                                    timeout=dict(
                                        type='int',
                                        required=False,
                                        default=30,
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            description=dict(
                type='str',
                required=False,
            ),
            tag=dict(
                type='list',
                elements='str',
                required=False,
            ),
            folder=dict(
                type='str',
                required=False,
            ),
            snippet=dict(
                type='str',
                required=False,
            ),
            device=dict(
                type='str',
                required=False,
            ),
            provider=dict(
                type='dict',
                required=True,
                options=dict(
                    client_id=dict(
                        type='str',
                        required=True,
                    ),
                    client_secret=dict(
                        type='str',
                        required=True,
                        no_log=True,
                    ),
                    tsg_id=dict(
                        type='str',
                        required=True,
                    ),
                    log_level=dict(
                        type='str',
                        required=False,
                        default='INFO',
                    ),
                ),
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                required=True,
            ),
        )

    @staticmethod
    def service_group_spec() -> Dict[str, Any]:
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
                type='str',
                required=True,
            ),
            members=dict(
                type='list',
                elements='str',
                required=False,
            ),
            tag=dict(
                type='list',
                elements='str',
                required=False,
            ),
            folder=dict(
                type='str',
                required=False,
            ),
            snippet=dict(
                type='str',
                required=False,
            ),
            device=dict(
                type='str',
                required=False,
            ),
            provider=dict(
                type='dict',
                required=True,
                options=dict(
                    client_id=dict(
                        type='str',
                        required=True,
                    ),
                    client_secret=dict(
                        type='str',
                        required=True,
                        no_log=True,
                    ),
                    tsg_id=dict(
                        type='str',
                        required=True,
                    ),
                    log_level=dict(
                        type='str',
                        required=False,
                        default='INFO',
                    ),
                ),
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                required=True,
            ),
        )

    @staticmethod
    def tag_spec() -> Dict[str, Any]:
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
                type='str',
                required=True,
            ),
            color=dict(
                type='str',
                required=False,
                choices=[
                    'Azure Blue',
                    'Black',
                    'Blue',
                    'Blue Gray',
                    'Blue Violet',
                    'Brown',
                    'Burnt Sienna',
                    'Cerulean Blue',
                    'Chestnut',
                    'Cobalt Blue',
                    'Copper',
                    'Cyan',
                    'Forest Green',
                    'Gold',
                    'Gray',
                    'Green',
                    'Lavender',
                    'Light Gray',
                    'Light Green',
                    'Lime',
                    'Magenta',
                    'Mahogany',
                    'Maroon',
                    'Medium Blue',
                    'Medium Rose',
                    'Medium Violet',
                    'Midnight Blue',
                    'Olive',
                    'Orange',
                    'Orchid',
                    'Peach',
                    'Purple',
                    'Red',
                    'Red Violet',
                    'Red-Orange',
                    'Salmon',
                    'Thistle',
                    'Turquoise Blue',
                    'Violet Blue',
                    'Yellow',
                    'Yellow-Orange',
                ],
            ),
            comments=dict(
                type='str',
                required=False,
            ),
            folder=dict(
                type='str',
                required=False,
            ),
            snippet=dict(
                type='str',
                required=False,
            ),
            device=dict(
                type='str',
                required=False,
            ),
            provider=dict(
                type='dict',
                required=True,
                options=dict(
                    client_id=dict(
                        type='str',
                        required=True,
                    ),
                    client_secret=dict(
                        type='str',
                        required=True,
                        no_log=True,
                    ),
                    tsg_id=dict(
                        type='str',
                        required=True,
                    ),
                    log_level=dict(
                        type='str',
                        required=False,
                        default='INFO',
                    ),
                ),
            ),
            state=dict(
                type='str',
                choices=['present', 'absent'],
                required=True,
            ),
        )
