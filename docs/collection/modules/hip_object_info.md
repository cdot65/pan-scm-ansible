# HIP Object Information

## Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [HIP Object Info Parameters](#hip-object-info-parameters)
4. [Exceptions](#exceptions)
5. [Basic Configuration](#basic-configuration)
6. [Usage Examples](#usage-examples)
    - [Getting Information about a Specific HIP Object](#getting-information-about-a-specific-hip-object)
    - [Listing All HIP Objects in a Folder](#listing-all-hip-objects-in-a-folder)
    - [Filtering HIP Objects by Criteria Type](#filtering-hip-objects-by-criteria-type)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)
9. [Related Modules](#related-modules)

## Overview

The `hip_object_info` Ansible module provides functionality to gather information about Host Information Profile (HIP) objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is an info module that allows fetching details about specific HIP objects or listing objects with various filtering options.

## Core Methods

| Method      | Description                                      | Parameters                             | Returned                    |
|-------------|--------------------------------------------------|----------------------------------------|-----------------------------|
| `fetch`     | Gets a specific HIP object by name               | Name and container parameters          | Single HIP object details   |
| `list`      | Lists HIP objects with filtering options         | Container and filter parameters        | List of HIP objects         |

## HIP Object Info Parameters

| Parameter           | Type          | Required           | Description                                                                      |
|---------------------|---------------|-------------------|----------------------------------------------------------------------------------|
| `name`              | str           | No                | Name of a specific HIP object to retrieve                                         |
| `gather_subset`     | list          | No                | Determines which information to gather (default: config)                          |
| `folder`            | str           | No*               | Filter HIP objects by folder container                                            |
| `snippet`           | str           | No*               | Filter HIP objects by snippet container                                           |
| `device`            | str           | No*               | Filter HIP objects by device container                                            |
| `exact_match`       | bool          | No                | When True, only return objects defined exactly in the specified container         |
| `exclude_folders`   | list          | No                | List of folder names to exclude from results                                      |
| `exclude_snippets`  | list          | No                | List of snippet values to exclude from results                                    |
| `exclude_devices`   | list          | No                | List of device values to exclude from results                                     |
| `criteria_types`    | list          | No                | Filter by criteria types (host_info, network_info, etc.)                          |

*One container parameter is required when `name` is not specified.

## Exceptions

| Exception                  | Description                                         |
|----------------------------|-----------------------------------------------------|
| `InvalidObjectError`       | Invalid request data or format                      |
| `MissingQueryParameterError`| Missing required parameters                        |
| `ObjectNotPresentError`    | HIP object not found                                |
| `AuthenticationError`      | Authentication failed                               |
| `ServerError`              | Internal server error                               |

## Basic Configuration

The HIP Object Info module requires proper authentication credentials to access the Strata Cloud Manager API.

<div class="termy">

<!-- termynal -->

```yaml
- name: Basic HIP Object Info Module Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about HIP objects
      cdot65.scm.hip_object_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: hip_objects_result
      
    - name: Display retrieved HIP objects
      debug:
        var: hip_objects_result
```

</div>

## Usage Examples

### Getting Information about a Specific HIP Object

Retrieve details about a specific HIP object by name and container.

<div class="termy">

<!-- termynal -->

```yaml
- name: Get information about a specific HIP object
  cdot65.scm.hip_object_info:
    provider: "{{ provider }}"
    name: "Windows_Workstation"
    folder: "Texas"
  register: hip_object_info
  
- name: Display HIP object information
  debug:
    var: hip_object_info.hip_object
```

</div>

### Listing All HIP Objects in a Folder

List all HIP objects in a specific folder.

<div class="termy">

<!-- termynal -->

```yaml
- name: List all HIP objects in a folder
  cdot65.scm.hip_object_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_hip_objects
  
- name: Display all HIP objects
  debug:
    var: all_hip_objects.hip_objects
    
- name: Display count of HIP objects
  debug:
    msg: "Found {{ all_hip_objects.hip_objects | length }} HIP objects"
```

</div>

### Filtering HIP Objects by Criteria Type

Filter HIP objects based on the type of criteria they contain.

<div class="termy">

<!-- termynal -->

```yaml
- name: List only disk encryption HIP objects
  cdot65.scm.hip_object_info:
    provider: "{{ provider }}"
    folder: "Texas"
    criteria_types: ["disk_encryption"]
  register: disk_encryption_hip_objects
  
- name: Display disk encryption HIP objects
  debug:
    var: disk_encryption_hip_objects.hip_objects
    
- name: List HIP objects with host information criteria
  cdot65.scm.hip_object_info:
    provider: "{{ provider }}"
    folder: "Texas"
    criteria_types: ["host_info"]
  register: host_info_hip_objects
```

</div>

### Using Advanced Filtering Options

Use advanced filtering options to refine your query results.

<div class="termy">

<!-- termynal -->

```yaml
- name: List HIP objects with exact match and exclusions
  cdot65.scm.hip_object_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_hip_objects
  
- name: Process filtered HIP objects
  debug:
    msg: "HIP object: {{ item.name }}, defined in {{ item.folder }}"
  loop: "{{ filtered_hip_objects.hip_objects }}"
```

</div>

## Error Handling

It's important to handle potential errors when retrieving information about HIP objects.

<div class="termy">

<!-- termynal -->

```yaml
- name: Get information about HIP objects with error handling
  block:
    - name: Try to retrieve information about a HIP object
      cdot65.scm.hip_object_info:
        provider: "{{ provider }}"
        name: "Windows_Workstation"
        folder: "Texas"
      register: hip_info_result
      
    - name: Display HIP object information
      debug:
        var: hip_info_result.hip_object
        
  rescue:
    - name: Handle errors
      debug:
        msg: "Failed to retrieve HIP object information: {{ ansible_failed_result.msg }}"
```

</div>

## Best Practices

1. **Efficient Querying**
   - Use specific filters to reduce API load and improve performance
   - When looking for a specific HIP object, use the `name` parameter instead of filtering results
   - Use container parameters consistently across queries

2. **Result Processing**
   - Always register the module output to a variable for later use
   - Check if the expected data is present before processing it
   - Use appropriate looping constructs for processing multiple results

3. **Filter Usage**
   - Use `exact_match` when you only want HIP objects defined directly in the specified container
   - Use exclusion filters to refine results without overcomplicating queries
   - Combine multiple filters for more precise results

4. **Error Handling**
   - Implement try/except blocks to handle potential errors
   - Verify that the HIP objects exist before attempting operations on them
   - Provide meaningful error messages for troubleshooting

5. **Performance Considerations**
   - Avoid retrieving all HIP objects when only specific ones are needed
   - Consider breaking up large queries into smaller, more targeted ones
   - Cache results when making multiple queries for the same information

## Related Modules

- [hip_object](hip_object.md) - Create, update, and delete HIP objects
- [hip_profile](hip_profile.md) - Manage HIP profiles that use HIP objects
- [commit](commit.md) - Commit configuration changes
