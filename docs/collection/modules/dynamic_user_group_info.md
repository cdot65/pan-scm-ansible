# Dynamic User Group Information Object

## Overview

The Dynamic User Group Info module (`cdot65.scm.dynamic_user_group_info`) provides a read-only
interface to retrieve information about dynamic user groups in Palo Alto Networks' Strata Cloud
Manager. This module allows you to retrieve detailed information about specific dynamic user groups
by name or list all dynamic user groups with various filtering options.

## Module Parameters

| Parameter          | Type    | Required | Default    | Choices     | Description                                                 |
| ------------------ | ------- | -------- | ---------- | ----------- | ----------------------------------------------------------- |
| `name`             | string  | No       |            |             | Name of a specific dynamic user group to retrieve           |
| `gather_subset`    | list    | No       | ['config'] | all, config | Determines which information to gather                      |
| `folder`           | string  | No\*     |            |             | Filter dynamic user groups by folder container              |
| `snippet`          | string  | No\*     |            |             | Filter dynamic user groups by snippet container             |
| `device`           | string  | No\*     |            |             | Filter dynamic user groups by device container              |
| `exact_match`      | boolean | No       | False      |             | When True, only return objects defined exactly in container |
| `exclude_folders`  | list    | No       |            |             | List of folder names to exclude from results                |
| `exclude_snippets` | list    | No       |            |             | List of snippet values to exclude from results              |
| `exclude_devices`  | list    | No       |            |             | List of device values to exclude from results               |
| `filters`          | list    | No       |            |             | Filter by filter expressions                                |
| `tags`             | list    | No       |            |             | Filter by tags                                              |
| `provider`         | dict    | Yes      |            |             | Authentication credentials                                  |

\*Note: When `name` is not specified, exactly one of `folder`, `snippet`, or `device` is required.

### Provider Dictionary

| Parameter       | Type   | Required | Default | Choices                               | Description                      |
| --------------- | ------ | -------- | ------- | ------------------------------------- | -------------------------------- |
| `client_id`     | string | Yes      |         |                                       | Client ID for authentication     |
| `client_secret` | string | Yes      |         |                                       | Client secret for authentication |
| `tsg_id`        | string | Yes      |         |                                       | Tenant Service Group ID          |
| `log_level`     | string | No       | "INFO"  | DEBUG, INFO, WARNING, ERROR, CRITICAL | Log level for the SDK            |

## Examples

### Retrieving a Specific Dynamic User Group



```yaml
- name: Get information about a specific dynamic user group
  cdot65.scm.dynamic_user_group_info:
    provider: "{{ provider }}"
    name: "high_risk_users"
    folder: "Security"
  register: dug_info

- name: Display dynamic user group information
  debug:
    var: dug_info.dynamic_user_group
```


### Listing All Dynamic User Groups in a Folder



```yaml
- name: List all dynamic user group objects in a folder
  cdot65.scm.dynamic_user_group_info:
    provider: "{{ provider }}"
    folder: "Security"
  register: all_dugs

- name: Display all dynamic user groups
  debug:
    var: all_dugs.dynamic_user_groups
    
- name: Count total number of dynamic user groups
  debug:
    msg: "Found {{ all_dugs.dynamic_user_groups | length }} dynamic user groups"
```


### Filtering by Tags



```yaml
- name: List dynamic user groups with specific tags
  cdot65.scm.dynamic_user_group_info:
    provider: "{{ provider }}"
    folder: "Security"
    tags: ["RiskManagement", "Security"]
  register: tagged_dugs

- name: Display tag-filtered dynamic user groups
  debug:
    var: tagged_dugs.dynamic_user_groups
```


### Filtering by Filter Expressions



```yaml
- name: List dynamic user groups with specific filter expressions
  cdot65.scm.dynamic_user_group_info:
    provider: "{{ provider }}"
    folder: "Security"
    filters: ["tag.criticality.high"]
  register: filtered_dugs

- name: Display filtered dynamic user groups
  debug:
    var: filtered_dugs.dynamic_user_groups
```


### Using Advanced Filtering Options



```yaml
- name: List dynamic user groups with exact match (no inherited objects)
  cdot65.scm.dynamic_user_group_info:
    provider: "{{ provider }}"
    folder: "Security"
    exact_match: true
  register: exact_dugs

- name: List dynamic user groups excluding specific folders
  cdot65.scm.dynamic_user_group_info:
    provider: "{{ provider }}"
    folder: "Security"
    exclude_folders: ["All", "Shared"]
  register: filtered_dugs
```


## Return Values

### When Requesting a Specific Dynamic User Group by Name



