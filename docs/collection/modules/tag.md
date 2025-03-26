# Tag Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Tag Model Attributes](#tag-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating Tags](#creating-tags)
    - [Basic Tag Creation](#basic-tag-creation)
    - [Creating Multiple Tags](#creating-multiple-tags)
    - [Advanced Tag Creation](#advanced-tag-creation)
    - [Updating Tags](#updating-tags)
    - [Deleting Tags](#deleting-tags)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `tag` module provides functionality to manage tag objects in Palo Alto Networks' Strata Cloud
Manager (SCM). This module allows you to create, update, and delete tag objects that can be used to
categorize and organize various resources within SCM. Tags are metadata labels that can be attached
to objects for filtering, policy application, and organization. They play a crucial role in dynamic
address groups and policy enforcement, enabling more flexible and maintainable security
configurations.

## Core Methods

| Method     | Description               | Parameters                    | Return Type              |
| ---------- | ------------------------- | ----------------------------- | ------------------------ |
| `create()` | Creates a new tag         | `data: Dict[str, Any]`        | `TagResponseModel`       |
| `update()` | Updates an existing tag   | `tag: TagUpdateModel`         | `TagResponseModel`       |
| `delete()` | Removes a tag             | `object_id: str`              | `None`                   |
| `fetch()`  | Gets a tag by name        | `name: str`, `container: str` | `TagResponseModel`       |
| `list()`   | Lists tags with filtering | `folder: str`, `**filters`    | `List[TagResponseModel]` |

## Tag Model Attributes

| Attribute  | Type | Required        | Description                                                     |
| ---------- | ---- | --------------- | --------------------------------------------------------------- |
| `name`     | str  | Yes             | Tag name (max 63 chars). Must match pattern: ^[a-zA-Z0-9.\_-]+$ |
| `color`    | str  | Yes             | Color associated with the tag from predefined list              |
| `comments` | str  | No              | Comments for the tag (max 1023 chars)                           |
| `folder`   | str  | One container\* | The folder where the tag is stored (max 64 chars)               |
| `snippet`  | str  | One container\* | The configuration snippet for the tag (max 64 chars)            |
| `device`   | str  | One container\* | The device where the tag is configured (max 64 chars)           |
| `state`    | str  | Yes             | Desired state of the tag object ("present" or "absent")         |

\*Exactly one container parameter must be provided.

### Available Tag Colors

Azure Blue, Black, Blue, Blue Gray, Blue Violet, Brown, Burnt Sienna, Cerulean Blue, Chestnut,
Cobalt Blue, Copper, Cyan, Forest Green, Gold, Gray, Green, Lavender, Light Gray, Light Green, Lime,
Magenta, Mahogany, Maroon, Medium Blue, Medium Rose, Medium Violet, Midnight Blue, Olive, Orange,
Orchid, Peach, Purple, Red, Red Violet, Red-Orange, Salmon, Thistle, Turquoise Blue, Violet Blue,
Yellow, Yellow-Orange

### Provider Dictionary

| Parameter       | Type | Required | Description                             |
| --------------- | ---- | -------- | --------------------------------------- |
| `client_id`     | str  | Yes      | Client ID for SCM authentication        |
| `client_secret` | str  | Yes      | Client secret for SCM authentication    |
| `tsg_id`        | str  | Yes      | Tenant Service Group ID                 |
| `log_level`     | str  | No       | Log level for the SDK (default: "INFO") |

## Exceptions

| Exception                    | Description                 |
| ---------------------------- | --------------------------- |
| `InvalidObjectError`         | Invalid tag data or format  |
| `NameNotUniqueError`         | Tag name already exists     |
| `ObjectNotPresentError`      | Tag not found               |
| `MissingQueryParameterError` | Missing required parameters |
| `AuthenticationError`        | Authentication failed       |
| `ServerError`                | Internal server error       |

## Basic Configuration

The Tag module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Tag Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a tag exists
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "Production"
        color: "Red"
        comments: "Production environment tag"
        folder: "Texas"
        state: "present"
```

## Usage Examples

### Creating Tags

Tags can be created with various colors and comments to visually identify and organize objects in
the Strata Cloud Manager.

### Basic Tag Creation

This example creates a simple tag for a production environment.

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

### Creating Multiple Tags

This example shows how to create multiple tags efficiently using a loop.

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

### Advanced Tag Creation

This example demonstrates creating a tag in a snippet instead of a folder.

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

### Updating Tags

```yaml
- name: Update tag color
  cdot65.scm.tag:
    provider: "{{ provider }}"
    name: "Production"
    color: "Red"
    folder: "Texas"
    state: "present"
```

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

### Deleting Tags

```yaml
- name: Remove tag
  cdot65.scm.tag:
    provider: "{{ provider }}"
    name: "Production"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting tags, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated tag objects"
```

### Return Values

| Name    | Description                   | Type | Returned              | Sample                                                                                                                                             |
| ------- | ----------------------------- | ---- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| changed | Whether any changes were made | bool | always                | true                                                                                                                                               |
| tag     | Details about the tag object  | dict | when state is present | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Production", "color": "Blue", "comments": "Production environment tag", "folder": "Texas"} |

## Error Handling

Common errors you might encounter when using this module:

| Error                   | Description                                                 | Resolution                                                                    |
| ----------------------- | ----------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Invalid tag data        | The tag parameters don't match required formats             | Verify the tag data conforms to SCM requirements, including valid color names |
| Tag name already exists | Attempt to create a tag with a name that already exists     | Use a unique name or update the existing tag                                  |
| Tag not found           | Attempt to update or delete a tag that doesn't exist        | Verify the tag name and container location                                    |
| Tag still in use        | Attempt to delete a tag that is referenced by other objects | Remove the tag from all objects before deletion                               |

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

## Best Practices

### Naming Convention

- Use descriptive names that indicate the tag's purpose
- Keep tag names concise but clear
- Use lowercase names for consistency
- Create a documented naming standard
- Consider using prefixes for tag categories (e.g., env-production, loc-dallas)

### Color Coding

- Use consistent colors for similar categories
- Create a color scheme for your organization (e.g., red for production, green for development)
- Document the meaning of each color
- Choose colors that provide good visual contrast
- Use color families for related tag categories

### Organization

- Create a hierarchical tagging system
- Use tags for environment, function, location, compliance, etc.
- Document your tagging strategy
- Limit the total number of tag categories to avoid complexity
- Create standard tags across all deployments for consistency

### Dynamic Address Groups

- Design tags specifically for use with dynamic address groups
- Use logical combinations of tags in dynamic address group filters
- Test tag expressions before implementing in production
- Consider tag dependencies when designing tag hierarchies
- Document tag combinations used in dynamic address groups

### Security Policy Design

- Align your tag strategy with security policy requirements
- Create tags that directly relate to security policy requirements
- Use tags to simplify policy management across multiple locations
- Document the relationship between tags and security policies
- Consider using tags for temporary policy exceptions

### Maintenance

- Regularly review and clean up unused tags
- Ensure tags are applied consistently across objects
- Document which objects use each tag
- Check for tag usage before deletion
- Implement automation for tag management and documentation

## Related Modules

- [tag_info](tag_info.md) - Retrieve information about tag objects
- [address](address.md) - Manage address objects that can use tags
- [address_group](address_group.md) - Use tags in dynamic address group filters
- [service](service.md) - Apply tags to service objects
- [service_group](service_group.md) - Apply tags to service group objects
- [security_rule](security_rule.md) - Configure security policies that may use tagged objects

## Author

- Calvin Remsburg (@cdot65)
