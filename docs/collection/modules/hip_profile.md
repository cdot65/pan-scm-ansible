# Hip Profile Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [HIP Profile Model Attributes](#hip-profile-model-attributes)
4. [Exceptions](#exceptions)
5. [Basic Configuration](#basic-configuration)
6. [Usage Examples](#usage-examples)
    - [Creating HIP Profiles](#creating-hip-profiles)
    - [Basic HIP Profile](#basic-hip-profile)
    - [Complex Match Expression](#complex-match-expression)
    - [Updating HIP Profiles](#updating-hip-profiles)
    - [Deleting HIP Profiles](#deleting-hip-profiles)
7. [Managing Configuration Changes](#managing-configuration-changes)
    - [Performing Commits](#performing-commits)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `hip_profile` Ansible module provides functionality to manage Host Information Profile (HIP)
profiles in Palo Alto Networks' Strata Cloud Manager (SCM). HIP profiles define match criteria
expressions that can be used to associate HIP objects with policy rules for enhanced security
posture-based access control.

## Core Methods

| Method   | Description                     | Parameters                          | Returned            |
| -------- | ------------------------------- | ----------------------------------- | ------------------- |
| `create` | Creates a new HIP profile       | HIP profile configuration           | HIP profile details |
| `update` | Updates an existing HIP profile | HIP profile data with modifications | Updated HIP profile |
| `delete` | Removes a HIP profile           | HIP profile name and container      | Status of operation |
| `fetch`  | Gets a HIP profile by name      | Name and container                  | HIP profile details |

## HIP Profile Model Attributes

| Attribute     | Type | Required         | Description                                                |
| ------------- | ---- | ---------------- | ---------------------------------------------------------- |
| `name`        | str  | Yes              | Name of the HIP profile (max 31 chars)                     |
| `description` | str  | No               | Description of the HIP profile (max 255 chars)             |
| `match`       | str  | Yes (if present) | Match expression for the profile (max 2048 chars)          |
| `folder`      | str  | One container    | The folder in which the profile is defined (max 64 chars)  |
| `snippet`     | str  | One container    | The snippet in which the profile is defined (max 64 chars) |
| `device`      | str  | One container    | The device in which the profile is defined (max 64 chars)  |

## Exceptions

| Exception                    | Description                        |
| ---------------------------- | ---------------------------------- |
| `InvalidObjectError`         | Invalid HIP profile data or format |
| `NameNotUniqueError`         | HIP profile name already exists    |
| `ObjectNotPresentError`      | HIP profile not found              |
| `MissingQueryParameterError` | Missing required parameters        |
| `AuthenticationError`        | Authentication failed              |
| `ServerError`                | Internal server error              |

## Basic Configuration

The HIP Profile module requires proper authentication credentials to access the Strata Cloud Manager
API.



```yaml
- name: Basic HIP Profile Module Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a HIP profile exists
      cdot65.scm.hip_profile:
        provider: "{{ provider }}"
        name: "windows-workstations"
        description: "Windows workstations profile"
        match: '"is-win"'
        folder: "Shared"
        state: "present"
```


## Usage Examples

### Creating HIP Profiles

HIP profiles can contain match expressions that reference HIP objects to define security criteria
for endpoints.

### Basic HIP Profile

This example creates a simple HIP profile with a basic match expression that matches Windows
workstations.



```yaml
- name: Create a basic HIP profile with single match expression
  cdot65.scm.hip_profile:
    provider: "{{ provider }}"
    name: "windows-workstations"
    description: "Windows workstations basic profile"
    match: '"is-win"'
    folder: "Shared"
    state: "present"
```


### Complex Match Expression

This example creates a HIP profile with a more complex match expression that combines multiple
conditions.



```yaml
- name: Create a HIP profile with complex match expression
  cdot65.scm.hip_profile:
    provider: "{{ provider }}"
    name: "secure-workstations"
    description: "Secured workstations profile"
    match: '"is-win" and "is-firewall-enabled"'
    folder: "Shared"
    state: "present"
```


### Updating HIP Profiles

This example updates an existing HIP profile with a new match expression.



```yaml
- name: Update a HIP profile with new match expression
  cdot65.scm.hip_profile:
    provider: "{{ provider }}"
    name: "secure-workstations"
    description: "Enhanced secure workstations profile"
    match: '"is-win" and "is-firewall-enabled" and "is-disk-encrypted"'
    folder: "Shared"
    state: "present"
```


### Deleting HIP Profiles

This example removes a HIP profile.



```yaml
- name: Delete a HIP profile
  cdot65.scm.hip_profile:
    provider: "{{ provider }}"
    name: "windows-workstations"
    folder: "Shared"
    state: "absent"
```


## Managing Configuration Changes

### Performing Commits

After creating, updating, or deleting HIP profiles, you need to commit your changes to apply them.



```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Shared"]
    description: "Updated HIP profiles"
```


## Error Handling

It's important to handle potential errors when working with HIP profiles.



```yaml
- name: Create or update HIP profile with error handling
  block:
    - name: Ensure HIP profile exists
      cdot65.scm.hip_profile:
        provider: "{{ provider }}"
        name: "secure-workstations"
        description: "Secured workstations profile"
        match: '"is-win" and "is-firewall-enabled"'
        folder: "Shared"
        state: "present"
      register: hip_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Shared"]
        description: "Updated HIP profiles"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```


## Best Practices

1. **Match Expression Formatting**

   - Use double quotes around HIP object names in match expressions
   - Keep match expressions readable by using appropriate spacing
   - Use parentheses for complex expressions to ensure proper evaluation order

2. **Container Management**

   - Always specify exactly one container (folder, snippet, or device)
   - Use consistent container names across operations
   - Organize related HIP profiles in the same container

3. **Naming Conventions**

   - Use descriptive names that reflect the purpose of the HIP profile
   - Keep names concise but meaningful
   - Follow a consistent naming convention

4. **Error Handling**

   - Implement comprehensive error handling for all operations
   - Check operation results carefully
   - Use debug messages to track the progress of operations

5. **Relationship Management**

   - Understand the relationship between HIP profiles and HIP objects
   - Ensure referenced HIP objects exist before creating profiles
   - Create HIP objects before referencing them in HIP profiles

6. **Security Policy Integration**

   - Use HIP profiles in security policies to enforce endpoint security requirements
   - Test HIP profiles thoroughly before applying them to production policies
   - Document the purpose and expected behavior of each HIP profile

## Related Modules

- [hip_profile_info](hip_profile_info.md) - Retrieve information about HIP profiles
- [hip_object](hip_object.md) - Manage HIP objects that can be referenced in HIP profiles
- [hip_object_info](hip_object_info.md) - Retrieve information about HIP objects
- [security_rule](security_rule.md) - Manage security rules that can use HIP profiles
