# Address Group Information Object

## Table of Contents

- [Address Group Information Object](#address-group-information-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [Address Group Info Model Attributes](#address-group-info-model-attributes)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Retrieving Address Group Information](#retrieving-address-group-information)
    - [Getting a Specific Address Group](#getting-a-specific-address-group)
    - [Listing All Address Groups](#listing-all-address-groups)
    - [Filtering by Address Group Type](#filtering-by-address-group-type)
    - [Filtering by Tags](#filtering-by-tags)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
  - [Processing Retrieved Information](#processing-retrieved-information)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Efficient Filtering](#efficient-filtering)
    - [Container Selection](#container-selection)
    - [Information Handling](#information-handling)
    - [Performance Optimization](#performance-optimization)
    - [Security Considerations](#security-considerations)
  - [Related Modules](#related-modules)

## Overview

The `address_group_info` Ansible module provides functionality to retrieve information about address
group objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is a read-only module that can
retrieve detailed information about a specific address group object by name, or list multiple
address group objects with various filtering options. It supports advanced filtering capabilities
including group type filtering (static or dynamic), tag-based filtering, and exclusion filters.

## Core Methods

| Method     | Description                           | Parameters                                    | Return Type                       |
| ---------- | ------------------------------------- | --------------------------------------------- | --------------------------------- |
| `get()`    | Gets a specific address group by name | `name: str`, `container: str`                 | `AddressGroupResponseModel`       |
| `list()`   | Lists address groups with filtering   | `folder: str`, `**filters`                    | `List[AddressGroupResponseModel]` |
| `filter()` | Applies filters to the results        | `address_groups: List`, `filter_params: Dict` | `List[AddressGroupResponseModel]` |

## Address Group Info Model Attributes

| Attribute          | Type | Required      | Description                                                  |
| ------------------ | ---- | ------------- | ------------------------------------------------------------ |
| `name`             | str  | No            | The name of a specific address group to retrieve             |
| `gather_subset`    | list | No            | Determines which information to gather (default: ['config']) |
| `folder`           | str  | One container | Filter address groups by folder (max 64 chars)               |
| `snippet`          | str  | One container | Filter address groups by snippet (max 64 chars)              |
| `device`           | str  | One container | Filter address groups by device (max 64 chars)               |
| `exact_match`      | bool | No            | When True, only return objects in the specified container    |
| `exclude_folders`  | list | No            | List of folder names to exclude from results                 |
| `exclude_snippets` | list | No            | List of snippet values to exclude from results               |
| `exclude_devices`  | list | No            | List of device values to exclude from results                |
| `types`            | list | No            | Filter by address group types ("static", "dynamic")          |
| `values`           | list | No            | Filter by address group values (members or filter)           |
| `tags`             | list | No            | Filter by tags                                               |

## Exceptions

| Exception                    | Description                            |
| ---------------------------- | -------------------------------------- |
| `ObjectNotPresentError`      | Address group not found                |
| `MissingQueryParameterError` | Missing required parameters            |
| `InvalidFilterError`         | Invalid filter parameters              |
| `AuthenticationError`        | Authentication failed                  |
| `ServerError`                | Internal server error                  |
| `MultipleMatchesError`       | Multiple address groups match criteria |

## Basic Configuration

The Address Group Info module requires proper authentication credentials to access the Strata Cloud
Manager API.

```yaml
- name: Basic Address Group Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about address groups
      cdot65.scm.address_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: groups_info
      
    - name: Display retrieved information
      debug:
        var: groups_info.address_groups
```

## Usage Examples

### Retrieving Address Group Information

The module provides several ways to retrieve address group information based on your specific needs.

### Getting a Specific Address Group

This example retrieves detailed information about a specific address group by name.

```yaml
- name: Get information about a specific address group
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    name: "Test_Static_Group_Info"
    folder: "Texas"
  register: specific_info

- name: Display specific address group information
  debug:
    var: specific_info.address_group
```

### Listing All Address Groups

This example lists all address groups in a specific folder.

```yaml
- name: List all address groups in the folder
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_groups

- name: Display count of address groups
  debug:
    msg: "Found {{ all_groups.address_groups | length }} address groups in Texas folder"
```

### Filtering by Address Group Type

These examples show how to filter address groups by their type (static or dynamic).

```yaml
- name: List only static address groups
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    types: ["static"]
  register: static_groups

- name: List only dynamic address groups
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    types: ["dynamic"]
  register: dynamic_groups
```

### Filtering by Tags

This example demonstrates how to find address groups with specific tags.

```yaml
- name: List address groups with specific tag
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["dev-test"]
  register: tagged_groups

- name: Process tagged address groups
  debug:
    msg: "Address group {{ item.name }} is tagged with dev-test"
  loop: "{{ tagged_groups.address_groups }}"
  when: "'dev-test' in item.tag"
```

### Using Advanced Filtering Options

These examples illustrate more advanced filtering options including exact match and exclusions.

```yaml
- name: List address groups with exact match and exclusions
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_groups

- name: Use complex filtering with tags and group types
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["dev-automation"]
    types: ["dynamic"]
    exclude_devices: ["DeviceA"]
  register: complex_filtered_groups
```

## Processing Retrieved Information

After retrieving address group information, you can process the data for various purposes such as
reporting, inventory, or integration with other systems.

```yaml
- name: Create a summary of address group information
  block:
    - name: Get all address groups
      cdot65.scm.address_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_groups
      
    - name: Count static vs dynamic groups
      set_fact:
        static_count: "{{ all_groups.address_groups | selectattr('static', 'defined') | list | length }}"
        dynamic_count: "{{ all_groups.address_groups | selectattr('dynamic', 'defined') | list | length }}"
        
    - name: Display summary information
      debug:
        msg: |
          Address Group Summary:
          - Total Groups: {{ all_groups.address_groups | length }}
          - Static Groups: {{ static_count }}
          - Dynamic Groups: {{ dynamic_count }}
          - Groups with tags: {{ all_groups.address_groups | selectattr('tag', 'defined') | list | length }}
```

## Error Handling

It's important to handle potential errors when retrieving address group information.

```yaml
- name: Retrieve address group info with error handling
  block:
    - name: Attempt to retrieve address group information
      cdot65.scm.address_group_info:
        provider: "{{ provider }}"
        name: "non_existent_group"
        folder: "Texas"
      register: group_info
      
  rescue:
    - name: Handle group not found error
      debug:
        msg: "Address group not found or other error occurred"
        
    - name: Continue with fallback actions
      cdot65.scm.address_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_groups
      
    - name: Log the error and continue
      debug:
        msg: "Continuing with list of all groups instead of specific group"
```

## Best Practices

### Efficient Filtering

- Use specific filters to minimize the result set
- Filter by group type when you only need static or dynamic groups
- Combine multiple filters for more precise results
- Consider performance implications when retrieving large datasets

### Container Selection

- Use folder, snippet, or device consistently across operations
- Verify container existence before querying
- Use exclusion filters to refine results when working with large containers

### Information Handling

- Register results to variables for further processing
- Use Ansible's filtering capabilities (selectattr, map, etc.) on the returned lists
- Check if address_groups/address_group is defined before accessing properties
- Process static and dynamic groups differently as they have different structure

### Performance Optimization

- Retrieve only the information you need
- Use name parameter when you need only one specific group
- Use filters to minimize result set size
- Consider caching results for repeated access within the same playbook

### Security Considerations

- Protect sensitive information in filter criteria
- Store credentials securely using Ansible Vault
- Limit information gathering to necessary objects only
- Use least privilege accounts for API access

## Related Modules

- [address_group](address_group.md) - Manage address group objects (create, update, delete)
- [address](address.md) - Manage address objects
- [address_info](address_info.md) - Retrieve information about address objects
- [tag](tag.md) - Manage tags used with address groups
- [security_rule](security_rule.md) - Manage security rules that use address groups
