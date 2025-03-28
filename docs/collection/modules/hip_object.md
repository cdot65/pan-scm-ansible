# Hip Object Configuration Object

## Table of Contents

- [Hip Object Configuration Object](#hip-object-configuration-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [HIP Object Model Attributes](#hip-object-model-attributes)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Creating HIP Objects](#creating-hip-objects)
    - [Basic Host Information HIP Object](#basic-host-information-hip-object)
    - [Patch Management HIP Object](#patch-management-hip-object)
    - [Disk Encryption HIP Object](#disk-encryption-hip-object)
    - [Updating HIP Objects](#updating-hip-objects)
    - [Deleting HIP Objects](#deleting-hip-objects)
  - [Managing Configuration Changes](#managing-configuration-changes)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
  - [Related Modules](#related-modules)

## Overview

The `hip_object` Ansible module provides functionality to manage Host Information Profile (HIP)
objects in Palo Alto Networks' Strata Cloud Manager (SCM). HIP objects are used for endpoint
security posture assessment and contain various criteria that determine endpoint security
compliance. This module supports creating, updating, and deleting HIP objects with various criteria
types.

## Core Methods

| Method   | Description                    | Parameters                         | Returned            |
| -------- | ------------------------------ | ---------------------------------- | ------------------- |
| `create` | Creates a new HIP object       | HIP object configuration           | HIP object details  |
| `update` | Updates an existing HIP object | HIP object data with modifications | Updated HIP object  |
| `delete` | Removes a HIP object           | HIP object name and container      | Status of operation |
| `fetch`  | Gets a HIP object by name      | Name and container                 | HIP object details  |

## HIP Object Model Attributes

| Attribute          | Type | Required          | Description                                                            |
| ------------------ | ---- | ----------------- | ---------------------------------------------------------------------- |
| `name`             | str  | Yes               | Name of the HIP object (max 31 chars)                                  |
| `description`      | str  | No                | Description of the HIP object (max 255 chars)                          |
| `host_info`        | dict | One criteria type | Host information criteria including OS, domain, client version, etc.   |
| `network_info`     | dict | One criteria type | Network information criteria                                           |
| `patch_management` | dict | One criteria type | Patch management criteria with vendor information and patch status     |
| `disk_encryption`  | dict | One criteria type | Disk encryption criteria with encrypted locations and encryption state |
| `mobile_device`    | dict | One criteria type | Mobile device criteria including jailbroken status, encryption, etc.   |
| `certificate`      | dict | One criteria type | Certificate validation criteria                                        |
| `folder`           | str  | One container     | The folder in which the HIP object is defined (max 64 chars)           |
| `snippet`          | str  | One container     | The snippet in which the HIP object is defined (max 64 chars)          |
| `device`           | str  | One container     | The device in which the HIP object is defined (max 64 chars)           |

## Exceptions

| Exception                    | Description                       |
| ---------------------------- | --------------------------------- |
| `InvalidObjectError`         | Invalid HIP object data or format |
| `NameNotUniqueError`         | HIP object name already exists    |
| `ObjectNotPresentError`      | HIP object not found              |
| `MissingQueryParameterError` | Missing required parameters       |
| `AuthenticationError`        | Authentication failed             |
| `ServerError`                | Internal server error             |

## Basic Configuration

The HIP Object module requires proper authentication credentials to access the Strata Cloud Manager
API.

```yaml
- name: Basic HIP Object Module Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a HIP object exists
      cdot65.scm.hip_object:
        provider: "{{ provider }}"
        name: "Windows_Workstation"
        description: "HIP object for Windows workstations"
        folder: "Texas"
        host_info:
          criteria:
            os:
              contains:
                Microsoft: "All"
            managed: true
        state: "present"
```

## Usage Examples

### Creating HIP Objects

HIP objects can contain different types of criteria based on the security requirements for
endpoints.

### Basic Host Information HIP Object

This example creates a HIP object that matches Windows workstations that are managed.

```yaml
- name: Create a basic HIP object with host information
  cdot65.scm.hip_object:
    provider: "{{ provider }}"
    name: "Windows_Workstation"
    description: "HIP object for Windows workstations"
    folder: "Texas"
    host_info:
      criteria:
        os:
          contains:
            Microsoft: "All"
        managed: true
    state: "present"
```

### Patch Management HIP Object

This example creates a HIP object that matches endpoints with properly installed and enabled patch
management software with no severe missing patches.

```yaml
- name: Create HIP object with patch management criteria
  cdot65.scm.hip_object:
    provider: "{{ provider }}"
    name: "Patched_Endpoints"
    description: "HIP object for patch management"
    folder: "Texas"
    patch_management:
      criteria:
        is_installed: true
        is_enabled: "yes"
        missing_patches:
          severity: 3
          check: "has-none"
      vendor:
        - name: "Microsoft"
          product: ["Windows Update"]
    state: "present"
```

### Disk Encryption HIP Object

This example creates a HIP object that matches endpoints with disk encryption enabled on the C:
drive.

```yaml
- name: Create HIP object with disk encryption requirements
  cdot65.scm.hip_object:
    provider: "{{ provider }}"
    name: "Encrypted_Drives"
    description: "HIP object for disk encryption"
    folder: "Texas"
    disk_encryption:
      criteria:
        is_installed: true
        encrypted_locations:
          - name: "C:"
            encryption_state: 
              is: "encrypted"
    state: "present"
```

### Updating HIP Objects

This example updates an existing HIP object with additional criteria.

```yaml
- name: Update an existing HIP object
  cdot65.scm.hip_object:
    provider: "{{ provider }}"
    name: "Windows_Workstation"
    description: "Updated Windows workstation requirements"
    folder: "Texas"
    host_info:
      criteria:
        os:
          contains:
            Microsoft: "All"
        managed: true
        domain:
          contains: "company.local"
    state: "present"
```

### Deleting HIP Objects

This example removes a HIP object.

```yaml
- name: Delete a HIP object
  cdot65.scm.hip_object:
    provider: "{{ provider }}"
    name: "Encrypted_Drives"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting HIP objects, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated HIP objects"
```

## Error Handling

It's important to handle potential errors when working with HIP objects.

```yaml
- name: Create or update HIP object with error handling
  block:
    - name: Ensure HIP object exists
      cdot65.scm.hip_object:
        provider: "{{ provider }}"
        name: "Windows_Workstation"
        description: "HIP object for Windows workstations"
        folder: "Texas"
        host_info:
          criteria:
            os:
              contains:
                Microsoft: "All"
            managed: true
        state: "present"
      register: hip_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated HIP objects"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```

## Best Practices

1. **Container Consistency**

   - Always specify exactly one container (folder, snippet, or device)
   - Use consistent container names across operations
   - Organize related HIP objects in the same container

2. **HIP Object Naming**

   - Use descriptive names that reflect the purpose of the HIP object
   - Keep names concise but meaningful
   - Follow a consistent naming convention

3. **Criteria Selection**

   - Include only necessary criteria to match your security requirements
   - Avoid overly restrictive criteria that might exclude legitimate endpoints
   - Test HIP objects thoroughly before deploying to production

4. **Error Handling**

   - Implement comprehensive error handling for all operations
   - Check operation results carefully
   - Use debug messages to track the progress of operations

5. **Security Practices**

   - Follow the principle of least privilege when defining HIP objects
   - Regularly review and update HIP objects to reflect current security policies
   - Document your HIP object configurations and their purposes

## Related Modules

- [hip_object_info](hip_object_info.md) - Retrieve information about HIP objects
- [hip_profile](hip_profile.md) - Manage HIP profiles that use HIP objects
- [hip_profile_info](hip_profile_info.md) - Retrieve information about HIP profiles
