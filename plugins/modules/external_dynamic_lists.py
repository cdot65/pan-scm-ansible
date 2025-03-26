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
Ansible module for managing external dynamic lists in SCM.

This module provides functionality to create, update, and delete external dynamic
lists (EDLs) in the SCM (Strata Cloud Manager) system. It handles various EDL types
including IP, Domain, URL, IMSI, and IMEI with configurable update intervals.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.external_dynamic_lists import (
    ExternalDynamicListsSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.objects import ExternalDynamicListsUpdateModel

DOCUMENTATION = r"""
---
module: external_dynamic_lists

short_description: Manage external dynamic lists in SCM.

version_added: "0.1.0"

description:
    - Manage external dynamic lists within Strata Cloud Manager (SCM).
    - Create, update, and delete dynamic lists of various types including IP, Domain, URL, IMSI, and IMEI.
    - Ensures that exactly one list type is provided for create/update operations.
    - Ensures that exactly one container type (folder, snippet, device) is provided.
    - Supports various update intervals including five minute, hourly, daily, weekly, and monthly.

options:
    name:
        description: The name of the external dynamic list (max 63 chars).
        required: true
        type: str
    description:
        description: Description of the external dynamic list (max 255 chars).
        required: false
        type: str
    ip_list:
        description: Configuration for an IP-based external dynamic list.
        required: false
        type: dict
        suboptions:
            url:
                description: URL for the list content.
                required: true
                type: str
            exception_list:
                description: List of entries to exclude from the external dynamic list.
                required: false
                type: list
                elements: str
            certificate_profile:
                description: Client certificate profile for secure connections.
                required: false
                type: str
            auth:
                description: Authentication credentials for the list URL.
                required: false
                type: dict
                suboptions:
                    username:
                        description: Username for authentication.
                        required: true
                        type: str
                    password:
                        description: Password for authentication.
                        required: true
                        type: str
    domain_list:
        description: Configuration for a domain-based external dynamic list.
        required: false
        type: dict
        suboptions:
            url:
                description: URL for the list content.
                required: true
                type: str
            exception_list:
                description: List of entries to exclude from the external dynamic list.
                required: false
                type: list
                elements: str
            certificate_profile:
                description: Client certificate profile for secure connections.
                required: false
                type: str
            expand_domain:
                description: Enable domain expansion.
                required: false
                type: bool
                default: false
            auth:
                description: Authentication credentials for the list URL.
                required: false
                type: dict
                suboptions:
                    username:
                        description: Username for authentication.
                        required: true
                        type: str
                    password:
                        description: Password for authentication.
                        required: true
                        type: str
    url_list:
        description: Configuration for a URL-based external dynamic list.
        required: false
        type: dict
        suboptions:
            url:
                description: URL for the list content.
                required: true
                type: str
            exception_list:
                description: List of entries to exclude from the external dynamic list.
                required: false
                type: list
                elements: str
            certificate_profile:
                description: Client certificate profile for secure connections.
                required: false
                type: str
            auth:
                description: Authentication credentials for the list URL.
                required: false
                type: dict
                suboptions:
                    username:
                        description: Username for authentication.
                        required: true
                        type: str
                    password:
                        description: Password for authentication.
                        required: true
                        type: str
    imsi_list:
        description: Configuration for an IMSI-based external dynamic list.
        required: false
        type: dict
        suboptions:
            url:
                description: URL for the list content.
                required: true
                type: str
            exception_list:
                description: List of entries to exclude from the external dynamic list.
                required: false
                type: list
                elements: str
            certificate_profile:
                description: Client certificate profile for secure connections.
                required: false
                type: str
            auth:
                description: Authentication credentials for the list URL.
                required: false
                type: dict
                suboptions:
                    username:
                        description: Username for authentication.
                        required: true
                        type: str
                    password:
                        description: Password for authentication.
                        required: true
                        type: str
    imei_list:
        description: Configuration for an IMEI-based external dynamic list.
        required: false
        type: dict
        suboptions:
            url:
                description: URL for the list content.
                required: true
                type: str
            exception_list:
                description: List of entries to exclude from the external dynamic list.
                required: false
                type: list
                elements: str
            certificate_profile:
                description: Client certificate profile for secure connections.
                required: false
                type: str
            auth:
                description: Authentication credentials for the list URL.
                required: false
                type: dict
                suboptions:
                    username:
                        description: Username for authentication.
                        required: true
                        type: str
                    password:
                        description: Password for authentication.
                        required: true
                        type: str
    five_minute:
        description: Configure list to update every five minutes.
        required: false
        type: bool
    hourly:
        description: Configure list to update hourly.
        required: false
        type: bool
    daily:
        description: Configure list to update daily at specified hour.
        required: false
        type: dict
        suboptions:
            at:
                description: Hour of day for update (00-23).
                required: false
                type: str
                default: "00"
    weekly:
        description: Configure list to update weekly on specified day and time.
        required: false
        type: dict
        suboptions:
            day_of_week:
                description: Day of week for update.
                required: true
                type: str
                choices: ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
            at:
                description: Hour of day for update (00-23).
                required: false
                type: str
                default: "00"
    monthly:
        description: Configure list to update monthly on specified day and time.
        required: false
        type: dict
        suboptions:
            day_of_month:
                description: Day of month for update (1-31).
                required: true
                type: int
            at:
                description: Hour of day for update (00-23).
                required: false
                type: str
                default: "00"
    folder:
        description: The folder in which the resource is defined (max 64 chars).
        required: false
        type: str
    snippet:
        description: The snippet in which the resource is defined (max 64 chars).
        required: false
        type: str
    device:
        description: The device in which the resource is defined (max 64 chars).
        required: false
        type: str
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
        description: Desired state of the external dynamic list.
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
- name: Manage External Dynamic Lists in Strata Cloud Manager
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

    - name: Create IP-based external dynamic list with hourly updates
      cdot65.scm.external_dynamic_lists:
        provider: "{{ provider }}"
        name: "malicious-ips"
        description: "Known malicious IPs"
        folder: "Texas"
        ip_list:
          url: "https://threatfeeds.example.com/ips.txt"
          auth:
            username: "user123"
            password: "pass123"
        hourly: true
        state: "present"

    - name: Create domain-based external dynamic list with daily updates at 3 AM
      cdot65.scm.external_dynamic_lists:
        provider: "{{ provider }}"
        name: "blocked-domains"
        description: "Blocked domains list"
        folder: "Texas"
        domain_list:
          url: "https://threatfeeds.example.com/domains.txt"
          expand_domain: true
        daily:
          at: "03"
        state: "present"

    - name: Create URL-based external dynamic list with weekly updates
      cdot65.scm.external_dynamic_lists:
        provider: "{{ provider }}"
        name: "malicious-urls"
        description: "Malicious URLs list"
        folder: "Texas"
        url_list:
          url: "https://threatfeeds.example.com/urls.txt"
          exception_list:
            - "example.com/allowed"
            - "example.org/allowed"
        weekly:
          day_of_week: "monday"
          at: "12"
        state: "present"

    - name: Update external dynamic list with new description and auth
      cdot65.scm.external_dynamic_lists:
        provider: "{{ provider }}"
        name: "malicious-ips"
        description: "Updated malicious IPs list"
        folder: "Texas"
        ip_list:
          url: "https://threatfeeds.example.com/ips.txt"
          auth:
            username: "newuser"
            password: "newpass"
        five_minute: true
        state: "present"

    - name: Delete external dynamic list
      cdot65.scm.external_dynamic_lists:
        provider: "{{ provider }}"
        name: "blocked-domains"
        folder: "Texas"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
external_dynamic_list:
    description: Details about the external dynamic list.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "malicious-ips"
        description: "Known malicious IPs"
        type:
          ip:
            url: "https://threatfeeds.example.com/ips.txt"
            description: "Known malicious IPs"
            recurring:
              hourly: {}
        folder: "Texas"
"""


def build_recurring_data(module_params):
    """
    Build recurring update interval data from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Recurring interval configuration for the EDL
    """
    recurring = {}
    if module_params.get("five_minute"):
        recurring = {"five_minute": {}}
    elif module_params.get("hourly"):
        recurring = {"hourly": {}}
    elif module_params.get("daily"):
        recurring = {"daily": module_params.get("daily")}
    elif module_params.get("weekly"):
        recurring = {"weekly": module_params.get("weekly")}
    elif module_params.get("monthly"):
        recurring = {"monthly": module_params.get("monthly")}
    return recurring


def build_edl_type_data(module_params, recurring):
    """
    Build EDL type configuration from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters
        recurring (dict): Recurring interval configuration

    Returns:
        dict: Type configuration for the EDL
    """
    type_data = {}
    edl_types = ["ip_list", "domain_list", "url_list", "imsi_list", "imei_list"]

    for edl_type in edl_types:
        if module_params.get(edl_type):
            # Convert ip_list to ip, domain_list to domain, etc.
            sdk_type = edl_type.replace("_list", "")
            type_config = module_params[edl_type].copy()

            # Add description if available
            if module_params.get("description"):
                type_config["description"] = module_params["description"]

            # Add recurring interval configuration
            type_config["recurring"] = recurring

            # Add to the type data
            type_data = {sdk_type: type_config}
            break

    return type_data


def build_edl_data(module_params):
    """
    Build EDL data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing EDL configuration
    """
    # Extract basic parameters
    edl_data = {"name": module_params["name"]}

    # Add container (folder, snippet, device)
    for container in ["folder", "snippet", "device"]:
        if module_params.get(container):
            edl_data[container] = module_params[container]

    # Build recurring data
    recurring = build_recurring_data(module_params)

    # Build type data
    type_data = build_edl_type_data(module_params, recurring)

    if type_data:
        edl_data["type"] = type_data

    return edl_data


def is_container_specified(edl_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        edl_data (dict): EDL parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [edl_data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def is_edl_type_specified(module_params):
    """
    Check if exactly one EDL type is specified.

    Args:
        module_params (dict): Module parameters

    Returns:
        bool: True if exactly one EDL type is specified, False otherwise
    """
    edl_types = [
        module_params.get(edl_type)
        for edl_type in ["ip_list", "domain_list", "url_list", "imsi_list", "imei_list"]
    ]
    return sum(edl_type is not None for edl_type in edl_types) == 1


def is_recurring_interval_specified(module_params):
    """
    Check if exactly one recurring interval is specified.

    Args:
        module_params (dict): Module parameters

    Returns:
        bool: True if exactly one recurring interval is specified, False otherwise
    """
    intervals = [
        module_params.get(interval)
        for interval in ["five_minute", "hourly", "daily", "weekly", "monthly"]
    ]
    return sum(interval is not None for interval in intervals) == 1


def get_existing_edl(client, edl_data):
    """
    Attempt to fetch an existing external dynamic list.

    Args:
        client: SCM client instance
        edl_data (dict): EDL parameters to search for

    Returns:
        tuple: (bool, object) indicating if EDL exists and the EDL object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if container in edl_data and edl_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in edl_data:
            return False, None

        # Fetch the EDL using the appropriate container
        existing = client.external_dynamic_list.fetch(
            name=edl_data["name"], **{container_type: edl_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def needs_update(existing, new_data):
    """
    Determine if the external dynamic list needs to be updated by comparing
    the existing object with new data.

    Args:
        existing: Existing EDL object from the SCM API
        new_data (dict): EDL parameters with desired state from Ansible module

    Returns:
        (bool, dict): Tuple containing:
            - bool: Whether an update is needed
            - dict: Update data for the EDL
    """
    # Start with basic fields from existing EDL
    update_data = {
        "id": str(existing.id),
        "name": existing.name,
    }

    # Add the container field (folder, snippet, or device)
    for container in ["folder", "snippet", "device"]:
        container_value = getattr(existing, container, None)
        if container_value is not None:
            update_data[container] = container_value

    # Extract type information from existing EDL
    existing_type = None
    existing_type_config = None

    if existing.type:
        for type_key in ["ip", "domain", "url", "imsi", "imei"]:
            type_value = getattr(existing.type, type_key, None)
            if type_value is not None:
                existing_type = type_key
                existing_type_config = type_value
                break

    # Extract type information from new data
    new_type = None
    new_type_config = None

    if "type" in new_data and new_data["type"]:
        for type_key, type_config in new_data["type"].items():
            new_type = type_key
            new_type_config = type_config
            break

    changed = False

    # If types match, compare configurations
    if existing_type == new_type and existing_type_config and new_type_config:
        # Create a base configuration from existing data
        type_config = {}

        # Copy existing configuration attributes
        for attr in ["url", "description", "certificate_profile", "expand_domain"]:
            if hasattr(existing_type_config, attr):
                type_config[attr] = getattr(existing_type_config, attr)

        # Copy exception_list as a special case
        if hasattr(existing_type_config, "exception_list"):
            type_config["exception_list"] = (
                existing_type_config.exception_list if existing_type_config.exception_list else []
            )

        # Copy auth information
        if hasattr(existing_type_config, "auth") and existing_type_config.auth:
            type_config["auth"] = {
                "username": existing_type_config.auth.username,
                "password": existing_type_config.auth.password,
            }

        # Copy recurring configuration
        if hasattr(existing_type_config, "recurring") and existing_type_config.recurring:
            recurring_type = None
            recurring_config = None

            for rec_type in ["five_minute", "hourly", "daily", "weekly", "monthly"]:
                if hasattr(existing_type_config.recurring, rec_type):
                    recurring_type = rec_type
                    recurring_config = getattr(existing_type_config.recurring, rec_type)
                    break

            if recurring_type:
                type_config["recurring"] = {recurring_type: {}}

                # Add specific configuration for daily, weekly, monthly
                if recurring_type == "daily" and hasattr(recurring_config, "at"):
                    type_config["recurring"][recurring_type] = {"at": recurring_config.at}
                elif recurring_type == "weekly" and hasattr(recurring_config, "day_of_week"):
                    type_config["recurring"][recurring_type] = {
                        "day_of_week": recurring_config.day_of_week,
                        "at": recurring_config.at if hasattr(recurring_config, "at") else "00",
                    }
                elif recurring_type == "monthly" and hasattr(recurring_config, "day_of_month"):
                    type_config["recurring"][recurring_type] = {
                        "day_of_month": recurring_config.day_of_month,
                        "at": recurring_config.at if hasattr(recurring_config, "at") else "00",
                    }

        # Checking if there are actual changes in the configuration
        # Always set the base configuration
        update_data["type"] = {existing_type: type_config}

        # Check if URL has changed
        if "url" in new_type_config and type_config.get("url") != new_type_config["url"]:
            changed = True

        # Check if description has changed
        if (
            "description" in new_type_config
            and type_config.get("description") != new_type_config["description"]
        ):
            changed = True

        # Check if certificate_profile has changed
        if (
            "certificate_profile" in new_type_config
            and type_config.get("certificate_profile") != new_type_config["certificate_profile"]
        ):
            changed = True

        # Check if expand_domain has changed (for domain type)
        if (
            "expand_domain" in new_type_config
            and type_config.get("expand_domain") != new_type_config["expand_domain"]
        ):
            changed = True

        # Compare exception_list if provided
        if "exception_list" in new_type_config:
            existing_exceptions = set(type_config.get("exception_list", []))
            new_exceptions = set(new_type_config["exception_list"])
            if existing_exceptions != new_exceptions:
                changed = True

        # Check recurring schedule changes
        if "recurring" in new_type_config:
            # Get the type of recurring schedule in new data
            new_rec_type = next(iter(new_type_config["recurring"]))

            # Check if the schedule type is different
            if "recurring" not in type_config or new_rec_type not in type_config["recurring"]:
                changed = True
            # For detailed schedules, check their specific properties
            elif new_rec_type in ["daily", "weekly", "monthly"]:
                if type_config["recurring"].get(new_rec_type) != new_type_config["recurring"].get(
                    new_rec_type
                ):
                    changed = True

    # If types don't match or new configuration is provided but not existing, use new data
    elif new_type and new_type_config:
        update_data["type"] = {new_type: new_type_config}
        changed = True

    return changed, update_data


def main():
    """
    Main execution path for the external dynamic lists module.

    This module provides functionality to create, update, and delete external dynamic lists
    in the SCM (Strata Cloud Manager) system with various list types and update intervals.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=ExternalDynamicListsSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["ip_list", "domain_list", "url_list", "imsi_list", "imei_list"],
            ["folder", "snippet", "device"],
            ["five_minute", "hourly", "daily", "weekly", "monthly"],
        ],
        required_one_of=[["folder", "snippet", "device"]],
        required_if=[
            [
                "state",
                "present",
                ["ip_list", "domain_list", "url_list", "imsi_list", "imei_list"],
                True,
            ],
            ["state", "present", ["five_minute", "hourly", "daily", "weekly", "monthly"], True],
        ],
    )

    result = {"changed": False, "external_dynamic_list": None}

    try:
        client = get_scm_client(module)

        # Validate input parameters
        if module.params["state"] == "present":
            if not is_edl_type_specified(module.params):
                module.fail_json(
                    msg="Exactly one of 'ip_list', 'domain_list', 'url_list', 'imsi_list', or 'imei_list' must be provided."
                )

            if not is_recurring_interval_specified(module.params):
                module.fail_json(
                    msg="Exactly one recurring interval ('five_minute', 'hourly', 'daily', 'weekly', 'monthly') must be provided."
                )

        # Build EDL data
        edl_data = build_edl_data(module.params)

        # Validate container is specified
        if not is_container_specified(edl_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Special handling for certificate_profile and exception_list in all EDL types
        if "type" in edl_data:
            for edl_type in ["ip", "domain", "url", "imsi", "imei"]:
                if edl_type in edl_data["type"]:
                    # Remove certificate_profile if it's not provided (to avoid API validation issues)
                    if (
                        "certificate_profile" in edl_data["type"][edl_type]
                        and not edl_data["type"][edl_type]["certificate_profile"]
                    ):
                        del edl_data["type"][edl_type]["certificate_profile"]

                    # Remove empty exception_list to avoid API validation issues
                    if "exception_list" in edl_data["type"][edl_type]:
                        if not edl_data["type"][edl_type]["exception_list"]:
                            del edl_data["type"][edl_type]["exception_list"]

        # Get existing EDL
        exists, existing_edl = get_existing_edl(client, edl_data)

        if module.params["state"] == "present":
            if not exists:
                # Create new EDL
                if not module.check_mode:
                    # Check the specific path of certificate_profile
                    if (
                        "type" in edl_data
                        and "url" in edl_data["type"]
                        and "certificate_profile" in edl_data["type"]["url"]
                    ):
                        # Ensure certificate_profile is a string
                        if edl_data["type"]["url"]["certificate_profile"] is None:
                            edl_data["type"]["url"]["certificate_profile"] = "None"

                    try:
                        new_edl = client.external_dynamic_list.create(data=edl_data)
                        result["external_dynamic_list"] = serialize_response(new_edl)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"An external dynamic list with name '{edl_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        # Add more detailed error output
                        module.fail_json(
                            msg=f"Invalid external dynamic list data: {str(e)}",
                            edl_data=str(edl_data),
                        )
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_edl, edl_data)

                if need_update:
                    if not module.check_mode:
                        # Special handling for certificate_profile and exception_list in all EDL types
                        if "type" in update_data:
                            for edl_type in ["ip", "domain", "url", "imsi", "imei"]:
                                if edl_type in update_data["type"]:
                                    # Remove certificate_profile if it's not provided (to avoid API validation issues)
                                    if (
                                        "certificate_profile" in update_data["type"][edl_type]
                                        and not update_data["type"][edl_type]["certificate_profile"]
                                    ):
                                        del update_data["type"][edl_type]["certificate_profile"]

                                    # Remove empty exception_list to avoid API validation issues
                                    if "exception_list" in update_data["type"][edl_type]:
                                        if not update_data["type"][edl_type]["exception_list"]:
                                            del update_data["type"][edl_type]["exception_list"]

                        # Create update model with complete object data
                        update_model = ExternalDynamicListsUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_edl = client.external_dynamic_list.update(update_model)
                        result["external_dynamic_list"] = serialize_response(updated_edl)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["external_dynamic_list"] = serialize_response(existing_edl)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.external_dynamic_list.delete(str(existing_edl.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
