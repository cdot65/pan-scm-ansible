# Log Forwarding Profile Information Object

## Table of Contents

- [Log Forwarding Profile Information Object](#log-forwarding-profile-information-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [Log Forwarding Profile Info Parameters](#log-forwarding-profile-info-parameters)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Getting Information about a Specific Log Forwarding Profile](#getting-information-about-a-specific-log-forwarding-profile)
    - [Listing All Log Forwarding Profiles in a Folder](#listing-all-log-forwarding-profiles-in-a-folder)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
  - [Managing Configuration Changes](#managing-configuration-changes)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Efficient Querying](#efficient-querying)
    - [Result Processing](#result-processing)
    - [Filter Usage](#filter-usage)
    - [Error Handling](#error-handling-1)
    - [Integration with Other Modules](#integration-with-other-modules)
    - [Performance Considerations](#performance-considerations)
  - [Related Modules](#related-modules)

## Overview

The `log_forwarding_profile_info` Ansible module provides functionality to gather information about
Log Forwarding Profile objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is an info
module that allows fetching details about specific log forwarding profiles or listing profiles with
various filtering options.

## Core Methods

| Method    | Description                                    | Parameters                    | Return Type                               |
| --------- | ---------------------------------------------- | ----------------------------- | ----------------------------------------- |
| `fetch()` | Gets a specific log forwarding profile by name | `name: str`, `container: str` | `LogForwardingProfileResponseModel`       |
| `list()`  | Lists log forwarding profiles with filtering   | `folder: str`, `**filters`    | `List[LogForwardingProfileResponseModel]` |

## Log Forwarding Profile Info Parameters

| Parameter          | Type | Required        | Description                                                               |
| ------------------ | ---- | --------------- | ------------------------------------------------------------------------- |
| `name`             | str  | No              | Name of a specific log forwarding profile to retrieve                     |
| `gather_subset`    | list | No              | Determines which information to gather (default: config)                  |
| `folder`           | str  | One container\* | Filter log forwarding profiles by folder container                        |
| `snippet`          | str  | One container\* | Filter log forwarding profiles by snippet container                       |
| `device`           | str  | One container\* | Filter log forwarding profiles by device container                        |
| `exact_match`      | bool | No              | When True, only return objects defined exactly in the specified container |
| `exclude_folders`  | list | No              | List of folder names to exclude from results                              |
| `exclude_snippets` | list | No              | List of snippet values to exclude from results                            |
| `exclude_devices`  | list | No              | List of device values to exclude from results                             |

\*One container parameter is required when `name` is not specified.

## Exceptions

| Exception                    | Description                      |
| ---------------------------- | -------------------------------- |
| `InvalidObjectError`         | Invalid request data or format   |
| `MissingQueryParameterError` | Missing required parameters      |
| `ObjectNotPresentError`      | Log forwarding profile not found |
| `AuthenticationError`        | Authentication failed            |
| `ServerError`                | Internal server error            |

## Basic Configuration

The Log Forwarding Profile Info module requires proper authentication credentials to access the
Strata Cloud Manager API.

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

## Usage Examples

### Getting Information about a Specific Log Forwarding Profile

Retrieve details about a specific log forwarding profile by name and container.

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

### Listing All Log Forwarding Profiles in a Folder

List all log forwarding profiles in a specific folder.

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

### Using Advanced Filtering Options

Use advanced filtering options to refine your query results.

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

## Managing Configuration Changes

For info modules like `log_forwarding_profile_info`, no commit is needed since these modules only
retrieve information and do not modify the configuration. However, you may need to commit changes if
you use the retrieved information to make configuration changes with other modules.

```yaml
- name: Use info results to make configuration changes
  block:
    - name: Get existing log forwarding profiles
      cdot65.scm.log_forwarding_profile_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: existing_profiles
      
    - name: Create new profile if specific one doesn't exist
      cdot65.scm.log_forwarding_profile:
        provider: "{{ provider }}"
        name: "new-log-profile"
        description: "New log forwarding profile"
        folder: "Texas"
        filter:
          - name: "critical-events"
            filter: "severity eq critical"
        match_list:
          - name: "forward-critical-threats"
            action: "forwarding"
            send_http: ["secure-profile"]
            log_type: "threat"
            filter: "critical-events"
            send_to_panorama: true
        state: "present"
      when: >
        existing_profiles.log_forwarding_profiles | 
        selectattr('name', 'equalto', 'new-log-profile') | 
        list | length == 0
      register: profile_created
      
    - name: Commit changes if profile was created
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Created new log forwarding profile"
      when: profile_created is changed
```

## Error Handling

It's important to handle potential errors when retrieving information about log forwarding profiles.

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

## Best Practices

### Efficient Querying

- Use specific filters to reduce API load and improve performance
- When looking for a specific log forwarding profile, use the `name` parameter instead of filtering
  results
- Use container parameters consistently across queries
- Leverage exclusion filters to refine results without complex queries

### Result Processing

- Always register the module output to a variable for later use
- Check if the expected data is present before processing it
- Use appropriate Ansible filters and tests when processing complex nested structures
- Consider using set_fact to create simplified data structures for complex results

### Filter Usage

- Use `exact_match` when you only want log forwarding profiles defined directly in the specified
  container
- Use exclusion filters to refine results without overcomplicating queries
- Combine multiple filters for more precise results
- Document the purpose of complex filters for maintainability

### Error Handling

- Implement try/except blocks to handle potential errors
- Verify that the log forwarding profiles exist before attempting operations on them
- Provide meaningful error messages for troubleshooting
- Consider fallback mechanisms when expected data is not available

### Integration with Other Modules

- Use the info module to check for existing profiles before creating new ones
- Combine with the log_forwarding_profile module for complete profile management
- Use the retrieved information to make decisions in your playbooks
- Keep conditional logic simple and readable

### Performance Considerations

- Cache results when making multiple queries for the same information
- Limit the data retrieved to only what's needed for your task
- Consider batching operations when processing multiple profiles
- For large environments, use appropriate pagination techniques

## Related Modules

- [log_forwarding_profile](log_forwarding_profile.md) - Create, update, and delete log forwarding
  profiles
- [http_server_profiles](http_server_profiles.md) - Manage HTTP server profiles used in log
  forwarding
- [http_server_profiles_info](http_server_profiles_info.md) - Retrieve information about HTTP server
  profiles
- [syslog_server_profiles](syslog_server_profiles.md) - Manage syslog server profiles for log
  forwarding
- [security_rule](security_rule.md) - Configure security policies that use log forwarding profiles
