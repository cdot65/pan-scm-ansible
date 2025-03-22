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
Ansible module for managing application objects in SCM.

This module provides functionality to create, update, and delete application objects
in the SCM (Strata Cloud Manager) system. It handles various application attributes
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.application import ApplicationSpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import serialize_response
from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.objects import ApplicationUpdateModel

DOCUMENTATION = r"""
---
module: application

short_description: Manage application objects in SCM.

version_added: "0.1.0"

description:
    - Manage application objects within Strata Cloud Manager (SCM).
    - Supports creation, modification, and deletion of application objects.
    - Ensures proper validation of application attributes.
    - Ensures that exactly one of 'folder' or 'snippet' is provided.

options:
    name:
        description: The name of the application.
        required: true
        type: str
    category:
        description: High-level category to which the application belongs.
        required: true
        type: str
    subcategory:
        description: Specific sub-category within the high-level category.
        required: true
        type: str
    technology:
        description: The underlying technology utilized by the application.
        required: true
        type: str
    risk:
        description: The risk level associated with the application (1-5).
        required: true
        type: int
    description:
        description: Description for the application.
        required: false
        type: str
    ports:
        description: List of TCP/UDP ports associated with the application.
        required: false
        type: list
        elements: str
    folder:
        description: The folder where the application configuration is stored.
        required: false
        type: str
    snippet:
        description: The configuration snippet for the application.
        required: false
        type: str
    evasive:
        description: Indicates if the application uses evasive techniques.
        required: false
        type: bool
        default: false
    pervasive:
        description: Indicates if the application is widely used.
        required: false
        type: bool
        default: false
    excessive_bandwidth_use:
        description: Indicates if the application uses excessive bandwidth.
        required: false
        type: bool
        default: false
    used_by_malware:
        description: Indicates if the application is commonly used by malware.
        required: false
        type: bool
        default: false
    transfers_files:
        description: Indicates if the application transfers files.
        required: false
        type: bool
        default: false
    has_known_vulnerabilities:
        description: Indicates if the application has known vulnerabilities.
        required: false
        type: bool
        default: false
    tunnels_other_apps:
        description: Indicates if the application tunnels other applications.
        required: false
        type: bool
        default: false
    prone_to_misuse:
        description: Indicates if the application is prone to misuse.
        required: false
        type: bool
        default: false
    no_certifications:
        description: Indicates if the application lacks certifications.
        required: false
        type: bool
        default: false
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
                no_log: true
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
        description: Desired state of the application object.
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
- name: Manage Application Objects in Strata Cloud Manager
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
    - name: Create a custom application
      cdot65.scm.application:
        provider: "{{ provider }}"
        name: "custom-app"
        category: "business-systems"
        subcategory: "database"
        technology: "client-server"
        risk: 3
        description: "Custom database application"
        ports:
          - "tcp/1521"
        folder: "Texas"
        transfers_files: true
        state: "present"

    - name: Update application risk level
      cdot65.scm.application:
        provider: "{{ provider }}"
        name: "custom-app"
        category: "business-systems"
        subcategory: "database"
        technology: "client-server"
        risk: 4
        folder: "Texas"
        has_known_vulnerabilities: true
        state: "present"

    - name: Remove application
      cdot65.scm.application:
        provider: "{{ provider }}"
        name: "custom-app"
        folder: "Texas"
        state: "absent"
"""

RETURN = r"""
application:
    description: Details about the application object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "custom-app"
        category: "business-systems"
        subcategory: "database"
        technology: "client-server"
        risk: 3
        folder: "Texas"
"""


def build_application_data(module_params):
    """
    Build application data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant application parameters
    """
    return {
        k: v for k, v in module_params.items() if k not in ["provider", "state"] and v is not None
    }


