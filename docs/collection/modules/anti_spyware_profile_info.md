# Anti Spyware Profile Information Object

## Table of Contents

- [Anti Spyware Profile Information Object](#anti-spyware-profile-information-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [Anti Spyware Profile Info Model Attributes](#anti-spyware-profile-info-model-attributes)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Retrieving Anti Spyware Profile Information](#retrieving-anti-spyware-profile-information)
    - [Getting a Specific Profile](#getting-a-specific-profile)
    - [Listing All Profiles](#listing-all-profiles)
    - [Filtering by Cloud Inline Analysis](#filtering-by-cloud-inline-analysis)
    - [Filtering by Rules](#filtering-by-rules)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
  - [Processing Retrieved Information](#processing-retrieved-information)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Efficient Filtering](#efficient-filtering)
    - [Container Selection](#container-selection)
    - [Information Handling](#information-handling)
    - [Performance Optimization](#performance-optimization)
    - [Security Considerations](#security-considerations)
    - [Integration with Other Modules](#integration-with-other-modules)
  - [Related Modules](#related-modules)

## Overview

The `anti_spyware_profile_info` Ansible module provides functionality to retrieve information about
anti-spyware profile objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is a read-only
module that can retrieve detailed information about a specific anti-spyware profile by name, or list
multiple profiles with various filtering options including cloud inline analysis, rules, and
container-based filtering.

## Core Methods

| Method     | Description                                | Parameters                              | Return Type                             |
| ---------- | ------------------------------------------ | --------------------------------------- | --------------------------------------- |
| `get()`    | Gets a specific anti-spyware profile       | `name: str`, `container: str`           | `AntiSpywareProfileResponseModel`       |
| `list()`   | Lists anti-spyware profiles with filtering | `folder: str`, `**filters`              | `List[AntiSpywareProfileResponseModel]` |
| `filter()` | Applies filters to the results             | `profiles: List`, `filter_params: Dict` | `List[AntiSpywareProfileResponseModel]` |

## Anti Spyware Profile Info Model Attributes

| Attribute               | Type | Required      | Description                                                  |
| ----------------------- | ---- | ------------- | ------------------------------------------------------------ |
| `name`                  | str  | No            | The name of a specific anti-spyware profile to retrieve      |
| `gather_subset`         | list | No            | Determines which information to gather (default: ['config']) |
| `folder`                | str  | One container | Filter profiles by folder (max 64 chars)                     |
| `snippet`               | str  | One container | Filter profiles by snippet (max 64 chars)                    |
| `device`                | str  | One container | Filter profiles by device (max 64 chars)                     |
| `exact_match`           | bool | No            | When True, only return objects in the specified container    |
| `exclude_folders`       | list | No            | List of folder names to exclude from results                 |
| `exclude_snippets`      | list | No            | List of snippet values to exclude from results               |
| `exclude_devices`       | list | No            | List of device values to exclude from results                |
| `cloud_inline_analysis` | bool | No            | Filter by cloud inline analysis setting                      |
| `rules`                 | list | No            | Filter by rule names                                         |

## Exceptions

| Exception                    | Description                      |
| ---------------------------- | -------------------------------- |
| `ObjectNotPresentError`      | Profile not found                |
| `MissingQueryParameterError` | Missing required parameters      |
| `InvalidFilterError`         | Invalid filter parameters        |
| `AuthenticationError`        | Authentication failed            |
| `ServerError`                | Internal server error            |
| `MultipleMatchesError`       | Multiple profiles match criteria |

## Basic Configuration

The Anti-Spyware Profile Info module requires proper authentication credentials to access the Strata
Cloud Manager API.

```yaml
- name: Basic Anti-Spyware Profile Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about anti-spyware profiles
      cdot65.scm.anti_spyware_profile_info:
        provider: "{{ provider }}"
        folder: "Production"
      register: profiles_info
      
    - name: Display retrieved information
      debug:
        var: profiles_info.anti_spyware_profiles
```

## Usage Examples

### Retrieving Anti Spyware Profile Information

The module provides several ways to retrieve anti-spyware profile information based on your specific
needs.

### Getting a Specific Profile

This example retrieves detailed information about a specific anti-spyware profile by name.

```yaml
- name: Get information about a specific anti-spyware profile
  cdot65.scm.anti_spyware_profile_info:
    provider: "{{ provider }}"
    name: "Custom-Spyware-Profile"
    folder: "Production"
  register: profile_info
  
- name: Display specific profile information
  debug:
    var: profile_info.anti_spyware_profile
```

### Listing All Profiles

This example lists all anti-spyware profiles in a specific folder.

```yaml
- name: List all anti-spyware profiles in a folder
  cdot65.scm.anti_spyware_profile_info:
    provider: "{{ provider }}"
    folder: "Production"
  register: all_profiles
  
- name: Display count of profiles
  debug:
    msg: "Found {{ all_profiles.anti_spyware_profiles | length }} anti-spyware profiles in Production folder"
```

### Filtering by Cloud Inline Analysis

This example demonstrates how to filter profiles by their cloud inline analysis setting.

```yaml
- name: List profiles with cloud inline analysis enabled
  cdot65.scm.anti_spyware_profile_info:
    provider: "{{ provider }}"
    folder: "Production"
    cloud_inline_analysis: true
  register: cloud_enabled_profiles
  
- name: Display profiles with cloud inline analysis
  debug:
    msg: "Found {{ cloud_enabled_profiles.anti_spyware_profiles | length }} profiles with cloud inline analysis enabled"
```

### Filtering by Rules

This example shows how to find profiles that include specific rules.

```yaml
- name: List profiles with specific rules
  cdot65.scm.anti_spyware_profile_info:
    provider: "{{ provider }}"
    folder: "Production"
    rules: ["Block-Critical-Threats"]
  register: rule_profiles
  
- name: Process profiles with specific rules
  debug:
    msg: "Profile {{ item.name }} includes the Block-Critical-Threats rule"
  loop: "{{ rule_profiles.anti_spyware_profiles }}"
```

### Using Advanced Filtering Options

This example illustrates more advanced filtering options including exact match and exclusions.

```yaml
- name: List profiles with exact match and exclusions
  cdot65.scm.anti_spyware_profile_info:
    provider: "{{ provider }}"
    folder: "Production"
    exact_match: true
    exclude_folders: ["Development"]
    exclude_snippets: ["default"]
  register: filtered_profiles
  
- name: Use multiple filters together
  cdot65.scm.anti_spyware_profile_info:
    provider: "{{ provider }}"
    folder: "Production"
    cloud_inline_analysis: true
    rules: ["Block-Critical-Threats"]
    exclude_devices: ["DeviceA"]
  register: complex_filtered_profiles
```

## Processing Retrieved Information

After retrieving anti-spyware profile information, you can process the data for various purposes
such as reporting, analysis, or integration with other systems.

```yaml
- name: Create a summary of anti-spyware profile information
  block:
    - name: Get all anti-spyware profiles
      cdot65.scm.anti_spyware_profile_info:
        provider: "{{ provider }}"
        folder: "Production"
      register: all_profiles
      
    - name: Analyze profile configurations
      set_fact:
        profiles_with_cloud_analysis: "{{ all_profiles.anti_spyware_profiles | selectattr('cloud_inline_analysis', 'defined') | selectattr('cloud_inline_analysis', 'equalto', true) | list }}"
        profiles_with_packet_capture: "{{ all_profiles.anti_spyware_profiles | selectattr('packet_capture', 'defined') | selectattr('packet_capture', 'equalto', true) | list }}"
        
    - name: Create a report on rule severity distribution
      set_fact:
        critical_rules: "{{ all_profiles.anti_spyware_profiles | map(attribute='rules') | flatten | selectattr('severity', 'defined') | selectattr('severity', 'contains', 'critical') | list | length }}"
        high_rules: "{{ all_profiles.anti_spyware_profiles | map(attribute='rules') | flatten | selectattr('severity', 'defined') | selectattr('severity', 'contains', 'high') | list | length }}"
        medium_rules: "{{ all_profiles.anti_spyware_profiles | map(attribute='rules') | flatten | selectattr('severity', 'defined') | selectattr('severity', 'contains', 'medium') | list | length }}"
        
    - name: Display summary information
      debug:
        msg: |
          Anti-Spyware Profile Summary:
          - Total Profiles: {{ all_profiles.anti_spyware_profiles | length }}
          - Profiles with Cloud Analysis: {{ profiles_with_cloud_analysis | length }}
          - Profiles with Packet Capture: {{ profiles_with_packet_capture | length }}
          
          Rule Severity Distribution:
          - Critical Rules: {{ critical_rules }}
          - High Rules: {{ high_rules }}
          - Medium Rules: {{ medium_rules }}
```

## Error Handling

It's important to handle potential errors when retrieving anti-spyware profile information.

```yaml
- name: Retrieve anti-spyware profile info with error handling
  block:
    - name: Attempt to retrieve profile information
      cdot65.scm.anti_spyware_profile_info:
        provider: "{{ provider }}"
        name: "NonExistentProfile"
        folder: "Production"
      register: profile_info
      
  rescue:
    - name: Handle profile not found error
      debug:
        msg: "Anti-spyware profile not found or other error occurred"
        
    - name: Continue with fallback actions
      cdot65.scm.anti_spyware_profile_info:
        provider: "{{ provider }}"
        folder: "Production"
      register: all_profiles
      
    - name: Log the error and continue
      debug:
        msg: "Continuing with list of all profiles instead of specific profile"
```

## Best Practices

### Efficient Filtering

- Use specific filters to minimize the result set
- Filter by cloud inline analysis setting when specifically needed
- Filter by rule names to find profiles with specific rules
- Combine multiple filters for more precise results

### Container Selection

- Use folder, snippet, or device consistently across operations
- Verify container existence before querying
- Use exclusion filters to refine results when working with large containers

### Information Handling

- Register results to variables for further processing
- Use Ansible's filtering capabilities (selectattr, map, etc.) on the returned lists
- Check if anti_spyware_profiles/anti_spyware_profile is defined before accessing properties
- Process rule information separately for detailed analysis

### Performance Optimization

- Retrieve only the information you need
- Use name parameter when you need only one specific profile
- Use filters to minimize result set size
- Consider caching results for repeated access within the same playbook

### Security Considerations

- Protect sensitive information in filter criteria
- Store credentials securely using Ansible Vault
- Limit information gathering to necessary objects only
- Use least privilege accounts for API access

### Integration with Other Modules

- Use retrieved profile information to inform anti_spyware_profile module operations
- Combine with security_rule_info to see where profiles are used
- Create dynamic inventories based on profile usage
- Generate compliance reports using profile configurations

## Related Modules

- [anti_spyware_profile](anti_spyware_profile.md) - Manage anti-spyware profile objects
- [security_rule](security_rule.md) - Manage security rules that use anti-spyware profiles
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules using
  profiles
- [security_profiles_group](security_profiles_group.md) - Manage security profile groups that
  include anti-spyware profiles
