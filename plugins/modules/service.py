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
Ansible module for managing service objects in SCM.

This module provides functionality to create, update, and delete service objects
in the SCM (Strata Cloud Manager) system. It handles TCP and UDP services
and supports check mode operations.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text
from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.service import ServiceSpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from pydantic import ValidationError

from scm.exceptions import InvalidObjectError, NameNotUniqueError, ObjectNotPresentError
from scm.models.objects.service import ServiceUpdateModel

DOCUMENTATION = r"""
---
module: service

short_description: Manage service objects in SCM.

version_added: "0.1.0"

description:
    - Manage service objects within Strata Cloud Manager (SCM).
    - Create, update, and delete service objects for TCP or UDP protocols with port information.
    - Supports custom timeout overrides for protocols.
    - Ensures that exactly one protocol type (TCP or UDP) is configured.
    - Ensures that exactly one container type (folder, snippet, or device) is provided.

options:
    name:
        description: The name of the service (max 63 chars, must match pattern ^[a-zA-Z0-9_ \\.-]+$).
        required: true
        type: str
    protocol:
        description: Protocol configuration (TCP or UDP). Exactly one of 'tcp' or 'udp' must be provided.
        required: true
        type: dict
        suboptions:
            tcp:
                description: TCP protocol configuration with port information.
                type: dict
                suboptions:
                    port:
                        description: TCP port(s) for the service (e.g., '80' or '80,443,8080').
                        type: str
                        required: true
                    override:
                        description: Override settings for TCP timeouts.
                        type: dict
                        suboptions:
                            timeout:
                                description: Connection timeout in seconds.
                                type: int
                                default: 3600
                            halfclose_timeout:
                                description: Half-close timeout in seconds.
                                type: int
                                default: 120
                            timewait_timeout:
                                description: Time-wait timeout in seconds.
                                type: int
                                default: 15
            udp:
                description: UDP protocol configuration with port information.
                type: dict
                suboptions:
                    port:
                        description: UDP port(s) for the service (e.g., '53' or '67,68').
                        type: str
                        required: true
                    override:
                        description: Override settings for UDP timeouts.
                        type: dict
                        suboptions:
                            timeout:
                                description: Connection timeout in seconds.
                                type: int
                                default: 30
    description:
        description: Description of the service (max 1023 chars).
        required: false
        type: str
    tag:
        description: List of tags associated with the service (max 64 chars each).
        required: false
        type: list
        elements: str
    folder:
        description: The folder in which the service is defined (max 64 chars).
        required: false
        type: str
    snippet:
        description: The snippet in which the service is defined (max 64 chars).
        required: false
        type: str
    device:
        description: The device in which the service is defined (max 64 chars).
        required: false
        type: str
    provider:
        description: Authentication credentials for connecting to SCM.
        required: true
        type: dict
        suboptions:
            client_id:
                description: Client ID for authentication with SCM.
                required: true
                type: str
            client_secret:
                description: Client secret for authentication with SCM.
                required: true
                type: str
                no_log: true
            tsg_id:
                description: Tenant Service Group ID.
                required: true
                type: str
            log_level:
                description: Log level for the SDK (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                required: false
                type: str
                default: "INFO"
    state:
        description: Desired state of the service object.
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
- name: Manage Service Objects in Strata Cloud Manager
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
    - name: Create TCP service
      cdot65.scm.service:
        provider: "{{ provider }}"
        name: "web-service"
        protocol:
          tcp:
            port: "80,443"
            override:
              timeout: 30
              halfclose_timeout: 15
        description: "Web service ports"
        folder: "Texas"
        tag: ["Web", "Production"]
        state: "present"

    - name: Create UDP service
      cdot65.scm.service:
        provider: "{{ provider }}"
        name: "dns-service"
        protocol:
          udp:
            port: "53"
            override:
              timeout: 60
        description: "DNS service"
        folder: "Texas"
        tag: ["DNS", "Network"]
        state: "present"

    - name: Update service with new port and tag
      cdot65.scm.service:
        provider: "{{ provider }}"
        name: "web-service"
        protocol:
          tcp:
            port: "80,443,8080"
            override:
              timeout: 60
        description: "Updated web service ports"
        folder: "Texas"
        tag: ["Web", "Production", "Updated"]
        state: "present"

    - name: Remove service
      cdot65.scm.service:
        provider: "{{ provider }}"
        name: "web-service"
        folder: "Texas"
        state: "absent"
"""

RETURN = r"""
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
service:
    description: Details about the service object.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "web-service"
        description: "Web service ports"
        protocol:
          tcp:
            port: "80,443"
            override:
              timeout: 30
              halfclose_timeout: 15
        folder: "Texas"
        tag: ["Web", "Production"]
"""