def is_container_specified(application_data):
    """
    Check if exactly one container type (folder, snippet) is specified.

    Args:
        application_data (dict): Application parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [application_data.get(container) for container in ["folder", "snippet"]]
    return sum(container is not None for container in containers) == 1


def needs_update(existing, params):
    """
    Determine if the application object needs to be updated.

    Args:
        existing: Existing application object from the SCM API
        params (dict): Application parameters with desired state from Ansible module

    Returns:
        (bool, dict): Tuple containing:
            - bool: Whether an update is needed
            - dict: Complete object data for update including all fields from the existing
                   object with any modifications from the params
    """
    changed = False
    
    # Start with a fresh update model using all fields from existing object
    update_data = {
        "id": existing.id,
        "name": existing.name
    }
    
    # Add the container field (folder or snippet)
    for container in ["folder", "snippet"]:
        container_value = getattr(existing, container, None)
        if container_value is not None:
            update_data[container] = container_value
    
    # Add required application fields
    required_fields = ["category", "subcategory", "technology", "risk"]
    for field in required_fields:
        current_value = getattr(existing, field, None)
        update_data[field] = current_value
        
        # If user provided a new value, use it and check if it's different
        if field in params and params[field] is not None:
            if current_value != params[field]:
                update_data[field] = params[field]
                changed = True
                
    # Add optional text fields
    optional_fields = ["description"]
    for field in optional_fields:
        current_value = getattr(existing, field, None)
        update_data[field] = current_value
        
        # If user provided a new value, use it and check if it's different
        if field in params and params[field] is not None:
            if current_value != params[field]:
                update_data[field] = params[field]
                changed = True
    
    # Add optional list fields
    list_fields = ["ports"]
    for field in list_fields:
        current_value = getattr(existing, field, None)
        update_data[field] = current_value if current_value is not None else []
        
        # If user provided a new value, use it and check if it's different
        if field in params and params[field] is not None:
            if current_value != params[field]:
                update_data[field] = params[field]
                changed = True
    
    # Add boolean fields
    boolean_fields = [
        "evasive", "pervasive", "excessive_bandwidth_use", "used_by_malware",
        "transfers_files", "has_known_vulnerabilities", "tunnels_other_apps",
        "prone_to_misuse", "no_certifications"
    ]
    
    for field in boolean_fields:
        current_value = getattr(existing, field, False)
        update_data[field] = current_value
        
        # If user provided a new value, use it and check if it's different
        if field in params and params[field] is not None:
            if current_value != params[field]:
                update_data[field] = params[field]
                changed = True

    return changed, update_data


def get_existing_application(client, application_data):
    """
    Attempt to fetch an existing application object.

    Args:
        client: SCM client instance
        application_data (dict): Application parameters to search for

    Returns:
        tuple: (bool, object) indicating if application exists and the application object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet"]:
            if container in application_data and application_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in application_data:
            return False, None

        # Fetch the application using the appropriate container
        existing = client.application.fetch(
            name=application_data["name"],
            **{container_type: application_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def main():
    """
    Main execution path for the application object module.

    This module provides functionality to create, update, and delete application objects
    in the SCM (Strata Cloud Manager) system. It handles various application attributes
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=ApplicationSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet"]
        ],
        required_one_of=[
            ["folder", "snippet"]
        ],
        required_if=[
            ['state', 'present', ['category', 'subcategory', 'technology', 'risk']]
        ]
    )

    result = {
        "changed": False,
        "application": None
    }

    try:
        client = get_scm_client(module)
        application_data = build_application_data(module.params)

        # Validate container is specified
        if not is_container_specified(application_data):
            module.fail_json(
                msg="Exactly one of 'folder' or 'snippet' must be provided."
            )

        # Get existing application
        exists, existing_application = get_existing_application(client, application_data)

        if module.params["state"] == "present":
            # Application attributes validation is handled by required_if in the AnsibleModule definition

            if not exists:
                # Create new application
                if not module.check_mode:
                    try:
                        new_application = client.application.create(data=application_data)
                        result["application"] = serialize_response(new_application)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(msg=f"An application with name '{application_data['name']}' already exists")
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid application data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_application, application_data)

                if need_update:
                    if not module.check_mode:
                        # Create update model with complete object data
                        update_model = ApplicationUpdateModel(**update_data)
                        
                        # Perform update with complete object
                        updated_application = client.application.update(update_model)
                        result["application"] = serialize_response(updated_application)
                        result["changed"] = True
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["application"] = serialize_response(existing_application)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.application.delete(str(existing_application.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
