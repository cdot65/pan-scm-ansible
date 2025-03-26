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
Ansible module for managing URL categories in SCM.

This module provides functionality to create, update, and delete URL categories
in the SCM (Strata Cloud Manager) system. It handles different category types
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.url_categories import (
    URLCategoriesSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.security import URLCategoriesUpdateModel

DOCUMENTATION = r"""
---
module: url_categories

short_description: Manage URL categories in SCM.

version_added: "0.1.0"

description:
    - Manage URL categories within Strata Cloud Manager (SCM).
    - Create, update, and delete URL category objects of various types.
    - Ensures that exactly one container type (folder, snippet, device) is provided.

options:
    name:
        description: The name of the URL category object.
        required: true
        type: str
    description:
        description: Description of the URL category object.
        required: false
        type: str
    list:
        description: List of URLs or categories associated with the URL category object.
        required: false
        type: list
        elements: str
    type:
        description: Type of URL category (URL List or Category Match).
        required: false
        type: str
        choices: ["URL List", "Category Match"]
        default: "URL List"
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
        description: Desired state of the URL category object.
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
- name: Manage URL Categories in Strata Cloud Manager
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

    - name: Create a URL category with URL List type
      cdot65.scm.url_categories:
        provider: "{{ provider }}"
        name: "Malicious_URLs"
        description: "List of known malicious URLs"
        type: "URL List"
        list: ["malware.example.com", "phishing.example.net"]
        folder: "Security"
        state: "present"

    - name: Create a URL category with Category Match type
      cdot65.scm.url_categories:
        provider: "{{ provider }}"
        name: "Social_Media"
        description: "Category for social media sites"
        type: "Category Match"
        list: ["social-networking"]
        folder: "Security"
        state: "present"

    - name: Update a URL category with new URLs
      cdot65.scm.url_categories:
        provider: "{{ provider }}"
        name: "Malicious_URLs"
        description: "Updated list of known malicious URLs"
        type: "URL List"
        list: ["malware.example.com", "phishing.example.net", "ransomware.example.org"]
        folder: "Security"
        state: "present"

    - name: Delete URL category
      cdot65.scm.url_categories:
        provider: "{{ provider }}"
        name: "Social_Media"
        folder: "Security"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
url_category:
    description: Details about the URL category object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Malicious_URLs"
        description: "List of known malicious URLs"
        type: "URL List"
        list: ["malware.example.com", "phishing.example.net"]
        folder: "Security"
"""


def build_url_category_data(module_params):
    """
    Build URL category data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant URL category parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(url_category_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        url_category_data (dict): URL category parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [url_category_data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the URL category object needs to be updated.

    Args:
        existing: Existing URL category object from the SCM API
        params (dict): URL category parameters with desired state from Ansible module

    Returns:
        (bool, dict): Tuple containing:
            - bool: Whether an update is needed
            - dict: Complete object data for update including all fields from the existing
                   object with any modifications from the params
    """
    changed = False

    # Start with a fresh update model using all fields from existing object
    update_data = {
        "id": str(existing.id),  # Convert UUID to string for Pydantic
        "name": existing.name,
    }

    # Add the container field (folder, snippet, or device)
    for container in ["folder", "snippet", "device"]:
        container_value = getattr(existing, container, None)
        if container_value is not None:
            update_data[container] = container_value

    # Check each parameter that can be updated
    for param in ["description", "type"]:
        # Set the current value as default
        current_value = getattr(existing, param, None)
        update_data[param] = current_value

        # If user provided a new value, use it and check if it's different
        if param in params and params[param] is not None:
            if current_value != params[param]:
                update_data[param] = params[param]
                changed = True

    # Handle the list parameter specially (like tag in address module)
    current_list = getattr(existing, "list", None)
    # If existing list is None, use empty list to avoid Pydantic validation error
    update_data["list"] = [] if current_list is None else current_list

    # If user provided a list value, use it and check if it's different
    if "list" in params and params["list"] is not None:
        if sorted(current_list) != sorted(params["list"]):
            update_data["list"] = params["list"]
            changed = True

    return changed, update_data


def add_url_categories_to_client(client):
    """
    Add the URLCategories class to the SCM client.

    This is a temporary solution until the SDK includes the URL categories functionality.

    Args:
        client: SCM client instance

    Returns:
        None
    """
    # Import the URLCategories class from the SDK module
    from scm.config.security.url_categories import URLCategories

    # Add the url_categories attribute to the client
    client.url_categories = URLCategories(client)

    return client


def get_existing_url_category(client, url_category_data):
    """
    Attempt to fetch an existing URL category object.

    Args:
        client: SCM client instance
        url_category_data (dict): URL category parameters to search for

    Returns:
        tuple: (bool, object) indicating if URL category exists and the URL category object if found
    """
    try:
        # Make sure the client has the url_categories functionality
        client = add_url_categories_to_client(client)

        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if container in url_category_data and url_category_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in url_category_data:
            return False, None

        # Fetch the URL category using the appropriate container
        existing = client.url_categories.fetch(
            name=url_category_data["name"], **{container_type: url_category_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the URL categories module.

    This module provides functionality to create, update, and delete URL category objects
    in the SCM (Strata Cloud Manager) system with support for check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=URLCategoriesSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet", "device"],
        ],
        required_one_of=[["folder", "snippet", "device"]],
        required_if=[["state", "present", ["list"], True]],
    )

    result = {"changed": False, "url_category": None}

    try:
        client = get_scm_client(module)

        # Add URL categories functionality to the client
        client = add_url_categories_to_client(client)

        url_category_data = build_url_category_data(module.params)

        # Validate container is specified
        if not is_container_specified(url_category_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing URL category
        exists, existing_url_category = get_existing_url_category(client, url_category_data)

        if module.params["state"] == "present":
            if not exists:
                # Create new URL category
                if not module.check_mode:
                    try:
                        new_url_category = client.url_categories.create(data=url_category_data)
                        result["url_category"] = serialize_response(new_url_category)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"A URL category with name '{url_category_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid URL category data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_url_category, url_category_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = URLCategoriesUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_url_category = client.url_categories.update(update_model)
                        result["url_category"] = serialize_response(updated_url_category)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["url_category"] = serialize_response(existing_url_category)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.url_categories.delete(str(existing_url_category.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
