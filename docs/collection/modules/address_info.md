# Address Information Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Address Info Model Attributes](#address-info-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Retrieving Address Information](#retrieving-address-information)
    - [Getting a Specific Address](#getting-a-specific-address)
    - [Listing All Address Objects](#listing-all-address-objects)
    - [Filtering by Address Type](#filtering-by-address-type)
    - [Filtering by Tags](#filtering-by-tags)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
07. [Processing Retrieved Information](#processing-retrieved-information)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `address_info` Ansible module provides functionality to retrieve information about address
objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is a read-only module that can
retrieve detailed information about a specific address object by name, or list multiple address
objects with various filtering options. It supports advanced filtering capabilities including
container-based filtering, address type filtering, tag-based filtering, and exclusion filters.

## Core Methods

| Method     | Description                     | Parameters                               | Return Type                  |
| ---------- | ------------------------------- | ---------------------------------------- | ---------------------------- |
| `get()`    | Gets a specific address by name | `name: str`, `container: str`            | `AddressResponseModel`       |
| `list()`   | Lists addresses with filtering  | `folder: str`, `**filters`               | `List[AddressResponseModel]` |
| `filter()` | Applies filters to the results  | `addresses: List`, `filter_params: Dict` | `List[AddressResponseModel]` |

## Address Info Model Attributes

| Attribute          | Type | Required      | Description                                                      |
| ------------------ | ---- | ------------- | ---------------------------------------------------------------- |
| `name`             | str  | No            | The name of a specific address to retrieve                       |
| `gather_subset`    | list | No            | Determines which information to gather (default: ['config'])     |
| `folder`           | str  | One container | Filter addresses by folder (max 64 chars)                        |
| `snippet`          | str  | One container | Filter addresses by snippet (max 64 chars)                       |
| `device`           | str  | One container | Filter addresses by device (max 64 chars)                        |
| `exact_match`      | bool | No            | When True, only return objects in the specified container        |
| `exclude_folders`  | list | No            | List of folder names to exclude from results                     |
| `exclude_snippets` | list | No            | List of snippet values to exclude from results                   |
| `exclude_devices`  | list | No            | List of device values to exclude from results                    |
| `types`            | list | No            | Filter by address types ("netmask", "range", "wildcard", "fqdn") |
| `values`           | list | No            | Filter by address values                                         |
| `tags`             | list | No            | Filter by tags                                                   |

## Exceptions

| Exception                    | Description                       |
| ---------------------------- | --------------------------------- |
| `ObjectNotPresentError`      | Address not found                 |
| `MissingQueryParameterError` | Missing required parameters       |
| `InvalidFilterError`         | Invalid filter parameters         |
| `AuthenticationError`        | Authentication failed             |
| `ServerError`                | Internal server error             |
| `MultipleMatchesError`       | Multiple addresses match criteria |

## Basic Configuration

The Address Info module requires proper authentication credentials to access the Strata Cloud
Manager API.

```yaml
- name: Basic Address Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about addresses
      cdot65.scm.address_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: addresses_info
      
    - name: Display retrieved information
      debug:
        var: addresses_info.addresses
```

## Usage Examples

### Retrieving Address Information

The module provides several ways to retrieve address information based on your specific needs.

### Getting a Specific Address

This example retrieves detailed information about a specific address by name.

```yaml
- name: Get information about a specific address
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    name: "web-server"
    folder: "Texas"
  register: address_info

- name: Display address information
  debug:
    var: address_info.address
```

### Listing All Address Objects

This example lists all address objects in a specific folder.

```yaml
- name: List all address objects in a folder
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_addresses

- name: Display count of addresses
  debug:
    msg: "Found {{ all_addresses.addresses | length }} addresses in Texas folder"
```

### Filtering by Address Type

These examples show how to filter addresses by their type.

```yaml
- name: List only FQDN address objects
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
    types: ["fqdn"]
  register: fqdn_addresses

- name: List all IP/Netmask address objects
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
    types: ["netmask"]
  register: netmask_addresses
```

### Filtering by Tags

This example demonstrates how to find addresses with specific tags.

```yaml
- name: List addresses with specific tags
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["Production", "Web"]
  register: tagged_addresses

- name: Process tagged addresses
  debug:
    msg: "Address {{ item.name }} is tagged with Production and Web"
  loop: "{{ tagged_addresses.addresses }}"
  when: "'Production' in item.tag and 'Web' in item.tag"
```

### Using Advanced Filtering Options

These examples illustrate more advanced filtering options including exact match and exclusions.

```yaml
- name: List addresses with exact match and exclusions
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_addresses

- name: Use complex filtering with tags and address types
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["Dev"]
    types: ["netmask", "fqdn"]
    exclude_devices: ["DeviceA"]
  register: complex_filtered_addresses
```

## Processing Retrieved Information

After retrieving address information, you can process the data for various purposes such as
reporting, inventory management, or integration with other systems.

```yaml
- name: Create a summary of address information
  block:
    - name: Get all addresses
      cdot65.scm.address_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_addresses
      
    - name: Group addresses by type
      set_fact:
        netmask_addresses: "{{ all_addresses.addresses | selectattr('ip_netmask', 'defined') | list }}"
        fqdn_addresses: "{{ all_addresses.addresses | selectattr('fqdn', 'defined') | list }}"
        range_addresses: "{{ all_addresses.addresses | selectattr('ip_range', 'defined') | list }}"
        wildcard_addresses: "{{ all_addresses.addresses | selectattr('ip_wildcard', 'defined') | list }}"
        
    - name: Display summary information
      debug:
        msg: |
          Address Summary:
          - Total Addresses: {{ all_addresses.addresses | length }}
          - IP/Netmask Addresses: {{ netmask_addresses | length }}
          - FQDN Addresses: {{ fqdn_addresses | length }}
          - IP Range Addresses: {{ range_addresses | length }}
          - IP Wildcard Addresses: {{ wildcard_addresses | length }}
          - Addresses with tags: {{ all_addresses.addresses | selectattr('tag', 'defined') | list | length }}
```

## Error Handling

It's important to handle potential errors when retrieving address information.

```yaml
- name: Retrieve address info with error handling
  block:
    - name: Attempt to retrieve address information
      cdot65.scm.address_info:
        provider: "{{ provider }}"
        name: "nonexistent-address"
        folder: "Texas"
      register: address_info
      
  rescue:
    - name: Handle address not found error
      debug:
        msg: "Address not found or other error occurred"
        
    - name: Continue with fallback actions
      cdot65.scm.address_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_addresses
      
    - name: Log the error and continue
      debug:
        msg: "Continuing with list of all addresses instead of specific address"
```

## Best Practices

### Efficient Filtering

- Use specific filters to minimize the result set
- Filter by address type when you only need certain address types
- Combine multiple filters for more precise results
- Consider performance implications when retrieving large datasets

### Container Selection

- Use folder, snippet, or device consistently across operations
- Verify container existence before querying
- Use exclusion filters to refine results when working with large containers

### Information Handling

- Register results to variables for further processing
- Use Ansible's filtering capabilities (selectattr, map, etc.) on the returned lists
- Check if addresses/address is defined before accessing properties
- Process different address types appropriately (IP/Netmask, FQDN, etc.)

### Performance Optimization

- Retrieve only the information you need
- Use name parameter when you need only one specific address
- Use filters to minimize result set size
- Consider caching results for repeated access within the same playbook

### Security Considerations

- Protect sensitive information in filter criteria
- Store credentials securely using Ansible Vault
- Limit information gathering to necessary objects only
- Use least privilege accounts for API access

### Integration with Other Modules

- Use retrieved address information to inform other module operations
- Combine with address_group_info to understand object relationships
- Create dynamic inventories based on address information
- Generate reports on address usage and distribution

## Related Modules

- [address](address.md) - Manage address objects (create, update, delete)
- [address_group_info](address_group_info.md) - Retrieve information about address groups
- [address_group](address_group.md) - Manage address group objects
- [tag_info](tag_info.md) - Retrieve information about tags used with address objects
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules that use
  addresses
