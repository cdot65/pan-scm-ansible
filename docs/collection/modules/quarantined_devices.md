# Quarantined Devices Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Quarantined Devices Model Attributes](#quarantined-devices-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Quarantining Devices](#quarantining-devices)
    - [Basic Device Quarantine](#basic-device-quarantine)
    - [Device Quarantine with Serial Number](#device-quarantine-with-serial-number)
    - [Removing Devices from Quarantine](#removing-devices-from-quarantine)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `quarantined_devices` Ansible module provides functionality to manage quarantined devices in
Palo Alto Networks' Strata Cloud Manager (SCM). This module enables you to add devices to quarantine
and remove them from quarantine. Note that SCM's API only supports create, list, and delete
operations for quarantined devices (no direct fetch or update).

## Core Methods

| Method     | Description                      | Parameters                | Return Type                            |
| ---------- | -------------------------------- | ------------------------- | -------------------------------------- |
| `create()` | Adds a device to quarantine      | `data: Dict[str, Any]`    | `QuarantinedDeviceResponseModel`       |
| `delete()` | Removes a device from quarantine | `host_id: str`            | `None`                                 |
| `list()`   | Lists quarantined devices        | `filters: Dict[str, Any]` | `List[QuarantinedDeviceResponseModel]` |

## Quarantined Devices Model Attributes

| Attribute       | Type | Required | Description                                   |
| --------------- | ---- | -------- | --------------------------------------------- |
| `host_id`       | str  | Yes      | The host ID of the device to quarantine       |
| `serial_number` | str  | No       | The serial number of the device to quarantine |

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
| `InvalidObjectError`         | Invalid device data or format  |
| `NameNotUniqueError`         | Device already quarantined     |
| `ObjectNotPresentError`      | Device not found in quarantine |
| `MissingQueryParameterError` | Missing required parameters    |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The Quarantined Devices module requires proper authentication credentials to access the Strata Cloud
Manager API.

```yaml
- name: Basic Quarantined Devices Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Quarantine a device
      cdot65.scm.quarantined_devices:
        provider: "{{ provider }}"
        host_id: "device-12345"
        serial_number: "PA-987654321"
        state: "present"
```

## Usage Examples

### Quarantining Devices

Quarantined devices allow for isolating potentially compromised or problematic devices from your
network.

### Basic Device Quarantine

This example shows how to add a device to quarantine using its host ID.

```yaml
- name: Quarantine a device
  cdot65.scm.quarantined_devices:
    provider: "{{ provider }}"
    host_id: "device-12345"
    state: "present"
  register: result

- name: Display result
  debug:
    var: result
```

### Device Quarantine with Serial Number

This example shows how to quarantine a device with both host ID and serial number for better
identification.

```yaml
- name: Quarantine a device with serial number
  cdot65.scm.quarantined_devices:
    provider: "{{ provider }}"
    host_id: "device-12345"
    serial_number: "PA-987654321"
    state: "present"
  register: result

- name: Display result
  debug:
    var: result
```

### Removing Devices from Quarantine

This example demonstrates how to remove a device from quarantine.

```yaml
- name: Remove a device from quarantine
  cdot65.scm.quarantined_devices:
    provider: "{{ provider }}"
    host_id: "device-12345"
    state: "absent"
  register: result

- name: Display result
  debug:
    var: result
```

## Managing Configuration Changes

Quarantining or unquarantining devices takes effect immediately and does not require a commit
operation.

```yaml
- name: Manage quarantined devices
  block:
    - name: Quarantine a device
      cdot65.scm.quarantined_devices:
        provider: "{{ provider }}"
        host_id: "device-12345"
        serial_number: "PA-987654321"
        state: "present"
      register: quarantine_result

    - name: Log successful quarantine action
      syslog:
        msg: "Device {{ quarantine_result.quarantined_device.host_id }} successfully quarantined"
        facility: local7
        priority: info
      when: quarantine_result.changed
```

## Error Handling

It's important to handle potential errors when working with quarantined devices.

```yaml
- name: Quarantine a device with error handling
  block:
    - name: Attempt to quarantine a device
      cdot65.scm.quarantined_devices:
        provider: "{{ provider }}"
        host_id: "device-12345"
        serial_number: "PA-987654321"
        state: "present"
      register: result
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Log quarantine failure
      syslog:
        msg: "Failed to quarantine device: {{ ansible_failed_result.msg }}"
        facility: local7
        priority: err
```

## Best Practices

### Device Identification

- Always specify a meaningful host_id that makes devices easily identifiable
- Include the serial_number when available for better device tracking
- Establish a consistent naming convention for host_id values
- Document the purpose and reason for each quarantine action
- Maintain an inventory of quarantined devices with quarantine reasons

### Security Operations

- Integrate quarantine operations into security incident response playbooks
- Establish clear criteria for when devices should be quarantined
- Create automated workflows for quarantine based on security alerts
- Implement approval processes for quarantine actions in production environments
- Regularly review quarantined devices to determine if they can be released

### Error Management

- Implement proper error handling for API failures
- Create notification mechanisms for quarantine failures
- Log all quarantine actions for audit purposes
- Verify quarantine status after operations using the info module
- Handle timeouts and connection issues gracefully

### Workflow Integration

- Use with monitoring systems to automate quarantine of suspicious devices
- Include validation steps before and after quarantining devices
- Integrate with ticketing systems for tracking quarantine incidents
- Implement automated remediation workflows for quarantined devices
- Create reports of quarantine actions for security teams

## Related Modules

- [quarantined_devices_info](quarantined_devices_info.md) - Retrieve information about quarantined
  devices
- [address](address.md) - Manage address objects that can be used to represent quarantined devices
- [tag](tag.md) - Manage tag objects that can be used to mark quarantined devices
- [security_rule](security_rule.md) - Create security policies affecting quarantined devices
