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
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `tag_info` module provides functionality to gather information about tag objects in Palo Alto Networks' Strata Cloud Manager. This is an information-gathering module that doesn't make any changes to the system. It supports retrieving a specific tag by name or listing all tags with various filter options including color, container type, and exclusion filters.

## Module Parameters

| Parameter              | Required | Type  | Choices                                                                                              | Default    | Comments                                                           |
|------------------------|----------|-------|------------------------------------------------------------------------------------------------------|------------|-------------------------------------------------------------------|
| name                   | no       | str   |                                                                                                      |            | The name of a specific tag object to retrieve.                     |
| gather_subset          | no       | list  | all, config                                                                                          | ['config'] | Determines which information to gather about tags.                 |
| folder                 | no*      | str   |                                                                                                      |            | Filter tags by folder container.                                   |
| snippet                | no*      | str   |                                                                                                      |            | Filter tags by snippet container.                                  |
| device                 | no*      | str   |                                                                                                      |            | Filter tags by device container.                                   |
| exact_match            | no       | bool  |                                                                                                      | false      | Only return objects defined exactly in the specified container.    |
| exclude_folders        | no       | list  |                                                                                                      |            | List of folder names to exclude from results.                      |
| exclude_snippets       | no       | list  |                                                                                                      |            | List of snippet values to exclude from results.                    |
| exclude_devices        | no       | list  |                                                                                                      |            | List of device values to exclude from results.                     |
| colors                 | no       | list  | Azure Blue, Black, Blue, Blue Gray, Blue Violet, Brown, etc. (see module documentation for full list)|            | Filter by tag colors.                                              |
| provider               | yes      | dict  |                                                                                                      |            | Authentication credentials.                                        |
| provider.client_id     | yes      | str   |                                                                                                      |            | Client ID for authentication.                                      |
| provider.client_secret | yes      | str   |                                                                                                      |            | Client secret for authentication.                                  |
| provider.tsg_id        | yes      | str   |                                                                                                      |            | Tenant Service Group ID.                                           |
| provider.log_level     | no       | str   |                                                                                                      | INFO       | Log level for the SDK.                                             |

!!! note
    - If `name` is not specified, one container type (`folder`, `snippet`, or `device`) must be provided.
    - Container parameters (`folder`, `snippet`, `device`) are mutually exclusive.
    - The `colors` parameter accepts a wide range of color values - see module documentation for the full list.

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

- name: Filter tags for dev- prefix in memory
  set_fact:
    dev_tags: 
      tags: "{{ all_tags.tags | selectattr('name', 'match', '^dev-.*') | list }}"
```

</div>

## Return Values

| Name  | Description                                                | Type | Returned                         | Sample                                                                                                                                       |
|-------|------------------------------------------------------------|------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| tags  | List of tag objects matching the filter criteria.          | list | when name is not specified       | [{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Production", "color": "Red", "comments": "Production environment tag", "folder": "Texas"}, {...}] |
| tag   | Information about the requested tag.                       | dict | when name is specified           | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Production", "color": "Red", "comments": "Production environment tag", "folder": "Texas"} |

## Error Handling

Common errors you might encounter when using this module:

| Error | Description | Resolution |
|-------|-------------|------------|
| Tag not found | Specified tag does not exist in the given container | Verify the tag name and container location |
| Invalid color | Provided color not in list of valid colors | Check valid color options in module documentation |
| Missing query parameter | Required parameter not provided | Ensure all required parameters are specified |
| Invalid filter parameters | Filter parameters in incorrect format | Check parameter format requirements |

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

2. **Performance Optimization**
   - Include specific container parameters to narrow search scope
   - Use exact_match parameter when possible to improve performance
   - Use exclusion filters to narrow down results when querying large systems

3. **Color Filtering**
   - Remember colors are case-sensitive in filter parameters
   - Use list notation even for single color filtering
   - Combine color filtering with other filters for precise results

4. **Integration with Other Modules**
   - Use tag_info module output as input for tag module operations
   - Chain tag_info queries with other modules to automate complex workflows
   - Leverage the registered variables for conditional tasks

5. **Error Management**
   - Implement proper error handling with block/rescue pattern
   - Handle non-existent tags gracefully in playbooks
   - Use ignore_errors where appropriate for non-critical tag queries

## Related Modules

- [tag](tag.md) - Manage tag objects
- [address](address.md) - Manage address objects that can use tags
- [service](service.md) - Manage service objects that can use tags
- [application](application.md) - Manage application objects that can use tags

## Author

- Calvin Remsburg (@cdot65)