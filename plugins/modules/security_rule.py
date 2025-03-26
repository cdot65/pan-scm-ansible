# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.

"""
Ansible module for managing security rule objects in SCM.

This module provides functionality to create, update, and delete security rule objects
in the SCM (Strata Cloud Manager) system. It handles various rule parameters
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.security_rule import (
    SecurityRuleSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.security import SecurityRuleUpdateModel

DOCUMENTATION = r"""
---
module: security_rule

short_description: Manage security rule objects in SCM.

version_added: "0.1.0"

description:
    - Manage security rule objects within Strata Cloud Manager (SCM).
    - Create, update, and delete security rule objects with various parameters.
    - Ensures that exactly one container type (folder, snippet, device) is provided.
    - Supports both pre-rulebase and post-rulebase configurations.

options:
    name:
        description: The name of the security rule object.
        required: true
        type: str
    disabled:
        description: Whether the security rule is disabled.
        required: false
        type: bool
        default: false
    description:
        description: Description of the security rule object.
        required: false
        type: str
    tag:
        description: List of tags associated with the security rule object.
        required: false
        type: list
        elements: str
    from_:
        description: List of source security zones.
        required: false
        type: list
        elements: str
        default: ["any"]
    source:
        description: List of source addresses.
        required: false
        type: list
        elements: str
        default: ["any"]
    negate_source:
        description: Whether to negate the source addresses.
        required: false
        type: bool
        default: false
    source_user:
        description: List of source users and/or groups.
        required: false
        type: list
        elements: str
        default: ["any"]
    source_hip:
        description: List of source Host Integrity Profiles.
        required: false
        type: list
        elements: str
        default: ["any"]
    to_:
        description: List of destination security zones.
        required: false
        type: list
        elements: str
        default: ["any"]
    destination:
        description: List of destination addresses.
        required: false
        type: list
        elements: str
        default: ["any"]
    negate_destination:
        description: Whether to negate the destination addresses.
        required: false
        type: bool
        default: false
    destination_hip:
        description: List of destination Host Integrity Profiles.
        required: false
        type: list
        elements: str
        default: ["any"]
    application:
        description: List of applications being accessed.
        required: false
        type: list
        elements: str
        default: ["any"]
    service:
        description: List of services being accessed.
        required: false
        type: list
        elements: str
        default: ["any"]
    category:
        description: List of URL categories being accessed.
        required: false
        type: list
        elements: str
        default: ["any"]
    action:
        description: Action to be taken when the rule is matched.
        required: false
        type: str
        default: "allow"
        choices: ["allow", "deny", "drop", "reset-client", "reset-server", "reset-both"]
    profile_setting:
        description: Security profile settings for the rule.
        required: false
        type: dict
        suboptions:
            group:
                description: List of security profile groups.
                required: false
                type: list
                elements: str
                default: ["best-practice"]
    log_setting:
        description: Log forwarding profile for the rule.
        required: false
        type: str
    schedule:
        description: Schedule for the rule.
        required: false
        type: str
    log_start:
        description: Whether to log at the start of the session.
        required: false
        type: bool
    log_end:
        description: Whether to log at the end of the session.
        required: false
        type: bool
    folder:
        description: The folder in which the resource is defined.
        required: false
        type: str
    snippet:
        description: The snippet in which the resource is defined.
        required: false
        type: str
    device:
        description: The device in which the resource is defined.
        required: false
        type: str
    rulebase:
        description: Which rulebase to use.
        required: false
        type: str
        default: "pre"
        choices: ["pre", "post"]
    provider:
        description: Authentication credentials.
        required: true
        type: dict
        suboptions:
            client_id:
                description: Client ID for authentication.
                required: true
                type: str
            client_secret:
                description: Client secret for authentication.
                required: true
                type: str
            tsg_id:
                description: Tenant Service Group ID.
                required: true
                type: str
            log_level:
                description: Log level for the SDK.
                required: false
                type: str
                default: "INFO"
    state:
        description: Desired state of the security rule object.
        required: true
        type: str
        choices:
          - present
          - absent

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
---
- name: Manage Security Rules in Strata Cloud Manager
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:

    - name: Create a security rule
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Allow_Web_Traffic"
        description: "Allow web traffic to the web server"
        from_: ["Internet"]
        source: ["any"]
        to_: ["DMZ"]
        destination: ["Web-Servers"]
        application: ["web-browsing", "ssl"]
        service: ["application-default"]
        action: "allow"
        folder: "Texas"
        rulebase: "pre"
        profile_setting:
          group: ["best-practice"]
        tag: ["web", "internet"]
        state: "present"

    - name: Update a security rule
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Allow_Web_Traffic"
        description: "Allow web traffic to the web server (updated)"
        from_: ["Internet"]
        source: ["any"]
        to_: ["DMZ"]
        destination: ["Web-Servers"]
        application: ["web-browsing", "ssl", "http2"]
        service: ["application-default"]
        action: "allow"
        folder: "Texas"
        rulebase: "pre"
        profile_setting:
          group: ["strict-security"]
        tag: ["web", "internet", "updated"]
        state: "present"

    - name: Create a security rule in post-rulebase
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Block_Malicious_Traffic"
        description: "Block traffic to known malicious sites"
        from_: ["any"]
        source: ["any"]
        to_: ["any"]
        destination: ["any"]
        application: ["any"]
        service: ["any"]
        category: ["malware", "command-and-control"]
        action: "deny"
        folder: "Texas"
        rulebase: "post"
        log_setting: "default-log-profile"
        log_end: true
        state: "present"

    - name: Delete security rule
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Allow_Web_Traffic"
        folder: "Texas"
        rulebase: "pre"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
