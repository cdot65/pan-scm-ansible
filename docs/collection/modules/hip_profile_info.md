# Hip Profile Information Object

## Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [HIP Profile Info Parameters](#hip-profile-info-parameters)
4. [Exceptions](#exceptions)
5. [Basic Configuration](#basic-configuration)
6. [Usage Examples](#usage-examples)
   - [Getting Information about a Specific HIP Profile](#getting-information-about-a-specific-hip-profile)
   - [Listing All HIP Profiles in a Folder](#listing-all-hip-profiles-in-a-folder)
   - [Using Advanced Filtering Options](#using-advanced-filtering-options)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)
9. [Related Modules](#related-modules)

## Overview

The `hip_profile_info` Ansible module provides functionality to gather information about Host
Information Profile (HIP) profiles in Palo Alto Networks' Strata Cloud Manager (SCM). This is an
info module that allows fetching details about specific HIP profiles or listing profiles with
various filtering options.

## Core Methods

| Method  | Description                               | Parameters                      | Returned                   |
| ------- | ----------------------------------------- | ------------------------------- | -------------------------- |
| `fetch` | Gets a specific HIP profile by name       | Name and container parameters   | Single HIP profile details |
| `list`  | Lists HIP profiles with filtering options | Container and filter parameters | List of HIP profiles       |

## HIP Profile Info Parameters

| Parameter          | Type | Required | Description                                                               |
| ------------------ | ---- | -------- | ------------------------------------------------------------------------- |
| `name`             | str  | No       | Name of a specific HIP profile to retrieve                                |
| `gather_subset`    | list | No       | Determines which information to gather (default: config)                  |
| `folder`           | str  | No\*     | Filter HIP profiles by folder container                                   |
| `snippet`          | str  | No\*     | Filter HIP profiles by snippet container                                  |
| `device`           | str  | No\*     | Filter HIP profiles by device container                                   |
| `exact_match`      | bool | No       | When True, only return objects defined exactly in the specified container |
| `exclude_folders`  | list | No       | List of folder names to exclude from results                              |
| `exclude_snippets` | list | No       | List of snippet values to exclude from results                            |
| `exclude_devices`  | list | No       | List of device values to exclude from results                             |

\*One container parameter is required when `name` is not specified.

## Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid request data or format |
| `MissingQueryParameterError` | Missing required parameters    |
| `ObjectNotPresentError`      | HIP profile not found          |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The HIP Profile Info module requires proper authentication credentials to access the Strata Cloud
Manager API.



```yaml
- name: Basic HIP Profile Info Module Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about HIP profiles
      cdot65.scm.hip_profile_info:
        provider: "{{ provider }}"
        folder: "Shared"
      register: hip_profiles_result
      
    - name: Display retrieved HIP profiles
      debug:
        var: hip_profiles_result
```


## Usage Examples

### Getting Information about a Specific HIP Profile

Retrieve details about a specific HIP profile by name and container.



```yaml
- name: Get information about a specific HIP profile
  cdot65.scm.hip_profile_info:
    provider: "{{ provider }}"
    name: "secure-workstations"
    folder: "Shared"
  register: hip_profile_info
  
- name: Display HIP profile information
  debug:
    var: hip_profile_info.hip_profile
```


### Listing All HIP Profiles in a Folder

List all HIP profiles in a specific folder.



```yaml
- name: List all HIP profiles in a folder
  cdot65.scm.hip_profile_info:
    provider: "{{ provider }}"
    folder: "Shared"
  register: all_hip_profiles
  
- name: Display all HIP profiles
  debug:
    var: all_hip_profiles.hip_profiles
    
- name: Display count of HIP profiles
  debug:
    msg: "Found {{ all_hip_profiles.hip_profiles | length }} HIP profiles"
```


### Using Advanced Filtering Options

Use advanced filtering options to refine your query results.



```yaml
- name: List HIP profiles with exact match and exclusions
  cdot65.scm.hip_profile_info:
    provider: "{{ provider }}"
    folder: "Shared"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_hip_profiles
  
- name: Process filtered HIP profiles
  debug:
    msg: "HIP profile: {{ item.name }}, match expression: {{ item.match }}"
  loop: "{{ filtered_hip_profiles.hip_profiles }}"
```


## Error Handling

It's important to handle potential errors when retrieving information about HIP profiles.



```yaml
- name: Get information about HIP profiles with error handling
  block:
    - name: Try to retrieve information about a HIP profile
      cdot65.scm.hip_profile_info:
        provider: "{{ provider }}"
        name: "secure-workstations"
        folder: "Shared"
      register: hip_info_result
      
    - name: Display HIP profile information
      debug:
        var: hip_info_result.hip_profile
        
  rescue:
    - name: Handle errors
      debug:
        msg: "Failed to retrieve HIP profile information: {{ ansible_failed_result.msg }}"
```


## Best Practices

1. **Efficient Querying**

   - Use specific filters to reduce API load and improve performance
   - When looking for a specific HIP profile, use the `name` parameter instead of filtering results
   - Use container parameters consistently across queries

2. **Result Processing**

   - Always register the module output to a variable for later use
   - Check if the expected data is present before processing it
   - Use appropriate looping constructs for processing multiple results

3. **Filter Usage**

   - Use `exact_match` when you only want HIP profiles defined directly in the specified container
   - Use exclusion filters to refine results without overcomplicating queries
   - Combine multiple filters for more precise results

4. **Error Handling**

   - Implement try/except blocks to handle potential errors
   - Verify that the HIP profiles exist before attempting operations on them
   - Provide meaningful error messages for troubleshooting

5. **Integration with Other Modules**

   - Use the info module to check for existing profiles before creating new ones
   - Combine with the hip_profile module for complete profile management
   - Use the retrieved information to make decisions in your playbooks

## Related Modules

- [hip_profile](hip_profile.md) - Create, update, and delete HIP profiles
- [hip_object](hip_object.md) - Manage HIP objects that can be referenced in HIP profiles
- [hip_object_info](hip_object_info.md) - Retrieve information about HIP objects
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules
