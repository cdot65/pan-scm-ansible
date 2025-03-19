# -*- coding: utf-8 -*-

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.

from traceback import format_exc

from ansible.module_utils._text import to_native
from scm.client import Scm
from scm.exceptions import AuthenticationError


def get_scm_client(module):
    """Initialize and return an SCM client instance with proper error handling.

    This function creates a new SCM client instance using the provided configuration
    parameters from the Ansible module. It handles authentication and initialization
    errors appropriately.

    Args:
        module: An AnsibleModule instance containing the module parameters.
                Must include a 'provider' dictionary with the following keys:
                - client_id: The client ID for authentication
                - client_secret: The client secret for authentication
                - tsg_id: The TSG ID for the client
                - log_level: Optional logging level (defaults to "INFO")

    Returns:
        Scm: An initialized SCM client instance

    Raises:
        AnsibleFailJson: When authentication fails or other errors occur during initialization.
            The error message will contain details about the failure.
    """
    try:
        provider = module.params["provider"]
        client = Scm(
            client_id=provider["client_id"],
            client_secret=provider["client_secret"],
            tsg_id=provider["tsg_id"],
            log_level=provider.get("log_level", "INFO"),
        )
        return client
    except AuthenticationError as e:
        module.fail_json(
            msg=f"Authentication failed: {to_native(e)}",
            error_code=getattr(
                e,
                'error_code',
                None,
            ),
            http_status=getattr(
                e,
                'http_status_code',
                None,
            ),
        )
    except Exception as e:
        module.fail_json(
            msg=to_native(e),
            exception=format_exc(),
        )