```yaml
dynamic_user_group:
    description: Information about the requested dynamic user group.
    returned: success, when name is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "high_risk_users"
        description: "Users with high risk classification"
        filter: "tag.criticality.high"
        folder: "Security"
        tag: ["RiskManagement", "Security"]
```


### When Listing Multiple Dynamic User Groups



```yaml
dynamic_user_groups:
    description: List of dynamic user group objects matching the filter criteria.
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "high_risk_users"
        description: "Users with high risk classification"
        filter: "tag.criticality.high"
        folder: "Security"
        tag: ["RiskManagement", "Security"]
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "risky_contractors"
        description: "High risk contractors"
        filter: "tag.user_type.contractor and (tag.criticality.high or tag.risk_score.gt.80)"
        folder: "Security"
        tag: ["RiskManagement", "Contractors"]
```


## Complete Playbook Example

This example demonstrates comprehensive use of the Dynamic User Group info module to retrieve and
filter results:



```yaml
---
# Playbook for retrieving Dynamic User Group information in SCM
- name: Gather Dynamic User Group Information in SCM
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
    # Get information about a specific dynamic user group
    - name: Get information about a specific dynamic user group
      cdot65.scm.dynamic_user_group_info:
        provider: "{{ provider }}"
        name: "high_risk_users"
        folder: "Security"
      register: dug_info
      ignore_errors: true
      
    - name: Display dynamic user group details if found
      debug:
        var: dug_info.dynamic_user_group
      when: not dug_info.failed
        
    # List all dynamic user groups in the folder
    - name: List all dynamic user groups in the folder
      cdot65.scm.dynamic_user_group_info:
        provider: "{{ provider }}"
        folder: "Security"
      register: all_dugs
      
    # Filter by tags
    - name: Get dynamic user groups with specific tags
      cdot65.scm.dynamic_user_group_info:
        provider: "{{ provider }}"
        folder: "Security"
        tags: ["RiskManagement"]
      register: tagged_dugs
      
    - name: Create summary list of tagged dynamic user groups
      set_fact:
        tagged_dug_names: "{{ tagged_dugs.dynamic_user_groups | map(attribute='name') | list }}"
        
    - name: Display tag-filtered dynamic user group names
      debug:
        var: tagged_dug_names
        
    # Filter by expressions
    - name: Filter dynamic user groups with filter expression criteria
      cdot65.scm.dynamic_user_group_info:
        provider: "{{ provider }}"
        folder: "Security"
        filters: ["tag.criticality.high"]
      register: filtered_dugs
      
    - name: Create an inventory of all dynamic user groups
      copy:
        content: "{{ all_dugs | to_nice_yaml }}"
        dest: "./dug_inventory.yml"
```


## Error Handling

When the module fails to retrieve information (for example, when a specified dynamic user group
doesn't exist), an error will be returned. You can handle these errors using Ansible's standard
error handling mechanisms:



```yaml
- name: Try to get information about a non-existent dynamic user group
  cdot65.scm.dynamic_user_group_info:
    provider: "{{ provider }}"
    name: "non-existent-dug"
    folder: "Security"
  register: dug_info
  failed_when: false

- name: Display error if dynamic user group not found
  debug:
    msg: "Dynamic user group not found: {{ dug_info.msg }}"
  when: dug_info.failed

- name: Handle dynamic user group retrieval with proper error checking
  block:
    - name: Get dynamic user group information
      cdot65.scm.dynamic_user_group_info:
        provider: "{{ provider }}"
        name: "high_risk_users"
        folder: "Security"
      register: dug_info
  rescue:
    - name: Handle dynamic user group not found
      debug:
        msg: "Dynamic user group not found or another error occurred: {{ ansible_failed_result.msg }}"
```


## Notes and Limitations

### Container Parameters

- When retrieving a specific dynamic user group by name, you must also specify exactly one container
  parameter (`folder`, `snippet`, or `device`)
- When listing dynamic user groups without a name, at least one container parameter is required to
  scope the query

### Filtering Behavior

- The `exact_match` parameter only returns objects defined directly in the specified container,
  excluding inherited objects
- Exclusion filters (`exclude_folders`, `exclude_snippets`, `exclude_devices`) are applied after the
  initial query
- The `filters` parameter is used to filter dynamic user groups by their filter expressions
- The `tags` parameter is used to filter dynamic user groups by assigned tags

### Performance Considerations

- For large environments, consider using specific filtering to reduce the result set size
- When retrieving only specific dynamic user groups based on tags or filter expressions, add these
  filters to improve query performance

## Related Information

- [Dynamic User Group module](dynamic_user_group.md) - For creating, updating, and deleting dynamic
  user groups
- [Security Rule module](security_rule.md) - For configuring security rules that utilize dynamic
  user groups
