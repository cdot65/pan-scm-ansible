# Quarantined Devices Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Examples](#examples)
   - [Quarantine a Device](#quarantine-a-device)
   - [Remove a Device from Quarantine](#remove-a-device-from-quarantine)
   - [Using Check Mode](#using-check-mode)
4. [Return Values](#return-values) 
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)
7. [Related Modules](#related-modules)

## Overview

The `quarantined_devices` module provides functionality to manage quarantined devices in Palo Alto Networks' Strata Cloud Manager (SCM). This module enables you to add devices to quarantine and remove them from quarantine. Note that SCM's API only supports create, list, and delete operations for quarantined devices (no direct fetch or update).

## Module Parameters

| Parameter       | Type   | Required | Description                                               |
|----------------|--------|----------|-----------------------------------------------------------|
| `host_id`      | str    | Yes      | The host ID of the device to quarantine                    |
| `serial_number`| str    | No       | The serial number of the device to quarantine              |
| `provider`     | dict   | Yes      | Authentication credentials for SCM                         |
| `state`        | str    | Yes      | Desired state of the quarantined device (`present` or `absent`) |

### Provider Dictionary

| Parameter       | Type   | Required | Description                                    |
|----------------|--------|----------|------------------------------------------------|
| `client_id`    | str    | Yes      | Client ID for authentication                    |
| `client_secret`| str    | Yes      | Client secret for authentication                |
| `tsg_id`       | str    | Yes      | Tenant Service Group ID                         |
| `log_level`    | str    | No       | Log level for the SDK (default: "INFO")         |

## Examples

### Quarantine a Device

<div class="termy">

<!-- termynal -->

```yaml
---
- name: Quarantine a device in Strata Cloud Manager
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
    - name: Quarantine a device
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

</div>

### Remove a Device from Quarantine

<div class="termy">

<!-- termynal -->

```yaml
---
- name: Remove a device from quarantine in Strata Cloud Manager
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

</div>

### Using Check Mode

<div class="termy">

<!-- termynal -->

```yaml
---
- name: Test changes in check mode without applying
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
    - name: Check what would happen when quarantining a device
      cdot65.scm.quarantined_devices:
        provider: "{{ provider }}"
        host_id: "device-12345"
        serial_number: "PA-987654321"
        state: "present"
      check_mode: yes
      register: result

    - name: Display check mode result
      debug:
        var: result
```

</div>

## Return Values

| Name               | Description                                | Type     | Sample                                            |
|--------------------|--------------------------------------------|----------|---------------------------------------------------|
| `changed`          | Whether any changes were made              | boolean  | `true`                                            |
| `quarantined_device` | Details about the quarantined device     | dict     | `{"host_id": "device-12345", "serial_number": "PA-987654321"}` |

## Error Handling

<div class="termy">

<!-- termynal -->

```yaml
---
- name: Error handling example
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
    - name: Quarantine a device with error handling
      cdot65.scm.quarantined_devices:
        provider: "{{ provider }}"
        host_id: "device-12345"
        serial_number: "PA-987654321"
        state: "present"
      register: result
      failed_when: false

    - name: Handle potential errors
      debug:
        msg: "Error occurred: {{ result.msg }}"
      when: result.failed is defined and result.failed
```

</div>

## Best Practices

1. **Basic Usage**
   - Always specify the host_id when quarantining devices
   - Include the serial_number when available for better identification
   - Use meaningful host_id values that make devices easily identifiable

2. **Error Handling**
   - Implement proper error handling for API failures
   - Use the failed_when pattern to handle potential errors gracefully
   - Log error details for troubleshooting

3. **Security**
   - Store credentials securely using Ansible Vault
   - Use the least privileged access principle for SCM authentication
   - Regularly rotate client credentials

4. **Workflow Integration**
   - Integrate quarantine operations into security incident response playbooks
   - Use with monitoring systems to automate quarantine of suspicious devices
   - Include validation steps before and after quarantining devices

## Related Modules

- [quarantined_devices_info](quarantined_devices_info.md): Retrieve information about quarantined devices
- [address](address.md): Manage address objects
- [tag](tag.md): Manage tag objects that can be used to mark quarantined devices