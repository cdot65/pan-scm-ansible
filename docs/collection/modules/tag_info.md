# Tag Information Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Tag Info Parameters](#tag-info-parameters)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Retrieving Specific Tag Information](#retrieving-specific-tag-information)
    - [Listing All Tags](#listing-all-tags)
    - [Filtering Tags by Color](#filtering-tags-by-color)
    - [Using Advanced Filters](#using-advanced-filters)
    - [Filtering Tags by Prefix](#filtering-tags-by-prefix)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `tag_info` module provides functionality to gather information about tag objects in Palo Alto
Networks' Strata Cloud Manager (SCM). This is an information-gathering module that doesn't make any
changes to the system. It supports retrieving a specific tag by name or listing all tags with
various filter options including color, container type, and exclusion filters. The module is
essential for inventory management, policy planning, and auditing tag usage across the organization.

## Core Methods

| Method    | Description                 | Parameters                    | Return Type              |
| --------- | --------------------------- | ----------------------------- | ------------------------ |
| `fetch()` | Gets a specific tag by name | `name: str`, `container: str` | `TagResponseModel`       |
| `list()`  | Lists tags with filtering   | `folder: str`, `**filters`    | `List[TagResponseModel]` |

## Tag Info Parameters

| Parameter          | Type | Required        | Description                                                    |
| ------------------ | ---- | --------------- | -------------------------------------------------------------- |
| `name`             | str  | No              | The name of a specific tag object to retrieve                  |
| `gather_subset`    | list | No              | Determines which information to gather (default: ['config'])   |
| `folder`           | str  | One container\* | Filter tags by folder container                                |
| `snippet`          | str  | One container\* | Filter tags by snippet container                               |
| `device`           | str  | One container\* | Filter tags by device container                                |
| `exact_match`      | bool | No              | Only return objects defined exactly in the specified container |
| `exclude_folders`  | list | No              | List of folder names to exclude from results                   |
| `exclude_snippets` | list | No              | List of snippet values to exclude from results                 |
| `exclude_devices`  | list | No              | List of device values to exclude from results                  |
| `colors`           | list | No              | Filter by tag colors                                           |

\*One container parameter is required when `name` is not specified.

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

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid request data or format |
| `MissingQueryParameterError` | Missing required parameters    |
| `ObjectNotPresentError`      | Tag not found                  |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The Tag Info module requires proper authentication credentials to access the Strata Cloud Manager
API.

```yaml
- name: Basic Tag Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about tags
      cdot65.scm.tag_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: tags_result
    
    - name: Display tags
      debug:
        var: tags_result.tags
```

## Usage Examples

### Retrieving Specific Tag Information

```yaml
- name: Get information about a specific tag
  cdot65.scm.tag_info:
    provider: "{{ provider }}"
    name: "Production"
    folder: "Texas"
  register: tag_info

- name: Display specific tag information
  debug:
    var: tag_info
    verbosity: 1

- name: Verify tag properties
  assert:
    that:
      - tag_info.tag.name == "Production"
      - tag_info.tag.color == "Red"
    fail_msg: "Failed to retrieve specific tag information"
    success_msg: "Successfully retrieved specific tag information"
```

### Listing All Tags

```yaml
- name: List all tag objects in a folder
  cdot65.scm.tag_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_tags

- name: Display all tags
  debug:
    var: all_tags
    verbosity: 1

- name: Verify tags listing
  assert:
    that:
      - all_tags.tags is defined
      - '"Production" in (all_tags.tags | map(attribute="name") | list)'
      - '"Development" in (all_tags.tags | map(attribute="name") | list)'
    fail_msg: "Failed to retrieve all tags"
    success_msg: "Successfully retrieved all tags"
```

### Filtering Tags by Color

```yaml
- name: List only tags with specific colors
  cdot65.scm.tag_info:
    provider: "{{ provider }}"
    folder: "Texas"
    colors: ["Red", "Blue"]
  register: colored_tags

- name: Display colored tags
  debug:
    var: colored_tags
    verbosity: 1

- name: Verify color-filtered tag query
  assert:
    that:
      - colored_tags.tags | selectattr('name', 'equalto', 'Production') | list | length == 1
      - colored_tags.tags | selectattr('name', 'equalto', 'Development') | list | length == 1
      - colored_tags.tags | selectattr('name', 'equalto', 'Testing') | list | length == 0
    fail_msg: "Failed to filter tags by color"
    success_msg: "Successfully filtered tags by color"
```

### Using Advanced Filters

```yaml
- name: List tags with exact match and exclusions
  cdot65.scm.tag_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_tags

- name: Display filtered tags
  debug:
    var: filtered_tags
    verbosity: 1
```

### Filtering Tags by Prefix

```yaml
# Since we can't filter by prefix directly using the module,
# we can filter the results using Ansible's built-in filters

# First, get all the tags
- name: Get all tags for dev- prefix filtering
  cdot65.scm.tag_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_tags_for_filtering

# Then, filter in memory for tags with names that start with dev-
- name: Filter tags for dev- prefix in memory
  set_fact:
    dev_tags: 
      tags: "{{ all_tags_for_filtering.tags | selectattr('name', 'match', '^dev-.*') | list }}"

- name: Display dev tags
  debug:
    var: dev_tags
    verbosity: 1

- name: Verify dev tags filtering
  assert:
    that:
      - dev_tags.tags | selectattr('name', 'equalto', 'dev-ansible') | list | length == 1
      - dev_tags.tags | selectattr('name', 'equalto', 'dev-automation') | list | length == 1
      - dev_tags.tags | selectattr('name', 'equalto', 'Production') | list | length == 0
    fail_msg: "Failed to filter tags by prefix"
    success_msg: "Successfully filtered tags by prefix"
```

## Managing Configuration Changes

As an info module, `tag_info` does not make any configuration changes. However, you can use the
information it retrieves to make decisions about other configuration operations.

```yaml
- name: Use tag information for dynamic address group configuration
  block:
    - name: Get available tags
      cdot65.scm.tag_info:
        provider: "{{ provider }}"
        folder: "Texas"
        colors: ["Red"]  # Get only production tags
      register: production_tags
      
    - name: Create dynamic address group using production tags
      cdot65.scm.address_group:
        provider: "{{ provider }}"
        name: "Production-Servers"
        folder: "Texas"
        dynamic_filter: "{{ production_tags.tags | map(attribute='name') | join(' or ') }}"
        description: "Dynamic group of all production servers"
        state: "present"
      when: production_tags.tags | length > 0
      
    - name: Commit changes if address group was created
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Created dynamic address group for production servers"
      when: production_tags.tags | length > 0
```

### Return Values

| Name | Description                                       | Type | Returned                   | Sample                                                                                                                                                     |
| ---- | ------------------------------------------------- | ---- | -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tags | List of tag objects matching the filter criteria. | list | when name is not specified | [{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Production", "color": "Red", "comments": "Production environment tag", "folder": "Texas"}, {...}] |
| tag  | Information about the requested tag.              | dict | when name is specified     | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Production", "color": "Red", "comments": "Production environment tag", "folder": "Texas"}          |

## Error Handling

Common errors you might encounter when using this module:

| Error                     | Description                                         | Resolution                                        |
| ------------------------- | --------------------------------------------------- | ------------------------------------------------- |
| Tag not found             | Specified tag does not exist in the given container | Verify the tag name and container location        |
| Invalid color             | Provided color not in list of valid colors          | Check valid color options in module documentation |
| Missing query parameter   | Required parameter not provided                     | Ensure all required parameters are specified      |
| Invalid filter parameters | Filter parameters in incorrect format               | Check parameter format requirements               |

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to retrieve tag information
      cdot65.scm.tag_info:
        provider: "{{ provider }}"
        name: "NonExistentTag"
        folder: "Texas"
      register: tag_info_result
  rescue:
    - name: Handle tag not found error
      debug:
        msg: "Tag could not be found, continuing with other tasks"
    - name: Continue with other tasks
      # Additional recovery tasks
```

## Best Practices

### Querying Strategies

- Use name parameter for querying specific tags
- Use container filters (folder, snippet, device) for listing tags
- Combine with JMESPath filters in Ansible for advanced filtering
- Create utility tasks for common filtering operations
- Document query patterns for reuse across playbooks

### Performance Optimization

- Include specific container parameters to narrow search scope
- Use exact_match parameter when possible to improve performance
- Use exclusion filters to narrow down results when querying large systems
- Cache results when making multiple queries on the same dataset
- Process large result sets in batches for better performance

### Color Filtering

- Remember colors are case-sensitive in filter parameters
- Use list notation even for single color filtering
- Combine color filtering with other filters for precise results
- Consider creating color variables or dictionaries for consistency
- Document color coding standards across your organization

### Testing and Validation

- Use assert tasks to validate results as shown in examples
- Include proper error handling for non-existent tags
- Set up test tags with a variety of attributes for thorough testing
- Use meaningful tag names that reflect their purpose
- Verify tag existence before dependency creation

### Integration with Other Modules

- Use tag_info module output as input for tag module operations
- Chain tag_info queries with other modules to automate complex workflows
- Leverage the registered variables for conditional tasks
- Consider creating custom filters for common tag operations
- Build helper roles for frequently used tag operations

### Dynamic Address Group Integration

- Retrieve tags strategically for dynamic address group filters
- Create standardized naming conventions for tags used in filters
- Document the relationship between tags and dynamic address groups
- Test tag expression updates before applying them to production
- Consider tag hierarchy when designing dynamic address groups

## Related Modules

- [tag](tag.md) - Manage tag objects (create, update, delete)
- [address](address.md) - Manage address objects that can use tags
- [address_group](address_group.md) - Use tags in dynamic address group filters
- [service](service.md) - Manage service objects that can use tags
- [service_group](service_group.md) - Apply tags to service group objects
- [security_rule](security_rule.md) - Configure security policies that may use tagged objects
- [application](application.md) - Manage application objects that can use tags

## Author

- Calvin Remsburg (@cdot65)
