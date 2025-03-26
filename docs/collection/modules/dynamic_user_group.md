# Dynamic User Group Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Return Values](#return-values)
4. [Usage Examples](#usage-examples)
   - [Creating Dynamic User Groups](#creating-dynamic-user-groups)
   - [Updating Dynamic User Groups](#updating-dynamic-user-groups)
   - [Deleting Dynamic User Groups](#deleting-dynamic-user-groups)
5. [Filter Expression Syntax](#filter-expression-syntax)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `dynamic_user_group` module allows you to create, update, and delete dynamic user group objects
within Strata Cloud Manager (SCM). Dynamic user groups are used to group users based on tag-based
filter expressions, enabling flexible and dynamic security policies based on user attributes.

This module is part of the `cdot65.scm` collection and requires proper authentication credentials to
interact with the Strata Cloud Manager API.

## Module Parameters

| Parameter     | Type | Required | Default | Choices         | Description                                                   |
| ------------- | ---- | -------- | ------- | --------------- | ------------------------------------------------------------- |
| `name`        | str  | yes      |         |                 | Name of the dynamic user group (max 63 chars)                 |
| `filter`      | str  | yes\*    |         |                 | Tag-based filter expression (max 2047 chars)                  |
| `description` | str  | no       |         |                 | Description of the dynamic user group (max 1023 chars)        |
| `tag`         | list | no       |         |                 | List of tags associated with this object (max 127 chars each) |
| `folder`      | str  | no\*\*   |         |                 | The folder containing the dynamic user group                  |
| `snippet`     | str  | no\*\*   |         |                 | The snippet containing the dynamic user group                 |
| `device`      | str  | no\*\*   |         |                 | The device containing the dynamic user group                  |
| `provider`    | dict | yes      |         |                 | Authentication credentials for SCM API                        |
| `state`       | str  | yes      |         | present, absent | Whether the group should exist or not                         |

\* Required when `state=present`\
\*\* Exactly one container type (folder, snippet, device) must be specified

### Provider Dictionary

| Parameter       | Type | Required | Default | Description                      |
| --------------- | ---- | -------- | ------- | -------------------------------- |
| `client_id`     | str  | yes      |         | Client ID for authentication     |
| `client_secret` | str  | yes      |         | Client secret for authentication |
| `tsg_id`        | str  | yes      |         | Tenant Service Group ID          |
| `log_level`     | str  | no       | "INFO"  | Log level for the SDK            |

## Return Values

| Key                  | Type | Returned              | Description                                 |
| -------------------- | ---- | --------------------- | ------------------------------------------- |
| `changed`            | bool | always                | Whether any changes were made               |
| `dynamic_user_group` | dict | when state is present | Details about the dynamic user group object |

### Dynamic User Group Return Dictionary

| Key           | Type | Description                                  |
| ------------- | ---- | -------------------------------------------- |
| `id`          | str  | Unique identifier for the dynamic user group |
| `name`        | str  | Name of the dynamic user group               |
| `filter`      | str  | Tag-based filter expression                  |
| `description` | str  | Description of the dynamic user group        |
| `folder`      | str  | The folder containing the dynamic user group |
| `tag`         | list | List of tags associated with this object     |

## Usage Examples

### Creating Dynamic User Groups



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
    tag: ["RiskManagement", "Security"]
    state: "present"
```




```yaml
- name: Create a dynamic user group with a complex filter
  cdot65.scm.dynamic_user_group:
    provider: "{{ provider }}"
    name: "risky_contractors"
    filter: "tag.user_type.contractor and (tag.criticality.high or tag.risk_score.gt.80)"
    description: "High risk contractors"
    folder: "Security"
    tag: ["RiskManagement", "Contractors"]
    state: "present"
```


### Updating Dynamic User Groups



```yaml
- name: Update an existing dynamic user group's filter and tags
  cdot65.scm.dynamic_user_group:
    provider: "{{ provider }}"
    name: "high_risk_users"
    filter: "tag.criticality.high or tag.risk_score.gt.90"
    description: "Updated user group for high risk classification"
    folder: "Security"
    tag: ["RiskManagement", "Security", "HighPriority"]
    state: "present"
```


### Deleting Dynamic User Groups



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

## Error Handling



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
  rescue:
    - name: Handle creation failure
      debug:
        msg: "Failed to create dynamic user group: {{ ansible_failed_result.msg }}"
```


## Best Practices

1. **Container Selection**

   - Always specify exactly one container type (folder, snippet, or device)
   - Use consistent container names across operations
   - Verify container existence before operations

2. **Filter Expressions**

   - Create clear, readable filter expressions
   - Test complex expressions in smaller parts before combining
   - Consider query performance for complex expressions
   - Document the purpose of each filter expression in the description field

3. **Naming and Organization**

   - Use descriptive names that reflect the group's purpose
   - Implement consistent naming conventions
   - Use tags to categorize and organize dynamic user groups
   - Add detailed descriptions for future reference

4. **Performance Considerations**

   - Keep filter expressions as simple as possible
   - Avoid excessive use of complex operations in filters
   - Consider the evaluation performance of filter expressions in production environments

5. **Security Considerations**

   - Regularly audit dynamic user group definitions
   - Implement strict access controls to dynamic user group management
   - Validate filter expressions to prevent unintended matches
   - Review dynamic user group membership regularly

## Related Modules

- [dynamic_user_group_info](dynamic_user_group_info.md): Used to retrieve information about dynamic
  user groups
- [tag](tag.md): Used to manage tags that can be used in dynamic user group filters
- [tag_info](tag_info.md): Used to retrieve information about available tags
