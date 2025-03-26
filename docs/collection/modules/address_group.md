# Address Group Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Address Group Model Attributes](#address-group-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating Address Groups](#creating-address-groups)
    - [Static Address Group](#static-address-group)
    - [Dynamic Address Group](#dynamic-address-group)
    - [Updating Address Groups](#updating-address-groups)
    - [Deleting Address Groups](#deleting-address-groups)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `address_group` Ansible module provides functionality to manage address group objects in Palo Alto
Networks' Strata Cloud Manager (SCM). This module allows you to create, update, and delete both static and
dynamic address groups. Static address groups contain a fixed list of address objects, while dynamic
address groups use tag-based filters to automatically include addresses based on their tags.

## Core Methods

| Method     | Description                       | Parameters                         | Return Type                     |
| ---------- | --------------------------------- | ---------------------------------- | ------------------------------- |
| `create()` | Creates a new address group       | `data: Dict[str, Any]`             | `AddressGroupResponseModel`     |
| `update()` | Updates an existing address group | `group: AddressGroupUpdateModel`   | `AddressGroupResponseModel`     |
| `delete()` | Removes an address group          | `object_id: str`                   | `None`                          |
| `fetch()`  | Gets an address group by name     | `name: str`, `container: str`      | `AddressGroupResponseModel`     |
| `list()`   | Lists address groups with filters | `folder: str`, `**filters`         | `List[AddressGroupResponseModel]`|

## Address Group Model Attributes

| Attribute      | Type | Required       | Description                                                 |
| -------------- | ---- | -------------- | ----------------------------------------------------------- |
| `name`         | str  | Yes            | The name of the address group                               |
| `description`  | str  | No             | Description of the address group                            |
| `tag`          | list | No             | List of tags associated with the address group              |
| `static`       | list | One type only  | List of static addresses in the group                       |
| `dynamic`      | dict | One type only  | Dynamic filter configuration                                |
| `folder`       | str  | One container  | The folder in which the group is defined (max 64 chars)     |
| `snippet`      | str  | One container  | The snippet in which the group is defined (max 64 chars)    |
| `device`       | str  | One container  | The device in which the group is defined (max 64 chars)     |

### Dynamic Filter Attributes

| Attribute | Type | Required | Description                                      |
| --------- | ---- | -------- | ------------------------------------------------ |
| `filter`  | str  | Yes      | Tag-based filter expression defining membership  |

## Exceptions

| Exception                    | Description                         |
| ---------------------------- | ----------------------------------- |
| `InvalidObjectError`         | Invalid address group data or format|
| `NameNotUniqueError`         | Address group name already exists   |
| `ObjectNotPresentError`      | Address group or referenced address not found |
| `MissingQueryParameterError` | Missing required parameters         |
| `InvalidFilterSyntaxError`   | Invalid dynamic filter expression   |
| `AuthenticationError`        | Authentication failed               |
| `ServerError`                | Internal server error               |

## Basic Configuration

The Address Group module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Address Group Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a static address group exists
      cdot65.scm.address_group:
        provider: "{{ provider }}"
        name: "Web-Servers"
        description: "Group containing web server addresses"
        folder: "Texas"
        static:
          - "Web-Server-01"
          - "Web-Server-02"
        tag: ["Web", "Production"]
        state: "present"
```

## Usage Examples

### Creating Address Groups

Address groups can be created as either static (with explicit members) or dynamic (with tag-based filters).

### Static Address Group

This example creates a static address group with specific member addresses.

```yaml
- name: Create a static address group
  cdot65.scm.address_group:
    provider: "{{ provider }}"
    name: "Test_Static_Group"
    description: "A static address group"
    static:
      - "ansible_test_network1"
      - "ansible_test_network2"
    folder: "Texas"
    tag: ["dev-automation", "dev-cicd"]
    state: "present"
```

### Dynamic Address Group

This example creates a dynamic address group that automatically includes addresses based on tags.

```yaml
- name: Create a dynamic address group
  cdot65.scm.address_group:
    provider: "{{ provider }}"
    name: "Test_Dynamic_Group"
    description: "A dynamic address group"
    dynamic:
      filter: "'dev-test' or 'dev-cicd'"
    folder: "Texas"
    state: "present"
```

### Updating Address Groups

This example updates an existing static address group by modifying its members, description, and tags.

```yaml
- name: Update the static address group
  cdot65.scm.address_group:
    provider: "{{ provider }}"
    name: "Test_Static_Group"
    description: "An updated static address group"
    static:
      - "ansible_test_network1"
    folder: "Texas"
    tag: ["dev-ansible"]
    state: "present"
```

### Deleting Address Groups

This example removes address groups.

```yaml
- name: Delete address groups
  cdot65.scm.address_group:
    provider: "{{ provider }}"
    name: "{{ item }}"
    folder: "Texas"
    state: "absent"
  loop:
    - "Test_Static_Group"
    - "Test_Dynamic_Group"
```

## Managing Configuration Changes

After creating, updating, or deleting address groups, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated address groups"
```

## Error Handling

It's important to handle potential errors when working with address groups.

```yaml
- name: Create or update address group with error handling
  block:
    - name: Ensure address group exists
      cdot65.scm.address_group:
        provider: "{{ provider }}"
        name: "Web-Servers"
        description: "Group containing web server addresses"
        folder: "Texas"
        static:
          - "Web-Server-01"
          - "Web-Server-02"
        tag: ["Web", "Production"]
        state: "present"
      register: group_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated address groups"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```

## Best Practices

### Group Type Selection

- Choose between static and dynamic groups based on management needs
- Use static groups for fixed sets of addresses
- Use dynamic groups for addresses that share attributes or purposes
- Consider operational impact of each approach

### Static Group Management

- Create address objects before referencing them in groups
- Use consistent naming conventions for related addresses
- Group logically related addresses together
- Review member lists regularly to ensure they're current

### Dynamic Group Filters

- Keep filter expressions simple and readable
- Use parentheses to clarify complex expressions
- Test filter expressions thoroughly before deployment
- Document the expected behavior of filter expressions
- Use consistent tagging strategies across address objects

### Container Management

- Always specify exactly one container (folder, snippet, or device)
- Use consistent container names across operations
- Validate container existence before operations

### Naming Conventions

- Develop a consistent naming convention for address groups
- Make names descriptive of the group's purpose or function
- Use a consistent format like "Location-Function-Type"
- Document naming standards for team consistency

### Security Considerations

- Review address groups regularly to ensure they include only necessary addresses
- Document the purpose of each address group
- Limit the number of addresses in a group to improve performance
- Be careful with dynamic groups to prevent unintended inclusions

### Performance Optimization

- Limit the complexity of dynamic filters to improve evaluation time
- Use more specific filters to reduce the scope of dynamic groups
- Consider the impact of very large static groups on system performance
- Use address groups effectively in security policies to reduce rule count

## Related Modules

- [address](address.md) - Manage individual address objects
- [address_info](address_info.md) - Retrieve information about address objects
- [address_group_info](address_group_info.md) - Retrieve information about address groups
- [tag](tag.md) - Create and manage tags used in dynamic address groups
- [security_rule](security_rule.md) - Configure security policies that use address groups