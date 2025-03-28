# Dynamic User Group Configuration Object

## Table of Contents

- [Dynamic User Group Configuration Object](#dynamic-user-group-configuration-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [Dynamic User Group Model Attributes](#dynamic-user-group-model-attributes)
    - [Provider Dictionary Attributes](#provider-dictionary-attributes)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Creating Dynamic User Groups](#creating-dynamic-user-groups)
    - [Basic Dynamic User Group](#basic-dynamic-user-group)
    - [Complex Filter Dynamic User Group](#complex-filter-dynamic-user-group)
    - [Updating Dynamic User Groups](#updating-dynamic-user-groups)
    - [Deleting Dynamic User Groups](#deleting-dynamic-user-groups)
  - [Filter Expression Syntax](#filter-expression-syntax)
  - [Managing Configuration Changes](#managing-configuration-changes)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Container Selection](#container-selection)
    - [Filter Expressions](#filter-expressions)
    - [Naming and Organization](#naming-and-organization)
    - [Performance Considerations](#performance-considerations)
    - [Security Considerations](#security-considerations)
    - [Integration with Security Policies](#integration-with-security-policies)
  - [Related Modules](#related-modules)

## Overview

The `dynamic_user_group` Ansible module provides functionality to manage dynamic user group objects
within Palo Alto Networks' Strata Cloud Manager (SCM). Dynamic user groups are used to group users
based on tag-based filter expressions, enabling flexible and dynamic security policies based on user
attributes.

## Core Methods

| Method     | Description                            | Parameters                           | Return Type                           |
| ---------- | -------------------------------------- | ------------------------------------ | ------------------------------------- |
| `create()` | Creates a new dynamic user group       | `data: Dict[str, Any]`               | `DynamicUserGroupResponseModel`       |
| `update()` | Updates an existing dynamic user group | `group: DynamicUserGroupUpdateModel` | `DynamicUserGroupResponseModel`       |
| `delete()` | Removes a dynamic user group           | `object_id: str`                     | `None`                                |
| `fetch()`  | Gets a dynamic user group by name      | `name: str`, `container: str`        | `DynamicUserGroupResponseModel`       |
| `list()`   | Lists dynamic user groups with filters | `folder: str`, `**filters`           | `List[DynamicUserGroupResponseModel]` |

## Dynamic User Group Model Attributes

| Attribute     | Type | Required      | Description                                                   |
| ------------- | ---- | ------------- | ------------------------------------------------------------- |
| `name`        | str  | Yes           | Name of the dynamic user group (max 63 chars)                 |
| `filter`      | str  | Yes\*         | Tag-based filter expression (max 2047 chars)                  |
| `description` | str  | No            | Description of the dynamic user group (max 1023 chars)        |
| `tag`         | list | No            | List of tags associated with this object (max 127 chars each) |
| `folder`      | str  | One container | The folder containing the dynamic user group                  |
| `snippet`     | str  | One container | The snippet containing the dynamic user group                 |
| `device`      | str  | One container | The device containing the dynamic user group                  |

\* Required when `state=present`

### Provider Dictionary Attributes

| Attribute       | Type | Required | Default | Description                      |
| --------------- | ---- | -------- | ------- | -------------------------------- |
| `client_id`     | str  | Yes      |         | Client ID for authentication     |
| `client_secret` | str  | Yes      |         | Client secret for authentication |
| `tsg_id`        | str  | Yes      |         | Tenant Service Group ID          |
| `log_level`     | str  | No       | "INFO"  | Log level for the SDK            |

## Exceptions

| Exception               | Description                               |
| ----------------------- | ----------------------------------------- |
| `InvalidObjectError`    | Invalid dynamic user group data or format |
| `NameNotUniqueError`    | Dynamic user group name already exists    |
| `ObjectNotPresentError` | Dynamic user group not found              |
| `InvalidFilterError`    | Filter expression syntax is invalid       |
| `AuthenticationError`   | Authentication failed                     |
| `ServerError`           | Internal server error                     |

## Basic Configuration

The Dynamic User Group module requires proper authentication credentials to access the Strata Cloud
Manager API.

```yaml
- name: Basic Dynamic User Group Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a dynamic user group exists
      cdot65.scm.dynamic_user_group:
        provider: "{{ provider }}"
        name: "high_risk_users"
        filter: "tag.criticality.high"
        description: "Users with high risk classification"
        folder: "Security"
        tag: [ "RiskManagement", "Security" ]
        state: "present"
```

## Usage Examples

### Creating Dynamic User Groups

Dynamic user groups can be created with different levels of filter complexity to match specific user
attributes and conditions.

### Basic Dynamic User Group

This example creates a simple dynamic user group with a basic filter expression.

```yaml
- name: Create a dynamic user group with a simple filter
  cdot65.scm.dynamic_user_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
    name: "high_risk_users"
    filter: "tag.criticality.high"
    description: "Users with high risk classification"
    folder: "Security"
    tag: [ "RiskManagement", "Security" ]
    state: "present"
```

### Complex Filter Dynamic User Group

This example creates a dynamic user group with a more complex filter expression using logical
operators.

```yaml
- name: Create a dynamic user group with a complex filter
  cdot65.scm.dynamic_user_group:
    provider: "{{ provider }}"
    name: "risky_contractors"
    filter: "tag.user_type.contractor and (tag.criticality.high or tag.risk_score.gt.80)"
    description: "High risk contractors"
    folder: "Security"
    tag: [ "RiskManagement", "Contractors" ]
    state: "present"
```

### Updating Dynamic User Groups

This example updates an existing dynamic user group with a modified filter expression and additional
tags.

```yaml
- name: Update an existing dynamic user group's filter and tags
  cdot65.scm.dynamic_user_group:
    provider: "{{ provider }}"
    name: "high_risk_users"
    filter: "tag.criticality.high or tag.risk_score.gt.90"
    description: "Updated user group for high risk classification"
    folder: "Security"
    tag: [ "RiskManagement", "Security", "HighPriority" ]
    state: "present"
```

### Deleting Dynamic User Groups

This example removes a dynamic user group from SCM.

```yaml
- name: Delete a dynamic user group
  cdot65.scm.dynamic_user_group:
    provider: "{{ provider }}"
    name: "risky_contractors"
    folder: "Security"
    state: "absent"
```

## Filter Expression Syntax

Dynamic user groups use tag-based filter expressions to determine group membership. The filter
syntax supports various operations:

| Operator | Description           | Example                                                                     |
| -------- | --------------------- | --------------------------------------------------------------------------- |
| `.`      | Access tag value      | `tag.criticality.high`                                                      |
| `and`    | Logical AND           | `tag.department.finance and tag.location.hq`                                |
| `or`     | Logical OR            | `tag.location.remote or tag.location.branch`                                |
| `not`    | Logical NOT           | `not tag.clearance.classified`                                              |
| `()`     | Grouping              | `(tag.department.it or tag.department.security) and tag.access_level.admin` |
| `.gt.`   | Greater than          | `tag.risk_score.gt.75`                                                      |
| `.lt.`   | Less than             | `tag.risk_score.lt.30`                                                      |
| `.ge.`   | Greater than or equal | `tag.access_level.ge.3`                                                     |
| `.le.`   | Less than or equal    | `tag.access_level.le.5`                                                     |

These filters allow you to create dynamic groups based on user attributes represented as tags in the
system.

## Managing Configuration Changes

After creating, updating, or deleting dynamic user groups, you need to commit your changes to apply
them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: [ "Security" ]
    description: "Updated dynamic user groups"
```

## Error Handling

It's important to handle potential errors when working with dynamic user groups.

```yaml
- name: Create dynamic user group with error handling
  block:
    - name: Attempt to create dynamic user group
      cdot65.scm.dynamic_user_group:
        provider: "{{ provider }}"
        name: "restricted_users"
        filter: "tag.access_level.restricted"
        folder: "Security"
        state: "present"
      register: result

    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: [ "Security" ]
        description: "Added restricted users group"
      when: result.changed

  rescue:
    - name: Handle creation failure
      debug:
        msg: "Failed to create dynamic user group: {{ ansible_failed_result.msg }}"

    - name: Check if it's a filter syntax error
      debug:
        msg: "The filter expression contains a syntax error, please review it"
      when: "'invalid filter' in ansible_failed_result.msg"
```

## Best Practices

### Container Selection

- Always specify exactly one container type (folder, snippet, or device)
- Use consistent container names across operations
- Verify container existence before operations
- Group related dynamic user groups in the same container

### Filter Expressions

- Create clear, readable filter expressions
- Test complex expressions in smaller parts before combining
- Consider query performance for complex expressions
- Document the purpose of each filter expression in the description field
- Use parentheses to make logic explicit in complex expressions
- Validate that tags used in filters exist in your environment

### Naming and Organization

- Use descriptive names that reflect the group's purpose
- Implement consistent naming conventions
- Use tags to categorize and organize dynamic user groups
- Add detailed descriptions for future reference
- Consider using a prefix to identify specific categories of groups

### Performance Considerations

- Keep filter expressions as simple as possible
- Avoid excessive use of complex operations in filters
- Consider the evaluation performance of filter expressions in production environments
- Monitor the performance impact of complex filter expressions on your security policies
- Test complex filters with a representative user base before deploying

### Security Considerations

- Regularly audit dynamic user group definitions
- Implement strict access controls to dynamic user group management
- Validate filter expressions to prevent unintended matches
- Review dynamic user group membership regularly
- Document the security implications of each dynamic user group
- Implement change management processes for modifying dynamic user groups

### Integration with Security Policies

- Plan how dynamic user groups will be used in security policies
- Test policy behavior with different user tag combinations
- Create hierarchical groups where appropriate (e.g., all-users, high-risk-users)
- Document the relationship between groups and policies
- Implement monitoring to detect unexpected behavior

## Related Modules

- [dynamic_user_group_info](dynamic_user_group_info.md) - Retrieve information about dynamic user
  groups
- [tag](tag.md) - Create, update, and delete tags that can be used in dynamic user group filters
- [tag_info](tag_info.md) - Retrieve information about available tags
- [security_rule](security_rule.md) - Configure security policies that use dynamic user groups
