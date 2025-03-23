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
Ansible module for managing tag objects in SCM.

This module provides functionality to create, update, and delete tag objects
in the SCM (Strata Cloud Manager) system. It handles tag attributes
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.tag import TagSpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import (
    InvalidObjectError,
    MissingQueryParameterError,
    NameNotUniqueError,
    ObjectNotPresentError,
    ReferenceNotZeroError,
)
from scm.models.objects.tag import TagUpdateModel

DOCUMENTATION = r"""
---
module: tag

short_description: Manage tag objects in SCM.

version_added: "0.1.0"

description:
    - Manage tag objects within Strata Cloud Manager (SCM).
    - Supports creation, modification, and deletion of tag objects.
    - Ensures proper validation of tag attributes including color values.
    - Ensures that exactly one of 'folder', 'snippet', or 'device' is provided.

options:
    name:
        description: The name of the tag (max 63 chars).
        required: true
        type: str
    color:
        description: Color associated with the tag.
        required: false
        type: str
        choices:
            - Azure Blue
            - Black
            - Blue
            - Blue Gray
            - Blue Violet
            - Brown
            - Burnt Sienna
            - Cerulean Blue
            - Chestnut
            - Cobalt Blue
            - Copper
            - Cyan
            - Forest Green
            - Gold
            - Gray
            - Green
            - Lavender
            - Light Gray
            - Light Green
            - Lime
            - Magenta
            - Mahogany
            - Maroon
            - Medium Blue
            - Medium Rose
            - Medium Violet
            - Midnight Blue
            - Olive
            - Orange
            - Orchid
            - Peach
            - Purple
            - Red
            - Red Violet
            - Red-Orange
            - Salmon
            - Thistle
            - Turquoise Blue
            - Violet Blue
            - Yellow
            - Yellow-Orange
    comments:
        description: Comments for the tag (max 1023 chars).
        required: false
        type: str
    folder:
        description: The folder where the tag is stored (max 64 chars).
        required: false
        type: str
    snippet:
        description: The configuration snippet for the tag (max 64 chars).
        required: false
        type: str
    device:
        description: The device where the tag is configured (max 64 chars).
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
                no_log: True
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
        description: Desired state of the tag object.
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
- name: Manage Tag Objects in Strata Cloud Manager
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
    - name: Create a new tag
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "Production"
        color: "Blue"
        comments: "Production environment tag"
        folder: "Texas"
        state: "present"

    - name: Update tag color
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "Production"
        color: "Red"
        folder: "Texas"
        state: "present"

    - name: Create a tag in a snippet
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "Development"
        color: "Green"
        comments: "Development environment tag"
        snippet: "Common"
        state: "present"

    - name: Create a tag for a device
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "Device-Tag"
        color: "Orange"
        device: "fw01"
        state: "present"

    - name: Remove tag
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "Production"
        folder: "Texas"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
tag:
    description: Details about the tag object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Production"
        color: "Blue"
        comments: "Production environment tag"
        folder: "Texas"
"""


def build_tag_data(module_params):
    """
    Build tag data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant tag parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(tag_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        tag_data (dict): Tag parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [tag_data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the tag object needs to be updated.

    Args:
        existing: Existing tag object from the SCM API
        params (dict): Tag parameters with desired state from Ansible module

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
    for param in ["color", "comments"]:
        # Set the current value as default
        current_value = getattr(existing, param, None)
        update_data[param] = current_value

        # If user provided a new value, use it and check if it's different
        if param in params and params[param] is not None:
            if current_value != params[param]:
                update_data[param] = params[param]
                changed = True

    return changed, update_data


def get_existing_tag(client, tag_data):
    """
    Attempt to fetch an existing tag object.

    Args:
        client: SCM client instance
        tag_data (dict): Tag parameters to search for

    Returns:
        tuple: (bool, object) indicating if tag exists and the tag object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if container in tag_data and tag_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in tag_data:
            return False, None

        # Fetch the tag using the appropriate container
        existing = client.tag.fetch(
            name=tag_data["name"], **{container_type: tag_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError, MissingQueryParameterError):
        return False, None


def main():
    """
    Main execution path for the tag object module.

    This module provides functionality to create, update, and delete tag objects
    in the SCM (Strata Cloud Manager) system. It handles tag attributes
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=TagSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        required_one_of=[["folder", "snippet", "device"]],
    )

    result = {"changed": False, "tag": None}

    try:
        client = get_scm_client(module)
        tag_data = build_tag_data(module.params)

        # Validate container is specified
        if not is_container_specified(tag_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # Get existing tag
        exists, existing_tag = get_existing_tag(client, tag_data)

        if module.params["state"] == "present":
            if not exists:
                # Create new tag
                if not module.check_mode:
                    try:
                        new_tag = client.tag.create(data=tag_data)
                        result["tag"] = serialize_response(new_tag)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(msg=f"A tag with name '{tag_data['name']}' already exists")
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid tag data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_tag, tag_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = TagUpdateModel(**update_data)

                        # Perform update with complete object
                        updated_tag = client.tag.update(update_model)
                        result["tag"] = serialize_response(updated_tag)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["tag"] = serialize_response(existing_tag)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    try:
                        client.tag.delete(str(existing_tag.id))
                        result["changed"] = True
                    except ReferenceNotZeroError:
                        module.fail_json(
                            msg=f"Tag '{tag_data['name']}' is still in use and cannot be deleted"
                        )
                else:
                    result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
