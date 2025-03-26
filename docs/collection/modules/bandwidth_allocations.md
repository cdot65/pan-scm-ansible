# Bandwidth Allocations Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Bandwidth Allocation Model Attributes](#bandwidth-allocation-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating Basic Bandwidth Allocations](#creating-basic-bandwidth-allocations)
    - [Creating Bandwidth Allocations with QoS](#creating-bandwidth-allocations-with-qos)
    - [Updating Bandwidth Allocations](#updating-bandwidth-allocations)
    - [Deleting Bandwidth Allocations](#deleting-bandwidth-allocations)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `bandwidth_allocations` Ansible module provides functionality to manage Bandwidth Allocation objects in Palo Alto Networks' Strata Cloud Manager (SCM). Bandwidth Allocations allow you to specify and control the amount of bandwidth allocated to specific Service Provider Network (SPN) regions, with optional Quality of Service (QoS) settings.

## Core Methods

| Method     | Description                           | Parameters                      | Return Type                            |
|------------|---------------------------------------|---------------------------------|----------------------------------------|
| `create()` | Creates a new bandwidth allocation    | `data: Dict[str, Any]`          | `BandwidthAllocationResponseModel`     |
| `update()` | Updates an existing allocation        | `data: Dict[str, Any]`          | `BandwidthAllocationResponseModel`     |
| `delete()` | Removes a bandwidth allocation        | `name: str, spn_name_list: str` | `None`                                 |
| `get()`    | Gets an allocation by name            | `name: str`                     | `Optional[BandwidthAllocationResponseModel]` |
| `list()`   | Lists allocations with filtering      | `**filters`                     | `List[BandwidthAllocationResponseModel]` |

## Bandwidth Allocation Model Attributes

| Attribute               | Type      | Required | Description                                        |
|-------------------------|-----------|----------|----------------------------------------------------|
| `name`                  | str       | Yes      | Name of the aggregated bandwidth region            |
| `allocated_bandwidth`   | float     | Yes      | Bandwidth to allocate in Mbps (must be > 0)        |
| `spn_name_list`         | list(str) | No       | List of SPN names for this region                  |
| `qos`                   | dict      | No       | QoS configuration for bandwidth allocation         |
| `qos.enabled`           | bool      | No       | Enable QoS for bandwidth allocation                |
| `qos.customized`        | bool      | No       | Use customized QoS settings                        |
| `qos.profile`           | str       | No       | QoS profile name                                   |
| `qos.guaranteed_ratio`  | float     | No       | Guaranteed ratio for bandwidth                     |

## Exceptions

| Exception                    | Description                                        |
|------------------------------|----------------------------------------------------|
| `InvalidObjectError`         | Invalid bandwidth allocation data or format        |
| `MissingQueryParameterError` | Missing required parameters (like name)            |
| `ObjectNotPresentError`      | Bandwidth allocation not found                     |
| `AuthenticationError`        | Authentication failed                              |
| `ServerError`                | Internal server error                              |

## Basic Configuration

The Bandwidth Allocations module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Bandwidth Allocation Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Create a basic bandwidth allocation
      cdot65.scm.bandwidth_allocations:
        provider: "{{ provider }}"
        name: "East_Region"
        allocated_bandwidth: 500.0
        spn_name_list:
          - "SPN1"
          - "SPN2"
        state: "present"
```

## Usage Examples

### Creating Basic Bandwidth Allocations

This example creates a basic bandwidth allocation for a region with specified SPNs.

```yaml
- name: Create a basic bandwidth allocation
  cdot65.scm.bandwidth_allocations:
    provider: "{{ provider }}"
    name: "East_Region"
    allocated_bandwidth: 500.0
    spn_name_list:
      - "SPN1"
      - "SPN2"
    state: "present"
  register: bandwidth_result

- name: Display created bandwidth allocation
  debug:
    var: bandwidth_result
```

### Creating Bandwidth Allocations with QoS

This example creates a bandwidth allocation with QoS settings enabled.

```yaml
- name: Create bandwidth allocation with QoS
  cdot65.scm.bandwidth_allocations:
    provider: "{{ provider }}"
    name: "West_Region"
    allocated_bandwidth: 750.0
    spn_name_list:
      - "SPN3"
      - "SPN4"
    qos:
      enabled: true
      customized: true
      profile: "High_Priority"
      guaranteed_ratio: 0.75
    state: "present"
```

For more customized QoS settings, you can specify additional parameters:

```yaml
- name: Create bandwidth allocation with customized QoS
  cdot65.scm.bandwidth_allocations:
    provider: "{{ provider }}"
    name: "Central_Region"
    allocated_bandwidth: 1000.0
    spn_name_list:
      - "SPN5"
      - "SPN6"
    qos:
      enabled: true
      customized: true
      profile: "High_Priority"
      guaranteed_ratio: 0.75
    state: "present"
```

### Updating Bandwidth Allocations

This example updates an existing bandwidth allocation with new bandwidth and QoS settings.

```yaml
- name: Update a bandwidth allocation
  cdot65.scm.bandwidth_allocations:
    provider: "{{ provider }}"
    name: "East_Region"
    allocated_bandwidth: 800.0
    spn_name_list:
      - "SPN1"
      - "SPN2"
    qos:
      enabled: true
      customized: false
    state: "present"
```

### Deleting Bandwidth Allocations

This example removes a bandwidth allocation. Note that both the name and spn_name_list are required for deletion.

```yaml
- name: Delete a bandwidth allocation
  cdot65.scm.bandwidth_allocations:
    provider: "{{ provider }}"
    name: "Central_Region"
    spn_name_list:
      - "SPN5"
      - "SPN6"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting bandwidth allocations, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    description: "Updated bandwidth allocation configurations"
```

## Error Handling

It's important to handle potential errors when working with bandwidth allocations.

```yaml
- name: Create or update bandwidth allocation with error handling
  block:
    - name: Ensure bandwidth allocation exists
      cdot65.scm.bandwidth_allocations:
        provider: "{{ provider }}"
        name: "East_Region"
        allocated_bandwidth: 500.0
        spn_name_list:
          - "SPN1"
          - "SPN2"
        state: "present"
      register: allocation_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        description: "Updated bandwidth allocation configurations"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```

## Best Practices

### Bandwidth Configuration

- Allocate bandwidth based on actual traffic requirements and business priorities
- Use meaningful names for your bandwidth regions that reflect geographical or logical groupings
- Document bandwidth allocations in your organization's network documentation
- Set appropriate bandwidth values based on available resources and network capacity
- Consider the impact of bandwidth allocations on other network services

### QoS Settings

- Enable QoS for regions with critical applications or prioritized traffic
- Use customized QoS settings for fine-grained control over traffic prioritization
- Set appropriate guaranteed ratios based on application requirements
- Document QoS profiles and their intended purposes
- Test QoS settings to ensure they deliver the expected performance

### SPN Management

- Group related SPNs in the same bandwidth allocation region
- Maintain a consistent naming convention for SPN references
- Regularly review and update SPN lists as your network evolves
- Consider the geographical proximity of SPNs when grouping them in regions
- Document the purpose and relationships between SPNs and bandwidth allocations

### Operations

- Implement change management procedures for bandwidth allocation modifications
- Schedule bandwidth changes during maintenance windows if possible
- Test configurations in a pre-production environment
- Monitor bandwidth utilization after changes
- Create a rollback plan for any bandwidth allocation changes

## Related Modules

- [bandwidth_allocations_info](bandwidth_allocations_info.md) - Retrieve information about bandwidth allocations
- [remote_networks](remote_networks.md) - Manage remote networks configuration
- [network_locations](network_locations.md) - Manage network locations
- [service_connections](service_connections.md) - Manage service connections