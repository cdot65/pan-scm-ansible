# Quarantined Devices Information Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Quarantined Devices Info Parameters](#quarantined-devices-info-parameters)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Retrieving Quarantined Devices Information](#retrieving-quarantined-devices-information)
    - [Listing All Quarantined Devices](#listing-all-quarantined-devices)
    - [Filtering by Host ID](#filtering-by-host-id)
    - [Filtering by Serial Number](#filtering-by-serial-number)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `quarantined_devices_info` Ansible module provides functionality to retrieve information about
quarantined devices in Palo Alto Networks' Strata Cloud Manager (SCM). This module allows you to
list all quarantined devices or filter the results by host ID or serial number. As an info module,
it only retrieves information and does not modify any configuration.

## Core Methods

| Method   | Description                   | Parameters                | Return Type                            |
| -------- | ----------------------------- | ------------------------- | -------------------------------------- |
| `list()` | Lists all quarantined devices | `filters: Dict[str, Any]` | `List[QuarantinedDeviceResponseModel]` |

## Quarantined Devices Info Parameters

| Parameter       | Type | Required | Description                                                  |
| --------------- | ---- | -------- | ------------------------------------------------------------ |
| `host_id`       | str  | No       | Filter quarantined devices by host ID                        |
| `serial_number` | str  | No       | Filter quarantined devices by serial number                  |
| `gather_subset` | list | No       | Determines which information to gather (default: ['config']) |

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
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The Quarantined Devices Info module requires proper authentication credentials to access the Strata
Cloud Manager API.

```yaml
- name: Basic Quarantined Devices Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about quarantined devices
      cdot65.scm.quarantined_devices_info:
        provider: "{{ provider }}"
      register: devices_result
    
    - name: Display quarantined devices
      debug:
        var: devices_result.quarantined_devices
```

## Usage Examples

### Retrieving Quarantined Devices Information

You can retrieve information about quarantined devices with various filtering options.

### Listing All Quarantined Devices

This example retrieves a list of all quarantined devices in the SCM environment.

```yaml
- name: List all quarantined devices
  cdot65.scm.quarantined_devices_info:
    provider: "{{ provider }}"
  register: result

- name: Display all quarantined devices
  debug:
    var: result.quarantined_devices

- name: Display count of quarantined devices
  debug:
    msg: "Found {{ result.quarantined_devices | length }} quarantined devices"
```

### Filtering by Host ID

This example demonstrates how to retrieve information about a specific quarantined device by its
host ID.

```yaml
- name: List quarantined devices by host ID
  cdot65.scm.quarantined_devices_info:
    provider: "{{ provider }}"
    host_id: "device-12345"
  register: result

- name: Display filtered devices
  debug:
    var: result.quarantined_devices

- name: Check if device is quarantined
  debug:
    msg: "Device is quarantined"
  when: result.quarantined_devices | length > 0
```

### Filtering by Serial Number

This example shows how to filter quarantined devices by serial number.

```yaml
- name: List quarantined devices by serial number
  cdot65.scm.quarantined_devices_info:
    provider: "{{ provider }}"
    serial_number: "PA-987654321"
  register: result

- name: Display filtered devices
  debug:
    var: result.quarantined_devices

- name: Process devices matching serial number
  debug:
    msg: "Found device with host_id: {{ item.host_id }}"
  loop: "{{ result.quarantined_devices }}"
  when: result.quarantined_devices | length > 0
```

## Managing Configuration Changes

As an info module, `quarantined_devices_info` does not make any configuration changes. However, you
can use the information it retrieves to make decisions about other configuration operations.

```yaml
- name: Make decisions based on quarantined device information
  block:
    - name: Get list of quarantined devices
      cdot65.scm.quarantined_devices_info:
        provider: "{{ provider }}"
      register: device_info
      
    - name: Create security policy for quarantined devices
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Block-Quarantined-Devices"
        folder: "Shared"
        source_addresses: "{{ device_info.quarantined_devices | map(attribute='host_id') | list }}"
        action: "deny"
        # Other parameters...
        state: "present"
      when: device_info.quarantined_devices | length > 0
      
    - name: Commit changes if policy was created
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folder: "Shared"
        description: "Added security rules for quarantined devices"
      when: device_info.quarantined_devices | length > 0
```

## Error Handling

It's important to handle potential errors when retrieving quarantined device information.

```yaml
- name: Get quarantined device information with error handling
  block:
    - name: Try to get quarantined device info
      cdot65.scm.quarantined_devices_info:
        provider: "{{ provider }}"
        host_id: "device-12345"
      register: result
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Log API failure
      syslog:
        msg: "Failed to retrieve quarantined device info: {{ ansible_failed_result.msg }}"
        facility: local7
        priority: err
```

## Best Practices

### Filtering Strategies

- Filter by host_id when you need information about a specific device
- Filter by serial_number when integrating with physical device inventory systems
- Avoid unnecessary filtering when you need the complete list
- Combine with other info modules to build comprehensive security reports
- Cache results when making multiple queries for the same information

### Data Processing

- Always verify the data structure before accessing nested elements
- Handle cases where no devices match your filter criteria
- Process quarantined device data efficiently in large environments
- Use Ansible filters to transform data into useful formats
- Create variables or facts for frequently referenced values

### Security Operations

- Regularly audit quarantined devices to review status
- Create automated reports of quarantined devices
- Integrate with security incident response workflows
- Correlate quarantined devices with security events
- Monitor quarantine status changes over time

### Error Management

- Implement proper error handling for API failures
- Validate results before using them in critical operations
- Include timeout handling for API operations
- Create alerts for changes in quarantine status
- Document error scenarios and remediation steps

## Related Modules

- [quarantined_devices](quarantined_devices.md) - Manage quarantined devices
- [address_info](address_info.md) - Retrieve information about address objects
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules that may
  affect quarantined devices
- [tag_info](tag_info.md) - Retrieve information about tags that may be applied to quarantined
  devices
