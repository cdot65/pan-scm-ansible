# DNS Security Profile Information Object

## 01. Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [DNS Security Profile Info Model Attributes](#dns-security-profile-info-model-attributes)
4. [Exceptions](#exceptions)
5. [Basic Configuration](#basic-configuration)
6. [Usage Examples](#usage-examples)
   - [Getting Information about a Specific DNS Security Profile](#getting-information-about-a-specific-dns-security-profile)
   - [Listing All DNS Security Profiles in a Folder](#listing-all-dns-security-profiles-in-a-folder)
   - [Filtering by DNS Security Categories](#filtering-by-dns-security-categories)
   - [Using Advanced Filtering Options](#using-advanced-filtering-options)
7. [Processing Retrieved Information](#processing-retrieved-information)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## 02. Overview

The `dns_security_profile_info` Ansible module provides functionality to gather information about DNS Security Profile objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is an info module that allows fetching details about specific DNS security profiles or listing profiles with various filtering options, including DNS security categories.

## 03. Core Methods

| Method    | Description                     | Parameters                    | Return Type                          |
| --------- | ------------------------------- | ----------------------------- | ------------------------------------ |
| `fetch()` | Gets a specific profile by name | `name: str`, `container: str` | `DnsSecurityProfileResponseModel`    |
| `list()`  | Lists profiles with filtering   | `folder: str`, `**filters`    | `List[DnsSecurityProfileResponseModel]` |

## 04. DNS Security Profile Info Model Attributes

| Parameter               | Type   | Required | Description                                                               |
| ----------------------- | ------ | -------- | ------------------------------------------------------------------------- |
| `name`                  | str    | No       | Name of a specific DNS security profile to retrieve                       |
| `gather_subset`         | list   | No       | Determines which information to gather (default: config)                  |
| `folder`                | str    | No\*     | Filter profiles by folder container                                       |
| `snippet`               | str    | No\*     | Filter profiles by snippet container                                      |
| `device`                | str    | No\*     | Filter profiles by device container                                       |
| `exact_match`           | bool   | No       | When True, only return objects defined exactly in the specified container |
| `exclude_folders`       | list   | No       | List of folder names to exclude from results                              |
| `exclude_snippets`      | list   | No       | List of snippet values to exclude from results                            |
| `exclude_devices`       | list   | No       | List of device values to exclude from results                             |
| `dns_security_categories`| list  | No       | Filter by DNS security categories                                         |

\*One container parameter is required when `name` is not specified.

## 05. Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid request data or format |
| `MissingQueryParameterError` | Missing required parameters    |
| `ObjectNotPresentError`      | Profile not found              |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## 06. Basic Configuration

The DNS Security Profile Info module requires proper authentication credentials to access the
Strata Cloud Manager API.

```yaml
- name: Basic DNS Security Profile Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about DNS security profiles
      cdot65.scm.dns_security_profile_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: profiles_result
      
    - name: Display retrieved DNS security profiles
      debug:
        var: profiles_result
```

## 07. Usage Examples

### Getting Information about a Specific DNS Security Profile

Retrieve details about a specific DNS security profile by name and container.

```yaml
- name: Get information about a specific DNS security profile
  cdot65.scm.dns_security_profile_info:
    provider: "{{ provider }}"
    name: "test-dns-security"
    folder: "Texas"
  register: profile_info
  
- name: Display DNS security profile information
  debug:
    var: profile_info.dns_security_profile
    
- name: Check if profile has botnet domains
  debug:
    msg: "Profile contains botnet domains configuration"
  when: >
    profile_info.dns_security_profile.botnet_domains is defined and
    profile_info.dns_security_profile.botnet_domains | length > 0
```

### Listing All DNS Security Profiles in a Folder

List all DNS security profiles in a specific folder.

```yaml
- name: List all DNS security profiles in a folder
  cdot65.scm.dns_security_profile_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_profiles
  
- name: Display all DNS security profiles
  debug:
    var: all_profiles.dns_security_profiles
    
- name: Display count of DNS security profiles
  debug:
    msg: "Found {{ all_profiles.dns_security_profiles | length }} DNS security profiles"
    
- name: List names of all DNS security profiles
  debug:
    msg: "{{ all_profiles.dns_security_profiles | map(attribute='name') | list }}"
```

### Filtering by DNS Security Categories

Filter DNS security profiles by security categories.

```yaml
- name: List DNS security profiles with specific security categories
  cdot65.scm.dns_security_profile_info:
    provider: "{{ provider }}"
    folder: "Texas"
    dns_security_categories: ["command-and-control", "malware"]
  register: category_profiles
  
- name: Process category filtered profiles
  debug:
    msg: "Category filtered profile: {{ item.name }}"
  loop: "{{ category_profiles.dns_security_profiles }}"
```

### Using Advanced Filtering Options

Use advanced filtering options to refine your query results.

```yaml
- name: List profiles with exact match parameter
  cdot65.scm.dns_security_profile_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
  register: exact_match_profiles

- name: List profiles with exact match and exclusions
  cdot65.scm.dns_security_profile_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_profiles
```

## 08. Processing Retrieved Information

Example of processing and utilizing the retrieved DNS security profile information.

```yaml
- name: Analyze DNS security profile information
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:
    - name: Get all DNS security profiles
      cdot65.scm.dns_security_profile_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: profiles_info
      
    - name: Create summary of DNS security categories used
      set_fact:
        category_summary: >-
          {{ category_summary | default({}) | combine({item.0: (item.1 | map(attribute='name') | list)}) }}
      loop: "{{ category_list | default([]) }}"
      vars:
        all_profiles: "{{ profiles_info.dns_security_profiles | default([]) }}"
        all_categories: "{{ all_profiles | map(attribute='dns_security_categories') | list | flatten | unique }}"
        category_list: >-
          {% set result = [] %}
          {% for category in all_categories %}
            {% set profiles_with_category = all_profiles | selectattr('dns_security_categories', 'defined') | 
               selectattr('dns_security_categories', 'contains', category) | list %}
            {% if profiles_with_category %}
              {% set _ = result.append([category, profiles_with_category]) %}
            {% endif %}
          {% endfor %}
          {{ result }}
      
    - name: Display category summary
      debug:
        var: category_summary
        
    - name: Find profiles with sinkhole configuration
      set_fact:
        sinkhole_profiles: "{{ profiles_info.dns_security_profiles | selectattr('sinkhole', 'defined') | list }}"
        
    - name: Display profiles with sinkhole configuration
      debug:
        msg: "Profiles using sinkhole configuration: {{ sinkhole_profiles | map(attribute='name') | list }}"
```

## 09. Error Handling

It's important to handle potential errors when retrieving information about DNS security profiles.

```yaml
- name: Get information about DNS security profiles with error handling
  block:
    - name: Try to retrieve information about a DNS security profile
      cdot65.scm.dns_security_profile_info:
        provider: "{{ provider }}"
        name: "test-dns-security"
        folder: "Texas"
      register: info_result
      
    - name: Display DNS security profile information
      debug:
        var: info_result.dns_security_profile
        
  rescue:
    - name: Handle errors
      debug:
        msg: "Failed to retrieve DNS security profile information: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a 'not found' error
      debug:
        msg: "The specified DNS security profile does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

## 10. Best Practices

### Efficient Querying

- Use specific filters to reduce API load and improve performance
- When looking for a specific profile, use the `name` parameter instead of filtering results
- Use container parameters consistently across queries
- Use DNS security category filters to target profiles with specific capabilities

### Result Processing

- Always register the module output to a variable for later use
- Check if the expected data is present before processing it
- Use appropriate Ansible filters and tests when processing complex nested structures
- Create structured summaries when analyzing multiple profiles

### Filter Usage

- Use `exact_match` when you only want profiles defined directly in the specified container
- Use exclusion filters to refine results without overcomplicating queries
- Filter by DNS security categories to find profiles addressing specific threats
- Combine multiple filters for precise results

### Security Analysis

- Review DNS security profiles for consistency in category coverage
- Check for duplicate profiles that serve the same purpose
- Verify sinkhole configurations are properly implemented
- Analyze botnet domain configurations for comprehensive protection

### Error Handling

- Implement try/except blocks to handle potential errors
- Verify that the profiles exist before attempting operations on them
- Provide meaningful error messages for troubleshooting
- Plan for graceful recovery when profiles are not found

### Integration with Other Modules

- Use the info module to check for existing profiles before creating new ones
- Combine with the dns_security_profile module for complete profile management
- Use the retrieved information to make decisions in your playbooks
- Integrate with security rule modules to verify profile utilization

## 11. Related Modules

- [dns_security_profile](dns_security_profile.md) - Create, update, and delete DNS security profiles
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules that use DNS security profiles
- [security_profiles_group](security_profiles_group.md) - Manage security profile groups that include DNS security profiles
- [vulnerability_protection_profile_info](vulnerability_protection_profile_info.md) - Retrieve information about vulnerability protection profiles