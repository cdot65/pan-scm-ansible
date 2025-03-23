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
Ansible module for gathering information about address group objects in SCM.

This module provides functionality to retrieve information about address group objects
in the SCM (Strata Cloud Manager) system with various filtering options.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError

DOCUMENTATION = r"""
---
module: address_group_info

short_description: Gather information about address group objects in SCM.

version_added: "0.1.0"

description:
    - Gather information about address group objects within Strata Cloud Manager (SCM).
    - Supports retrieving a specific address group by name or listing address groups with various filters.
    - Provides additional client-side filtering capabilities for exact matches and exclusions.
    - Returns detailed information about each address group object.
    - This is an info module that only retrieves information and does not modify anything.

options:
    name:
        description: The name of a specific address group object to retrieve.
        required: false
        type: str
    gather_subset:
        description: 
            - Determines which information to gather about address groups.
            - C(all) gathers everything.
            - C(config) is the default which retrieves basic configuration.
        type: list
        elements: str
        default: ['config']
        choices: ['all', 'config']
    folder:
        description: Filter address groups by folder container.
        required: false
        type: str
    snippet:
        description: Filter address groups by snippet container.
        required: false
        type: str
    device:
        description: Filter address groups by device container.
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
    types:
        description: Filter by address group types.
        required: false
        type: list
        elements: str
        choices: ["static", "dynamic"]
    values:
        description: Filter by address group values (static members or dynamic filter).
        required: false
        type: list
        elements: str
    tags:
        description: Filter by tags.
        required: false
        type: list
        elements: str
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
- name: Gather Address Group Information in Strata Cloud Manager
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

    - name: Get information about a specific address group
      cdot65.scm.address_group_info:
        provider: "{{ provider }}"
        name: "web-servers"
        folder: "Texas"
      register: address_group_info

    - name: List all address group objects in a folder
      cdot65.scm.address_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_address_groups

    - name: List only static address group objects
      cdot65.scm.address_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
        types: ["static"]
      register: static_address_groups

    - name: List address groups with specific tags
      cdot65.scm.address_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
        tags: ["Production", "Web"]
      register: tagged_address_groups

    - name: List address groups with exact match and exclusions
      cdot65.scm.address_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
        exact_match: true
        exclude_folders: ["All"]
        exclude_snippets: ["default"]
      register: filtered_address_groups
"""

RETURN = r"""
address_groups:
    description: List of address group objects matching the filter criteria (returned when name is not specified).
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "web-servers"
        description: "Web server group"
        static: ["web1", "web2"]
        folder: "Texas"
        tag: ["Web", "Production"]
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "app-servers"
        description: "Application server group"
        dynamic:
          filter: "'app' and 'server'"
        folder: "Texas"
        tag: ["App", "Production"]
address_group:
    description: Information about the requested address group (returned when name is specified).
    returned: success, when name is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "web-servers"
        description: "Web server group"
        static: ["web1", "web2"]
        folder: "Texas"
        tag: ["Web", "Production"]
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

    # Convert "tags" parameter to "tags" for SDK
    if module_params.get("tags") is not None:
        filter_params["tags"] = module_params["tags"]

    # Add other filter parameters
    for param in ["types", "values"]:
        if module_params.get(param) is not None:
            filter_params[param] = module_params[param]

    return container_params, filter_params


def main():
    """
    Main execution path for the address_group_info module.

    This module provides functionality to gather information about address group objects
    in the SCM (Strata Cloud Manager) system with various filtering options.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type="str", required=False),
            gather_subset=dict(
                type="list", elements="str", default=["config"], choices=["all", "config"]
            ),
            folder=dict(type="str", required=False),
            snippet=dict(type="str", required=False),
            device=dict(type="str", required=False),
            exact_match=dict(type="bool", required=False, default=False),
            exclude_folders=dict(type="list", elements="str", required=False),
            exclude_snippets=dict(type="list", elements="str", required=False),
            exclude_devices=dict(type="list", elements="str", required=False),
            types=dict(type="list", elements="str", required=False, choices=["static", "dynamic"]),
            values=dict(type="list", elements="str", required=False),
            tags=dict(type="list", elements="str", required=False),
            provider=dict(
                type="dict",
                required=True,
                options=dict(
                    client_id=dict(type="str", required=True),
                    client_secret=dict(type="str", required=True, no_log=True),
                    tsg_id=dict(type="str", required=True),
                    log_level=dict(type="str", required=False, default="INFO"),
                ),
            ),
        ),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        # Only require a container if we're not provided with a specific name
        required_if=[["name", None, ["folder", "snippet", "device"], True]],
    )

    result = {}

    try:
        client = get_scm_client(module)

        # Check if we're fetching a specific address group by name
        if module.params.get("name"):
            name = module.params["name"]
            container_params = {}

            # Get the container param
            for container in ["folder", "snippet", "device"]:
                if module.params.get(container):
                    container_params[container] = module.params[container]

            try:
                # Fetch a specific address group
                address_group = client.address_group.fetch(name=name, **container_params)

                # Serialize response for Ansible output
                result["address_group"] = serialize_response(address_group)

            except ObjectNotPresentError:
                module.fail_json(
                    msg=f"Address group with name '{name}' not found in {list(container_params.keys())[0]} '{list(container_params.values())[0]}'"
                )
            except (MissingQueryParameterError, InvalidObjectError) as e:
                module.fail_json(msg=str(e))

        else:
            # List address groups with filtering
            container_params, filter_params = build_filter_params(module.params)

            try:
                address_groups = client.address_group.list(**container_params, **filter_params)

                # Serialize response for Ansible output
                result["address_groups"] = [
                    serialize_response(addr_group) for addr_group in address_groups
                ]

            except MissingQueryParameterError as e:
                module.fail_json(msg=f"Missing required parameter: {str(e)}")
            except InvalidObjectError as e:
                module.fail_json(msg=f"Invalid filter parameters: {str(e)}")

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
