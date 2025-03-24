# Log Forwarding Profile Information

## Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [Log Forwarding Profile Info Parameters](#log-forwarding-profile-info-parameters)
4. [Exceptions](#exceptions)
5. [Basic Configuration](#basic-configuration)
6. [Usage Examples](#usage-examples)
    - [Getting Information about a Specific Log Forwarding Profile](#getting-information-about-a-specific-log-forwarding-profile)
    - [Listing All Log Forwarding Profiles in a Folder](#listing-all-log-forwarding-profiles-in-a-folder)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)
9. [Related Modules](#related-modules)

## Overview

The `log_forwarding_profile_info` Ansible module provides functionality to gather information about Log Forwarding Profile objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is an info module that allows fetching details about specific log forwarding profiles or listing profiles with various filtering options.

## Core Methods

| Method      | Description                                      | Parameters                             | Returned                                 |
|-------------|--------------------------------------------------|----------------------------------------|-----------------------------------------|
| `fetch`     | Gets a specific log forwarding profile by name   | Name and container parameters          | Single log forwarding profile details    |
| `list`      | Lists log forwarding profiles with filtering     | Container and filter parameters        | List of log forwarding profiles          |

## Log Forwarding Profile Info Parameters

| Parameter          | Type          | Required           | Description                                                                      |
|--------------------|---------------|-------------------|----------------------------------------------------------------------------------|
| `name`             | str           | No                | Name of a specific log forwarding profile to retrieve                             |
| `gather_subset`    | list          | No                | Determines which information to gather (default: config)                          |
| `folder`           | str           | No*               | Filter log forwarding profiles by folder container                                |
| `snippet`          | str           | No*               | Filter log forwarding profiles by snippet container                               |
| `device`           | str           | No*               | Filter log forwarding profiles by device container                                |
| `exact_match`      | bool          | No                | When True, only return objects defined exactly in the specified container         |
| `exclude_folders`  | list          | No                | List of folder names to exclude from results                                      |
| `exclude_snippets` | list          | No                | List of snippet values to exclude from results                                    |
| `exclude_devices`  | list          | No                | List of device values to exclude from results                                     |

*One container parameter is required when `name` is not specified.

## Exceptions

| Exception                  | Description                                         |
|----------------------------|-----------------------------------------------------|
| `InvalidObjectError`       | Invalid request data or format                      |
| `MissingQueryParameterError`| Missing required parameters                        |
| `ObjectNotPresentError`    | Log forwarding profile not found                    |
| `AuthenticationError`      | Authentication failed                               |
| `ServerError`              | Internal server error                               |

## Basic Configuration

The Log Forwarding Profile Info module requires proper authentication credentials to access the Strata Cloud Manager API.

<div class="termy">

<!-- termynal -->

```yaml
- name: Basic Log Forwarding Profile Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about log forwarding profiles
      cdot65.scm.log_forwarding_profile_info:
        provider: "{{ provider }}"
        folder: "Shared"
      register: log_profiles_result
      
    - name: Display retrieved log forwarding profiles
      debug:
        var: log_profiles_result
```

</div>

## Usage Examples

### Getting Information about a Specific Log Forwarding Profile

Retrieve details about a specific log forwarding profile by name and container.

<div class="termy">

<!-- termynal -->

```yaml
- name: Get information about a specific log forwarding profile
  cdot65.scm.log_forwarding_profile_info:
    provider: "{{ provider }}"
    name: "test-log-profile"
    folder: "Texas"
  register: log_profile_info
  
- name: Display log forwarding profile information
  debug:
    var: log_profile_info.log_forwarding_profile
    
- name: Check if profile has specific match list
  debug:
    msg: "Profile contains critical-events filter"
  when: >
    log_profile_info.log_forwarding_profile.filter is defined and
    log_profile_info.log_forwarding_profile.filter | selectattr('name', 'equalto', 'critical-events') | list | length > 0
```

</div>

### Listing All Log Forwarding Profiles in a Folder

List all log forwarding profiles in a specific folder.

<div class="termy">

<!-- termynal -->

```yaml
- name: List all log forwarding profiles in a folder
  cdot65.scm.log_forwarding_profile_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_log_profiles
  
- name: Display all log forwarding profiles
  debug:
    var: all_log_profiles.log_forwarding_profiles
    
- name: Display count of log forwarding profiles
  debug:
    msg: "Found {{ all_log_profiles.log_forwarding_profiles | length }} log forwarding profiles"
    
- name: List names of all log forwarding profiles
  debug:
    msg: "{{ all_log_profiles.log_forwarding_profiles | map(attribute='name') | list }}"
```

</div>

### Using Advanced Filtering Options

Use advanced filtering options to refine your query results.

<div class="termy">

<!-- termynal -->

```yaml
- name: List log forwarding profiles with exact match and exclusions
  cdot65.scm.log_forwarding_profile_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_log_profiles
  
- name: Process filtered log forwarding profiles
  debug:
    msg: "Log forwarding profile: {{ item.name }}, with {{ item.match_list | length }} match lists"
  loop: "{{ filtered_log_profiles.log_forwarding_profiles }}"
  
- name: Find profiles that forward to Panorama
  set_fact:
    panorama_profiles: "{{ filtered_log_profiles.log_forwarding_profiles | 
                          selectattr('match_list', 'defined') | 
                          selectattr('match_list', 'iterable') | 
                          selectattr('match_list[0].send_to_panorama', 'defined') | 
                          selectattr('match_list[0].send_to_panorama', 'equalto', true) | 
                          list }}"
                        
- name: Display profiles that forward to Panorama
  debug:
    msg: "Found {{ panorama_profiles | length }} profiles that forward to Panorama"
```

</div>

## Error Handling

It's important to handle potential errors when retrieving information about log forwarding profiles.

<div class="termy">

<!-- termynal -->

```yaml
- name: Get information about log forwarding profiles with error handling
  block:
    - name: Try to retrieve information about a log forwarding profile
      cdot65.scm.log_forwarding_profile_info:
        provider: "{{ provider }}"
        name: "test-log-profile"
        folder: "Texas"
      register: log_info_result
      
    - name: Display log forwarding profile information
      debug:
        var: log_info_result.log_forwarding_profile
        
  rescue:
    - name: Handle errors
      debug:
        msg: "Failed to retrieve log forwarding profile information: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a 'not found' error
      debug:
        msg: "The specified log forwarding profile does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

</div>

## Best Practices

1. **Efficient Querying**
   - Use specific filters to reduce API load and improve performance
   - When looking for a specific log forwarding profile, use the `name` parameter instead of filtering results
   - Use container parameters consistently across queries

2. **Result Processing**
   - Always register the module output to a variable for later use
   - Check if the expected data is present before processing it
   - Use appropriate Ansible filters and tests when processing complex nested structures

3. **Filter Usage**
   - Use `exact_match` when you only want log forwarding profiles defined directly in the specified container
   - Use exclusion filters to refine results without overcomplicating queries
   - Combine multiple filters for more precise results

4. **Error Handling**
   - Implement try/except blocks to handle potential errors
   - Verify that the log forwarding profiles exist before attempting operations on them
   - Provide meaningful error messages for troubleshooting

5. **Integration with Other Modules**
   - Use the info module to check for existing profiles before creating new ones
   - Combine with the log_forwarding_profile module for complete profile management
   - Use the retrieved information to make decisions in your playbooks

6. **Performance Considerations**
   - Cache results when making multiple queries for the same information
   - Limit the data retrieved to only what's needed for your task
   - Consider batching operations when processing multiple profiles

## Related Modules

- [log_forwarding_profile](log_forwarding_profile.md) - Create, update, and delete log forwarding profiles
- [http_server_profiles](http_server_profiles.md) - Manage HTTP server profiles used in log forwarding
- [http_server_profiles_info](http_server_profiles_info.md) - Retrieve information about HTTP server profiles
- [commit](commit.md) - Commit configuration changes
