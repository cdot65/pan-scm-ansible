# Decryption Profile Information Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Decryption Profile Info Model Attributes](#decryption-profile-info-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Retrieving Decryption Profile Information](#retrieving-decryption-profile-information)
    - [Getting a Specific Decryption Profile](#getting-a-specific-decryption-profile)
    - [Listing All Decryption Profiles](#listing-all-decryption-profiles)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
    - [Analyzing Decryption Profile Configuration](#analyzing-decryption-profile-configuration)
07. [Processing Retrieved Information](#processing-retrieved-information)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `decryption_profile_info` Ansible module provides functionality to retrieve information about decryption 
profile objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is a read-only module that can retrieve 
detailed information about a specific decryption profile by name, or list multiple decryption profiles with 
various filtering options. It enables administrators to audit and analyze SSL/TLS decryption settings across 
their environment.

## Core Methods

| Method     | Description                              | Parameters                           | Return Type                      |
| ---------- | ---------------------------------------- | ------------------------------------ | -------------------------------- |
| `get()`    | Gets a specific decryption profile       | `name: str`, `container: str`        | `DecryptionProfileResponseModel` |
| `list()`   | Lists decryption profiles with filtering | `folder: str`, `**filters`           | `List[DecryptionProfileResponseModel]` |
| `filter()` | Applies filters to the results           | `profiles: List`, `filter_params: Dict` | `List[DecryptionProfileResponseModel]` |

## Decryption Profile Info Model Attributes

| Attribute          | Type | Required      | Description                                                      |
| ------------------ | ---- | ------------- | ---------------------------------------------------------------- |
| `name`             | str  | No            | The name of a specific decryption profile to retrieve            |
| `gather_subset`    | list | No            | Determines which information to gather (default: ['config'])     |
| `folder`           | str  | One container | Filter profiles by folder (max 64 chars)                         |
| `snippet`          | str  | One container | Filter profiles by snippet (max 64 chars)                        |
| `device`           | str  | One container | Filter profiles by device (max 64 chars)                         |
| `exact_match`      | bool | No            | When True, only return objects in the specified container        |
| `exclude_folders`  | list | No            | List of folder names to exclude from results                     |
| `exclude_snippets` | list | No            | List of snippet values to exclude from results                   |
| `exclude_devices`  | list | No            | List of device values to exclude from results                    |

## Exceptions

| Exception                    | Description                     |
| ---------------------------- | ------------------------------- |
| `ObjectNotPresentError`      | Profile not found               |
| `MissingQueryParameterError` | Missing required parameters     |
| `InvalidFilterError`         | Invalid filter parameters       |
| `AuthenticationError`        | Authentication failed           |
| `ServerError`                | Internal server error           |
| `MultipleMatchesError`       | Multiple profiles match criteria |

## Basic Configuration

The Decryption Profile Info module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Decryption Profile Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about decryption profiles
      cdot65.scm.decryption_profile_info:
        provider: "{{ provider }}"
        folder: "Production"
      register: profiles_info
      
    - name: Display retrieved information
      debug:
        var: profiles_info.profiles
```

## Usage Examples

### Retrieving Decryption Profile Information

The module provides several ways to retrieve decryption profile information based on your specific needs.

### Getting a Specific Decryption Profile

This example retrieves detailed information about a specific decryption profile by name.

```yaml
- name: Get information about a specific decryption profile
  cdot65.scm.decryption_profile_info:
    provider: "{{ provider }}"
    name: "Custom-Decryption-Profile"
    folder: "Production"
  register: profile_info

- name: Display specific profile information
  debug:
    var: profile_info.profile
```

### Listing All Decryption Profiles

This example lists all decryption profiles in a specific folder.

```yaml
- name: List all decryption profiles in a folder
  cdot65.scm.decryption_profile_info:
    provider: "{{ provider }}"
    folder: "Production"
  register: all_profiles

- name: Display count of profiles
  debug:
    msg: "Found {{ all_profiles.profiles | length }} decryption profiles in Production folder"
```

### Using Advanced Filtering Options

This example demonstrates how to use advanced filtering options to narrow down the list of profiles.

```yaml
- name: List profiles with exact match and exclusions
  cdot65.scm.decryption_profile_info:
    provider: "{{ provider }}"
    folder: "Production"
    exact_match: true
    exclude_folders: ["Shared"]
    exclude_snippets: ["default"]
  register: filtered_profiles

- name: Display filtered profiles
  debug:
    msg: "Found {{ filtered_profiles.profiles | length }} profiles after filtering"
```

### Analyzing Decryption Profile Configuration

This example retrieves decryption profiles and analyzes their configuration.

```yaml
- name: Get all decryption profiles for analysis
  cdot65.scm.decryption_profile_info:
    provider: "{{ provider }}"
    folder: "Production"
  register: all_profiles

- name: Find profiles with forward proxy enabled
  set_fact:
    forward_proxy_profiles: "{{ all_profiles.profiles | selectattr('ssl_forward_proxy', 'defined') 
                                | selectattr('ssl_forward_proxy.enabled', 'defined') 
                                | selectattr('ssl_forward_proxy.enabled', 'equalto', true) 
                                | list }}"

- name: Display forward proxy profiles
  debug:
    msg: "{{ forward_proxy_profiles | map(attribute='name') | list }}"
```

## Processing Retrieved Information

After retrieving decryption profile information, you can process the data for security auditing, 
compliance reporting, or operational analysis.

```yaml
- name: Analyze SSL/TLS security settings across profiles
  block:
    - name: Get all decryption profiles
      cdot65.scm.decryption_profile_info:
        provider: "{{ provider }}"
        folder: "Production"
      register: all_profiles
      
    - name: Analyze TLS version settings
      set_fact:
        legacy_tls_profiles: "{{ all_profiles.profiles | selectattr('ssl_protocol_settings', 'defined') 
                               | selectattr('ssl_protocol_settings.min_version', 'defined') 
                               | selectattr('ssl_protocol_settings.min_version', 'in', ['tls1-0', 'tls1-1']) 
                               | list }}"
        modern_tls_profiles: "{{ all_profiles.profiles | selectattr('ssl_protocol_settings', 'defined') 
                               | selectattr('ssl_protocol_settings.min_version', 'defined') 
                               | selectattr('ssl_protocol_settings.min_version', 'in', ['tls1-2', 'tls1-3']) 
                               | list }}"
                               
    - name: Analyze certificate validation settings
      set_fact:
        strict_cert_profiles: "{{ all_profiles.profiles | selectattr('ssl_forward_proxy', 'defined') 
                                | selectattr('ssl_forward_proxy.block_expired_cert', 'defined') 
                                | selectattr('ssl_forward_proxy.block_expired_cert', 'equalto', true) 
                                | selectattr('ssl_forward_proxy.block_untrusted_issuer', 'defined') 
                                | selectattr('ssl_forward_proxy.block_untrusted_issuer', 'equalto', true) 
                                | list }}"
                                
    - name: Create security summary
      debug:
        msg: |
          Decryption Profile Security Analysis:
          - Total Profiles: {{ all_profiles.profiles | length }}
          - Using Legacy TLS (1.0/1.1): {{ legacy_tls_profiles | map(attribute='name') | list }}
          - Using Modern TLS (1.2/1.3): {{ modern_tls_profiles | map(attribute='name') | list }}
          - Enforcing Strict Certificate Validation: {{ strict_cert_profiles | map(attribute='name') | list }}
