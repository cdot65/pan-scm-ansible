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
Ansible module for gathering information about service group objects in SCM.

This module provides functionality to retrieve information about service group objects
in the SCM (Strata Cloud Manager) system with various filtering options.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.service_group_info import (
    ServiceGroupInfoSpec,
)
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)

from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError

DOCUMENTATION = r"""
---
module: service_group_info

short_description: Gather information about service group objects in SCM.

version_added: "0.1.0"

description:
    - Gather information about service group objects within Strata Cloud Manager (SCM).
    - Supports retrieving a specific service group by name or listing service groups with various filters.
    - Provides additional client-side filtering capabilities for exact matches and exclusions.
    - Returns detailed information about each service group object.
    - This is an info module that only retrieves information and does not modify anything.

options:
    name:
        description: The name of a specific service group object to retrieve.
        required: false
        type: str
    gather_subset:
        description: 
            - Determines which information to gather about service groups.
            - C(all) gathers everything.
            - C(config) is the default which retrieves basic configuration.
        type: list
        elements: str
        default: ['config']
        choices: ['all', 'config']
    folder:
        description: Filter service groups by folder container.
        required: false
        type: str
    snippet:
        description: Filter service groups by snippet container.
        required: false
        type: str
    device:
        description: Filter service groups by device container.
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
    members:
        description: Filter by service members contained in the groups.
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
- name: Gather Service Group Information in Strata Cloud Manager
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

    - name: Get information about a specific service group
      cdot65.scm.service_group_info:
        provider: "{{ provider }}"
        name: "web-services"
        folder: "Texas"
      register: service_group_info

    - name: List all service group objects in a folder
      cdot65.scm.service_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_service_groups

    - name: List service groups containing a specific member
      cdot65.scm.service_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
        members: ["HTTPS"]
      register: https_service_groups

    - name: List service groups with specific tags
      cdot65.scm.service_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
        tags: ["Production", "Web"]
      register: tagged_service_groups

    - name: List service groups with exact match and exclusions
      cdot65.scm.service_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
        exact_match: true
        exclude_folders: ["All"]
        exclude_snippets: ["default"]
      register: filtered_service_groups
"""

RETURN = r"""
service_groups:
    description: List of service group objects matching the filter criteria (returned when name is not specified).
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "web-services"
        members: ["HTTPS", "SSH", "web-custom-service"]
        folder: "Texas"
        tag: ["Web", "Production"]
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "database-services"
        members: ["SQL", "mysql-custom", "Oracle"]
        folder: "Texas"
        tag: ["Database", "Production"]
service_group:
    description: Information about the requested service group (returned when name is specified).
    returned: success, when name is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "web-services"
        members: ["HTTPS", "SSH", "web-custom-service"]
        folder: "Texas"
        tag: ["Web", "Production"]
"""


def build_filter_params(module_params):
    """
    Build filter parameters dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        tuple: (container_params, filter_params)
            container_params: Dictionary containing container parameters
            filter_params: Dictionary containing filter parameters
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

    # Convert "tags" parameter for SDK
    if module_params.get("tags") is not None:
        filter_params["tags"] = module_params["tags"]

    # Convert "members" parameter for SDK
    if module_params.get("members") is not None:
        filter_params["members"] = module_params["members"]

    return container_params, filter_params


def main():
    """
    Main execution path for the service_group_info module.

    This module provides functionality to gather information about service group objects
    in the SCM (Strata Cloud Manager) system with various filtering options.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=ServiceGroupInfoSpec.spec(),
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
                result["service_group"] = {
                    "id": "00000000-0000-0000-0000-000000000000",
                    "name": module.params.get("name"),
                    "members": ["example-service-1", "example-service-2"],
                    "folder": module.params.get("folder"),
                    "snippet": module.params.get("snippet"),
                    "device": module.params.get("device"),
                    "tag": ["example-tag"],
                }
            else:
                result["service_groups"] = [
                    {
                        "id": "00000000-0000-0000-0000-000000000000",
                        "name": "example-service-group",
                        "members": ["example-service-1", "example-service-2"],
                        "folder": module.params.get("folder"),
                        "snippet": module.params.get("snippet"),
                        "device": module.params.get("device"),
                        "tag": ["example-tag"],
                    }
                ]
            module.exit_json(**result)
            return

        client = get_scm_client(module)

        # Check if we're fetching a specific service group by name
        if module.params.get("name"):
            name = module.params["name"]
            container_params = {}

            # Get the container param
            for container in ["folder", "snippet", "device"]:
                if module.params.get(container):
                    container_params[container] = module.params[container]

            try:
                # Fetch a specific service group
                service_group = client.service_group.fetch(name=name, **container_params)

                # Serialize response for Ansible output
                result["service_group"] = serialize_response(service_group)

            except ObjectNotPresentError:
                module.fail_json(
                    msg=f"Service group with name '{name}' not found in {list(container_params.keys())[0]} '{list(container_params.values())[0]}'"
                )
            except (MissingQueryParameterError, InvalidObjectError) as e:
                module.fail_json(msg=str(e))

        else:
            # List service groups with filtering
            container_params, filter_params = build_filter_params(module.params)

            try:
                service_groups = client.service_group.list(**container_params, **filter_params)

                # Serialize response for Ansible output
                result["service_groups"] = [serialize_response(sg) for sg in service_groups]

            except MissingQueryParameterError as e:
                module.fail_json(msg=f"Missing required parameter: {str(e)}")
            except InvalidObjectError as e:
                module.fail_json(msg=f"Invalid filter parameters: {str(e)}")

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