def build_service_data(module_params):
    """
    Build service data dictionary from module parameters.

    Args:
        module_params (dict): Dictionary of module parameters

    Returns:
        dict: Filtered dictionary containing only relevant service parameters
    """
    service_data = {
        k: v
        for k, v in module_params.items()
        if k not in ["provider", "state", "protocol"] and v is not None
    }

    # Handle protocol separately to ensure proper structure
    if "protocol" in module_params and module_params["protocol"]:
        protocol_data = {}

        # Handle TCP protocol
        if (
            "tcp" in module_params["protocol"]
            and module_params["protocol"]["tcp"] is not None
            and module_params["protocol"]["tcp"].get("port")
        ):
            tcp_data = module_params["protocol"]["tcp"].copy()
            if "override" in tcp_data and tcp_data["override"]:
                tcp_data["override"] = {
                    k: v for k, v in tcp_data["override"].items() if v is not None
                }
            protocol_data["tcp"] = tcp_data

        # Handle UDP protocol
        elif (
            "udp" in module_params["protocol"]
            and module_params["protocol"]["udp"] is not None
            and module_params["protocol"]["udp"].get("port")
        ):
            udp_data = module_params["protocol"]["udp"].copy()
            if "override" in udp_data and udp_data["override"]:
                udp_data["override"] = {
                    k: v for k, v in udp_data["override"].items() if v is not None
                }
            protocol_data["udp"] = udp_data

        # Only add protocol if we have valid data
        if protocol_data:
            service_data["protocol"] = protocol_data

    return service_data


