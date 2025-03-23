# External Dynamic Lists Info Module

## Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [Query Parameters](#query-parameters)
4. [Exceptions](#exceptions)
5. [Basic Configuration](#basic-configuration)
6. [Usage Examples](#usage-examples)
   - [Retrieving a Specific EDL](#retrieving-a-specific-edl)
   - [Listing All EDLs](#listing-all-edls)
   - [Filtering by EDL Types](#filtering-by-edl-types)
   - [Advanced Filtering](#advanced-filtering)
   - [Combining Multiple Filters](#combining-multiple-filters)
7. [Response Structure](#response-structure)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The External Dynamic Lists Info module provides read-only functionality to retrieve information about External Dynamic Lists (EDLs) in Palo Alto Networks' Strata Cloud Manager. This module supports retrieving detailed information about specific EDLs by name or listing all EDLs with various filtering options. It complements the External Dynamic Lists module, which handles create, update, and delete operations.

## Core Methods

| Method     | Description                          | Parameters                                | Return Type                            |
|------------|--------------------------------------|-------------------------------------------|----------------------------------------|
| `fetch()`  | Retrieves a specific EDL by name     | `name: str`, `folder/snippet/device: str` | `ExternalDynamicListResponseModel`     |
| `list()`   | Lists EDLs with filtering            | `folder/snippet/device: str`, `**filters` | `List[ExternalDynamicListResponseModel]` |
| `get()`    | Retrieves a specific EDL by ID       | `object_id: str`                          | `ExternalDynamicListResponseModel`     |

## Query Parameters

| Parameter          | Type       | Description                                           | Default |
|-------------------|------------|-------------------------------------------------------|---------|
| `name`            | str        | Name of a specific EDL to retrieve                    | None    |
| `folder`          | str        | Filter EDLs by folder container                       | None    |
| `snippet`         | str        | Filter EDLs by snippet container                      | None    |
| `device`          | str        | Filter EDLs by device container                       | None    |
| `types`           | List[str]  | Filter by EDL types (ip, domain, url, imsi, imei)     | None    |
| `exact_match`     | bool       | Only return objects defined in the specified container| False   |
| `exclude_folders` | List[str]  | List of folder names to exclude from results          | None    |
| `exclude_snippets`| List[str]  | List of snippet values to exclude from results        | None    |
| `exclude_devices` | List[str]  | List of device values to exclude from results         | None    |
| `gather_subset`   | List[str]  | Determines which information to gather                | ["config"] |

## Exceptions

| Exception                    | HTTP Code | Description                     |
|------------------------------|-----------|-------------------------------- |
| `ObjectNotPresentError`      | 404       | EDL not found                   |
| `MissingQueryParameterError` | 400       | Missing required parameters     |
| `InvalidObjectError`         | 400       | Invalid filter parameters       |
| `AuthenticationError`        | 401       | Authentication failed           |
| `ServerError`                | 500       | Internal server error           |

## Basic Configuration

The External Dynamic Lists Info module can be used to gather information about EDLs without making any changes to your configuration.

<div class="termy">

<!-- termynal -->

```yaml
- name: Gather External Dynamic Lists Information
  cdot65.scm.external_dynamic_lists_info:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
    folder: "Texas"
  register: edl_info
```

</div>

## Usage Examples

### Retrieving a Specific EDL

<div class="termy">

<!-- termynal -->

```yaml
- name: Get information about a specific external dynamic list
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    name: "malicious-ips"
    folder: "Texas"
  register: edl_info

- name: Display EDL information
  debug:
    var: edl_info.external_dynamic_list
```

</div>

### Listing All EDLs

<div class="termy">

<!-- termynal -->

```yaml
- name: List all external dynamic lists in a folder
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_edls

- name: Display all EDLs
  debug:
    var: all_edls.external_dynamic_lists
    
- name: Count total number of EDLs
  debug:
    msg: "Found {{ all_edls.external_dynamic_lists | length }} external dynamic lists"
```

</div>

### Filtering by EDL Types

<div class="termy">

<!-- termynal -->

```yaml
- name: List only IP-based external dynamic lists
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    folder: "Texas"
    types: ["ip"]
  register: ip_edls

- name: Display IP-based EDLs
  debug:
    var: ip_edls.external_dynamic_lists
    
- name: List domain and URL-based external dynamic lists
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    folder: "Texas"
    types: ["domain", "url"]
  register: domain_url_edls
```

</div>

### Advanced Filtering

<div class="termy">

<!-- termynal -->

```yaml
- name: List EDLs with exact match (no inherited objects)
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
  register: exact_edls

- name: List EDLs excluding specific folders
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exclude_folders: ["All", "Shared"]
  register: filtered_edls
  
- name: List EDLs from a snippet excluding specific devices
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    snippet: "policy_snippet"
    exclude_devices: ["DeviceA", "DeviceB"]
  register: snippet_edls
```

</div>

### Combining Multiple Filters

<div class="termy">

<!-- termynal -->

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

- name: Process filtered results
  debug:
    msg: "Name: {{ item.name }}, Type: {{ item.type | to_json | from_json | dict2items | first | json_query('key') }}"
  loop: "{{ combined_filters.external_dynamic_lists }}"
  loop_control:
    label: "{{ item.name }}"
```

</div>

## Response Structure

The module returns information in two different formats depending on the query parameters:

### Single EDL Response (when name is specified)

<div class="termy">

<!-- termynal -->

```yaml
external_dynamic_list:
  id: "123e4567-e89b-12d3-a456-426655440000"
  name: "malicious-ips"
  type:
    ip:
      url: "https://threatfeeds.example.com/ips.txt"
      description: "Known malicious IPs"
      recurring:
        hourly: {}
      exception_list:
        - "192.168.1.100"
        - "10.0.0.1"
  folder: "Texas"
```

</div>

### Multiple EDLs Response (when name is not specified)

<div class="termy">

<!-- termynal -->

```yaml
external_dynamic_lists:
  - id: "123e4567-e89b-12d3-a456-426655440000"
    name: "malicious-ips"
    type:
      ip:
        url: "https://threatfeeds.example.com/ips.txt"
        description: "Known malicious IPs"
        recurring:
          hourly: {}
    folder: "Texas"
  - id: "234e5678-e89b-12d3-a456-426655440001"
    name: "blocked-domains"
    type:
      domain:
        url: "https://threatfeeds.example.com/domains.txt"
        description: "Blocked domains list"
        recurring:
          daily:
            at: "03"
        expand_domain: true
    folder: "Texas"
```

</div>

## Error Handling

<div class="termy">

<!-- termynal -->

```yaml
- name: Try to get information about a non-existent EDL
  cdot65.scm.external_dynamic_lists_info:
    provider: "{{ provider }}"
    name: "non-existent-edl"
    folder: "Texas"
  register: edl_info
  failed_when: false

- name: Display error if EDL not found
  debug:
    msg: "EDL not found: {{ edl_info.msg }}"
  when: edl_info.failed

- name: Handle EDL retrieval with proper error checking
  block:
    - name: Get EDL information
      cdot65.scm.external_dynamic_lists_info:
        provider: "{{ provider }}"
        name: "malicious-ips"
        folder: "Texas"
      register: edl_info
  rescue:
    - name: Handle EDL not found
      debug:
        msg: "EDL not found or another error occurred: {{ ansible_failed_result.msg }}"
    - name: Take remedial action
      # Additional tasks for error handling
```

</div>

## Best Practices

1. **Container Specification**
   - Always specify exactly one container (folder, snippet, or device)
   - Use consistent container names across operations
   - Favor folder-based filtering when possible

2. **Efficient Filtering**
   - Use specific filters to limit result sets
   - Prefer `exact_match: true` when only looking for objects defined directly in a container
   - Combine `types` filter with container filters for faster queries
   - Use `exclude_folders` to filter out shared or common folders

3. **Performance**
   - When querying large environments, use specific filtering
   - Avoid multiple queries by retrieving all needed data in a single query
   - Cache query results when executing multiple operations against the same dataset

4. **Error Handling**
   - Always handle potential errors, especially `ObjectNotPresentError`
   - Use descriptive error messages when handling failures
   - Implement retry logic for transient errors

5. **Integration with Other Modules**
   - Use `register` to store results for use with other tasks
   - Combine with `external_dynamic_lists` module for full lifecycle management
   - Use jinja2 filters to process and transform result data

## Related Modules

- [external_dynamic_lists](external_dynamic_lists.md) - Create, update, and delete External Dynamic Lists
- [address](address.md) - Manage address objects that may be used in security policies with EDLs
- [security_rule](security_rule.md) - Configure security rules that utilize External Dynamic Lists