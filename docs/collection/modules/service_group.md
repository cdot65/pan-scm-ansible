# Service Group Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Service Group Model Attributes](#service-group-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating Service Groups](#creating-service-groups)
    - [Web Services Group](#web-services-group)
    - [Network Services Group](#network-services-group)
    - [Updating Service Groups](#updating-service-groups)
    - [Deleting Service Groups](#deleting-service-groups)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `service_group` Ansible module provides functionality to manage service group objects in Palo
Alto Networks' Strata Cloud Manager (SCM). This module allows you to create, update, and delete
service group objects, which combine multiple service objects into a single reference that can be
used in security policies, simplifying administration and policy management.

## Core Methods

| Method     | Description                 | Parameters                       | Return Type                       |
| ---------- | --------------------------- | -------------------------------- | --------------------------------- |
| `create()` | Creates a new service group | `data: Dict[str, Any]`           | `ServiceGroupResponseModel`       |
| `update()` | Updates an existing group   | `group: ServiceGroupUpdateModel` | `ServiceGroupResponseModel`       |
| `delete()` | Removes a group             | `object_id: str`                 | `None`                            |
| `fetch()`  | Gets a group by name        | `name: str`, `container: str`    | `ServiceGroupResponseModel`       |
| `list()`   | Lists groups with filtering | `folder: str`, `**filters`       | `List[ServiceGroupResponseModel]` |

## Service Group Model Attributes

| Attribute | Type | Required      | Description                                              |
| --------- | ---- | ------------- | -------------------------------------------------------- |
| `name`    | str  | Yes           | The name of the service group (max 63 chars)             |
| `members` | list | Yes           | List of service objects that are members of this group   |
| `tag`     | list | No            | List of tags associated with the service group           |
| `folder`  | str  | One container | The folder in which the group is defined (max 64 chars)  |
| `snippet` | str  | One container | The snippet in which the group is defined (max 64 chars) |
| `device`  | str  | One container | The device in which the group is defined (max 64 chars)  |

### Provider Dictionary

| Parameter       | Type | Required | Description                             |
| --------------- | ---- | -------- | --------------------------------------- |
| `client_id`     | str  | Yes      | Client ID for SCM authentication        |
| `client_secret` | str  | Yes      | Client secret for SCM authentication    |
| `tsg_id`        | str  | Yes      | Tenant Service Group ID                 |
| `log_level`     | str  | No       | Log level for the SDK (default: "INFO") |

## Exceptions

| Exception                    | Description                          |
| ---------------------------- | ------------------------------------ |
| `InvalidObjectError`         | Invalid service group data or format |
| `NameNotUniqueError`         | Service group name already exists    |
| `ObjectNotPresentError`      | Service group not found              |
| `MissingQueryParameterError` | Missing required parameters          |
| `AuthenticationError`        | Authentication failed                |
| `ServerError`                | Internal server error                |
| `ReferenceNotFoundError`     | Referenced service doesn't exist     |

## Basic Configuration

The Service Group module requires proper authentication credentials to access the Strata Cloud
Manager API.

```yaml
- name: Basic Service Group Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a service group exists
      cdot65.scm.service_group:
        provider: "{{ provider }}"
        name: "web-services"
        members:
          - "web-service"
          - "dns-service"
        folder: "Texas"
        state: "present"
```

## Usage Examples

### Creating Service Groups

Service groups allow you to combine multiple related service objects into a single reference for use
in security policies.

### Web Services Group

This example creates a service group for web-related services.

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

### Network Services Group

This example creates a service group for network infrastructure services.

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

### Updating Service Groups

This example updates an existing service group by changing its members and tags.

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

### Deleting Service Groups

This example removes a service group that is no longer needed.

```yaml
- name: Remove service group
  cdot65.scm.service_group:
    provider: "{{ provider }}"
    name: "web-services"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting service groups, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated service group configurations"
```

## Error Handling

It's important to handle potential errors when working with service groups.

```yaml
- name: Create or update service group with error handling
  block:
    - name: Ensure service group exists
      cdot65.scm.service_group:
        provider: "{{ provider }}"
        name: "web-services"
        members:
          - "web-service"
          - "dns-service"
        folder: "Texas"
        state: "present"
      register: group_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated service group configurations"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Check if referenced service doesn't exist
      debug:
        msg: "Check if all referenced services exist."
      when: "'referenced object does not exist' in ansible_failed_result.msg"
```

## Best Practices

### Naming and Organization

- Use descriptive names that indicate the function of the group
- Use a consistent naming convention across service groups
- Include the purpose of the service group in the description field
- Organize groups by functional categories for easier management
- Keep group names concise but meaningful

### Member Management

- Group services with related functions (web, database, email, etc.)
- Verify all member services exist before creating the group
- Avoid creating excessively large groups with too many services
- Document which services are included in each group
- Regularly review group membership to ensure relevance

### Security Policy Usage

- Use service groups in security policies to improve policy clarity and reduce maintenance
- Reference service groups instead of individual services when possible
- Document which policies reference each service group
- Consider the impact on security policies when modifying groups
- Test policy behavior after making changes to service groups

### Container Management

- Always specify exactly one container (folder, snippet, or device)
- Use consistent container names across operations
- Validate container existence before operations
- Document the container structure for better organization
- Implement appropriate access controls for each container

### Tag Management

- Leverage tags for classification and filtering
- Keep tag names consistent across objects
- Consider creating tag conventions (environment, purpose, etc.)
- Use tags to organize groups by logical function
- Document tag meanings and usage patterns

## Related Modules

- [service](service.md) - Manage individual service objects
- [service_info](service_info.md) - Retrieve information about service objects
- [service_group_info](service_group_info.md) - Retrieve information about service groups
- [tag](tag.md) - Manage tags used with service group objects
- [security_rule](security_rule.md) - Configure security policies that reference service groups