```

## Error Handling

It's important to handle potential errors when retrieving decryption profile information.

```yaml
- name: Retrieve decryption profile info with error handling
  block:
    - name: Attempt to retrieve specific profile information
      cdot65.scm.decryption_profile_info:
        provider: "{{ provider }}"
        name: "nonexistent-profile"
        folder: "Production"
      register: profile_info
      
  rescue:
    - name: Handle profile not found error
      debug:
        msg: "Decryption profile not found or other error occurred"
        
    - name: Continue with fallback actions
      cdot65.scm.decryption_profile_info:
        provider: "{{ provider }}"
        folder: "Production"
      register: all_profiles
      
    - name: Log the error and continue
      debug:
        msg: "Continuing with list of all decryption profiles instead of specific profile"
```

## Best Practices

### Efficient Information Retrieval

- Use specific name queries when you know the profile you need
- Apply appropriate filters to limit result set size
- Use gather_subset appropriately to retrieve only needed information
- Consider query performance impacts in large environments

### Security Auditing

- Regularly review profiles for outdated security settings
- Check for legacy TLS protocol usage (TLS 1.0/1.1)
- Verify certificate validation settings are appropriate for your security policy
- Document exceptions to security best practices with detailed justification

### Operational Analysis

- Inventory decryption profiles across your environment
- Identify redundant or duplicate profiles
- Document profile purposes and usage contexts
- Track changes to profiles over time for compliance purposes

### Container Management

- Use consistent container parameters across queries
- Verify container existence before querying
- Apply appropriate filters when searching across multiple containers
- Document container organization strategy

### Integration with Other Modules

- Combine with security rule analysis for complete decryption policy review
- Use retrieved information to inform decryption profile creation or updates
- Include decryption profile analysis in security posture reporting
- Cross-reference with application traffic patterns for comprehensive visibility

## Related Modules

- [decryption_profile](decryption_profile.md) - Manage decryption profile objects
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules using decryption
- [security_rule](security_rule.md) - Configure security policies that use decryption profiles
- [security_profiles_group](security_profiles_group.md) - Manage security profile groups that can include decryption settings