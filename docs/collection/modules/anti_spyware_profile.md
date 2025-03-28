# Anti Spyware Profile Configuration Object

## Table of Contents

- [Anti Spyware Profile Configuration Object](#anti-spyware-profile-configuration-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [Anti Spyware Profile Model Attributes](#anti-spyware-profile-model-attributes)
    - [Rule Attributes](#rule-attributes)
    - [Threat Exception Attributes](#threat-exception-attributes)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Creating Anti Spyware Profiles](#creating-anti-spyware-profiles)
    - [Basic Anti Spyware Profile](#basic-anti-spyware-profile)
    - [Comprehensive Anti Spyware Profile](#comprehensive-anti-spyware-profile)
    - [Updating Anti Spyware Profiles](#updating-anti-spyware-profiles)
    - [Deleting Anti Spyware Profiles](#deleting-anti-spyware-profiles)
  - [Managing Configuration Changes](#managing-configuration-changes)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Rule Design](#rule-design)
    - [Threat Exception Management](#threat-exception-management)
    - [Botnet Protection](#botnet-protection)
    - [Performance Considerations](#performance-considerations)
    - [Profile Management](#profile-management)
    - [Security Posture](#security-posture)
  - [Related Modules](#related-modules)

## Overview

The `anti_spyware_profile` Ansible module provides functionality to manage Anti-Spyware profiles in
Palo Alto Networks' Strata Cloud Manager (SCM). These profiles define rules for detecting and
blocking spyware and other malicious software on the network with support for various threat levels,
actions, and packet capture options.

## Core Methods

| Method     | Description                        | Parameters                               | Return Type                             |
| ---------- | ---------------------------------- | ---------------------------------------- | --------------------------------------- |
| `create()` | Creates a new Anti-Spyware profile | `data: Dict[str, Any]`                   | `AntiSpywareProfileResponseModel`       |
| `update()` | Updates an existing profile        | `profile: AntiSpywareProfileUpdateModel` | `AntiSpywareProfileResponseModel`       |
| `delete()` | Removes a profile                  | `object_id: str`                         | `None`                                  |
| `fetch()`  | Gets a profile by name             | `name: str`, `container: str`            | `AntiSpywareProfileResponseModel`       |
| `list()`   | Lists profiles with filtering      | `folder: str`, `**filters`               | `List[AntiSpywareProfileResponseModel]` |

## Anti Spyware Profile Model Attributes

| Attribute           | Type | Required      | Description                                                |
| ------------------- | ---- | ------------- | ---------------------------------------------------------- |
| `name`              | str  | Yes           | Profile name. Must match pattern: ^[a-zA-Z0-9.\_-]+$       |
| `description`       | str  | No            | Description of the profile                                 |
| `packet_capture`    | bool | No            | Whether packet capture is enabled                          |
| `rules`             | list | Yes           | List of rules for the profile                              |
| `botnet_lists`      | list | No            | List of botnet domain lists to use                         |
| `threat_exceptions` | list | No            | List of threat exceptions                                  |
| `folder`            | str  | One container | The folder in which the profile is defined (max 64 chars)  |
| `snippet`           | str  | One container | The snippet in which the profile is defined (max 64 chars) |
| `device`            | str  | One container | The device in which the profile is defined (max 64 chars)  |

### Rule Attributes

| Attribute        | Type | Required | Description                                                        |
| ---------------- | ---- | -------- | ------------------------------------------------------------------ |
| `name`           | str  | Yes      | Name of the rule                                                   |
| `threat_level`   | str  | Yes      | Threat severity level (critical, high, medium, low, informational) |
| `action`         | str  | Yes      | Action to take (block, alert, allow, default)                      |
| `packet_capture` | str  | No       | Packet capture setting (disable, single-packet, extended-capture)  |

### Threat Exception Attributes

| Attribute   | Type | Required | Description                             |
| ----------- | ---- | -------- | --------------------------------------- |
| `name`      | str  | Yes      | Name of the threat exception            |
| `threat_id` | str  | Yes      | ID of the threat to exempt              |
| `action`    | str  | Yes      | Action to take for this specific threat |
| `notes`     | str  | No       | Additional notes for the exception      |

## Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid profile data or format |
| `NameNotUniqueError`         | Profile name already exists    |
| `ObjectNotPresentError`      | Profile not found              |
| `MissingQueryParameterError` | Missing required parameters    |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The Anti-Spyware Profile module requires proper authentication credentials to access the Strata
Cloud Manager API.

```yaml
- name: Basic Anti-Spyware Profile Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure an Anti-Spyware profile exists
      cdot65.scm.anti_spyware_profile:
        provider: "{{ provider }}"
        name: "Basic-Anti-Spyware"
        description: "Basic Anti-Spyware profile"
        folder: "Texas"
        packet_capture: false
        rules:
          - name: "Block-Critical"
            threat_level: "critical"
            action: "block"
            packet_capture: "disable"
        state: "present"
```

## Usage Examples

### Creating Anti Spyware Profiles

Anti-Spyware profiles can contain multiple rules to detect and block spyware at different threat
levels.

### Basic Anti Spyware Profile

This example creates a simple Anti-Spyware profile with basic rules.

```yaml
- name: Create a basic Anti-Spyware profile
  cdot65.scm.anti_spyware_profile:
    provider: "{{ provider }}"
    name: "Basic-Anti-Spyware"
    description: "Basic Anti-Spyware profile"
    folder: "Texas"
    packet_capture: false
    rules:
      - name: "Block-Critical"
        threat_level: "critical"
        action: "block"
        packet_capture: "disable"
      - name: "Block-High"
        threat_level: "high"
        action: "block"
        packet_capture: "disable"
    state: "present"
```

### Comprehensive Anti Spyware Profile

This example creates a more comprehensive profile with multiple rules, exceptions, and botnet domain
lists.

```yaml
- name: Create a comprehensive Anti-Spyware profile
  cdot65.scm.anti_spyware_profile:
    provider: "{{ provider }}"
    name: "Advanced-Anti-Spyware"
    description: "Advanced Anti-Spyware profile with exceptions"
    folder: "Texas"
    packet_capture: true
    rules:
      - name: "Block-Critical"
        threat_level: "critical"
        action: "block"
        packet_capture: "single-packet"
      - name: "Block-High"
        threat_level: "high"
        action: "block"
        packet_capture: "disable"
      - name: "Alert-Medium"
        threat_level: "medium"
        action: "alert"
        packet_capture: "disable"
      - name: "Allow-Low"
        threat_level: "low"
        action: "allow"
        packet_capture: "disable"
    botnet_lists:
      - "default-paloalto-dns"
      - "custom-list1"
    threat_exceptions:
      - name: "Exception1"
        threat_id: "12345"
        action: "allow"
        notes: "False positive in our environment"
    state: "present"
```

### Updating Anti Spyware Profiles

This example updates an existing Anti-Spyware profile with new rules and changes the packet capture
setting.

```yaml
- name: Update an Anti-Spyware profile
  cdot65.scm.anti_spyware_profile:
    provider: "{{ provider }}"
    name: "Basic-Anti-Spyware"
    description: "Updated Anti-Spyware profile"
    folder: "Texas"
    packet_capture: true
    rules:
      - name: "Block-Critical"
        threat_level: "critical"
        action: "block"
        packet_capture: "single-packet"
      - name: "Block-High"
        threat_level: "high"
        action: "block"
        packet_capture: "disable"
      - name: "New-Medium-Rule"
        threat_level: "medium"
        action: "alert"
        packet_capture: "disable"
    state: "present"
```

### Deleting Anti Spyware Profiles

This example removes an Anti-Spyware profile.

```yaml
- name: Delete an Anti-Spyware profile
  cdot65.scm.anti_spyware_profile:
    provider: "{{ provider }}"
    name: "Basic-Anti-Spyware"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting Anti-Spyware profiles, you need to commit your changes to
apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated Anti-Spyware profiles"
```

## Error Handling

It's important to handle potential errors when working with Anti-Spyware profiles.

```yaml
- name: Create or update Anti-Spyware profile with error handling
  block:
    - name: Ensure Anti-Spyware profile exists
      cdot65.scm.anti_spyware_profile:
        provider: "{{ provider }}"
        name: "Basic-Anti-Spyware"
        description: "Basic Anti-Spyware profile"
        folder: "Texas"
        packet_capture: false
        rules:
          - name: "Block-Critical"
            threat_level: "critical"
            action: "block"
            packet_capture: "disable"
        state: "present"
      register: profile_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated Anti-Spyware profiles"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```

## Best Practices

### Rule Design

- Create specific rules for different threat levels
- Block critical and high-severity threats
- Consider alerting rather than blocking for medium and low threats
- Use packet capture selectively due to performance impact
- Prioritize the most important threats for your environment

### Threat Exception Management

- Document the reason for each threat exception thoroughly
- Review exceptions regularly to ensure they're still required
- Implement a robust change management process for exceptions
- Use exceptions judiciously, only when necessary

### Botnet Protection

- Enable appropriate botnet domain lists
- Consider using both default and custom botnet lists
- Update custom botnet lists regularly
- Monitor for false positives

### Performance Considerations

- Balance security needs with operational requirements
- Monitor the impact of packet capture on network performance
- Implement more specific rules for high-volume environments
- Test changes before implementing in production

### Profile Management

- Develop a consistent naming convention for profiles
- Document each profile's purpose and rules
- Test profiles in a non-production environment first
- Implement proper change management for profile modifications

### Security Posture

- Align Anti-Spyware profiles with your security policy
- Create different profiles for different security requirements
- Consider the impact of profile changes on security posture
- Regularly review and update profiles based on threat intelligence

## Related Modules

- [anti_spyware_profile_info](anti_spyware_profile_info.md) - Retrieve information about
  Anti-Spyware profiles
- [security_profiles_group](security_profiles_group.md) - Manage security profile groups that can
  include Anti-Spyware profiles
- [security_rule](security_rule.md) - Configure security policies that use Anti-Spyware profiles
