# External Dynamic Lists Info Module

## Overview

The External Dynamic Lists Info module (`cdot65.scm.external_dynamic_lists_info`) provides a read-only interface to
retrieve information about external dynamic lists (EDLs) in Palo Alto Networks' Strata Cloud Manager. This module allows
you to retrieve detailed information about specific EDLs by name or list all EDLs with various filtering options.

## Module Parameters

| Parameter          | Type    | Required      | Default    | Choices                                                    | Description                                                 |
|--------------------|---------|---------------|------------|------------------------------------------------------------|-------------------------------------------------------------|
| `name`             | string  | No            |            |                                                            | Name of a specific EDL to retrieve                          |
| `gather_subset`    | list    | No            | ['config'] | all, config                                                | Determines which information to gather                      |
| `folder`           | string  | One Required* |            |                                                            | Filter EDLs by folder container                             |
| `snippet`          | string  | One Required* |            |                                                            | Filter EDLs by snippet container                            |
| `device`           | string  | One Required* |            |                                                            | Filter EDLs by device container                             |
| `exact_match`      | boolean | No            | False      |                                                            | When True, only return objects defined exactly in container |
| `exclude_folders`  | list    | No            |            |                                                            | List of folder names to exclude from results                |
| `exclude_snippets` | list    | No            |            |                                                            | List of snippet values to exclude from results              |
| `exclude_devices`  | list    | No            |            |                                                            | List of device values to exclude from results               |
| `types`            | list    | No            |            | ip, domain, url, imsi, imei, predefined_ip, predefined_url | Filter by EDL types                                         |
| `provider`         | dict    | Yes           |            |                                                            | Authentication credentials                                  |

*Note: A container parameter (`folder`, `snippet`, or `device`) is required when `name` is not specified.

### Provider Dictionary

| Parameter       | Type   | Required | Default | Description                      |
|-----------------|--------|----------|---------|----------------------------------|
| `client_id`     | string | Yes      |         | Client ID for authentication     |
| `client_secret` | string | Yes      |         | Client secret for authentication |
| `tsg_id`        | string | Yes      |         | Tenant Service Group ID          |
| `log_level`     | string | No       | "INFO"  | Log level for the SDK            |

## Examples

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

### Listing All EDLs in a Folder

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

### Using Advanced Filtering Options

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

## Return Values

### When Requesting a Specific EDL by Name

<div class="termy">

<!-- termynal -->

```yaml
external_dynamic_list:
    description: Information about the requested external dynamic list.
    returned: success, when name is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "malicious-ips"
        type:
          ip:
            url: "https://threatfeeds.example.com/ips.txt"
            description: "Known malicious IPs"
            recurring:
              hourly: {}
        folder: "Texas"
```

</div>

### When Listing Multiple EDLs

<div class="termy">

<!-- termynal -->

```yaml
external_dynamic_lists:
    description: List of external dynamic list objects matching the filter criteria.
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
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

## Complete Playbook Example

This example demonstrates comprehensive use of the EDL info module to retrieve and filter results:

<div class="termy">

<!-- termynal -->

```yaml
---
# Playbook for retrieving External Dynamic Lists information in SCM
- name: Gather External Dynamic Lists Information in SCM
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:
    # Get information about a specific EDL
    - name: Get information about a specific external dynamic list
      cdot65.scm.external_dynamic_lists_info:
        provider: "{{ provider }}"
        name: "malicious-ips"
        folder: "Texas"
      register: edl_info
      ignore_errors: true
      
    - name: Display EDL details if found
      debug:
        var: edl_info.external_dynamic_list
      when: not edl_info.failed
        
    # List all EDLs in the folder
    - name: List all external dynamic lists in the folder
      cdot65.scm.external_dynamic_lists_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_edls
      
    - name: Count total EDLs
      debug:
        msg: "Found {{ all_edls.external_dynamic_lists | length }} external dynamic lists"
        
    # Filter by EDL type
    - name: Get only IP-based EDLs
      cdot65.scm.external_dynamic_lists_info:
        provider: "{{ provider }}"
        folder: "Texas"
        types: ["ip"]
      register: ip_edls
      
    - name: Create summary list of IP-based EDLs
      set_fact:
        ip_edl_names: "{{ ip_edls.external_dynamic_lists | map(attribute='name') | list }}"
        
    - name: Display IP EDL names
      debug:
        var: ip_edl_names
        
    # Advanced filtering example
    - name: Filter EDLs with multiple criteria
      cdot65.scm.external_dynamic_lists_info:
        provider: "{{ provider }}"
        folder: "Texas"
        exact_match: true
        exclude_folders: ["All"]
      register: filtered_edls
      
    - name: Create an inventory of all EDLs
      copy:
        content: "{{ filtered_edls | to_nice_yaml }}"
        dest: "./edl_inventory.yml"
```

</div>

## Error Handling

When the module fails to retrieve information (for example, when a specified EDL doesn't exist), an error will be
returned. You can handle these errors using Ansible's standard error handling mechanisms:

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
```

</div>

## Notes and Limitations

### Container Parameters

- When retrieving a specific EDL by name, you must also specify exactly one container parameter (`folder`, `snippet`, or
  `device`)
- When listing EDLs without a name, at least one container parameter is required to scope the query

### Filtering Behavior

- The `exact_match` parameter only returns objects defined directly in the specified container, excluding inherited
  objects
- Exclusion filters (`exclude_folders`, `exclude_snippets`, `exclude_devices`) are applied after the initial query
- Type filtering with `types` parameter is case-sensitive - use lowercase types as shown in the choices

### Performance Considerations

- For large environments, consider using specific filtering to reduce the result set size
- When retrieving only specific EDL types or from specific containers, add these filters to improve query performance

## Related Information

- [External Dynamic Lists module](external_dynamic_lists.md) - For creating, updating, and deleting external dynamic
  lists
- [Security Rule module](security_rule.md) - For configuring security rules that utilize external dynamic lists