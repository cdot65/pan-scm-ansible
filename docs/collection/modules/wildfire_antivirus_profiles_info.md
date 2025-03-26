# Wildfire Antivirus Profiles Information Object

## Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [WildFire Antivirus Profile Info Parameters](#wildfire-antivirus-profile-info-parameters)
4. [Exceptions](#exceptions)
5. [Basic Configuration](#basic-configuration)
6. [Usage Examples](#usage-examples)
   - [Getting Information about a Specific WildFire Antivirus Profile](#getting-information-about-a-specific-wildfire-antivirus-profile)
   - [Listing All WildFire Antivirus Profiles in a Folder](#listing-all-wildfire-antivirus-profiles-in-a-folder)
   - [Using Advanced Filtering Options](#using-advanced-filtering-options)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)
9. [Related Modules](#related-modules)

## Overview

The `wildfire_antivirus_profiles_info` Ansible module provides functionality to gather information
about WildFire Antivirus Profile objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is
an info module that allows fetching details about specific profiles or listing profiles with various
filtering options.

## Core Methods

| Method    | Description                     | Parameters                    | Return Type                            |
| --------- | ------------------------------- | ----------------------------- | -------------------------------------- |
| `fetch()` | Gets a specific profile by name | `name: str`, `container: str` | `WildfireAvProfileResponseModel`       |
| `list()`  | Lists profiles with filtering   | `folder: str`, `**filters`    | `List[WildfireAvProfileResponseModel]` |

## WildFire Antivirus Profile Info Parameters

| Parameter          | Type | Required | Description                                                               |
| ------------------ | ---- | -------- | ------------------------------------------------------------------------- |
| `name`             | str  | No       | Name of a specific WildFire antivirus profile to retrieve                 |
| `gather_subset`    | list | No       | Determines which information to gather (default: config)                  |
| `folder`           | str  | No\*     | Filter profiles by folder container                                       |
| `snippet`          | str  | No\*     | Filter profiles by snippet container                                      |
| `device`           | str  | No\*     | Filter profiles by device container                                       |
| `exact_match`      | bool | No       | When True, only return objects defined exactly in the specified container |
| `exclude_folders`  | list | No       | List of folder names to exclude from results                              |
| `exclude_snippets` | list | No       | List of snippet values to exclude from results                            |
| `exclude_devices`  | list | No       | List of device values to exclude from results                             |
| `rules`            | list | No       | Filter by rule names                                                      |

\*One container parameter is required when `name` is not specified.

## Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid request data or format |
| `MissingQueryParameterError` | Missing required parameters    |
| `ObjectNotPresentError`      | Profile not found              |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The WildFire Antivirus Profile Info module requires proper authentication credentials to access the
Strata Cloud Manager API.

```yaml
- name: Basic WildFire Antivirus Profile Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about WildFire antivirus profiles
      cdot65.scm.wildfire_antivirus_profiles_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: profiles_result
      
    - name: Display retrieved WildFire antivirus profiles
      debug:
        var: profiles_result
```

## Usage Examples

### Getting Information about a Specific WildFire Antivirus Profile

Retrieve details about a specific WildFire antivirus profile by name and container.

```yaml
- name: Get information about a specific WildFire antivirus profile
  cdot65.scm.wildfire_antivirus_profiles_info:
    provider: "{{ provider }}"
    name: "Basic-Wildfire-AV"
    folder: "Texas"
  register: profile_info
  
- name: Display WildFire antivirus profile information
  debug:
    var: profile_info.wildfire_antivirus_profile
    
- name: Check if profile has rules for downloads
  debug:
    msg: "Profile contains rules for download direction"
  when: >
    profile_info.wildfire_antivirus_profile.rules is defined and
    profile_info.wildfire_antivirus_profile.rules | selectattr('direction', 'equalto', 'download') | list | length > 0
```

### Listing All WildFire Antivirus Profiles in a Folder

List all WildFire antivirus profiles in a specific folder.

```yaml
- name: List all WildFire antivirus profiles in a folder
  cdot65.scm.wildfire_antivirus_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_profiles
  
- name: Display all WildFire antivirus profiles
  debug:
    var: all_profiles.wildfire_antivirus_profiles
    
- name: Display count of WildFire antivirus profiles
  debug:
    msg: "Found {{ all_profiles.wildfire_antivirus_profiles | length }} WildFire antivirus profiles"
    
- name: List names of all WildFire antivirus profiles
  debug:
    msg: "{{ all_profiles.wildfire_antivirus_profiles | map(attribute='name') | list }}"
```

### Using Advanced Filtering Options

Use advanced filtering options to refine your query results.

```yaml
- name: Filter WildFire antivirus profiles by rule name
  cdot65.scm.wildfire_antivirus_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    rules: ["Default-Rule"]
  register: rule_profiles
  
- name: Process rule filtered profiles
  debug:
    msg: "Rule filtered profile: {{ item.name }}"
  loop: "{{ rule_profiles.wildfire_antivirus_profiles }}"
  
- name: List profiles with exact match parameter
  cdot65.scm.wildfire_antivirus_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
  register: exact_match_profiles

- name: List profiles with exact match and exclusions
  cdot65.scm.wildfire_antivirus_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_profiles
```

## Error Handling

It's important to handle potential errors when retrieving information about WildFire antivirus
profiles.

```yaml
- name: Get information about WildFire antivirus profiles with error handling
  block:
    - name: Try to retrieve information about a WildFire antivirus profile
      cdot65.scm.wildfire_antivirus_profiles_info:
        provider: "{{ provider }}"
        name: "Basic-Wildfire-AV"
        folder: "Texas"
      register: info_result
      
    - name: Display WildFire antivirus profile information
      debug:
        var: info_result.wildfire_antivirus_profile
        
  rescue:
    - name: Handle errors
      debug:
        msg: "Failed to retrieve WildFire antivirus profile information: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a 'not found' error
      debug:
        msg: "The specified WildFire antivirus profile does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

## Best Practices

### Efficient Querying

- Use specific filters to reduce API load and improve performance
- When looking for a specific profile, use the `name` parameter instead of filtering results
- Use container parameters consistently across queries

### Result Processing

- Always register the module output to a variable for later use
- Check if the expected data is present before processing it
- Use appropriate Ansible filters and tests when processing complex nested structures

### Filter Usage

- Use `exact_match` when you only want profiles defined directly in the specified container
- Use exclusion filters to refine results without overcomplicating queries
- Filter by rule names to find profiles with specific rules

### Error Handling

- Implement try/except blocks to handle potential errors
- Verify that the profiles exist before attempting operations on them
- Provide meaningful error messages for troubleshooting

### Integration with Other Modules

- Use the info module to check for existing profiles before creating new ones
- Combine with the wildfire_antivirus_profiles module for complete profile management
- Use the retrieved information to make decisions in your playbooks

### Performance Considerations

- Cache results when making multiple queries for the same information
- Limit the data retrieved to only what's needed for your task
- Consider batching operations when processing multiple profiles

## Related Modules

- [wildfire_antivirus_profiles](wildfire_antivirus_profiles.md) - Create, update, and delete
  WildFire antivirus profiles
- [anti_spyware_profile_info](anti_spyware_profile_info.md) - Retrieve information about
  anti-spyware profiles
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules that use
  WildFire antivirus profiles
