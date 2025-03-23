# Service Group Information Module

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
    - [Retrieving Specific Service Group Information](#retrieving-specific-service-group-information)
    - [Listing All Service Groups](#listing-all-service-groups)
    - [Filtering by Members](#filtering-by-members)
    - [Filtering by Tags](#filtering-by-tags)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `service_group_info` module provides functionality to gather information about service group objects in Palo Alto Networks' Strata Cloud Manager. This is an information-gathering module that doesn't make any changes to the system. It supports retrieving a specific service group by name or listing all service groups with various filter options including members, tags, and container filters.

## Module Parameters

| Parameter              | Required | Type  | Choices          | Default    | Comments                                                           |
|------------------------|----------|-------|------------------|------------|-------------------------------------------------------------------|
| name                   | no       | str   |                  |            | The name of a specific service group object to retrieve.           |
| gather_subset          | no       | list  | all, config      | ['config'] | Determines which information to gather about service groups.       |
| folder                 | no*      | str   |                  |            | Filter service groups by folder container.                         |
| snippet                | no*      | str   |                  |            | Filter service groups by snippet container.                        |
| device                 | no*      | str   |                  |            | Filter service groups by device container.                         |
| exact_match            | no       | bool  |                  | false      | Only return objects defined exactly in the specified container.    |
| exclude_folders        | no       | list  |                  |            | List of folder names to exclude from results.                      |
| exclude_snippets       | no       | list  |                  |            | List of snippet values to exclude from results.                    |
| exclude_devices        | no       | list  |                  |            | List of device values to exclude from results.                     |
| members                | no       | list  |                  |            | Filter by service members contained in the groups.                 |
| tags                   | no       | list  |                  |            | Filter by tags associated with service groups.                      |
| provider               | yes      | dict  |                  |            | Authentication credentials.                                        |
| provider.client_id     | yes      | str   |                  |            | Client ID for authentication.                                      |
| provider.client_secret | yes      | str   |                  |            | Client secret for authentication.                                  |
| provider.tsg_id        | yes      | str   |                  |            | Tenant Service Group ID.                                           |
| provider.log_level     | no       | str   |                  | INFO       | Log level for the SDK.                                             |

!!! note
    - If `name` is not specified, one container type (`folder`, `snippet`, or `device`) must be provided.
    - Container parameters (`folder`, `snippet`, `device`) are mutually exclusive.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Retrieving Specific Service Group Information

<div class="termy">

<!-- termynal -->

```yaml
- name: Get information about a specific service group
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    name: "web-services"
    folder: "Texas"
  register: service_group_info
```

</div>

### Listing All Service Groups

<div class="termy">

<!-- termynal -->

```yaml
- name: List all service group objects in a folder
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_service_groups
```

</div>

### Filtering by Members

<div class="termy">

<!-- termynal -->

```yaml
- name: List service groups containing a specific member
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    members: ["HTTPS"]
  register: https_service_groups
```

</div>

### Filtering by Tags

<div class="termy">

<!-- termynal -->

```yaml
- name: List service groups with specific tags
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["Production", "Web"]
  register: tagged_service_groups
```

</div>

### Advanced Filtering with Ansible

<div class="termy">

<!-- termynal -->

```yaml
# Since the module doesn't support filtering by name prefix directly,
# we can use Ansible's built-in filters to achieve this
- name: Get all service groups for name prefix filtering
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_groups_for_filtering
  
# Filter service groups for names starting with "dev-" in memory
- name: Filter service groups for dev- prefix in memory
  set_fact:
    dev_groups: 
      service_groups: "{{ all_groups_for_filtering.service_groups | selectattr('name', 'match', '^dev-.*') | list }}"

# Work with the filtered results
- name: Display filtered service groups
  debug:
    var: dev_groups
```

</div>

## Return Values

| Name           | Description                                                | Type | Returned                         | Sample                                                                                                                                       |
|----------------|------------------------------------------------------------|------|----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| service_groups | List of service group objects matching the filter criteria.| list | when name is not specified       | [{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-services", "members": ["HTTPS", "SSH", "web-custom-service"], "folder": "Texas", "tag": ["Web", "Production"]}, {...}] |
| service_group  | Information about the requested service group.             | dict | when name is specified           | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-services", "members": ["HTTPS", "SSH", "web-custom-service"], "folder": "Texas", "tag": ["Web", "Production"]} |

## Error Handling

Common errors you might encounter when using this module:

| Error | Description | Resolution |
|-------|-------------|------------|
| Service group not found | Specified service group does not exist in the given container | Verify the service group name and container location |
| Missing query parameter | Required parameter not provided | Ensure all required parameters are specified |
| Invalid filter parameters | Filter parameters in incorrect format | Check parameter format requirements |

<div class="termy">

<!-- termynal -->

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to retrieve service group information
      cdot65.scm.service_group_info:
        provider: "{{ provider }}"
        name: "NonExistentGroup"
        folder: "Texas"
      register: service_group_info_result
  rescue:
    - name: Handle service group not found error
      debug:
        msg: "Service group could not be found, continuing with other tasks"
    - name: Continue with other tasks
      # Additional recovery tasks
```

</div>

## Best Practices

1. **Querying Strategies**
   - Use name parameter for querying specific service groups
   - Use container filters (folder, snippet, device) for listing service groups
   - Combine with JMESPath filters in Ansible for advanced filtering

2. **Performance Optimization**
   - Include specific container parameters to narrow search scope
   - Use exact_match parameter when possible to improve performance
   - Use exclusion filters to narrow down results when querying large systems

3. **Member-Based Filtering**
   - Filter by members to find groups containing specific services
   - Use member-based filtering to trace service dependencies
   - Identify all groups that would be affected by changes to a specific service

4. **Tag-Based Filtering**
   - Use tag filtering to group service groups by function or environment
   - Combine multiple tags with AND logic to narrow results
   - Create consistent tagging conventions for easier filtering

5. **Naming and Uniqueness**
   - Consider using timestamps in object names for test environments
   - Use Ansible's `lookup('pipe', 'date +%Y%m%d%H%M%S')` to generate timestamps
   - Store dynamic object names in variables for easier reference and cleanup
   - Ensure unique names to avoid conflicts when testing

6. **Integration with Other Modules**
   - Use service_group_info module output as input for service_group module operations
   - Chain info queries with security policy modules to see where service groups are used
   - Leverage the registered variables for conditional tasks and reporting

## Related Modules

- [service_group](service_group.md) - Manage service group objects
- [service](service.md) - Manage individual service objects 
- [service_info](service_info.md) - Retrieve information about service objects
- [tag](tag.md) - Manage tags used with service group objects

## Author

- Calvin Remsburg (@cdot65)