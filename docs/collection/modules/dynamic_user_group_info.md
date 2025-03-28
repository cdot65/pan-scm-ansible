# Dynamic User Group Information Object

## Table of Contents

- [Dynamic User Group Information Object](#dynamic-user-group-information-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [Dynamic User Group Info Model Attributes](#dynamic-user-group-info-model-attributes)
    - [Provider Dictionary Attributes](#provider-dictionary-attributes)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Getting Information about a Specific Dynamic User Group](#getting-information-about-a-specific-dynamic-user-group)
    - [Listing All Dynamic User Groups in a Folder](#listing-all-dynamic-user-groups-in-a-folder)
    - [Filtering by Tags](#filtering-by-tags)
    - [Filtering by Filter Expressions](#filtering-by-filter-expressions)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
  - [Processing Retrieved Information](#processing-retrieved-information)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Efficient Querying](#efficient-querying)
    - [Result Processing](#result-processing)
    - [Filter Usage](#filter-usage)
    - [Security Considerations](#security-considerations)
    - [Performance Management](#performance-management)
    - [Integration with Other Modules](#integration-with-other-modules)
  - [Related Modules](#related-modules)

## Overview

The `dynamic_user_group_info` Ansible module provides functionality to gather information about
Dynamic User Group objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is an info module
that allows fetching details about specific dynamic user groups or listing groups with various
filtering options, including by tags and filter expressions.

## Core Methods

| Method    | Description                                | Parameters                    | Return Type                           |
| --------- | ------------------------------------------ | ----------------------------- | ------------------------------------- |
| `fetch()` | Gets a specific dynamic user group by name | `name: str`, `container: str` | `DynamicUserGroupResponseModel`       |
| `list()`  | Lists dynamic user groups with filtering   | `folder: str`, `**filters`    | `List[DynamicUserGroupResponseModel]` |

## Dynamic User Group Info Model Attributes

| Parameter          | Type | Required | Description                                                 |
| ------------------ | ---- | -------- | ----------------------------------------------------------- |
| `name`             | str  | No       | Name of a specific dynamic user group to retrieve           |
| `gather_subset`    | list | No       | Determines which information to gather (default: config)    |
| `folder`           | str  | No\*     | Filter dynamic user groups by folder container              |
| `snippet`          | str  | No\*     | Filter dynamic user groups by snippet container             |
| `device`           | str  | No\*     | Filter dynamic user groups by device container              |
| `exact_match`      | bool | No       | When True, only return objects defined exactly in container |
| `exclude_folders`  | list | No       | List of folder names to exclude from results                |
| `exclude_snippets` | list | No       | List of snippet values to exclude from results              |
| `exclude_devices`  | list | No       | List of device values to exclude from results               |
| `filters`          | list | No       | Filter by filter expressions                                |
| `tags`             | list | No       | Filter by tags                                              |

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
| `ObjectNotPresentError`      | Dynamic user group not found   |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The Dynamic User Group Info module requires proper authentication credentials to access the Strata
Cloud Manager API.

```yaml
- name: Basic Dynamic User Group Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about dynamic user groups
      cdot65.scm.dynamic_user_group_info:
        provider: "{{ provider }}"
        folder: "Security"
      register: groups_result

    - name: Display retrieved dynamic user groups
      debug:
        var: groups_result
```

## Usage Examples

### Getting Information about a Specific Dynamic User Group

Retrieve details about a specific dynamic user group by name and container.

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

- name: Check filter expression
  debug:
    msg: "Dynamic user group uses filter: {{ dug_info.dynamic_user_group.filter }}"
```

### Listing All Dynamic User Groups in a Folder

List all dynamic user groups in a specific folder.

```yaml
- name: List all dynamic user groups in a folder
  cdot65.scm.dynamic_user_group_info:
    provider: "{{ provider }}"
    folder: "Security"
  register: all_dugs

- name: Display all dynamic user groups
  debug:
    var: all_dugs.dynamic_user_groups

- name: Display count of dynamic user groups
  debug:
    msg: "Found {{ all_dugs.dynamic_user_groups | length }} dynamic user groups"

- name: List names of all dynamic user groups
  debug:
    msg: "{{ all_dugs.dynamic_user_groups | map(attribute='name') | list }}"
```

### Filtering by Tags

Filter dynamic user groups by assigned tags.

```yaml
- name: List dynamic user groups with specific tags
  cdot65.scm.dynamic_user_group_info:
    provider: "{{ provider }}"
    folder: "Security"
    tags: [ "RiskManagement", "Security" ]
  register: tagged_dugs

- name: Process tag filtered dynamic user groups
  debug:
    msg: "Tag filtered group: {{ item.name }}"
  loop: "{{ tagged_dugs.dynamic_user_groups }}"
```

### Filtering by Filter Expressions

Filter dynamic user groups by their filter expressions.

```yaml
- name: List dynamic user groups with specific filter expressions
  cdot65.scm.dynamic_user_group_info:
    provider: "{{ provider }}"
    folder: "Security"
    filters: [ "tag.criticality.high" ]
  register: filtered_dugs

- name: Process filter expression filtered dynamic user groups
  debug:
    msg: "Filter expression filtered group: {{ item.name }}"
  loop: "{{ filtered_dugs.dynamic_user_groups }}"
```

### Using Advanced Filtering Options

Use advanced filtering options to refine your query results.

```yaml
- name: List dynamic user groups with exact match parameter
  cdot65.scm.dynamic_user_group_info:
    provider: "{{ provider }}"
    folder: "Security"
    exact_match: true
  register: exact_match_dugs

- name: List dynamic user groups with exact match and exclusions
  cdot65.scm.dynamic_user_group_info:
    provider: "{{ provider }}"
    folder: "Security"
    exact_match: true
    exclude_folders: [ "All" ]
    exclude_snippets: [ "default" ]
  register: filtered_dugs
```

## Processing Retrieved Information

Example of processing and utilizing the retrieved dynamic user group information.

```yaml
- name: Analyze dynamic user group information
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:
    - name: Get all dynamic user groups
      cdot65.scm.dynamic_user_group_info:
        provider: "{{ provider }}"
        folder: "Security"
      register: dugs_info

    - name: Create summary of filter expressions used
      set_fact:
        filter_summary: >-
          {{ filter_summary | default({}) | combine({item.0: (item.1 | map(attribute='name') | list)}) }}
      loop: "{{ filter_list | default([]) }}"
      vars:
        all_dugs: "{{ dugs_info.dynamic_user_groups | default([]) }}"
        all_filters: "{{ all_dugs | map(attribute='filter') | list | unique }}"
        filter_list: >-
          {% set result = [] %}
          {% for filter in all_filters %}
            {% set dugs_with_filter = all_dugs | selectattr('filter', 'defined') | 
               selectattr('filter', 'equalto', filter) | list %}
            {% if dugs_with_filter %}
              {% set _ = result.append([filter, dugs_with_filter]) %}
            {% endif %}
          {% endfor %}
          {{ result }}

    - name: Display filter expression summary
      debug:
        var: filter_summary

    - name: Find dynamic user groups with empty tags
      set_fact:
        untagged_dugs: "{{ dugs_info.dynamic_user_groups | selectattr('tag', 'undefined') | list + 
                         dugs_info.dynamic_user_groups | selectattr('tag', 'defined') | 
                         selectattr('tag', 'equalto', []) | list }}"

    - name: Display dynamic user groups with no tags
      debug:
        msg: "Dynamic user groups with no tags: {{ untagged_dugs | map(attribute='name') | list }}"
```

## Error Handling

It's important to handle potential errors when retrieving information about dynamic user groups.

```yaml
- name: Get information about dynamic user groups with error handling
  block:
    - name: Try to retrieve information about a dynamic user group
      cdot65.scm.dynamic_user_group_info:
        provider: "{{ provider }}"
        name: "high_risk_users"
        folder: "Security"
      register: info_result

    - name: Display dynamic user group information
      debug:
        var: info_result.dynamic_user_group

  rescue:
    - name: Handle errors
      debug:
        msg: "Failed to retrieve dynamic user group information: {{ ansible_failed_result.msg }}"

    - name: Check if it's a 'not found' error
      debug:
        msg: "The specified dynamic user group does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

## Best Practices

### Efficient Querying

- Use specific filters to reduce API load and improve performance
- When looking for a specific dynamic user group, use the `name` parameter instead of filtering
  results
- Use container parameters consistently across queries
- Filter by tags or filter expressions when you need to find groups with specific characteristics

### Result Processing

- Always register the module output to a variable for later use
- Check if the expected data is present before processing it
- Use appropriate Ansible filters and tests when processing complex nested structures
- Create structured summaries when analyzing multiple dynamic user groups

### Filter Usage

- Use `exact_match` when you only want dynamic user groups defined directly in the specified
  container
- Use exclusion filters to refine results without overcomplicating queries
- Filter by tags to find dynamic user groups within specific categories
- Filter by filter expressions to find dynamic user groups with similar membership criteria

### Security Considerations

- Analyze dynamic user group filter expressions to understand effective security policies
- Check for overlapping or redundant dynamic user groups
- Identify unused or deprecated dynamic user groups
- Verify consistent naming conventions and tagging across dynamic user groups

### Performance Management

- Limit the number of dynamic user groups to only what's necessary
- Monitor the performance impact of complex filter expressions
- Be aware of dynamic user group dependencies in security policies
- Consider caching results when making multiple queries for the same information

### Integration with Other Modules

- Use the info module to check for existing dynamic user groups before creating new ones
- Combine with the dynamic_user_group module for complete group management
- Use the retrieved information to make decisions in your playbooks
- Integrate with security rule modules to verify dynamic user group utilization

## Related Modules

- [dynamic_user_group](dynamic_user_group.md) - Create, update, and delete dynamic user groups
- [tag_info](tag_info.md) - Retrieve information about tags that can be used in dynamic user group
  filters
- [tag](tag.md) - Create, update, and delete tags
- [security_rule](security_rule.md) - Configure security policies that use dynamic user groups
