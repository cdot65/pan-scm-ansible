# Http Server Profiles Information Object

## Table of Contents

- [Http Server Profiles Information Object](#http-server-profiles-information-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [HTTP Server Profile Info Model Attributes](#http-server-profile-info-model-attributes)
    - [Provider Dictionary Attributes](#provider-dictionary-attributes)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Getting Information about a Specific HTTP Server Profile](#getting-information-about-a-specific-http-server-profile)
    - [Listing All HTTP Server Profiles in a Folder](#listing-all-http-server-profiles-in-a-folder)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
    - [Filtering by Server Configuration](#filtering-by-server-configuration)
  - [Processing Retrieved Information](#processing-retrieved-information)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Efficient Querying](#efficient-querying)
    - [Result Processing](#result-processing)
    - [Filter Usage](#filter-usage)
    - [Information Analysis](#information-analysis)
    - [Integration with Other Modules](#integration-with-other-modules)
    - [Security Practices](#security-practices)
  - [Related Modules](#related-modules)

## Overview

The `http_server_profiles_info` Ansible module provides functionality to gather information about
HTTP Server Profile objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is an info
module that allows fetching details about specific HTTP server profiles or listing profiles with
various filtering options, without making any changes to the system.

## Core Methods

| Method    | Description                                 | Parameters                    | Return Type                            |
| --------- | ------------------------------------------- | ----------------------------- | -------------------------------------- |
| `fetch()` | Gets a specific HTTP server profile by name | `name: str`, `container: str` | `HttpServerProfileResponseModel`       |
| `list()`  | Lists HTTP server profiles with filtering   | `folder: str`, `**filters`    | `List[HttpServerProfileResponseModel]` |

## HTTP Server Profile Info Model Attributes

| Parameter          | Type | Required | Description                                                 |
| ------------------ | ---- | -------- | ----------------------------------------------------------- |
| `name`             | str  | No       | Name of a specific HTTP server profile to retrieve          |
| `gather_subset`    | list | No       | Determines which information to gather (default: config)    |
| `folder`           | str  | No\*     | Filter profiles by folder container                         |
| `snippet`          | str  | No\*     | Filter profiles by snippet container                        |
| `device`           | str  | No\*     | Filter profiles by device container                         |
| `exact_match`      | bool | No       | When True, only return objects defined exactly in container |
| `exclude_folders`  | list | No       | List of folder names to exclude from results                |
| `exclude_snippets` | list | No       | List of snippet values to exclude from results              |
| `exclude_devices`  | list | No       | List of device values to exclude from results               |
| `protocol`         | str  | No       | Filter by server protocol ("HTTP" or "HTTPS")               |
| `tag_registration` | bool | No       | Filter by tag registration setting                          |

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
| `ObjectNotPresentError`      | Profile not found              |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The HTTP Server Profiles Info module requires proper authentication credentials to access the Strata
Cloud Manager API.

```yaml
- name: Basic HTTP Server Profiles Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about HTTP server profiles
      cdot65.scm.http_server_profiles_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: profiles_result
      
    - name: Display retrieved HTTP server profiles
      debug:
        var: profiles_result
```

## Usage Examples

### Getting Information about a Specific HTTP Server Profile

Retrieve details about a specific HTTP server profile by name and container.

```yaml
- name: Get information about a specific HTTP server profile
  cdot65.scm.http_server_profiles_info:
    provider: "{{ provider }}"
    name: "test-http-profile"
    folder: "Texas"
  register: profile_info
  
- name: Display HTTP server profile information
  debug:
    var: profile_info.http_server_profile
    
- name: Check server configuration
  debug:
    msg: "Server: {{ item.name }}, Protocol: {{ item.protocol }}, Address: {{ item.address }}"
  loop: "{{ profile_info.http_server_profile.server }}"
```

### Listing All HTTP Server Profiles in a Folder

List all HTTP server profiles in a specific folder.

```yaml
- name: List all HTTP server profiles in a folder
  cdot65.scm.http_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_profiles
  
- name: Display all HTTP server profiles
  debug:
    var: all_profiles.http_server_profiles
    
- name: Display count of HTTP server profiles
  debug:
    msg: "Found {{ all_profiles.http_server_profiles | length }} HTTP server profiles"
    
- name: List names of all HTTP server profiles
  debug:
    msg: "{{ all_profiles.http_server_profiles | map(attribute='name') | list }}"
```

### Using Advanced Filtering Options

Use advanced filtering options to refine your query results.

```yaml
- name: List HTTP server profiles with exact match parameter
  cdot65.scm.http_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
  register: exact_match_profiles

- name: List HTTP server profiles with exclusions
  cdot65.scm.http_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_profiles
```

### Filtering by Server Configuration

Filter HTTP server profiles by specific server configuration parameters.

```yaml
- name: List HTTPS server profiles
  cdot65.scm.http_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    protocol: "HTTPS"
  register: https_profiles
  
- name: Display HTTPS server profiles
  debug:
    var: https_profiles.http_server_profiles
    
- name: List profiles with tag registration enabled
  cdot65.scm.http_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tag_registration: true
  register: tag_profiles
```

## Processing Retrieved Information

Example of processing and utilizing the retrieved HTTP server profile information.

```yaml
- name: Analyze HTTP server profile information
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:
    - name: Get all HTTP server profiles
      cdot65.scm.http_server_profiles_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: profiles_info
      
    - name: Group profiles by protocol
      set_fact:
        protocol_summary: "{{ protocol_summary | default({}) | combine({item: protocol_profiles[item] | map(attribute='name') | list}) }}"
      loop: "{{ protocol_profiles.keys() | list }}"
      vars:
        all_profiles: "{{ profiles_info.http_server_profiles | default([]) }}"
        protocol_profiles: >-
          {% set result = {'HTTP': [], 'HTTPS': []} %}
          {% for profile in all_profiles %}
            {% for server in profile.server | default([]) %}
              {% if server.protocol == 'HTTP' and profile not in result['HTTP'] %}
                {% set _ = result['HTTP'].append(profile) %}
              {% elif server.protocol == 'HTTPS' and profile not in result['HTTPS'] %}
                {% set _ = result['HTTPS'].append(profile) %}
              {% endif %}
            {% endfor %}
          {% endfor %}
          {{ result }}
      
    - name: Display protocol summary
      debug:
        var: protocol_summary
        
    - name: Find profiles with multiple servers
      set_fact:
        multi_server_profiles: "{{ profiles_info.http_server_profiles | selectattr('server', 'defined') | selectattr('server', 'length_is_greater_than', 1) | list }}"
        
    - name: Display profiles with multiple servers
      debug:
        msg: "Profiles with multiple servers: {{ multi_server_profiles | map(attribute='name') | list }}"
```

## Error Handling

It's important to handle potential errors when retrieving information about HTTP server profiles.

```yaml
- name: Get information about HTTP server profiles with error handling
  block:
    - name: Try to retrieve information about an HTTP server profile
      cdot65.scm.http_server_profiles_info:
        provider: "{{ provider }}"
        name: "test-http-profile"
        folder: "Texas"
      register: info_result
      
    - name: Display HTTP server profile information
      debug:
        var: info_result.http_server_profile
        
  rescue:
    - name: Handle errors
      debug:
        msg: "Failed to retrieve HTTP server profile information: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a 'not found' error
      debug:
        msg: "The specified HTTP server profile does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

## Best Practices

### Efficient Querying

- Use specific filters to reduce API load and improve performance
- When looking for a specific profile, use the `name` parameter instead of filtering results
- Use container parameters consistently across queries
- Filter by protocol or other attributes when you need to find profiles with specific
  characteristics

### Result Processing

- Always register the module output to a variable for later use
- Check if the expected data is present before processing it
- Use appropriate Ansible filters and tests when processing complex nested structures
- Create structured summaries when analyzing multiple profiles

### Filter Usage

- Use `exact_match` when you only want profiles defined directly in the specified container
- Use exclusion filters to refine results without overcomplicating queries
- Filter by protocol to find specific types of server configurations
- Combine multiple filters for precise results

### Information Analysis

- Group profiles by protocol for better organization
- Analyze server configurations to understand communication patterns
- Check for redundant or overlapping profiles
- Verify certificate profile usage for HTTPS server configurations

### Integration with Other Modules

- Use the info module to check for existing profiles before creating new ones
- Combine with the http_server_profiles module for complete profile management
- Use the retrieved information to make decisions in your playbooks
- Link profile information with log forwarding profile configurations

### Security Practices

- Regularly audit server profiles to ensure they're still needed
- Verify that addresses and ports are still valid and accessible
- Check HTTPS configurations for proper TLS versions and certificate profiles
- Document your HTTP server profile inventory and their purposes

## Related Modules

- [http_server_profiles](http_server_profiles.md) - Create, update, and delete HTTP server profiles
- [log_forwarding_profile_info](log_forwarding_profile_info.md) - Retrieve information about log
  forwarding profiles that may use HTTP server profiles
- [syslog_server_profiles_info](syslog_server_profiles_info.md) - Retrieve information about syslog
  server profiles
