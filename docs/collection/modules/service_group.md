# Service Group Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
    - [Creating Service Groups](#creating-service-groups)
    - [Updating Service Groups](#updating-service-groups)
    - [Deleting Service Groups](#deleting-service-groups)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `service_group` module provides functionality to manage service group objects in Palo Alto Networks' Strata Cloud
Manager. This module allows you to create, update, and delete service group objects, which combine multiple service
objects into a single reference that can be used in security policies, simplifying administration and policy management.

## Module Parameters

| Parameter              | Required | Type | Choices         | Default | Comments                                                     |
|------------------------|----------|------|-----------------|---------|--------------------------------------------------------------|
| name                   | yes      | str  |                 |         | The name of the service group (max 63 chars).                |
| members                | yes*     | list |                 |         | List of service objects that are members of this group.      |
| tag                    | no       | list |                 |         | List of tags associated with the service group.              |
| folder                 | no*      | str  |                 |         | The folder in which the resource is defined (max 64 chars).  |
| snippet                | no*      | str  |                 |         | The snippet in which the resource is defined (max 64 chars). |
| device                 | no*      | str  |                 |         | The device in which the resource is defined (max 64 chars).  |
| provider               | yes      | dict |                 |         | Authentication credentials.                                  |
| provider.client_id     | yes      | str  |                 |         | Client ID for authentication.                                |
| provider.client_secret | yes      | str  |                 |         | Client secret for authentication.                            |
| provider.tsg_id        | yes      | str  |                 |         | Tenant Service Group ID.                                     |
| provider.log_level     | no       | str  |                 | INFO    | Log level for the SDK.                                       |
| state                  | yes      | str  | present, absent |         | Desired state of the service group object.                   |

!!! note
- Members are required when state is present.
- Exactly one container type (`folder`, `snippet`, or `device`) must be provided.
- All service objects in the members list must already exist in the system.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Creating Service Groups

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a service group for web services
  cdot65.scm.service_group:
    provider: "{{ provider }}"
    name: "web-services"
    members:
      - "web-service"
      - "dns-service"
    folder: "Texas"
    tag:
      - "dev-ansible"
      - "dev-test"
    state: "present"
```

</div>

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a service group for network services
  cdot65.scm.service_group:
    provider: "{{ provider }}"
    name: "network-services"
    members:
      - "dns-service"
      - "ssh-service"
    folder: "Texas"
    tag:
      - "dev-automation"
      - "dev-cicd"
    state: "present"
```

</div>

### Updating Service Groups

<div class="termy">

<!-- termynal -->

```yaml
- name: Update service group members and tags
  cdot65.scm.service_group:
    provider: "{{ provider }}"
    name: "web-services"
    members:
      - "web-service"  # Removed dns-service
    folder: "Texas"
    tag:
      - "dev-ansible"
      - "dev-cicd"     # Changed tag from dev-test to dev-cicd
    state: "present"
```

</div>

### Deleting Service Groups

<div class="termy">

<!-- termynal -->

```yaml
- name: Remove service groups
  cdot65.scm.service_group:
    provider: "{{ provider }}"
    name: "web-services"
    folder: "Texas"
    state: "absent"
```

</div>

## Return Values

| Name          | Description                            | Type | Returned              | Sample                                                                                                                                                                   |
|---------------|----------------------------------------|------|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| changed       | Whether any changes were made          | bool | always                | true                                                                                                                                                                     |
| service_group | Details about the service group object | dict | when state is present | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-services", "members": ["web-service", "dns-service"], "folder": "Texas", "tag": ["dev-ansible", "dev-test"]} |

## Error Handling

Common errors you might encounter when using this module:

| Error                             | Description                                               | Resolution                                                 |
|-----------------------------------|-----------------------------------------------------------|------------------------------------------------------------|
| Invalid service group data        | The service group parameters don't match required formats | Verify service group data conforms to SCM requirements     |
| Service not found                 | Referenced service member doesn't exist                   | Ensure all member services exist before creating the group |
| Service group name already exists | Attempt to create a group with a name that already exists | Use a unique name or update the existing group             |
| Missing required parameter        | Required parameter not provided                           | Ensure all required parameters are specified               |

<div class="termy">

<!-- termynal -->

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to create service group
      cdot65.scm.service_group:
        provider: "{{ provider }}"
        name: "web-services"
        members:
          - "web-service"
          - "non-existent-service"  # This service doesn't exist
        folder: "Texas"
        state: "present"
      register: result
  rescue:
    - name: Handle service not found error
      debug:
        msg: "Service member not found or invalid input provided"
    - name: Continue with other tasks
      # Additional recovery tasks
```

</div>

## Best Practices

1. **Naming and Organization**
    - Use descriptive names that indicate the function of the group
    - Use a consistent naming convention across service groups
    - Include the purpose of the service group in the description field

2. **Member Management**
    - Group services with related functions (web, database, email, etc.)
    - Verify all member services exist before creating the group
    - Avoid creating excessively large groups with too many services

3. **Security Policy Usage**
    - Use service groups in security policies to improve policy clarity and reduce maintenance
    - Reference service groups instead of individual services when possible
    - Document which policies reference each service group

4. **Container Management**
    - Always specify exactly one container (folder, snippet, or device)
    - Use consistent container names across operations
    - Validate container existence before operations

5. **Using Tags**
    - Leverage tags for classification and filtering
    - Keep tag names consistent across objects
    - Consider creating tag conventions (environment, purpose, etc.)

## Related Modules

- [service](service.md) - Manage individual service objects
- [service_info](service_info.md) - Retrieve information about service objects
- [tag](tag.md) - Manage tags used with service group objects
- [security_rule](security_rule.md) - Manage security rules that use service groups

## Author

- Calvin Remsburg (@cdot65)