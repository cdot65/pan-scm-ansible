# Syslog Server Profiles Information Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Syslog Server Profile Info Parameters](#syslog-server-profile-info-parameters)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Retrieving a Specific Syslog Server Profile](#retrieving-a-specific-syslog-server-profile)
    - [Listing Syslog Server Profiles](#listing-syslog-server-profiles)
    - [Filtering Syslog Server Profiles](#filtering-syslog-server-profiles)
    - [Advanced Filtering with Ansible](#advanced-filtering-with-ansible)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `syslog_server_profiles_info` module provides functionality to retrieve information about syslog
server profile objects in Palo Alto Networks' Strata Cloud Manager (SCM). This module allows you to
fetch details about a specific syslog server profile by name or list multiple profiles with various
filtering options. It's a read-only module that helps with inventory management, auditing
configurations, and collecting information needed for other operations.

## Core Methods

| Method    | Description                                 | Parameters                    | Return Type                              |
| --------- | ------------------------------------------- | ----------------------------- | ---------------------------------------- |
| `fetch()` | Gets a specific syslog server profile       | `name: str`, `container: str` | `SyslogServerProfileResponseModel`       |
| `list()`  | Lists syslog server profiles with filtering | `folder: str`, `**filters`    | `List[SyslogServerProfileResponseModel]` |

## Syslog Server Profile Info Parameters

| Parameter          | Type | Required        | Description                                                    |
| ------------------ | ---- | --------------- | -------------------------------------------------------------- |
| `name`             | str  | No              | The name of a specific syslog server profile to retrieve       |
| `gather_subset`    | list | No              | Determines which information to gather (default: ['config'])   |
| `folder`           | str  | One container\* | Filter syslog server profiles by folder container              |
| `snippet`          | str  | One container\* | Filter syslog server profiles by snippet container             |
| `device`           | str  | One container\* | Filter syslog server profiles by device container              |
| `exact_match`      | bool | No              | Only return objects defined exactly in the specified container |
| `exclude_folders`  | list | No              | List of folder names to exclude from results                   |
| `exclude_snippets` | list | No              | List of snippet values to exclude from results                 |
| `exclude_devices`  | list | No              | List of device values to exclude from results                  |
| `transport`        | list | No              | Filter by transport protocol used (UDP, TCP)                   |

\*One container parameter is required when `name` is not specified.

### Provider Dictionary

| Parameter       | Type | Required | Description                             |
| --------------- | ---- | -------- | --------------------------------------- |
| `client_id`     | str  | Yes      | Client ID for SCM authentication        |
| `client_secret` | str  | Yes      | Client secret for SCM authentication    |
| `tsg_id`        | str  | Yes      | Tenant Service Group ID                 |
| `log_level`     | str  | No       | Log level for the SDK (default: "INFO") |

## Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid request data or format |
| `MissingQueryParameterError` | Missing required parameters    |
| `ObjectNotPresentError`      | Profile not found              |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The Syslog Server Profiles Info module requires proper authentication credentials to access the
Strata Cloud Manager API.

```yaml
- name: Basic Syslog Server Profiles Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about syslog server profiles
      cdot65.scm.syslog_server_profiles_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: profiles_result
    
    - name: Display profiles
      debug:
        var: profiles_result.syslog_server_profiles
```

## Usage Examples

### Retrieving a Specific Syslog Server Profile

This example retrieves information about a specific syslog server profile by name.

```yaml
- name: Get information about a specific syslog server profile
  cdot65.scm.syslog_server_profiles_info:
    provider: "{{ provider }}"
    name: "test-syslog-profile"
    folder: "Texas"
  register: profile_info

- name: Display profile details
  debug:
    var: profile_info.syslog_server_profile
    
- name: Check server transport protocol
  debug:
    msg: "The profile uses {{ profile_info.syslog_server_profile.servers.transport }} transport"
  when: profile_info.syslog_server_profile is defined
```

### Listing Syslog Server Profiles

This example lists all syslog server profiles in a specific folder.

```yaml
- name: List all syslog server profiles in a folder
  cdot65.scm.syslog_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_profiles

- name: Display all profiles
  debug:
    var: all_profiles.syslog_server_profiles
    
- name: Count number of profiles
  debug:
    msg: "Found {{ all_profiles.syslog_server_profiles | length }} syslog server profiles"
```

### Filtering Syslog Server Profiles

This example demonstrates filtering profiles by transport protocol and other criteria.

```yaml
- name: List only UDP profiles
  cdot65.scm.syslog_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    transport: ["UDP"]
  register: udp_profiles

- name: Display UDP profiles count
  debug:
    msg: "Found {{ udp_profiles.syslog_server_profiles | length }} UDP syslog server profiles"
    
- name: List profiles with exact match and exclusions
  cdot65.scm.syslog_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_profiles
    
- name: Process filtered profiles
  debug:
    msg: "Profile {{ item.name }} is in folder {{ item.folder }}"
  loop: "{{ filtered_profiles.syslog_server_profiles }}"
```

### Advanced Filtering with Ansible

This example shows how to use Ansible's filters to further process results.

```yaml
- name: Get all syslog profiles for further filtering
  cdot65.scm.syslog_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_profiles_for_filtering
  
# Filter profiles by name pattern in memory
- name: Filter profiles for names starting with "log-"
  set_fact:
    log_profiles: 
      syslog_server_profiles: "{{ all_profiles_for_filtering.syslog_server_profiles | selectattr('name', 'match', '^log-.*') | list }}"

# Work with the filtered results
- name: Display filtered profiles
  debug:
    var: log_profiles
```

## Managing Configuration Changes

As an info module, `syslog_server_profiles_info` does not make any configuration changes. However,
you can use the information it retrieves to make decisions about other configuration operations.

```yaml
- name: Use syslog server profile information for log forwarding configuration
  block:
    - name: Get available syslog server profiles
      cdot65.scm.syslog_server_profiles_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: syslog_profiles
      
    - name: Create log forwarding profile using existing syslog profiles
      cdot65.scm.log_forwarding_profile:
        provider: "{{ provider }}"
        name: "system-logs-forwarding"
        folder: "Texas"
        match_list:
          - name: "System-Logs"
            log_type: "system"
            filter: "All Logs"
            send_to_syslog: "{{ syslog_profiles.syslog_server_profiles[0].name }}"
        state: "present"
      when: syslog_profiles.syslog_server_profiles | length > 0
      
    - name: Commit changes if log forwarding profile was created
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Created log forwarding profile using existing syslog server profiles"
      when: syslog_profiles.syslog_server_profiles | length > 0
```

### Return Values

| Name                   | Description                                                        | Type | Returned                         | Sample                                                                                                                                                         |
| ---------------------- | ------------------------------------------------------------------ | ---- | -------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| syslog_server_profile  | Information about the requested syslog server profile              | dict | when name is specified and found | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "test-syslog-profile", "servers": {"name": "primary-syslog", "server": "10.0.0.1", "transport": "UDP"}} |
| syslog_server_profiles | List of syslog server profile objects matching the filter criteria | list | when name is not specified       | [{"id": "123...", "name": "profile1", ...}, {"id": "456...", "name": "profile2", ...}]                                                                         |

## Error Handling

Common errors you might encounter when using this module:

| Error                           | Description                                      | Resolution                                                  |
| ------------------------------- | ------------------------------------------------ | ----------------------------------------------------------- |
| Syslog server profile not found | Attempt to retrieve a profile that doesn't exist | Verify the profile name and container location              |
| Missing query parameter         | Required parameter not provided for filtering    | Ensure required container parameters are specified          |
| Invalid filter parameters       | Invalid filter values provided                   | Check filter values for proper format and supported options |

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to retrieve syslog server profile
      cdot65.scm.syslog_server_profiles_info:
        provider: "{{ provider }}"
        name: "test-syslog-profile"
        folder: "Texas"
      register: result
  rescue:
    - name: Handle profile not found error
      debug:
        msg: "Syslog server profile not found or invalid input provided"
    - name: Continue with other tasks
      # Additional recovery tasks
```

## Best Practices

### Efficient Filtering

- Use specific filters to reduce the number of results
- Utilize the transport filter to find profiles with specific server types
- Combine multiple filters for precise results
- Use exact_match parameter for exact container filtering
- Filter at the API level rather than client side when possible for better performance

### Container Management

- Only specify one container type (folder, snippet, or device) at a time
- Use the same container type consistently across operations
- Document container hierarchy for better organization
- Create consistent naming conventions for containers
- Include container paths in reports and documentation

### Result Handling

- Check if results are empty before processing
- Handle potential errors with try/except or block/rescue
- Register results for further processing
- Use conditional logic based on returned data
- Process large result sets in batches for better performance

### Performance Optimization

- Use exact_match for faster, more specific queries
- Include exclusion filters to eliminate unwanted results
- Fetch specific profiles by name when possible instead of filtering large lists
- Minimize the number of API calls by retrieving all needed information at once
- Only request the gather_subset data that you need

### Integration with Other Modules

- Use the info module to verify existence before creating or updating profiles
- Chain tasks to create conditional workflows based on query results
- Use returned data as input for other tasks
- Combine with log_forwarding_profile for complete logging configuration
- Create documentation from retrieved information

### Automation and Inventory

- Use this module for automated documentation generation
- Build inventory reports of syslog configurations
- Create validation tasks to ensure correct syslog configuration
- Implement regular configuration checks and audits
- Develop configuration baseline templates from existing profiles

## Related Modules

- [syslog_server_profiles](syslog_server_profiles.md) - Manage syslog server profiles (create,
  update, delete)
- [log_forwarding_profile](log_forwarding_profile.md) - Manage log forwarding profiles that use
  syslog server profiles
- [log_forwarding_profile_info](log_forwarding_profile_info.md) - Retrieve information about log
  forwarding profiles
- [security_rule](security_rule.md) - Configure security policies that might reference log
  forwarding profiles
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules

## Author

- Calvin Remsburg (@cdot65)
