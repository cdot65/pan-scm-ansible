# Application Group Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
   - [Creating Application Groups](#creating-application-groups)
   - [Updating Application Groups](#updating-application-groups)
   - [Deleting Application Groups](#deleting-application-groups)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `application_group` module provides functionality to manage application group objects in Palo
Alto Networks' Strata Cloud Manager. This module allows you to create, update, and delete
application groups that can contain multiple application objects. Application groups simplify
security policy configuration by allowing you to reference multiple applications as a single object.

## Module Parameters

| Parameter              | Required | Type | Choices         | Default | Comments                                           |
| ---------------------- | -------- | ---- | --------------- | ------- | -------------------------------------------------- |
| name                   | yes      | str  |                 |         | The name of the application group.                 |
| members                | yes\*    | list |                 |         | List of application names to include in the group. |
| folder                 | no       | str  |                 |         | The folder in which the resource is defined.       |
| snippet                | no       | str  |                 |         | The snippet in which the resource is defined.      |
| device                 | no       | str  |                 |         | The device in which the resource is defined.       |
| provider               | yes      | dict |                 |         | Authentication credentials.                        |
| provider.client_id     | yes      | str  |                 |         | Client ID for authentication.                      |
| provider.client_secret | yes      | str  |                 |         | Client secret for authentication.                  |
| provider.tsg_id        | yes      | str  |                 |         | Tenant Service Group ID.                           |
| provider.log_level     | no       | str  |                 | INFO    | Log level for the SDK.                             |
| state                  | yes      | str  | present, absent |         | Desired state of the application group object.     |

!!! note * Members are required when state is "present".

```
\* Exactly one of folder, snippet, or device must be provided.
```

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Creating Application Groups



```yaml
- name: Create web applications group
  cdot65.scm.application_group:
    provider: "{{ provider }}"
    name: "web-apps"
    members:
      - "ssl"
      - "web-browsing"
    folder: "Texas"
    state: "present"
```


You can create groups with multiple applications:



```yaml
- name: Create network applications group
  cdot65.scm.application_group:
    provider: "{{ provider }}"
    name: "network-apps"
    members:
      - "dns-base"
      - "ntp"
    folder: "Texas"
    state: "present"
```


### Updating Application Groups

When updating an application group, you must provide the complete list of members. Any existing
members not included in the update will be removed from the group.



```yaml
- name: Update web applications group membership
  cdot65.scm.application_group:
    provider: "{{ provider }}"
    name: "web-apps"
    members:
      - "ssl"
      - "web-browsing"
      - "dns-base"
    folder: "Texas"
    state: "present"
```


### Deleting Application Groups



```yaml
- name: Remove application groups
  cdot65.scm.application_group:
    provider: "{{ provider }}"
    name: "{{ item }}"
    folder: "Texas"
    state: "absent"
  loop:
    - "web-apps"
    - "network-apps"
```


## Return Values

| Name              | Description                         | Type | Returned              | Sample                                                                                                                                |
| ----------------- | ----------------------------------- | ---- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| changed           | Whether any changes were made       | bool | always                | true                                                                                                                                  |
| application_group | Details about the application group | dict | when state is present | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-apps", "members": ["ssl", "web-browsing", "dns-base"], "folder": "Texas"} |

## Error Handling

Common errors you might encounter when using this module:

| Error                          | Description                                            | Resolution                                                                        |
| ------------------------------ | ------------------------------------------------------ | --------------------------------------------------------------------------------- |
| Invalid application group data | Required parameters missing or invalid format          | Ensure all required parameters are provided with valid values                     |
| Application not found          | One or more of the specified applications don't exist  | Verify that all applications in the members list exist in the specified container |
| Missing container              | None of folder, snippet, or device is specified        | Provide exactly one of folder, snippet, or device                                 |
| Application group not found    | Attempt to update or delete a group that doesn't exist | Verify the application group name and container location                          |



```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to create application group
      cdot65.scm.application_group:
        provider: "{{ provider }}"
        name: "web-apps"
        members:
          - "web-browsing"
          - "non-existent-app"  # This application doesn't exist
        folder: "Texas"
        state: "present"
      register: result
  rescue:
    - name: Handle validation error
      debug:
        msg: "Failed to create application group. Verify all applications exist."
    - name: Continue with other tasks
      # Additional recovery tasks
```


## Best Practices

1. **Group Organization**

   - Use descriptive names that indicate the function of the group
   - Group applications with similar functions or purposes
   - Use a consistent naming convention across application groups
   - Limit the number of applications in a group to maintain clarity

2. **Member Management**

   - Verify all member applications exist before creating the group
   - When updating groups, always provide the complete list of members
   - Consider organizing applications into functional groups (web, database, collaboration, etc.)
   - Document which applications are included in each group

3. **Policy Implementation**

   - Use application groups in security policies to improve policy clarity
   - Review application group membership regularly as part of security audits
   - Consider the impact on existing policies when modifying group membership
   - Test policy behavior after making changes to application groups

4. **Performance Considerations**

   - Balance between using many specific groups versus fewer large groups
   - Group commonly used applications together to reduce the number of policy rules
   - Consider the impact on policy processing when designing application groups
   - Update application groups during maintenance windows if used in active policies

5. **Module Usage**

   - Be aware of idempotent behavior—always providing all members when updating
   - Use check mode to preview changes before applying
   - Implement error handling with block/rescue for production playbooks
   - Use variables or external data sources to maintain group membership lists

## Related Modules

- [application](application.md) - Manage application objects
- [application_info](application_info.md) - Retrieve information about application objects
- [application_group_info](application_group_info.md) - Retrieve information about application
  groups
- [security_rule](security_rule.md) - Configure security policies that reference application groups

## Author

- Calvin Remsburg (@cdot65)