def is_container_specified(service_data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        service_data (dict): Service parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    containers = [service_data.get(container) for container in ["folder", "snippet", "device"]]
    return sum(container is not None for container in containers) == 1


def is_protocol_type_specified(service_data):
    """
    Check if exactly one protocol type (tcp, udp) is specified.

    Args:
        service_data (dict): Service parameters

    Returns:
        bool: True if exactly one protocol type is specified, False otherwise
    """
    if "protocol" not in service_data or not service_data["protocol"]:
        return False

    protocol_types = [service_data["protocol"].get(proto_type) for proto_type in ["tcp", "udp"]]
    return sum(proto_type is not None for proto_type in protocol_types) == 1


def get_existing_service(client, service_data):
    """
    Attempt to fetch an existing service object.

    Args:
        client: SCM client instance
        service_data (dict): Service parameters to search for

    Returns:
        tuple: (bool, object) indicating if service exists and the service object if found
    """
    try:
        # Determine which container type is specified
        container_type = None
        for container in ["folder", "snippet", "device"]:
            if container in service_data and service_data[container] is not None:
                container_type = container
                break

        if container_type is None or "name" not in service_data:
            return False, None

        # Fetch the service using the appropriate container
        existing = client.service.fetch(
            name=service_data["name"], **{container_type: service_data[container_type]}
        )
        return True, existing
    except (ObjectNotPresentError, InvalidObjectError):
        return False, None


def needs_update(existing, params):
    """
    Determine if the service object needs to be updated.

    Args:
        existing: Existing service object from the SCM API
        params (dict): Service parameters with desired state from Ansible module

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
    for param in ["description"]:
        # Set the current value as default
        current_value = getattr(existing, param, None)
        update_data[param] = current_value

        # If user provided a new value, use it and check if it's different
        if param in params and params[param] is not None:
            if current_value != params[param]:
                update_data[param] = params[param]
                changed = True

    # Handle the tag parameter specially due to Pydantic validation requirements
    # For tag, if it's None in the existing object, we need to set an empty list []
    current_tag = getattr(existing, "tag", None)
    # If existing tag is None, use empty list to avoid Pydantic validation error
    update_data["tag"] = [] if current_tag is None else current_tag

    # If user provided a tag value, use it and check if it's different
    if "tag" in params and params["tag"] is not None:
        if current_tag != params["tag"]:
            update_data["tag"] = params["tag"]
            changed = True

    # Handle protocol updates
    if "protocol" in params and params["protocol"] is not None:
        # Get current protocol type and data
        current_protocol = getattr(existing, "protocol", None)
        if current_protocol is not None:
            update_data["protocol"] = current_protocol.model_dump(exclude_unset=True)

            # Check if TCP protocol updates are needed
            if "tcp" in params["protocol"] and params["protocol"]["tcp"] is not None:
                if hasattr(current_protocol, "tcp") and current_protocol.tcp is not None:
                    # Check port updates
                    if (
                        "port" in params["protocol"]["tcp"]
                        and current_protocol.tcp.port != params["protocol"]["tcp"]["port"]
                    ):
                        update_data["protocol"]["tcp"]["port"] = params["protocol"]["tcp"]["port"]
                        changed = True

                    # Check override updates
                    if (
                        "override" in params["protocol"]["tcp"]
                        and params["protocol"]["tcp"]["override"] is not None
                    ):
                        current_override = getattr(current_protocol.tcp, "override", None)
                        current_override_dict = (
                            {}
                            if current_override is None
                            else {
                                k: getattr(current_override, k)
                                for k in ["timeout", "halfclose_timeout", "timewait_timeout"]
                                if getattr(current_override, k, None) is not None
                            }
                        )

                        for k, v in params["protocol"]["tcp"]["override"].items():
                            if v is not None and (
                                k not in current_override_dict or current_override_dict[k] != v
                            ):
                                if "override" not in update_data["protocol"]["tcp"]:
                                    update_data["protocol"]["tcp"]["override"] = {}
                                update_data["protocol"]["tcp"]["override"][k] = v
                                changed = True

            # Check if UDP protocol updates are needed
            elif "udp" in params["protocol"] and params["protocol"]["udp"] is not None:
                if hasattr(current_protocol, "udp") and current_protocol.udp is not None:
                    # Check port updates
                    if (
                        "port" in params["protocol"]["udp"]
                        and current_protocol.udp.port != params["protocol"]["udp"]["port"]
                    ):
                        update_data["protocol"]["udp"]["port"] = params["protocol"]["udp"]["port"]
                        changed = True

                    # Check override updates
                    if (
                        "override" in params["protocol"]["udp"]
                        and params["protocol"]["udp"]["override"] is not None
                    ):
                        current_override = getattr(current_protocol.udp, "override", None)
                        current_override_dict = (
                            {}
                            if current_override is None
                            else {"timeout": getattr(current_override, "timeout", None)}
                        )

                        if "timeout" in params["protocol"]["udp"]["override"]:
                            timeout_value = params["protocol"]["udp"]["override"]["timeout"]
                            if timeout_value is not None and (
                                "timeout" not in current_override_dict
                                or current_override_dict["timeout"] != timeout_value
                            ):
                                if "override" not in update_data["protocol"]["udp"]:
                                    update_data["protocol"]["udp"]["override"] = {}
                                update_data["protocol"]["udp"]["override"]["timeout"] = (
                                    timeout_value
                                )
                                changed = True

    return changed, update_data


def main():
    """
    Main execution path for the service object module.

    This module provides functionality to create, update, and delete service objects
    in the SCM (Strata Cloud Manager) system. It handles TCP and UDP services
    and supports check mode operations.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=ServiceSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[["folder", "snippet", "device"]],
        required_one_of=[["folder", "snippet", "device"]],
        required_if=[["state", "present", ["protocol"]]],
    )

    result = {"changed": False, "service": None}

    try:
        client = get_scm_client(module)
        service_data = build_service_data(module.params)

        # Validate container is specified
        if not is_container_specified(service_data):
            module.fail_json(
                msg="Exactly one of 'folder', 'snippet', or 'device' must be provided."
            )

        # When state is present, validate protocol is specified
        if module.params["state"] == "present" and not is_protocol_type_specified(service_data):
            module.fail_json(
                msg="For state='present', exactly one of 'tcp' or 'udp' must be provided in 'protocol'."
            )

        # Get existing service
        exists, existing_service = get_existing_service(client, service_data)

        if module.params["state"] == "present":
            if not exists:
                # Create new service
                if not module.check_mode:
                    try:
                        new_service = client.service.create(data=service_data)
                        result["service"] = serialize_response(new_service)
                        result["changed"] = True
                    except NameNotUniqueError:
                        module.fail_json(
                            msg=f"A service with name '{service_data['name']}' already exists"
                        )
                    except InvalidObjectError as e:
                        module.fail_json(msg=f"Invalid service data: {str(e)}")
                else:
                    result["changed"] = True
            else:
                # Compare and update if needed
                need_update, update_data = needs_update(existing_service, service_data)

                if need_update:
                    if not module.check_mode:
                        try:
                            # Create update model with complete object data
                            update_model = ServiceUpdateModel(**update_data)

                            # Perform update with complete object
                            updated_service = client.service.update(update_model)
                            result["service"] = serialize_response(updated_service)
                            result["changed"] = True
                        except ValidationError as e:
                            module.fail_json(msg=f"Service update validation error: {str(e)}")
                        except Exception as e:
                            module.fail_json(msg=f"Failed to update service: {str(e)}")
                    else:
                        result["changed"] = True
                else:
                    # No changes needed
                    result["service"] = serialize_response(existing_service)

        elif module.params["state"] == "absent":
            if exists:
                if not module.check_mode:
                    client.service.delete(str(existing_service.id))
                result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=to_text(e))


if __name__ == "__main__":
    main()
