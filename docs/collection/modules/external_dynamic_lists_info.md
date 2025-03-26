# External Dynamic Lists Information Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [External Dynamic List Info Model Attributes](#external-dynamic-list-info-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Getting Information about a Specific External Dynamic List](#getting-information-about-a-specific-external-dynamic-list)
    - [Listing All External Dynamic Lists in a Folder](#listing-all-external-dynamic-lists-in-a-folder)
    - [Filtering by EDL Types](#filtering-by-edl-types)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
    - [Combining Multiple Filters](#combining-multiple-filters)
07. [Processing Retrieved Information](#processing-retrieved-information)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `external_dynamic_lists_info` Ansible module provides functionality to gather information about
External Dynamic List (EDL) objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is an
info module that allows fetching details about specific EDLs or listing EDLs with various filtering
options, including by type (IP, domain, URL, IMSI, IMEI).

## Core Methods

| Method    | Description                 | Parameters                    | Return Type                              |
| --------- | --------------------------- | ----------------------------- | ---------------------------------------- |
| `fetch()` | Gets a specific EDL by name | `name: str`, `container: str` | `ExternalDynamicListResponseModel`       |
| `list()`  | Lists EDLs with filtering   | `folder: str`, `**filters`    | `List[ExternalDynamicListResponseModel]` |

## External Dynamic List Info Model Attributes

| Parameter          | Type | Required | Description                                                 |
| ------------------ | ---- | -------- | ----------------------------------------------------------- |
| `name`             | str  | No       | Name of a specific EDL to retrieve                          |
| `gather_subset`    | list | No       | Determines which information to gather (default: config)    |
| `folder`           | str  | No\*     | Filter EDLs by folder container                             |
| `snippet`          | str  | No\*     | Filter EDLs by snippet container                            |
| `device`           | str  | No\*     | Filter EDLs by device container                             |
| `exact_match`      | bool | No       | When True, only return objects defined exactly in container |
| `exclude_folders`  | list | No       | List of folder names to exclude from results                |
| `exclude_snippets` | list | No       | List of snippet values to exclude from results              |
| `exclude_devices`  | list | No       | List of device values to exclude from results               |
| `types`            | list | No       | Filter by EDL types (ip, domain, url, imsi, imei, etc.)     |

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
| `ObjectNotPresentError`      | EDL not found                  |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The External Dynamic Lists Info module requires proper authentication credentials to access the
Strata Cloud Manager API.

```yaml
- name: Basic External Dynamic Lists Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about external dynamic lists
      cdot65.scm.external_dynamic_lists_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: edls_result
      
    - name: Display retrieved external dynamic lists
      debug:
        var: edls_result
```

## Usage Examples

### Getting Information about a Specific External Dynamic List

Retrieve details about a specific external dynamic list by name and container.

```yaml
- name: Get information about a specific external dynamic list
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    name: "malicious-ips"
    folder: "Texas"
  register: edl_info
  
- name: Display external dynamic list information
  debug:
    var: edl_info.external_dynamic_list
    
- name: Check EDL type and URL
  debug:
    msg: "EDL type: {{ edl_info.external_dynamic_list.type | dict2items | first | json_query('key') }}, URL: {{ edl_info.external_dynamic_list.type[edl_info.external_dynamic_list.type | dict2items | first | json_query('key')].url }}"
```

### Listing All External Dynamic Lists in a Folder

List all external dynamic lists in a specific folder.

```yaml
- name: List all external dynamic lists in a folder
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_edls
  
- name: Display all external dynamic lists
  debug:
    var: all_edls.external_dynamic_lists
    
- name: Display count of external dynamic lists
  debug:
    msg: "Found {{ all_edls.external_dynamic_lists | length }} external dynamic lists"
    
- name: List names of all external dynamic lists
  debug:
    msg: "{{ all_edls.external_dynamic_lists | map(attribute='name') | list }}"
```

### Filtering by EDL Types

Filter external dynamic lists by their types.

```yaml
- name: List only IP-based external dynamic lists
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    folder: "Texas"
    types: ["ip"]
  register: ip_edls
  
- name: Process type filtered external dynamic lists
  debug:
    msg: "IP-based EDL: {{ item.name }}"
  loop: "{{ ip_edls.external_dynamic_lists }}"

- name: List domain and URL-based external dynamic lists
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    folder: "Texas"
    types: ["domain", "url"]
  register: domain_url_edls
```

### Using Advanced Filtering Options

Use advanced filtering options to refine your query results.

```yaml
- name: List external dynamic lists with exact match parameter
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
  register: exact_match_edls

- name: List external dynamic lists excluding specific folders
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exclude_folders: ["All", "Shared"]
  register: filtered_edls
```

### Combining Multiple Filters

Combine multiple filtering options for precise queries.

```yaml
- name: List external dynamic lists with combined filtering
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    types: ["ip", "domain"]
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: combined_filters

- name: Process combined filter results
  debug:
    msg: "Name: {{ item.name }}, Type: {{ item.type | dict2items | first | json_query('key') }}"
  loop: "{{ combined_filters.external_dynamic_lists }}"
  loop_control:
    label: "{{ item.name }}"
```

## Processing Retrieved Information

Example of processing and utilizing the retrieved external dynamic list information.

```yaml
- name: Analyze external dynamic list information
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:
    - name: Get all external dynamic lists
      cdot65.scm.external_dynamic_lists_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: edls_info
      
    - name: Group EDLs by type
      set_fact:
        edl_types: "{{ edl_types | default({}) | combine({item: types_list[item] | map(attribute='name') | list}) }}"
      loop: "{{ types_list.keys() | list }}"
      vars:
        all_edls: "{{ edls_info.external_dynamic_lists | default([]) }}"
        types_list: >-
          {% set result = {'ip': [], 'domain': [], 'url': [], 'imsi': [], 'imei': []} %}
          {% for edl in all_edls %}
            {% set edl_type = edl.type | dict2items | first | json_query('key') %}
            {% if edl_type in result %}
              {% set _ = result[edl_type].append(edl) %}
            {% endif %}
          {% endfor %}
          {{ result }}
      
    - name: Display EDLs grouped by type
      debug:
        var: edl_types
        
    - name: Find EDLs with five-minute update interval
      set_fact:
        frequent_edls: "{{ edls_info.external_dynamic_lists | selectattr('type.' + (item.type | dict2items | first | json_query('key')) + '.recurring.five_minute', 'defined') | list }}"
      with_items: "{{ edls_info.external_dynamic_lists }}"
        
    - name: Display EDLs with frequent updates
      debug:
        msg: "EDLs with five-minute updates: {{ frequent_edls | map(attribute='name') | list }}"
```

## Error Handling

It's important to handle potential errors when retrieving information about external dynamic lists.

```yaml
- name: Get information about external dynamic lists with error handling
  block:
    - name: Try to retrieve information about an external dynamic list
      cdot65.scm.external_dynamic_lists_info:
        provider: "{{ provider }}"
        name: "malicious-ips"
        folder: "Texas"
      register: info_result
      
    - name: Display external dynamic list information
      debug:
        var: info_result.external_dynamic_list
        
  rescue:
    - name: Handle errors
      debug:
        msg: "Failed to retrieve external dynamic list information: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a 'not found' error
      debug:
        msg: "The specified external dynamic list does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

## Best Practices

### Efficient Querying

- Use specific filters to reduce API load and improve performance
- When looking for a specific EDL, use the `name` parameter instead of filtering results
- Use container parameters consistently across queries
- Filter by EDL types when you need to find EDLs of specific varieties

### Result Processing

- Always register the module output to a variable for later use
- Check if the expected data is present before processing it
- Use appropriate Ansible filters and tests when processing complex nested structures
- Use `dict2items` and `json_query` to extract EDL type information effectively

### Filter Usage

- Use `exact_match` when you only want EDLs defined directly in the specified container
- Use exclusion filters to refine results without overcomplicating queries
- Filter by EDL types to find specific types of lists
- Combine multiple filters for precise results

### Information Analysis

- Group EDLs by type for better organization
- Analyze update intervals to understand refresh patterns
- Check URL sources to verify list provenance
- Look for exceptions to understand what's being excluded

### Security Considerations

- Regularly audit EDLs to ensure they're still needed
- Verify that EDL sources are still valid and secure
- Check for duplicate or overlapping EDLs that may cause confusion
- Understand how EDLs are being used in security policies

### Integration with Other Modules

- Use the info module to check for existing EDLs before creating new ones
- Combine with the external_dynamic_lists module for complete EDL management
- Use the retrieved information to make decisions in your playbooks
- Integrate with security rule modules to verify EDL utilization

## Related Modules

- [external_dynamic_lists](external_dynamic_lists.md) - Create, update, and delete external dynamic
  lists
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules that use
  external dynamic lists
- [security_profiles_group_info](security_profiles_group_info.md) - Retrieve information about
  security profile groups
- [tag_info](tag_info.md) - Retrieve information about tags that might be used to organize external
  dynamic lists
