# Hip Profile Information Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [HIP Profile Info Model Attributes](#hip-profile-info-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Getting Information about a Specific HIP Profile](#getting-information-about-a-specific-hip-profile)
    - [Listing All HIP Profiles in a Folder](#listing-all-hip-profiles-in-a-folder)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
    - [Filtering by HIP Objects](#filtering-by-hip-objects)
07. [Processing Retrieved Information](#processing-retrieved-information)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `hip_profile_info` Ansible module provides functionality to gather information about Host
Information Profile (HIP) profiles in Palo Alto Networks' Strata Cloud Manager (SCM). This is an
info module that allows fetching details about specific HIP profiles or listing profiles with
various filtering options, including by HIP objects used in match expressions.

## Core Methods

| Method    | Description                         | Parameters                    | Return Type                     |
| --------- | ----------------------------------- | ----------------------------- | ------------------------------- |
| `fetch()` | Gets a specific HIP profile by name | `name: str`, `container: str` | `HipProfileResponseModel`       |
| `list()`  | Lists HIP profiles with filtering   | `folder: str`, `**filters`    | `List[HipProfileResponseModel]` |

## HIP Profile Info Model Attributes

| Parameter          | Type | Required | Description                                                 |
| ------------------ | ---- | -------- | ----------------------------------------------------------- |
| `name`             | str  | No       | Name of a specific HIP profile to retrieve                  |
| `gather_subset`    | list | No       | Determines which information to gather (default: config)    |
| `folder`           | str  | No\*     | Filter HIP profiles by folder container                     |
| `snippet`          | str  | No\*     | Filter HIP profiles by snippet container                    |
| `device`           | str  | No\*     | Filter HIP profiles by device container                     |
| `exact_match`      | bool | No       | When True, only return objects defined exactly in container |
| `exclude_folders`  | list | No       | List of folder names to exclude from results                |
| `exclude_snippets` | list | No       | List of snippet values to exclude from results              |
| `exclude_devices`  | list | No       | List of device values to exclude from results               |
| `hip_objects`      | list | No       | Filter by HIP objects used in the profile                   |

\*One container parameter is required when `name` is not specified.

### Provider Dictionary Attributes

| Attribute       | Type | Required | Default | Description                      |
| --------------- | ---- | -------- | ------- | -------------------------------- |
| `client_id`     | str  | Yes      |         | Client ID for authentication     |
| `client_secret` | str  | Yes      |         | Client secret for authentication |
| `tsg_id`        | str  | Yes      |         | Tenant Service Group ID          |
| `log_level`     | str  | No       | "INFO"  | Log level for the SDK            |

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
- name: Basic HIP Profile Info Configuration
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
        folder: "Texas"
      register: profiles_result
      
    - name: Display retrieved HIP profiles
      debug:
        var: profiles_result
```

## Usage Examples

### Getting Information about a Specific HIP Profile

Retrieve details about a specific HIP profile by name and container.

```yaml
- name: Get information about a specific HIP profile
  cdot65.scm.hip_profile_info:
    provider: "{{ provider }}"
    name: "High_Security_Profile"
    folder: "Texas"
  register: profile_info
  
- name: Display HIP profile information
  debug:
    var: profile_info.hip_profile
    
- name: Check match expressions
  debug:
    msg: "Profile match expressions: {{ profile_info.hip_profile.match | default([]) | length }} expressions defined"
  when: profile_info.hip_profile.match is defined
```

### Listing All HIP Profiles in a Folder

List all HIP profiles in a specific folder.

```yaml
- name: List all HIP profiles in a folder
  cdot65.scm.hip_profile_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_profiles
  
- name: Display all HIP profiles
  debug:
    var: all_profiles.hip_profiles
    
- name: Display count of HIP profiles
  debug:
    msg: "Found {{ all_profiles.hip_profiles | length }} HIP profiles"
    
- name: List names of all HIP profiles
  debug:
    msg: "{{ all_profiles.hip_profiles | map(attribute='name') | list }}"
```

### Using Advanced Filtering Options

Use advanced filtering options to refine your query results.

```yaml
- name: List HIP profiles with exact match parameter
  cdot65.scm.hip_profile_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
  register: exact_match_profiles

- name: List HIP profiles with exclusions
  cdot65.scm.hip_profile_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_profiles
```

### Filtering by HIP Objects

Filter HIP profiles by specific HIP objects used in match expressions.

```yaml
- name: List HIP profiles that use specific HIP objects
  cdot65.scm.hip_profile_info:
    provider: "{{ provider }}"
    folder: "Texas"
    hip_objects: ["Windows_Workstation", "Encrypted_Drives"]
  register: object_filtered_profiles
  
- name: Display HIP profiles using specified objects
  debug:
    msg: "Profiles using specified HIP objects: {{ object_filtered_profiles.hip_profiles | map(attribute='name') | list }}"
```

## Processing Retrieved Information

Example of processing and utilizing the retrieved HIP profile information.

```yaml
- name: Analyze HIP profile information
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:
    - name: Get all HIP profiles
      cdot65.scm.hip_profile_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: profiles_info
      
    - name: Extract HIP objects used in profiles
      set_fact:
        hip_object_usage: >-
          {% set result = {} %}
          {% for profile in profiles_info.hip_profiles | default([]) %}
            {% for match in profile.match | default([]) %}
              {% for obj in match.object | default([]) %}
                {% if obj not in result %}
                  {% set _ = result.update({obj: []}) %}
                {% endif %}
                {% if profile.name not in result[obj] %}
                  {% set _ = result[obj].append(profile.name) %}
                {% endif %}
              {% endfor %}
            {% endfor %}
          {% endfor %}
          {{ result }}
      
    - name: Display HIP object usage
      debug:
        var: hip_object_usage
        
    - name: Find profiles with complex match expressions
      set_fact:
        complex_profiles: "{{ profiles_info.hip_profiles | selectattr('match', 'defined') | selectattr('match', 'length_is_greater_than', 1) | list }}"
        
    - name: Display profiles with complex match expressions
      debug:
        msg: "Profiles with complex match expressions: {{ complex_profiles | map(attribute='name') | list }}"
```

## Error Handling

It's important to handle potential errors when retrieving information about HIP profiles.

```yaml
- name: Get information about HIP profiles with error handling
  block:
    - name: Try to retrieve information about a HIP profile
      cdot65.scm.hip_profile_info:
        provider: "{{ provider }}"
        name: "High_Security_Profile"
        folder: "Texas"
      register: info_result
      
    - name: Display HIP profile information
      debug:
        var: info_result.hip_profile
        
  rescue:
    - name: Handle errors
      debug:
        msg: "Failed to retrieve HIP profile information: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a 'not found' error
      debug:
        msg: "The specified HIP profile does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

## Best Practices

### Efficient Querying

- Use specific filters to reduce API load and improve performance
- When looking for a specific HIP profile, use the `name` parameter instead of filtering results
- Use container parameters consistently across queries
- Filter by HIP objects when you need to find profiles using specific objects

### Result Processing

- Always register the module output to a variable for later use
- Check if the expected data is present before processing it
- Use appropriate Ansible filters and tests when processing complex nested structures
- Create structured summaries when analyzing multiple profiles

### Filter Usage

- Use `exact_match` when you only want profiles defined directly in the specified container
- Use exclusion filters to refine results without overcomplicating queries
- Filter by HIP objects to find profiles that use specific endpoint criteria
- Combine multiple filters for precise results

### Profile Analysis

- Study match expressions to understand profile behavior
- Map relationships between HIP objects and profiles
- Identify redundant or overly complex profiles
- Analyze profiles for consistency with security policies

### Integration with Other Modules

- Use the info module to check for existing HIP profiles before creating new ones
- Combine with the hip_profile module for complete profile management
- Use the retrieved information to make decisions in your playbooks
- Link profile information with HIP object configurations and security rules

### Security Practices

- Regularly audit HIP profiles to ensure they're still needed
- Review match expressions for logical correctness
- Document your HIP profile inventory and their purposes
- Maintain a clear mapping between HIP profiles and security policies

## Related Modules

- [hip_profile](hip_profile.md) - Create, update, and delete HIP profiles
- [hip_object_info](hip_object_info.md) - Retrieve information about HIP objects used in profiles
- [hip_object](hip_object.md) - Create, update, and delete HIP objects
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules that use
  HIP profiles
