# Security Zone Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Security Zone Model Attributes](#security-zone-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating Security Zones](#creating-security-zones)
    - [Creating Basic Security Zones](#creating-basic-security-zones)
    - [Creating Zone with User-ID Features](#creating-zone-with-user-id-features)
    - [Updating Security Zones](#updating-security-zones)
    - [Deleting Security Zones](#deleting-security-zones)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `security_zone` Ansible module provides functionality to manage security zone objects in Palo Alto Networks' Strata Cloud Manager (SCM). Security zones are logical boundaries that segment the network and provide security policy enforcement points. By defining zones, you can create security rules that control traffic between different network segments.

## Core Methods

| Method     | Description                    | Parameters                    | Return Type                 |
| ---------- | ------------------------------ | ----------------------------- | --------------------------- |
| `create()` | Creates a new security zone    | `data: Dict[str, Any]`        | `SecurityZoneResponseModel` |
| `update()` | Updates an existing zone       | `zone: SecurityZoneUpdateModel` | `SecurityZoneResponseModel` |
| `delete()` | Removes a zone                 | `object_id: str`              | `None`                      |
| `fetch()`  | Gets a zone by name            | `name: str`, `container: str` | `SecurityZoneResponseModel` |
| `list()`   | Lists zones with filtering     | `folder: str`, `**filters`    | `List[SecurityZoneResponseModel]` |

## Security Zone Model Attributes

| Attribute          | Type      | Required      | Description                                                  |
| ------------------ | --------- | ------------- | ------------------------------------------------------------ |
| `name`             | str       | Yes           | The name of the security zone                                |
| `description`      | str       | No            | Description of the security zone                             |
| `tag`              | List[str] | No            | List of tags associated with the zone                        |
| `user_id_mappings` | Dict      | No            | User ID mapping settings                                     |
| `log_setting`      | str       | No            | Log forwarding profile                                       |
| `enable_user_id`   | bool      | No            | Enable User-ID for this zone                                 |
| `exclude_ip`       | List[str] | No            | List of IP addresses to exclude from User-ID                 |
| `include_ip`       | List[str] | No            | List of IP addresses to include for User-ID                  |
| `folder`           | str       | One container | The folder in which the zone is defined (max 64 chars)       |
| `snippet`          | str       | One container | The snippet in which the zone is defined (max 64 chars)      |
| `device`           | str       | One container | The device in which the zone is defined (max 64 chars)       |

### User-ID Mapping Attributes

| Attribute  | Type | Required | Description                                    |
| ---------- | ---- | -------- | ---------------------------------------------- |
| `primary`  | Dict | No       | Primary User-ID mapping configuration          |
| `secondary`| Dict | No       | Secondary User-ID mapping configuration        |

## Exceptions

| Exception                    | Description                           |
| ---------------------------- | ------------------------------------- |
| `InvalidObjectError`         | Invalid security zone data or format  |
| `NameNotUniqueError`         | Security zone name already exists     |
| `ObjectNotPresentError`      | Security zone not found               |
| `MissingQueryParameterError` | Missing required parameters           |
| `AuthenticationError`        | Authentication failed                 |
| `ServerError`                | Internal server error                 |

## Basic Configuration

The Security Zone module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Security Zone Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a security zone exists
      cdot65.scm.security_zone:
        provider: "{{ provider }}"
        name: "trust"
        description: "Internal trusted zone"
        folder: "Texas"
        state: "present"
```

## Usage Examples

### Creating Security Zones

Security zones form the fundamental building blocks for network segmentation and security policy enforcement.

### Creating Basic Security Zones

This example creates standard security zones commonly used in network configurations.

```yaml
- name: Create standard security zones
  cdot65.scm.security_zone:
    provider: "{{ provider }}"
    name: "{{ item.name }}"
    description: "{{ item.description }}"
    folder: "Texas"
    state: "present"
  loop:
    - { name: "trust", description: "Internal trusted zone" }
    - { name: "untrust", description: "External untrusted zone" }
    - { name: "dmz", description: "Demilitarized zone" }
```

### Creating Zone with User-ID Features

This example creates a security zone with User-ID features enabled for user identification and mapping.

```yaml
- name: Create security zone with User-ID
  cdot65.scm.security_zone:
    provider: "{{ provider }}"
    name: "internal"
    description: "Internal zone with User-ID"
    enable_user_id: true
    include_ip:
      - "10.0.0.0/8"
    exclude_ip:
      - "10.1.1.0/24"  # Server subnet without users
    folder: "Texas"
    state: "present"
```

### Updating Security Zones

This example demonstrates how to update an existing security zone with new settings.

```yaml
- name: Update security zone settings
  cdot65.scm.security_zone:
    provider: "{{ provider }}"
    name: "trust"
    description: "Updated trusted zone"
    log_setting: "detailed-logging"
    tag:
      - "internal"
    folder: "Texas"
    state: "present"
```

### Deleting Security Zones

This example shows how to remove a security zone that is no longer needed.

```yaml
- name: Delete a security zone
  cdot65.scm.security_zone:
    provider: "{{ provider }}"
    name: "deprecated-zone"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting security zones, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated security zone configurations"
```

## Error Handling

It's important to handle potential errors when working with security zones.

```yaml
- name: Create or update security zone with error handling
  block:
    - name: Ensure security zone exists
      cdot65.scm.security_zone:
        provider: "{{ provider }}"
        name: "trust"
        description: "Internal trusted zone"
        log_setting: "detailed-logging"
        folder: "Texas"
        state: "present"
      register: zone_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated security zone configurations"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Check if referenced object doesn't exist
      debug:
        msg: "Check if the referenced log_setting profile exists."
      when: "'referenced object does not exist' in ansible_failed_result.msg"
```

## Best Practices

### Zone Naming and Design

- Use descriptive names for zones that reflect their security purpose
- Follow a consistent naming convention across all zones
- Include the purpose of the zone in the description field
- Design zones based on security requirements, not just network topology
- Keep zone names concise but meaningful

### Zone Structure

- Create a clear separation between trusted (internal) and untrusted (external) zones
- Use a DMZ for publicly accessible resources
- Segment internal networks into multiple zones based on security requirements
- Consider creating dedicated zones for sensitive systems or regulated data
- Implement a zero-trust model by properly segmenting all network areas

### User-ID Configuration

- Only enable User-ID on zones with user traffic
- Use include/exclude lists to optimize User-ID processing
- Configure appropriate User-ID timeouts for your environment
- Document all User-ID mapping settings
- Regularly review User-ID configurations for accuracy

### Log Settings

- Configure appropriate log settings for each zone
- Use more detailed logging for high-security zones
- Consider traffic volume when configuring logging
- Ensure log forwarding profiles exist before referencing them
- Balance security visibility with storage requirements

### Security Policy Integration

- Create clear security policies between zones
- Follow the principle of least privilege when allowing traffic between zones
- Use appropriate logging settings for inter-zone traffic
- Document security policy requirements between zones
- Regularly review zone-based security policies

## Related Modules

- [security_rule](security_rule.md) - Configure security policies between zones
- [address](address.md) - Define network objects within zones
- [tag](tag.md) - Apply tags to zones for organization
- [log_forwarding_profile](log_forwarding_profile.md) - Create log forwarding profiles for zone logging
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules