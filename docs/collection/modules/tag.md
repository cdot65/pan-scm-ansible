# Tag Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
    - [Creating Tags](#creating-tags)
    - [Updating Tags](#updating-tags)
    - [Deleting Tags](#deleting-tags)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `tag` module provides functionality to manage tag objects in Palo Alto Networks' Strata Cloud Manager. This module
allows you to create, update, and delete tag objects that can be used to categorize and organize various resources
within SCM. Tags are metadata labels that can be attached to objects for filtering, policy application, and
organization.

## Module Parameters

| Parameter              | Required | Type | Choices                                   | Default | Comments                                               |
|------------------------|----------|------|-------------------------------------------|---------|--------------------------------------------------------|
| name                   | yes      | str  |                                           |         | The name of the tag (max 63 chars).                    |
| color                  | no       | str  | Azure Blue, Black, Blue, etc. (see below) |         | Color associated with the tag.                         |
| comments               | no       | str  |                                           |         | Comments for the tag (max 1023 chars).                 |
| folder                 | no*      | str  |                                           |         | The folder where the tag is stored (max 64 chars).     |
| snippet                | no*      | str  |                                           |         | The configuration snippet for the tag (max 64 chars).  |
| device                 | no*      | str  |                                           |         | The device where the tag is configured (max 64 chars). |
| provider               | yes      | dict |                                           |         | Authentication credentials.                            |
| provider.client_id     | yes      | str  |                                           |         | Client ID for authentication.                          |
| provider.client_secret | yes      | str  |                                           |         | Client secret for authentication.                      |
| provider.tsg_id        | yes      | str  |                                           |         | Tenant Service Group ID.                               |
| provider.log_level     | no       | str  |                                           | INFO    | Log level for the SDK.                                 |
| state                  | yes      | str  | present, absent                           |         | Desired state of the tag object.                       |

**Available tag colors:** Azure Blue, Black, Blue, Blue Gray, Blue Violet, Brown, Burnt Sienna, Cerulean Blue, Chestnut,
Cobalt Blue, Copper, Cyan, Forest Green, Gold, Gray, Green, Lavender, Light Gray, Light Green, Lime, Magenta, Mahogany,
Maroon, Medium Blue, Medium Rose, Medium Violet, Midnight Blue, Olive, Orange, Orchid, Peach, Purple, Red, Red Violet,
Red-Orange, Salmon, Thistle, Turquoise Blue, Violet Blue, Yellow, Yellow-Orange

!!! note
- Exactly one container type (`folder`, `snippet`, or `device`) must be provided.
- When state is present, a color should be specified for new tags.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Creating Tags

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a new tag
  cdot65.scm.tag:
    provider: "{{ provider }}"
    name: "Production"
    color: "Blue"
    comments: "Production environment tag"
    folder: "Texas"
    state: "present"
```

</div>

<div class="termy">

<!-- termynal -->

```yaml
- name: Create multiple tags using loop
  cdot65.scm.tag:
    provider: "{{ provider }}"
    name: "{{ item.name }}"
    color: "{{ item.color }}"
    comments: "Tag for {{ item.name }} environment"
    folder: "Texas"
    state: "present"
  loop:
    - { name: "dev-ansible", color: "Blue" }
    - { name: "dev-automation", color: "Green" }
    - { name: "dev-test", color: "Orange" }
    - { name: "dev-cicd", color: "Red" }
```

</div>

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a tag in a snippet
  cdot65.scm.tag:
    provider: "{{ provider }}"
    name: "Development"
    color: "Green"
    comments: "Development environment tag"
    snippet: "Common"
    state: "present"
```

</div>

### Updating Tags

<div class="termy">

<!-- termynal -->

```yaml
- name: Update tag color
  cdot65.scm.tag:
    provider: "{{ provider }}"
    name: "Production"
    color: "Red"
    folder: "Texas"
    state: "present"
```

</div>

<div class="termy">

<!-- termynal -->

```yaml
- name: Update tag comments
  cdot65.scm.tag:
    provider: "{{ provider }}"
    name: "Production"
    color: "Red"
    comments: "Updated production environment tag"
    folder: "Texas"
    state: "present"
```

</div>

### Deleting Tags

<div class="termy">

<!-- termynal -->

```yaml
- name: Remove tag
  cdot65.scm.tag:
    provider: "{{ provider }}"
    name: "Production"
    folder: "Texas"
    state: "absent"
```

</div>

## Return Values

| Name    | Description                   | Type | Returned              | Sample                                                                                                                                             |
|---------|-------------------------------|------|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| changed | Whether any changes were made | bool | always                | true                                                                                                                                               |
| tag     | Details about the tag object  | dict | when state is present | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Production", "color": "Blue", "comments": "Production environment tag", "folder": "Texas"} |

## Error Handling

Common errors you might encounter when using this module:

| Error                   | Description                                                 | Resolution                                                                    |
|-------------------------|-------------------------------------------------------------|-------------------------------------------------------------------------------|
| Invalid tag data        | The tag parameters don't match required formats             | Verify the tag data conforms to SCM requirements, including valid color names |
| Tag name already exists | Attempt to create a tag with a name that already exists     | Use a unique name or update the existing tag                                  |
| Tag not found           | Attempt to update or delete a tag that doesn't exist        | Verify the tag name and container location                                    |
| Tag still in use        | Attempt to delete a tag that is referenced by other objects | Remove the tag from all objects before deletion                               |

<div class="termy">

<!-- termynal -->

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to create tag
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "Production"
        color: "Blue"
        folder: "Texas"
        state: "present"
      register: result
  rescue:
    - name: Handle tag already exists error
      debug:
        msg: "Tag already exists or invalid input provided"
    - name: Continue with other tasks
      # Additional recovery tasks
```

</div>

<div class="termy">

<!-- termynal -->

```yaml
- name: Handle tag deletion errors
  block:
    - name: Attempt to delete tag
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "Production"
        folder: "Texas"
        state: "absent"
  rescue:
    - name: Handle tag in use error
      debug:
        msg: "Unable to delete tag - it may still be in use"
    - name: List objects using this tag
      cdot65.scm.tag_info:
        provider: "{{ provider }}"
        name: "Production"
        folder: "Texas"
      register: tag_info
```

</div>

## Best Practices

1. **Naming Convention**
    - Use descriptive names that indicate the tag's purpose
    - Keep tag names concise but clear
    - Use lowercase names for consistency
    - Create a documented naming standard

2. **Color Coding**
    - Use consistent colors for similar categories
    - Create a color scheme for your organization (e.g., red for production, green for development)
    - Document the meaning of each color
    - Choose colors that provide good visual contrast

3. **Organization**
    - Create a hierarchical tagging system
    - Use tags for environment, function, location, compliance, etc.
    - Document your tagging strategy
    - Limit the total number of tag categories to avoid complexity

4. **Dynamic Address Groups**
    - Design tags specifically for use with dynamic address groups
    - Use logical combinations of tags in dynamic address group filters
    - Test tag expressions before implementing in production
    - Consider tag dependencies when designing tag hierarchies

5. **Maintenance**
    - Regularly review and clean up unused tags
    - Ensure tags are applied consistently across objects
    - Document which objects use each tag
    - Check for tag usage before deletion

## Related Modules

- [tag_info](tag_info.md) - Retrieve information about tag objects
- [address](address.md) - Manage address objects that can use tags
- [address_group](address_group.md) - Use tags in dynamic address group filters
- [service](service.md) - Apply tags to service objects
- [service_group](service_group.md) - Apply tags to service group objects

## Author

- Calvin Remsburg (@cdot65)