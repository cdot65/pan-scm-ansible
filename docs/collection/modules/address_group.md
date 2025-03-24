# Address Group Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
    - [Creating Static Address Groups](#creating-static-address-groups)
    - [Creating Dynamic Address Groups](#creating-dynamic-address-groups)
    - [Updating Address Groups](#updating-address-groups)
    - [Deleting Address Groups](#deleting-address-groups)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `address_group` module provides functionality to manage address group objects in Palo Alto Networks' Strata Cloud
Manager. This module allows you to create, update, and delete both static and dynamic address groups. Static address
groups contain a fixed list of address objects, while dynamic address groups use tag-based filters to automatically
include addresses based on their tags.

## Module Parameters

| Parameter              | Required | Type | Choices         | Default | Comments                                        |
|------------------------|----------|------|-----------------|---------|-------------------------------------------------|
| name                   | yes      | str  |                 |         | The name of the address group.                  |
| description            | no       | str  |                 |         | Description of the address group.               |
| tag                    | no       | list |                 |         | List of tags associated with the address group. |
| dynamic                | no       | dict |                 |         | Dynamic filter defining group membership.       |
| dynamic.filter         | yes      | str  |                 |         | Tag-based filter defining group membership.     |
| static                 | no       | list |                 |         | List of static addresses in the group.          |
| folder                 | no       | str  |                 |         | The folder in which the resource is defined.    |
| snippet                | no       | str  |                 |         | The snippet in which the resource is defined.   |
| device                 | no       | str  |                 |         | The device in which the resource is defined.    |
| provider               | yes      | dict |                 |         | Authentication credentials.                     |
| provider.client_id     | yes      | str  |                 |         | Client ID for authentication.                   |
| provider.client_secret | yes      | str  |                 |         | Client secret for authentication.               |
| provider.tsg_id        | yes      | str  |                 |         | Tenant Service Group ID.                        |
| provider.log_level     | no       | str  |                 | INFO    | Log level for the SDK.                          |
| state                  | yes      | str  | present, absent |         | Desired state of the address group object.      |

!!! note
- Exactly one of `static` or `dynamic` must be provided when state is present.
- Exactly one of `folder`, `snippet`, or `device` must be provided.
- For dynamic address groups, the filter expression uses tag names in single quotes with operators like 'and', 'or',
and 'not'.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Creating Static Address Groups

Static address groups contain a fixed list of address objects. These address objects must already exist in the same
container (folder, snippet, or device).

<div class="termy">

<!-- termynal -->

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

</div>

### Creating Dynamic Address Groups

Dynamic address groups use tag-based filters to automatically include address objects based on their tags. Any address
object with tags matching the filter will be included in the group.

<div class="termy">

<!-- termynal -->

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

</div>

### Updating Address Groups

You can update an existing address group to modify its description, tags, or members. When updating a static group, you
provide the complete list of members that should be in the group.

<div class="termy">

<!-- termynal -->

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

</div>

### Deleting Address Groups

<div class="termy">

<!-- termynal -->

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

</div>

## Return Values

| Name          | Description                     | Type | Returned              | Sample                                                                                                                                                                                                                       |
|---------------|---------------------------------|------|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| changed       | Whether any changes were made   | bool | always                | true                                                                                                                                                                                                                         |
| address_group | Details about the address group | dict | when state is present | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Test_Static_Group", "description": "A static address group", "static": ["test_network1", "test_network2"], "folder": "Texas", "tag": ["dev-automation", "dev-cicd"]} |

## Error Handling

Common errors you might encounter when using this module:

| Error                             | Description                                                     | Resolution                                                 |
|-----------------------------------|-----------------------------------------------------------------|------------------------------------------------------------|
| Invalid address group data        | The address group parameters don't meet validation requirements | Verify parameters, especially static/dynamic settings      |
| Address group name already exists | Attempting to create a group with a name that already exists    | Use a unique name or update the existing group             |
| Address not found in static group | Referenced address doesn't exist in the container               | Ensure referenced addresses exist before adding to a group |
| Invalid filter expression         | Incorrect syntax in dynamic group filter                        | Use proper syntax with quoted tag names and operators      |

<div class="termy">

<!-- termynal -->

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to create address group
      cdot65.scm.address_group:
        provider: "{{ provider }}"
        name: "Test_Static_Group"
        static:
          - "nonexistent_address"
        folder: "Texas"
        state: "present"
      register: result
  rescue:
    - name: Handle address group creation error
      debug:
        msg: "Failed to create address group. Make sure referenced addresses exist."
    - name: Continue with other tasks
      # Additional recovery tasks
```

</div>

## Best Practices

1. **Group Organization**
    - Use descriptive names for address groups
    - Include purpose in the description field
    - Apply consistent tagging strategies
    - Group related addresses together for easier management

2. **Static vs Dynamic Groups**
    - Use static groups for fixed sets of addresses
    - Use dynamic groups for addresses that share attributes
    - Use clear, understandable filter expressions for dynamic groups
    - Test filters before deployment to ensure they include the expected addresses

3. **Security Considerations**
    - Review address groups regularly to ensure they include only necessary addresses
    - Document the purpose of each address group
    - Limit the number of addresses in a group to improve performance
    - Be careful with dynamic groups to prevent unintended inclusions

4. **Management Efficiency**
    - Create address objects before referencing them in groups
    - Use consistent container (folder/snippet/device) across related objects
    - Leverage idempotent operations to safely run playbooks multiple times
    - Implement proper error handling with block/rescue

5. **Dynamic Group Filters**
    - Keep filter expressions simple and readable
    - Use parentheses to clarify complex expressions
    - Test filter expressions thoroughly before deployment
    - Document the expected behavior of filter expressions

## Related Modules

- [address](address.md) - Manage individual address objects
- [address_info](address_info.md) - Retrieve information about address objects
- [address_group_info](address_group_info.md) - Retrieve information about address groups
- [tag](tag.md) - Create and manage tags used in dynamic address groups
- [security_rule](security_rule.md) - Configure security policies that use address groups

## Author

- Calvin Remsburg (@cdot65)