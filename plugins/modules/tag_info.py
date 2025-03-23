# -*- coding: utf-8 -*-

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.

"""
Ansible module for gathering information about tag objects in SCM.

This module provides functionality to retrieve information about tag objects
in the SCM (Strata Cloud Manager) system with various filtering options.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.tag_info import TagInfoSpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError

DOCUMENTATION = r"""
---
module: tag_info

short_description: Gather information about tag objects in SCM.

version_added: "0.1.0"

description:
    - Gather information about tag objects within Strata Cloud Manager (SCM).
    - Supports retrieving a specific tag by name or listing tags with various filters.
    - Provides additional client-side filtering capabilities for exact matches and exclusions.
    - Returns detailed information about each tag object.
    - This is an info module that only retrieves information and does not modify anything.

options:
    name:
        description: The name of a specific tag object to retrieve.
        required: false
        type: str
    gather_subset:
        description: 
            - Determines which information to gather about tags.
            - C(all) gathers everything.
            - C(config) is the default which retrieves basic configuration.
        type: list
        elements: str
        default: ['config']
        choices: ['all', 'config']
    folder:
        description: Filter tags by folder container.
        required: false
        type: str
    snippet:
        description: Filter tags by snippet container.
        required: false
        type: str
    device:
        description: Filter tags by device container.
        required: false
        type: str
    exact_match:
        description: When True, only return objects defined exactly in the specified container.
        required: false
        type: bool
        default: false
    exclude_folders:
        description: List of folder names to exclude from results.
        required: false
        type: list
        elements: str
    exclude_snippets:
        description: List of snippet values to exclude from results.
        required: false
        type: list
        elements: str
    exclude_devices:
        description: List of device values to exclude from results.
        required: false
        type: list
        elements: str
    colors:
        description: Filter by tag colors.
        required: false
        type: list
        elements: str
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

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
---
- name: Gather Tag Information in Strata Cloud Manager
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

    - name: Get information about a specific tag
      cdot65.scm.tag_info:
        provider: "{{ provider }}"
        name: "Production"
        folder: "Texas"
      register: tag_info

    - name: List all tag objects in a folder
      cdot65.scm.tag_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_tags

    - name: List only tags with specific colors
      cdot65.scm.tag_info:
        provider: "{{ provider }}"
        folder: "Texas"
        colors: ["Red", "Blue"]
      register: colored_tags

    - name: List tags with exact match and exclusions
      cdot65.scm.tag_info:
        provider: "{{ provider }}"
        folder: "Texas"
        exact_match: true
        exclude_folders: ["All"]
        exclude_snippets: ["default"]
      register: filtered_tags
"""

RETURN = r"""
tags:
    description: List of tag objects matching the filter criteria (returned when name is not specified).
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Production"
        color: "Red"
        comments: "Production environment tag" 
        folder: "Texas"
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "Development"
        color: "Blue"
        comments: "Development environment tag"
        folder: "Texas"
tag:
    description: Information about the requested tag (returned when name is specified).
    returned: success, when name is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Production"
        color: "Red"
        comments: "Production environment tag"
        folder: "Texas"
"""


def build_filter_params(module_params):
    """
    Build filter parameters dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant filter parameters
    """
    # Container params
    container_params = {}
    for container in ["folder", "snippet", "device"]:
        if module_params.get(container) is not None:
            container_params[container] = module_params[container]

    # Filter params
    filter_params = {}
    for filter_param in ["exact_match", "exclude_folders", "exclude_snippets", "exclude_devices"]:
        if module_params.get(filter_param) is not None:
            filter_params[filter_param] = module_params[filter_param]

    # Convert "colors" parameter for SDK
    if module_params.get("colors") is not None:
        filter_params["colors"] = module_params["colors"]

    return container_params, filter_params


def main():
    """
    Main execution path for the tag_info module.

    This module provides functionality to gather information about tag objects
    in the SCM (Strata Cloud Manager) system with various filtering options.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=TagInfoSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        # Only require a container if we're not provided with a specific name
        required_if=[["name", None, ["folder", "snippet", "device"], True]],
    )

    result = {}

    try:
        # Handle check mode - return empty result since this is a read-only module
        if module.check_mode:
            if module.params.get("name"):
                result["tag"] = {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "name": module.params.get("name"),
                    "color": "Red",
                    "comments": "Check mode - no actual data retrieved",
                    "folder": module.params.get("folder"),
                    "snippet": module.params.get("snippet"),
                    "device": module.params.get("device"),
                }
            else:
                result["tags"] = [
                    {
                        "id": "00000000-0000-0000-0000-000000000000",
                        "name": "example-tag",
                        "color": "Red",
                        "comments": "Check mode - no actual data retrieved",
                        "folder": module.params.get("folder"),
                        "snippet": module.params.get("snippet"),
                        "device": module.params.get("device"),
                    }
                ]
            module.exit_json(**result)
            return

        client = get_scm_client(module)

        # Check if we're fetching a specific tag by name
        if module.params.get("name"):
            name = module.params["name"]
            container_params = {}

            # Get the container param
            for container in ["folder", "snippet", "device"]:
                if module.params.get(container):
                    container_params[container] = module.params[container]

            try:
                # Fetch a specific tag
                tag = client.tag.fetch(name=name, **container_params)

                # Serialize response for Ansible output
                result["tag"] = serialize_response(tag)

            except ObjectNotPresentError:
                module.fail_json(
                    msg=f"Tag with name '{name}' not found in {list(container_params.keys())[0]} '{list(container_params.values())[0]}'"
                )
            except (MissingQueryParameterError, InvalidObjectError) as e:
                module.fail_json(msg=str(e))

        else:
            # List tags with filtering
            container_params, filter_params = build_filter_params(module.params)

            try:
                tags = client.tag.list(**container_params, **filter_params)

                # Serialize response for Ansible output
                result["tags"] = [serialize_response(tag) for tag in tags]

            except MissingQueryParameterError as e:
                module.fail_json(msg=f"Missing required parameter: {str(e)}")
            except InvalidObjectError as e:
                module.fail_json(msg=f"Invalid filter parameters: {str(e)}")

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
