# Quarantined Devices Information Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Examples](#examples)
   - [List All Quarantined Devices](#list-all-quarantined-devices)
   - [Filter by Host ID](#filter-by-host-id)
   - [Filter by Serial Number](#filter-by-serial-number)
   - [Using Different Gather Subsets](#using-different-gather-subsets)
4. [Return Values](#return-values)
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)
7. [Related Modules](#related-modules)

## Overview

The `quarantined_devices_info` module provides functionality to retrieve information about
quarantined devices in Palo Alto Networks' Strata Cloud Manager (SCM). This module allows you to
list all quarantined devices or filter the results by host ID or serial number. As an info module,
it only retrieves information and does not modify any configuration.

## Module Parameters

| Parameter       | Type | Required | Description                                                  |
| --------------- | ---- | -------- | ------------------------------------------------------------ |
| `host_id`       | str  | No       | Filter quarantined devices by host ID                        |
| `serial_number` | str  | No       | Filter quarantined devices by serial number                  |
| `gather_subset` | list | No       | Determines which information to gather (default: ['config']) |
| `provider`      | dict | Yes      | Authentication credentials for SCM                           |

### Provider Dictionary

| Parameter       | Type | Required | Description                             |
| --------------- | ---- | -------- | --------------------------------------- |
| `client_id`     | str  | Yes      | Client ID for authentication            |
| `client_secret` | str  | Yes      | Client secret for authentication        |
| `tsg_id`        | str  | Yes      | Tenant Service Group ID                 |
| `log_level`     | str  | No       | Log level for the SDK (default: "INFO") |

## Examples

### List All Quarantined Devices



```yaml
---
- name: List all quarantined devices in Strata Cloud Manager
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:
    - name: List all quarantined devices
      cdot65.scm.quarantined_devices_info:
        provider: "{{ provider }}"
      register: result

    - name: Display all quarantined devices
      debug:
        var: result.quarantined_devices
```


### Filter by Host ID



```yaml
---
- name: Filter quarantined devices by host ID
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:
    - name: List quarantined devices by host ID
      cdot65.scm.quarantined_devices_info:
        provider: "{{ provider }}"
        host_id: "device-12345"
      register: result

    - name: Display filtered devices
      debug:
        var: result.quarantined_devices
```


### Filter by Serial Number



```yaml
---
- name: Filter quarantined devices by serial number
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:
    - name: List quarantined devices by serial number
      cdot65.scm.quarantined_devices_info:
        provider: "{{ provider }}"
        serial_number: "PA-987654321"
      register: result

    - name: Display filtered devices
      debug:
        var: result.quarantined_devices
```


### Using Different Gather Subsets



```yaml
---
- name: Use different gather subsets for quarantined devices
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:
    - name: Gather all information about quarantined devices
      cdot65.scm.quarantined_devices_info:
        provider: "{{ provider }}"
        gather_subset: 
          - all
      register: result_all

    - name: Display full information
      debug:
        var: result_all.quarantined_devices
```


## Return Values

| Name                  | Description                                          | Type | Sample                                                           |
| --------------------- | ---------------------------------------------------- | ---- | ---------------------------------------------------------------- |
| `quarantined_devices` | List of quarantined devices matching filter criteria | list | `[{"host_id": "device-12345", "serial_number": "PA-987654321"}]` |

## Error Handling



```yaml
---
- name: Error handling example for info module
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:
    - name: Try to get quarantined device info with error handling
      cdot65.scm.quarantined_devices_info:
        provider: "{{ provider }}"
        host_id: "device-12345"
      register: result
      failed_when: false

    - name: Handle potential errors
      debug:
        msg: "Error occurred: {{ result.msg }}"
      when: result.failed is defined and result.failed

    - name: Check if devices were found
      debug:
        msg: "No devices found matching the criteria"
      when: result.quarantined_devices is defined and result.quarantined_devices | length == 0
```


## Best Practices

1. **Filtering**

   - Filter by host_id when you want to check a specific device
   - Filter by serial_number when integrating with physical device inventory systems
   - Avoid unnecessary filtering when you need the complete list
   - Combine multiple filters for more precise results

2. **Error Handling**

   - Implement proper error handling for API failures
   - Handle cases where no devices match the filters
   - Validate return structures before accessing nested data

3. **Performance**

   - Be mindful of listing all devices in large environments
   - Use specific filters when possible to reduce response size
   - Process results efficiently when dealing with large device lists

4. **Integration**

   - Use with monitoring systems to track quarantined devices
   - Combine with security automation for incident response
   - Create reports of quarantined devices for security operations

## Related Modules

- [quarantined_devices](quarantined_devices.md): Manage quarantined devices (create, delete)
- [address_info](address_info.md): Retrieve information about address objects
- [service_info](service_info.md): Retrieve information about service objects
