# Bandwidth Allocations Information Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Bandwidth Allocation Info Parameters](#bandwidth-allocation-info-parameters)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Getting Information about a Specific Bandwidth Allocation](#getting-information-about-a-specific-bandwidth-allocation)
    - [Listing All Bandwidth Allocations](#listing-all-bandwidth-allocations)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
07. [Error Handling](#error-handling)
08. [Best Practices](#best-practices)
09. [Related Modules](#related-modules)

## Overview

The `bandwidth_allocations_info` Ansible module provides functionality to gather information about Bandwidth Allocation objects in Palo Alto Networks' Strata Cloud Manager (SCM). This info module allows fetching details about specific bandwidth allocations or listing allocations with various filtering options.

## Core Methods

| Method    | Description                      | Parameters                   | Return Type                            |
| --------- | -------------------------------- | ---------------------------- | -------------------------------------- |
| `get()`   | Gets a specific allocation by ID | `allocation_id: str`         | `BandwidthAllocationResponseModel`     |
| `list()`  | Lists allocations with filtering | `**filters`                  | `List[BandwidthAllocationResponseModel]` |

## Bandwidth Allocation Info Parameters

| Parameter         | Type    | Required | Description                                     |
| ----------------- | ------- | -------- | ----------------------------------------------- |
| `provider`        | dict    | Yes      | Authentication credentials for SCM              |
| `name`            | str     | No       | Name of a specific bandwidth allocation to retrieve |
| `spn_name_list`   | list    | No       | Filter allocations by SPN name list             |
| `region`          | str     | No       | Filter allocations by region name               |
| `limit`           | int     | No       | Limit the number of results returned            |
| `offset`          | int     | No       | Offset for pagination of results                |
| `order_by`        | str     | No       | Field to order results by                       |
| `sort`            | str     | No       | Sort direction ('asc' or 'desc')               |

## Exceptions

| Exception                    | Description                       |
| ---------------------------- | --------------------------------- |
| `InvalidObjectError`         | Invalid request data or format    |
| `MissingQueryParameterError` | Missing required parameters       |
| `ObjectNotPresentError`      | Bandwidth allocation not found    |
| `AuthenticationError`        | Authentication failed             |
| `ServerError`                | Internal server error             |

## Basic Configuration

The Bandwidth Allocations Info module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Bandwidth Allocation Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about bandwidth allocations
      cdot65.scm.bandwidth_allocations_info:
        provider: "{{ provider }}"
      register: allocations_result
      
    - name: Display retrieved bandwidth allocations
      debug:
        var: allocations_result
```

## Usage Examples

### Getting Information about a Specific Bandwidth Allocation

Retrieve details about a specific bandwidth allocation by name.

```yaml
- name: Get information about a specific bandwidth allocation
  cdot65.scm.bandwidth_allocations_info:
    provider: "{{ provider }}"
    name: "East_Region"
  register: allocation_info
  
- name: Display bandwidth allocation information
  debug:
    var: allocation_info.bandwidth_allocation
    
- name: Check allocated bandwidth
  debug:
    msg: "Allocated bandwidth is {{ allocation_info.bandwidth_allocation.allocated_bandwidth }} Mbps"
  when: allocation_info.bandwidth_allocation is defined
```

### Listing All Bandwidth Allocations

List all bandwidth allocations.

```yaml
- name: List all bandwidth allocations
  cdot65.scm.bandwidth_allocations_info:
    provider: "{{ provider }}"
  register: all_allocations
  
- name: Display all bandwidth allocations
  debug:
    var: all_allocations.bandwidth_allocations
    
- name: Display count of bandwidth allocations
  debug:
    msg: "Found {{ all_allocations.bandwidth_allocations | length }} bandwidth allocations"
    
- name: List names of all bandwidth allocations
  debug:
    msg: "{{ all_allocations.bandwidth_allocations | map(attribute='name') | list }}"
```

### Using Advanced Filtering Options

Use advanced filtering options to refine your query results.

```yaml
- name: Filter bandwidth allocations by region
  cdot65.scm.bandwidth_allocations_info:
    provider: "{{ provider }}"
    region: "us-east-1"
    limit: 5
    order_by: "name"
    sort: "asc"
  register: filtered_allocations
  
- name: Process filtered allocations
  debug:
    msg: "Allocation: {{ item.name }} ({{ item.allocated_bandwidth }} Mbps)"
  loop: "{{ filtered_allocations.bandwidth_allocations }}"
  
- name: Find allocations for specific SPNs
  cdot65.scm.bandwidth_allocations_info:
    provider: "{{ provider }}"
    spn_name_list:
      - "SPN1"
  register: spn_allocations
```

## Error Handling

It's important to handle potential errors when retrieving information about bandwidth allocations.

```yaml
- name: Get information about bandwidth allocations with error handling
  block:
    - name: Try to retrieve information about a bandwidth allocation
      cdot65.scm.bandwidth_allocations_info:
        provider: "{{ provider }}"
        name: "East_Region"
      register: info_result
      
    - name: Display bandwidth allocation information
      debug:
        var: info_result.bandwidth_allocation
        
  rescue:
    - name: Handle errors
      debug:
        msg: "Failed to retrieve bandwidth allocation information: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a 'not found' error
      debug:
        msg: "The specified bandwidth allocation does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

## Best Practices

### Efficient Querying

- Use specific filters to reduce API load and improve performance
- When looking for a specific allocation, use the `name` parameter instead of filtering results
- Use pagination (limit and offset) when dealing with large numbers of allocations
- Sort results to maintain consistent ordering across queries

### Result Processing

- Always register the module output to a variable for later use
- Check if the expected data is present before processing it
- Use appropriate Ansible filters and tests when processing complex nested structures
- Process allocation data to extract meaningful information for your automation tasks
- Use conditionals to handle cases where allocations may not exist

### Inventory Management

- Use the info module to build dynamic inventories based on bandwidth allocations
- Map bandwidth allocations to their corresponding network elements
- Track allocation usage and changes over time
- Use allocation information to make capacity planning decisions

### Integration with Other Modules

- Use the info module to check for existing allocations before creating new ones
- Combine with the bandwidth_allocations module for complete allocation management
- Use retrieved allocation information to make decisions in your playbooks
- Feed allocation data into monitoring and reporting systems

### Troubleshooting

- Use the info module to diagnose bandwidth allocation issues
- Compare actual and expected allocation configurations
- Verify QoS settings against performance requirements
- Check SPN assignments to ensure proper network coverage

## Related Modules

- [bandwidth_allocations](bandwidth_allocations.md) - Create, update, and delete bandwidth allocations
- [remote_networks](remote_networks.md) - Manage remote networks configuration
- [network_locations](network_locations.md) - Manage network locations
- [service_connections](service_connections.md) - Manage service connections