security_rule:
    description: Details about the security rule object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Allow_Web_Traffic"
        description: "Allow web traffic to the web server"
        disabled: false
        from_: ["Internet"]
        source: ["any"]
        to_: ["DMZ"]
        destination: ["Web-Servers"]
        application: ["web-browsing", "ssl"]
        service: ["application-default"]
        action: "allow"
        folder: "Texas"
        tag: ["web", "internet"]
"""


def build_security_rule_data(module_params):
    """
    Build security rule data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant security rule parameters
    """
    return {
        k: v
        for k, v in module_params.items()
        if k not in ["provider", "state", "rulebase"] and v is not None
    }


def is_container_specified(rule_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        rule_data (dict): Security rule parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [rule_data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the security rule needs to be updated.

    Args:
        existing: Existing security rule object from the SCM API
        params (dict): Security rule parameters with desired state from Ansible module

    Returns:
        (bool, dict): Tuple containing:
            - bool: Whether an update is needed
            - dict: Minimal object data for update containing only necessary fields
    """
    changed = False

    # Start with minimal required fields
    update_data = {
        "id": str(existing.id),  # Convert UUID to string for Pydantic
        "name": existing.name,
    }

    # Add the container field (folder, snippet, or device)
    for container in ["folder", "snippet", "device"]:
        container_value = getattr(existing, container, None)
        if container_value is not None:
            update_data[container] = container_value

    # Define fields that can be safely updated
    field_mapping = [
        "description",
        "disabled",
        "negate_source",
        "negate_destination",
        "action",
    ]

    # Process regular fields - only include fields that are explicitly provided and different from current value
    for param in field_mapping:
        # If user provided a value and it's different from the current value, add it to update_data
        current_value = getattr(existing, param, None)
        if param in params and params[param] is not None:
            if current_value != params[param]:
                update_data[param] = params[param]
                changed = True

    # List parameters - handle similarly to regular fields
    list_params = [
        "tag",
        "from_",
        "source",
        "source_user",
        "source_hip",
        "to_",
        "destination",
        "destination_hip",
        "application",
        "service",
        "category",
    ]
    for param in list_params:
        current_value = getattr(existing, param, None)
        # Only add to update_data if the user provided a value and it's different from current
        if param in params and params[param] is not None:
            if current_value is None or sorted(current_value) != sorted(params[param]):
                update_data[param] = params[param]
                changed = True

    # Handle profile_setting specially since it's a nested object
    if "profile_setting" in params and params["profile_setting"] is not None:
        if hasattr(existing, "profile_setting") and existing.profile_setting is not None:
            current_profile_setting = {"group": existing.profile_setting.group}
            if "group" in params["profile_setting"] and sorted(
                current_profile_setting["group"]
            ) != sorted(params["profile_setting"]["group"]):
                update_data["profile_setting"] = params["profile_setting"]
                changed = True
        else:
            update_data["profile_setting"] = params["profile_setting"]
            changed = True

    # IMPORTANT: Explicitly exclude problematic fields that cause validation errors
    # Do not include log_setting, schedule, log_start, or log_end in the update

    return changed, update_data


def get_existing_security_rule(client, rule_data, rulebase):
    """
    Attempt to fetch an existing security rule object.

    Args:
        client: SCM client instance
        rule_data (dict): Security rule parameters to search for
        rulebase (str): Which rulebase to use ('pre' or 'post')

    Returns:
        tuple: (bool, object) indicating if rule exists and the rule object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if container in rule_data and rule_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in rule_data:
            return False, None

        # Fetch the security rule using the appropriate container
        existing = client.security_rule.fetch(
            name=rule_data["name"], rulebase=rulebase, **{container_type: rule_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the security rule module.

    This module provides functionality to create, update, and delete security rule objects
    in the SCM (Strata Cloud Manager) system. It handles various rule parameters
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=SecurityRuleSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet", "device"],
        ],
        required_one_of=[["folder", "snippet", "device"]],
    )

    result = {"changed": False, "security_rule": None}

    try:
        client = get_scm_client(module)
        rule_data = build_security_rule_data(module.params)
        rulebase = module.params.get("rulebase", "pre")

        # Validate container is specified
        if not is_container_specified(rule_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing security rule
        exists, existing_rule = get_existing_security_rule(client, rule_data, rulebase)

        if module.params["state"] == "present":
            if not exists:
                # Create new security rule
                if not module.check_mode:
                    try:
                        new_rule = client.security_rule.create(data=rule_data, rulebase=rulebase)
                        result["security_rule"] = serialize_response(new_rule)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"A security rule with name '{rule_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid security rule data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_rule, rule_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with minimal object data (problematic fields excluded by needs_update)
                        update_model = SecurityRuleUpdateModel(**update_data)

                        # Perform update with minimal object
                        updated_rule = client.security_rule.update(update_model, rulebase=rulebase)
                        result["security_rule"] = serialize_response(updated_rule)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["security_rule"] = serialize_response(existing_rule)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.security_rule.delete(str(existing_rule.id), rulebase=rulebase)
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
