# Tag Information Module

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
    - [Retrieving Specific Tag Information](#retrieving-specific-tag-information)
    - [Listing All Tags](#listing-all-tags)
    - [Filtering Tags by Color](#filtering-tags-by-color)
    - [Using Advanced Filters](#using-advanced-filters)
    - [Filtering Tags by Prefix](#filtering-tags-by-prefix)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `tag_info` module provides functionality to gather information about tag objects in Palo Alto Networks' Strata Cloud
Manager. This is an information-gathering module that doesn't make any changes to the system. It supports retrieving a
specific tag by name or listing all tags with various filter options including color, container type, and exclusion
filters.

## Module Parameters

| Parameter              | Required | Type | Choices                                                      | Default    | Comments                                                        |
|------------------------|----------|------|--------------------------------------------------------------|------------|-----------------------------------------------------------------|
| name                   | no       | str  |                                                              |            | The name of a specific tag object to retrieve.                  |
| gather_subset          | no       | list | all, config                                                  | ['config'] | Determines which information to gather about tags.              |
| folder                 | no*      | str  |                                                              |            | Filter tags by folder container.                                |
| snippet                | no*      | str  |                                                              |            | Filter tags by snippet container.                               |
| device                 | no*      | str  |                                                              |            | Filter tags by device container.                                |
| exact_match            | no       | bool |                                                              | false      | Only return objects defined exactly in the specified container. |
| exclude_folders        | no       | list |                                                              |            | List of folder names to exclude from results.                   |
| exclude_snippets       | no       | list |                                                              |            | List of snippet values to exclude from results.                 |
| exclude_devices        | no       | list |                                                              |            | List of device values to exclude from results.                  |
| colors                 | no       | list | Azure Blue, Black, Blue, Blue Gray, Blue Violet, Brown, etc. |            | Filter by tag colors.                                           |
| provider               | yes      | dict |                                                              |            | Authentication credentials.                                     |
| provider.client_id     | yes      | str  |                                                              |            | Client ID for authentication.                                   |
| provider.client_secret | yes      | str  |                                                              |            | Client secret for authentication.                               |
| provider.tsg_id        | yes      | str  |                                                              |            | Tenant Service Group ID.                                        |
| provider.log_level     | no       | str  |                                                              | INFO       | Log level for the SDK.                                          |

**Available tag colors:** Azure Blue, Black, Blue, Blue Gray, Blue Violet, Brown, Burnt Sienna, Cerulean Blue, Chestnut,
Cobalt Blue, Copper, Cyan, Forest Green, Gold, Gray, Green, Lavender, Light Gray, Light Green, Lime, Magenta, Mahogany,
Maroon, Medium Blue, Medium Rose, Medium Violet, Midnight Blue, Olive, Orange, Orchid, Peach, Purple, Red, Red Violet,
Red-Orange, Salmon, Thistle, Turquoise Blue, Violet Blue, Yellow, Yellow-Orange

!!! note
- If `name` is not specified, one container type (`folder`, `snippet`, or `device`) must be provided.
- Container parameters (`folder`, `snippet`, `device`) are mutually exclusive.
- The `colors` parameter accepts a wide range of color values as listed above.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Retrieving Specific Tag Information

<div class="termy">

<!-- termynal -->

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

</div>

### Listing All Tags

<div class="termy">

<!-- termynal -->

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

</div>

### Filtering Tags by Color

<div class="termy">

<!-- termynal -->

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

</div>

### Using Advanced Filters

<div class="termy">

<!-- termynal -->

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

</div>

### Filtering Tags by Prefix

<div class="termy">

<!-- termynal -->

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

</div>

## Return Values

| Name | Description                                       | Type | Returned                   | Sample                                                                                                                                                     |
|------|---------------------------------------------------|------|----------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|
| tags | List of tag objects matching the filter criteria. | list | when name is not specified | [{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Production", "color": "Red", "comments": "Production environment tag", "folder": "Texas"}, {...}] |
| tag  | Information about the requested tag.              | dict | when name is specified     | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Production", "color": "Red", "comments": "Production environment tag", "folder": "Texas"}          |

## Error Handling

Common errors you might encounter when using this module:

| Error                     | Description                                         | Resolution                                        |
|---------------------------|-----------------------------------------------------|---------------------------------------------------|
| Tag not found             | Specified tag does not exist in the given container | Verify the tag name and container location        |
| Invalid color             | Provided color not in list of valid colors          | Check valid color options in module documentation |
| Missing query parameter   | Required parameter not provided                     | Ensure all required parameters are specified      |
| Invalid filter parameters | Filter parameters in incorrect format               | Check parameter format requirements               |

<div class="termy">

<!-- termynal -->

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

</div>

## Best Practices

1. **Querying Strategies**
    - Use name parameter for querying specific tags
    - Use container filters (folder, snippet, device) for listing tags
    - Combine with JMESPath filters in Ansible for advanced filtering
    - Create utility tasks for common filtering operations

2. **Performance Optimization**
    - Include specific container parameters to narrow search scope
    - Use exact_match parameter when possible to improve performance
    - Use exclusion filters to narrow down results when querying large systems
    - Cache results when making multiple queries on the same dataset

3. **Color Filtering**
    - Remember colors are case-sensitive in filter parameters
    - Use list notation even for single color filtering
    - Combine color filtering with other filters for precise results
    - Consider creating color variables or dictionaries for consistency

4. **Testing and Validation**
    - Use assert tasks to validate results as shown in examples
    - Include proper error handling for non-existent tags
    - Set up test tags with a variety of attributes for thorough testing
    - Use meaningful tag names that reflect their purpose

5. **Integration with Other Modules**
    - Use tag_info module output as input for tag module operations
    - Chain tag_info queries with other modules to automate complex workflows
    - Leverage the registered variables for conditional tasks
    - Consider creating custom filters for common tag operations

## Related Modules

- [tag](tag.md) - Manage tag objects
- [address](address.md) - Manage address objects that can use tags
- [service](service.md) - Manage service objects that can use tags
- [application](application.md) - Manage application objects that can use tags
- [address_group](address_group.md) - Use tags in dynamic address group filters

## Author

- Calvin Remsburg (@cdot65)