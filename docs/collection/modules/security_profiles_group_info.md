# Security Profiles Group Information Object

## Table of Contents

- [Security Profiles Group Information Object](#security-profiles-group-information-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [Security Profiles Group Info Parameters](#security-profiles-group-info-parameters)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Getting Information about a Specific Security Profiles Group](#getting-information-about-a-specific-security-profiles-group)
    - [Listing All Security Profiles Groups in a Folder](#listing-all-security-profiles-groups-in-a-folder)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
  - [Managing Configuration Changes](#managing-configuration-changes)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Efficient Querying](#efficient-querying)
    - [Result Processing](#result-processing)
    - [Filter Usage](#filter-usage)
    - [Error Handling](#error-handling-1)
    - [Integration with Other Modules](#integration-with-other-modules)
    - [Profile Evaluation](#profile-evaluation)
  - [Related Modules](#related-modules)

## Overview

The `security_profiles_group_info` Ansible module provides functionality to gather information about
Security Profiles Group objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is an info
module that allows fetching details about specific groups or listing groups with various filtering
options. Security Profiles Groups bundle multiple security profiles (Anti-Spyware, Vulnerability
Protection, URL Filtering, etc.) into a single group that can be applied to security rules.

## Core Methods

| Method    | Description                   | Parameters                    | Return Type                                |
| --------- | ----------------------------- | ----------------------------- | ------------------------------------------ |
| `fetch()` | Gets a specific group by name | `name: str`, `container: str` | `SecurityProfilesGroupResponseModel`       |
| `list()`  | Lists groups with filtering   | `folder: str`, `**filters`    | `List[SecurityProfilesGroupResponseModel]` |

## Security Profiles Group Info Parameters

| Parameter          | Type | Required        | Description                                                               |
| ------------------ | ---- | --------------- | ------------------------------------------------------------------------- |
| `name`             | str  | No              | Name of a specific security profiles group to retrieve                    |
| `gather_subset`    | list | No              | Determines which information to gather (default: config)                  |
| `folder`           | str  | One container\* | Filter groups by folder container                                         |
| `snippet`          | str  | One container\* | Filter groups by snippet container                                        |
| `device`           | str  | One container\* | Filter groups by device container                                         |
| `exact_match`      | bool | No              | When True, only return objects defined exactly in the specified container |
| `exclude_folders`  | list | No              | List of folder names to exclude from results                              |
| `exclude_snippets` | list | No              | List of snippet values to exclude from results                            |
| `exclude_devices`  | list | No              | List of device values to exclude from results                             |
| `profile_type`     | list | No              | Filter by profile types included (e.g., anti_spyware, vulnerability)      |
| `tag_name`         | list | No              | Filter by tag names associated with the groups                            |

\*One container parameter is required when `name` is not specified.

## Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid request data or format |
| `MissingQueryParameterError` | Missing required parameters    |
| `ObjectNotPresentError`      | Group not found                |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The Security Profiles Group Info module requires proper authentication credentials to access the
Strata Cloud Manager API.

```yaml
- name: Basic Security Profiles Group Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about security profiles groups
      cdot65.scm.security_profiles_group_info:
        provider: "{{ provider }}"
        folder: "Shared"
      register: groups_result

    - name: Display retrieved security profiles groups
      debug:
        var: groups_result
```

## Usage Examples

### Getting Information about a Specific Security Profiles Group

Retrieve details about a specific security profiles group by name and container.

```yaml
- name: Get information about a specific security profiles group
  cdot65.scm.security_profiles_group_info:
    provider: "{{ provider }}"
    name: "Enhanced-Protection"
    folder: "Texas"
  register: group_info

- name: Display security profiles group information
  debug:
    var: group_info.security_profiles_group

- name: Check if the group includes Anti-Spyware protection
  debug:
    msg: "Group includes Anti-Spyware protection"
  when: group_info.security_profiles_group.anti_spyware_profile is defined and group_info.security_profiles_group.anti_spyware_profile != ''
```

### Listing All Security Profiles Groups in a Folder

List all security profiles groups in a specific folder.

```yaml
- name: List all security profiles groups in a folder
  cdot65.scm.security_profiles_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_groups

- name: Display all security profiles groups
  debug:
    var: all_groups.security_profiles_groups

- name: Display count of security profiles groups
  debug:
    msg: "Found {{ all_groups.security_profiles_groups | length }} security profiles groups"

- name: List names of all security profiles groups
  debug:
    msg: "{{ all_groups.security_profiles_groups | map(attribute='name') | list }}"
```

### Using Advanced Filtering Options

Use advanced filtering options to refine your query results.

```yaml
- name: List groups containing vulnerability protection profiles
  cdot65.scm.security_profiles_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    profile_type: [ "vulnerability" ]
  register: vulnerability_groups

- name: Process vulnerability protection groups
  debug:
    msg: "Group with vulnerability protection: {{ item.name }}"
  loop: "{{ vulnerability_groups.security_profiles_groups }}"

- name: List groups with specific tags
  cdot65.scm.security_profiles_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tag_name: [ "enhanced-security" ]
  register: tagged_groups

- name: List groups with exact match and exclusions
  cdot65.scm.security_profiles_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: [ "All" ]
    exclude_snippets: [ "default" ]
  register: filtered_groups
```

## Managing Configuration Changes

As an info module, `security_profiles_group_info` does not make any configuration changes. However,
you can use the information it retrieves to make decisions about other configuration operations.

```yaml
- name: Use security profiles group information for security rule configuration
  block:
    - name: Get security profiles groups with enhanced security features
      cdot65.scm.security_profiles_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
        tag_name: [ "enhanced-security" ]
      register: enhanced_groups

    - name: Create security rule using enhanced security profiles group
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Allow-Web-Enhanced-Security"
        folder: "Texas"
        source_zone: [ "Internal" ]
        destination_zone: [ "Internet" ]
        application: [ "web-browsing" ]
        source_address: [ "internal-subnets" ]
        destination_address: [ "any" ]
        service: [ "application-default" ]
        profile_group: "{{ enhanced_groups.security_profiles_groups[0].name }}"
        action: "allow"
        state: "present"
      when: enhanced_groups.security_profiles_groups | length > 0
```

## Error Handling

It's important to handle potential errors when retrieving information about security profiles
groups.

```yaml
- name: Get information about security profiles groups with error handling
  block:
    - name: Try to retrieve information about a security profiles group
      cdot65.scm.security_profiles_group_info:
        provider: "{{ provider }}"
        name: "Enhanced-Protection"
        folder: "Texas"
      register: info_result

    - name: Display security profiles group information
      debug:
        var: info_result.security_profiles_group

  rescue:
    - name: Handle errors
      debug:
        msg: "Failed to retrieve security profiles group information: {{ ansible_failed_result.msg }}"

    - name: Check if it's a 'not found' error
      debug:
        msg: "The specified security profiles group does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

## Best Practices

### Efficient Querying

- Use specific filters to reduce API load and improve performance
- When looking for a specific group, use the `name` parameter instead of filtering results
- Use container parameters consistently across queries
- Structure queries to minimize the number of API calls
- Document common query patterns for reuse

### Result Processing

- Always register the module output to a variable for later use
- Check if the expected data is present before processing it
- Use appropriate Ansible filters and tests when processing complex nested structures
- Create reusable tasks for common processing patterns
- Consider using set_fact for intermediate data transformation

### Filter Usage

- Use `exact_match` when you only want groups defined directly in the specified container
- Use exclusion filters to refine results without overcomplicating queries
- Combine multiple filters for more precise results
- Test filter combinations to ensure they return the expected results
- Document filter combinations for complex scenarios

### Error Handling

- Implement try/except blocks to handle potential errors
- Verify that the groups exist before attempting operations on them
- Provide meaningful error messages for troubleshooting
- Create recovery paths for common error scenarios
- Log errors with sufficient context for later analysis

### Integration with Other Modules

- Use the info module to check for existing groups before creating new ones
- Combine with the security_profiles_group module for complete group management
- Use the retrieved information to make decisions in your playbooks
- Build helper roles for common security profile management tasks
- Create workflows that combine multiple modules for end-to-end processes

### Profile Evaluation

- Check which types of profiles are included in each group
- Evaluate security profiles groups for policy consistency
- Compare groups to identify potential gaps in protection
- Use the information to standardize security implementations
- Document which security profiles groups include which protections

## Related Modules

- [security_profiles_group](security_profiles_group.md) - Create, update, and delete security
  profiles groups
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules that use
  security profiles groups
- [anti_spyware_profile_info](anti_spyware_profile_info.md) - Retrieve information about
  anti-spyware profiles
- [vulnerability_protection_profile_info](vulnerability_protection_profile_info.md) - Retrieve
  information about vulnerability protection profiles
- [wildfire_antivirus_profiles_info](wildfire_antivirus_profiles_info.md) - Retrieve information
  about WildFire antivirus profiles
- [url_categories_info](url_categories_info.md) - Retrieve information about URL categories used in
  filtering profiles
