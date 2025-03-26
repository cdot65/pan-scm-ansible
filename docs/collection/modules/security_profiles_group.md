# Security Profiles Group Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Security Profiles Group Model Attributes](#security-profiles-group-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating Security Profiles Groups](#creating-security-profiles-groups)
    - [Standard Security Profiles Group](#standard-security-profiles-group)
    - [Enhanced Security Profiles Group](#enhanced-security-profiles-group)
    - [Updating Security Profiles Groups](#updating-security-profiles-groups)
    - [Deleting Security Profiles Groups](#deleting-security-profiles-groups)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `security_profiles_group` Ansible module provides functionality to manage Security Profiles Groups in Palo Alto Networks' Strata Cloud Manager (SCM). Security Profiles Groups allow you to bundle multiple security profiles (Anti-Spyware, Vulnerability Protection, URL Filtering, etc.) into a single group that can be applied to security rules, simplifying policy management and ensuring consistent security controls.

## Core Methods

| Method     | Description                              | Parameters                    | Return Type                          |
| ---------- | ---------------------------------------- | ----------------------------- | ------------------------------------ |
| `create()` | Creates a new Security Profiles Group    | `data: Dict[str, Any]`        | `SecurityProfilesGroupResponseModel` |
| `update()` | Updates an existing group                | `group: SecurityProfilesGroupUpdateModel` | `SecurityProfilesGroupResponseModel` |
| `delete()` | Removes a group                          | `object_id: str`              | `None`                               |
| `fetch()`  | Gets a group by name                     | `name: str`, `container: str` | `SecurityProfilesGroupResponseModel` |
| `list()`   | Lists groups with filtering              | `folder: str`, `**filters`    | `List[SecurityProfilesGroupResponseModel]` |

## Security Profiles Group Model Attributes

| Attribute                   | Type   | Required      | Description                                             |
| --------------------------- | ------ | ------------- | ------------------------------------------------------- |
| `name`                      | str    | Yes           | Name of the Security Profiles Group                     |
| `description`               | str    | No            | Description of the Security Profiles Group              |
| `anti_spyware_profile`      | str    | No            | Name of the Anti-Spyware profile to include             |
| `anti_virus_profile`        | str    | No            | Name of the Anti-Virus profile to include               |
| `vulnerability_profile`     | str    | No            | Name of the Vulnerability profile to include            |
| `url_filtering_profile`     | str    | No            | Name of the URL Filtering profile to include            |
| `file_blocking_profile`     | str    | No            | Name of the File Blocking profile to include            |
| `wildfire_analysis_profile` | str    | No            | Name of the WildFire Analysis profile to include        |
| `data_filtering_profile`    | str    | No            | Name of the Data Filtering profile to include           |
| `tags`                      | list   | No            | List of tags to apply to the group                      |
| `folder`                    | str    | One container | The folder in which the group is defined (max 64 chars) |
| `snippet`                   | str    | One container | The snippet in which the group is defined (max 64 chars)|
| `device`                    | str    | One container | The device in which the group is defined (max 64 chars) |

## Exceptions

| Exception                    | Description                             |
| ---------------------------- | --------------------------------------- |
| `InvalidObjectError`         | Invalid group data or format            |
| `NameNotUniqueError`         | Group name already exists               |
| `ObjectNotPresentError`      | Group not found                         |
| `MissingQueryParameterError` | Missing required parameters             |
| `AuthenticationError`        | Authentication failed                   |
| `ServerError`                | Internal server error                   |
| `ReferenceNotFoundError`     | Referenced security profile doesn't exist|

## Basic Configuration

The Security Profiles Group module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Security Profiles Group Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a security profiles group exists
      cdot65.scm.security_profiles_group:
        provider: "{{ provider }}"
        name: "Standard-Protection"
        description: "Standard protection profile for corporate assets"
        anti_spyware_profile: "Default-AS-Profile"
        url_filtering_profile: "Corporate-URL-Filter"
        folder: "Texas"
        state: "present"
```

## Usage Examples

### Creating Security Profiles Groups

Security Profiles Groups allow you to bundle multiple security profiles together for consistent application in security policies.

### Standard Security Profiles Group

This example creates a standard security profiles group with basic protection.

```yaml
- name: Create Standard Security Profiles Group
  cdot65.scm.security_profiles_group:
    provider: "{{ provider }}"
    name: "Standard-Protection"
    description: "Standard protection profile for corporate assets"
    anti_spyware_profile: "Standard-AS-Profile"
    anti_virus_profile: "Standard-AV"
    url_filtering_profile: "Corporate-URL-Filter"
    tags: 
      - "standard-security"
    folder: "Texas"
    state: "present"
```

### Enhanced Security Profiles Group

This example creates a more comprehensive security profiles group with enhanced protection for sensitive assets.

```yaml
- name: Create Enhanced Security Profiles Group
  cdot65.scm.security_profiles_group:
    provider: "{{ provider }}"
    name: "Enhanced-Protection"
    description: "Enhanced protection profile for sensitive assets"
    anti_spyware_profile: "Enhanced-AS-Profile"
    anti_virus_profile: "Enhanced-AV"
    vulnerability_profile: "Enhanced-VP"
    url_filtering_profile: "Strict-URL-Filter"
    file_blocking_profile: "Block-Risky-Files"
    wildfire_analysis_profile: "Enhanced-WF"
    data_filtering_profile: "DLP-Strict"
    tags: 
      - "enhanced-security"
      - "sensitive-assets"
    folder: "Texas"
    state: "present"
```

### Updating Security Profiles Groups

This example updates an existing security profiles group with new profile references.

```yaml
- name: Update Security Profiles Group
  cdot65.scm.security_profiles_group:
    provider: "{{ provider }}"
    name: "Standard-Protection"
    description: "Updated standard protection profile"
    anti_spyware_profile: "Updated-AS-Profile"
    anti_virus_profile: "Standard-AV"
    vulnerability_profile: "Basic-VP"
    url_filtering_profile: "Corporate-URL-Filter"
    tags: 
      - "standard-security"
      - "updated"
    folder: "Texas"
    state: "present"
```

### Deleting Security Profiles Groups

This example removes a security profiles group that is no longer needed.

```yaml
- name: Delete Security Profiles Group
  cdot65.scm.security_profiles_group:
    provider: "{{ provider }}"
    name: "Standard-Protection"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting security profiles groups, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated security profiles group configurations"
```

## Error Handling

It's important to handle potential errors when working with security profiles groups.

```yaml
- name: Create or update security profiles group with error handling
  block:
    - name: Ensure security profiles group exists
      cdot65.scm.security_profiles_group:
        provider: "{{ provider }}"
        name: "Standard-Protection"
        description: "Standard protection profile for corporate assets"
        anti_spyware_profile: "Standard-AS-Profile"
        anti_virus_profile: "Standard-AV"
        url_filtering_profile: "Corporate-URL-Filter"
        folder: "Texas"
        state: "present"
      register: group_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated security profiles group configurations"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Check if referenced profile doesn't exist
      debug:
        msg: "Check if all referenced security profiles exist."
      when: "'referenced object does not exist' in ansible_failed_result.msg"
```

## Best Practices

### Group Design

- Create different Security Profiles Groups for different security postures or asset types
- Use descriptive names that indicate the security level or purpose
- Include a balanced selection of security profiles based on the required protection level
- Document the purpose of each group in its description field
- Start with a small set of profiles and add more as needed

### Profile Selection

- Select appropriate profiles based on the assets you're protecting
- Include anti-spyware and anti-virus profiles for baseline protection
- Add URL filtering profiles to control web access
- Consider vulnerability protection profiles for critical systems
- Use file blocking and WildFire analysis for comprehensive protection

### Group Organization

- Use tags to categorize and organize groups
- Create a tiered approach with standard, enhanced, and strict protection levels
- Document which security rules use each group
- Maintain a consistent naming convention across all groups
- Consider creating specialized groups for specific application types

### Management and Maintenance

- Regularly review and update the profiles included in each group
- Apply more stringent profiles to groups used for sensitive assets
- Test changes to Security Profiles Groups in pre-production environments
- Document the security profiles used in each group
- Implement change management procedures for group modifications

### Policy Implementation

- Apply appropriate groups based on the sensitivity of protected assets
- Use standard groups for general corporate assets
- Apply enhanced or strict groups for sensitive data
- Balance security needs with performance considerations
- Regularly audit group usage in security policies

## Related Modules

- [anti_spyware_profile](anti_spyware_profile.md) - Manage anti-spyware profiles
- [vulnerability_protection_profile](vulnerability_protection_profile.md) - Manage vulnerability protection profiles
- [wildfire_antivirus_profiles](wildfire_antivirus_profiles.md) - Manage WildFire antivirus profiles
- [security_rule](security_rule.md) - Configure security policies that reference security profiles groups
- [url_categories](url_categories.md) - Define URL categories for URL filtering profiles