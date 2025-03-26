# Wildfire Antivirus Profiles Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [WildFire Antivirus Profile Model Attributes](#wildfire-antivirus-profile-model-attributes)
4. [Exceptions](#exceptions)
5. [Basic Configuration](#basic-configuration)
6. [Usage Examples](#usage-examples)
    - [Creating WildFire Antivirus Profiles](#creating-wildfire-antivirus-profiles)
    - [Basic WildFire Antivirus Profile](#basic-wildfire-antivirus-profile)
    - [Comprehensive WildFire Antivirus Profile](#comprehensive-wildfire-antivirus-profile)
    - [Updating WildFire Antivirus Profiles](#updating-wildfire-antivirus-profiles)
    - [Deleting WildFire Antivirus Profiles](#deleting-wildfire-antivirus-profiles)
7. [Managing Configuration Changes](#managing-configuration-changes)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `wildfire_antivirus_profiles` Ansible module provides functionality to manage WildFire antivirus
profiles in Palo Alto Networks' Strata Cloud Manager (SCM). These profiles define rules for malware
analysis using either public or private cloud infrastructure, with support for packet capture, MLAV
exceptions, and threat exceptions.

## Core Methods

| Method     | Description                              | Parameters                              | Return Type                            |
| ---------- | ---------------------------------------- | --------------------------------------- | -------------------------------------- |
| `create()` | Creates a new WildFire antivirus profile | `data: Dict[str, Any]`                  | `WildfireAvProfileResponseModel`       |
| `update()` | Updates an existing profile              | `profile: WildfireAvProfileUpdateModel` | `WildfireAvProfileResponseModel`       |
| `delete()` | Removes a profile                        | `object_id: str`                        | `None`                                 |
| `fetch()`  | Gets a profile by name                   | `name: str`, `container: str`           | `WildfireAvProfileResponseModel`       |
| `list()`   | Lists profiles with filtering            | `folder: str`, `**filters`              | `List[WildfireAvProfileResponseModel]` |

## WildFire Antivirus Profile Model Attributes

| Attribute          | Type | Required      | Description                                                |
| ------------------ | ---- | ------------- | ---------------------------------------------------------- |
| `name`             | str  | Yes           | Profile name. Must match pattern: ^[a-zA-Z0-9.\_-]+$       |
| `description`      | str  | No            | Description of the profile                                 |
| `packet_capture`   | bool | No            | Whether packet capture is enabled                          |
| `rules`            | list | Yes           | List of rules for the profile                              |
| `mlav_exception`   | list | No            | List of Machine Learning Anti-Virus exceptions             |
| `threat_exception` | list | No            | List of threat exceptions                                  |
| `folder`           | str  | One container | The folder in which the profile is defined (max 64 chars)  |
| `snippet`          | str  | One container | The snippet in which the profile is defined (max 64 chars) |
| `device`           | str  | One container | The device in which the profile is defined (max 64 chars)  |

### Rule Attributes

| Attribute     | Type | Required | Description                                                       |
| ------------- | ---- | -------- | ----------------------------------------------------------------- |
| `name`        | str  | Yes      | Name of the rule                                                  |
| `direction`   | str  | Yes      | Direction of traffic to inspect (download, upload, both)          |
| `analysis`    | str  | No       | Analysis type for malware detection (public-cloud, private-cloud) |
| `application` | list | No       | List of applications this rule applies to                         |
| `file_type`   | list | No       | List of file types this rule applies to                           |

### MLAV Exception Attributes

| Attribute     | Type | Required | Description                       |
| ------------- | ---- | -------- | --------------------------------- |
| `name`        | str  | Yes      | Name of the MLAV exception        |
| `description` | str  | No       | Description of the MLAV exception |
| `filename`    | str  | Yes      | Filename to exempt from scanning  |

### Threat Exception Attributes

| Attribute | Type | Required | Description                               |
| --------- | ---- | -------- | ----------------------------------------- |
| `name`    | str  | Yes      | Name of the threat exception              |
| `notes`   | str  | No       | Additional notes for the threat exception |

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

The WildFire Antivirus Profile module requires proper authentication credentials to access the
Strata Cloud Manager API.

```yaml
- name: Basic WildFire Antivirus Profile Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a WildFire antivirus profile exists
      cdot65.scm.wildfire_antivirus_profiles:
        provider: "{{ provider }}"
        name: "Basic-Wildfire-AV"
        description: "Basic WildFire antivirus profile"
        folder: "Texas"
        packet_capture: true
        rules:
          - name: "Default-Rule"
            direction: "both"
            analysis: "public-cloud"
            application: ["any"]
            file_type: ["any"]
        state: "present"
```

## Usage Examples

### Creating WildFire Antivirus Profiles

WildFire antivirus profiles can contain multiple rules to analyze malware in different types of
traffic and applications.

### Basic WildFire Antivirus Profile

This example creates a simple WildFire antivirus profile with a basic rule.

```yaml
- name: Create a basic WildFire antivirus profile
  cdot65.scm.wildfire_antivirus_profiles:
    provider: "{{ provider }}"
    name: "Basic-Wildfire-AV"
    description: "Basic WildFire antivirus profile"
    folder: "Texas"
    packet_capture: true
    rules:
      - name: "Default-Rule"
        direction: "both"
        analysis: "public-cloud"
        application: ["any"]
        file_type: ["any"]
    state: "present"
```

### Comprehensive WildFire Antivirus Profile

This example creates a more comprehensive profile with multiple rules and exceptions.

```yaml
- name: Create a comprehensive WildFire antivirus profile
  cdot65.scm.wildfire_antivirus_profiles:
    provider: "{{ provider }}"
    name: "Advanced-Wildfire-AV"
    description: "Advanced WildFire antivirus profile with exceptions"
    folder: "Texas"
    packet_capture: true
    rules:
      - name: "Web-Traffic-Rule"
        direction: "download"
        analysis: "public-cloud"
        application: ["web-browsing"]
        file_type: ["any"]
      - name: "FTP-Upload-Rule"
        direction: "upload"
        analysis: "private-cloud"
        application: ["ftp"]
        file_type: ["any"]
    mlav_exception:
      - name: "Exception1"
        description: "Test exception"
        filename: "legitimate.exe"
    threat_exception:
      - name: "ThreatEx1"
        notes: "Known false positive"
    state: "present"
```

### Updating WildFire Antivirus Profiles

This example updates an existing WildFire antivirus profile with a new rule and changes the packet
capture setting.

```yaml
- name: Update a WildFire antivirus profile
  cdot65.scm.wildfire_antivirus_profiles:
    provider: "{{ provider }}"
    name: "Basic-Wildfire-AV"
    description: "Updated WildFire antivirus profile"
    folder: "Texas"
    packet_capture: false
    rules:
      - name: "Default-Rule"
        direction: "both"
        analysis: "public-cloud"
        application: ["any"]
        file_type: ["any"]
      - name: "New-Web-Rule"
        direction: "download"
        analysis: "public-cloud"
        application: ["web-browsing"]
        file_type: ["pe"]
    state: "present"
```

### Deleting WildFire Antivirus Profiles

This example removes a WildFire antivirus profile.

```yaml
- name: Delete a WildFire antivirus profile
  cdot65.scm.wildfire_antivirus_profiles:
    provider: "{{ provider }}"
    name: "Basic-Wildfire-AV"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting WildFire antivirus profiles, you need to commit your changes
to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated WildFire antivirus profiles"
```

## Error Handling

It's important to handle potential errors when working with WildFire antivirus profiles.

```yaml
- name: Create or update WildFire antivirus profile with error handling
  block:
    - name: Ensure WildFire antivirus profile exists
      cdot65.scm.wildfire_antivirus_profiles:
        provider: "{{ provider }}"
        name: "Basic-Wildfire-AV"
        description: "Basic WildFire antivirus profile"
        folder: "Texas"
        packet_capture: true
        rules:
          - name: "Default-Rule"
            direction: "both"
            analysis: "public-cloud"
            application: ["any"]
            file_type: ["any"]
        state: "present"
      register: profile_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated WildFire antivirus profiles"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```

## Best Practices

1. **Rule Design**

   - Create specific, well-defined rules for precise malware detection
   - Configure rules for different traffic directions based on risk
   - Use application-specific rules for high-risk applications
   - Balance detection capabilities with performance considerations

2. **Analysis Selection**

   - Use public-cloud analysis for general threat detection
   - Consider private-cloud analysis for sensitive environments
   - Match analysis type to your organization's security requirements

3. **File Type Selection**

   - Focus on high-risk file types (PE, EXE, PDF, etc.)
   - Consider the performance impact of scanning all file types
   - Prioritize file types based on your organization's risk profile

4. **Exception Handling**

   - Use MLAV exceptions judiciously, only for legitimate applications
   - Document the reason for each exception thoroughly
   - Review exceptions regularly to ensure they're still required
   - Implement a robust change management process for exceptions

5. **Profile Management**

   - Develop a consistent naming convention for profiles
   - Document each profile's purpose and rules
   - Test profiles in a non-production environment first
   - Implement proper change management for profile modifications

6. **Performance Considerations**

   - Monitor the impact of packet capture on network performance
   - Balance security needs with operational requirements
   - Consider implementing more targeted rules for high-volume environments
   - Test changes before implementing in production

## Related Modules

- [wildfire_antivirus_profiles_info](wildfire_antivirus_profiles_info.md) - Retrieve information
  about WildFire antivirus profiles
- [anti_spyware_profile](anti_spyware_profile.md) - Manage anti-spyware profiles for additional
  protection
- [security_rule](security_rule.md) - Configure security policies that use WildFire antivirus
  profiles
- commit - Commit configuration changes
