# Application Group Information Object

## Table of Contents

- [Application Group Information Object](#application-group-information-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [Application Group Info Model Attributes](#application-group-info-model-attributes)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Retrieving Application Group Information](#retrieving-application-group-information)
    - [Getting a Specific Application Group](#getting-a-specific-application-group)
    - [Listing All Application Groups](#listing-all-application-groups)
    - [Analyzing Application Group Membership](#analyzing-application-group-membership)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
  - [Processing Retrieved Information](#processing-retrieved-information)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Efficient Filtering](#efficient-filtering)
    - [Container Selection](#container-selection)
    - [Information Handling](#information-handling)
    - [Security Analysis](#security-analysis)
    - [Integration with Security Policies](#integration-with-security-policies)
  - [Related Modules](#related-modules)

## Overview

The `application_group_info` Ansible module provides functionality to retrieve information about
application group objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is a read-only
module that can retrieve detailed information about a specific application group by name, or list
multiple application groups with various filtering options. It supports advanced filtering
capabilities including container-based filtering and exclusion filters.

## Core Methods

| Method     | Description                             | Parameters                            | Return Type                           |
| ---------- | --------------------------------------- | ------------------------------------- | ------------------------------------- |
| `get()`    | Gets a specific application group       | `name: str`, `container: str`         | `ApplicationGroupResponseModel`       |
| `list()`   | Lists application groups with filtering | `folder: str`, `**filters`            | `List[ApplicationGroupResponseModel]` |
| `filter()` | Applies filters to the results          | `groups: List`, `filter_params: Dict` | `List[ApplicationGroupResponseModel]` |

## Application Group Info Model Attributes

| Attribute          | Type | Required      | Description                                                  |
| ------------------ | ---- | ------------- | ------------------------------------------------------------ |
| `name`             | str  | No            | The name of a specific application group to retrieve         |
| `gather_subset`    | list | No            | Determines which information to gather (default: ['config']) |
| `folder`           | str  | One container | Filter application groups by folder (max 64 chars)           |
| `snippet`          | str  | One container | Filter application groups by snippet (max 64 chars)          |
| `device`           | str  | One container | Filter application groups by device (max 64 chars)           |
| `exact_match`      | bool | No            | When True, only return objects in the specified container    |
| `exclude_folders`  | list | No            | List of folder names to exclude from results                 |
| `exclude_snippets` | list | No            | List of snippet values to exclude from results               |

## Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `ObjectNotPresentError`      | Application group not found    |
| `MissingQueryParameterError` | Missing required parameters    |
| `InvalidFilterError`         | Invalid filter parameters      |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |
| `MultipleMatchesError`       | Multiple groups match criteria |

## Basic Configuration

The Application Group Info module requires proper authentication credentials to access the Strata
Cloud Manager API.

```yaml
- name: Basic Application Group Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about application groups
      cdot65.scm.application_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: groups_info
      
    - name: Display retrieved information
      debug:
        var: groups_info.application_groups
```

## Usage Examples

### Retrieving Application Group Information

The module provides several ways to retrieve application group information based on your specific
needs.

### Getting a Specific Application Group

This example retrieves detailed information about a specific application group by name.

```yaml
- name: Get information about a specific application group
  cdot65.scm.application_group_info:
    provider: "{{ provider }}"
    name: "web-apps"
    folder: "Texas"
  register: app_group_info

- name: Display application group information
  debug:
    var: app_group_info.application_group
```

### Listing All Application Groups

This example lists all application group objects in a specific folder.

```yaml
- name: List all application group objects in a folder
  cdot65.scm.application_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_app_groups

- name: Display count of application groups
  debug:
    msg: "Found {{ all_app_groups.application_groups | length }} application groups in Texas folder"
```

### Analyzing Application Group Membership

This example retrieves application groups and analyzes their membership.

```yaml
- name: Get application groups and analyze membership
  cdot65.scm.application_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: app_groups

- name: Display groups with their member counts
  debug:
    msg: "Group: {{ item.name }} - Contains {{ item.members | length }} applications"
  loop: "{{ app_groups.application_groups }}"
  
- name: Find groups containing specific applications
  debug:
    msg: "Group {{ item.name }} contains web-browsing"
  loop: "{{ app_groups.application_groups }}"
  when: "'web-browsing' in item.members"
```

### Using Advanced Filtering Options

These examples illustrate more advanced filtering options including exact match and exclusions.

```yaml
- name: List application groups with exact match and exclusions
  cdot65.scm.application_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_app_groups

- name: Get application groups from multiple folders except specific ones
  cdot65.scm.application_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: false
    exclude_folders: ["Development", "Testing"]
  register: production_app_groups
```

## Processing Retrieved Information

After retrieving application group information, you can process the data for various purposes such
as policy analysis, inventory management, or security auditing.

```yaml
- name: Create an application group analysis report
  block:
    - name: Get all application groups
      cdot65.scm.application_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_app_groups
      
    - name: Get applications for cross-reference
      cdot65.scm.application_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_applications
      
    - name: Create analysis data structures
      set_fact:
        large_groups: "{{ all_app_groups.application_groups | selectattr('members', 'defined') | selectattr('members', 'length_is_greater_than', 10) | list }}"
        empty_groups: "{{ all_app_groups.application_groups | selectattr('members', 'defined') | selectattr('members', 'equalto', []) | list }}"
        app_usage: {}
        
    - name: Count application usage across groups
      set_fact:
        app_usage: "{{ app_usage | combine({item: (all_app_groups.application_groups | selectattr('members', 'defined') | selectattr('members', 'contains', item) | list | length)}) }}"
      loop: "{{ all_applications.applications | map(attribute='name') | list }}"
      when: all_applications.applications is defined
      
    - name: Find most commonly used applications in groups
      set_fact:
        common_apps: "{{ app_usage.keys() | sort(attribute=app_usage.get, reverse=true) | list | first(5) }}"
        
    - name: Display analysis results
      debug:
        msg: |
          Application Group Analysis:
          - Total Groups: {{ all_app_groups.application_groups | length }}
          - Large Groups (>10 members): {{ large_groups | length }}
          - Empty Groups: {{ empty_groups | length }}
          
          Most Used Applications in Groups:
          {% for app in common_apps %}
          - {{ app }}: Used in {{ app_usage[app] }} groups
          {% endfor %}
```

## Error Handling

It's important to handle potential errors when retrieving application group information.

```yaml
- name: Retrieve application group info with error handling
  block:
    - name: Attempt to retrieve application group information
      cdot65.scm.application_group_info:
        provider: "{{ provider }}"
        name: "nonexistent-group"
        folder: "Texas"
      register: app_group_info
      
  rescue:
    - name: Handle group not found error
      debug:
        msg: "Application group not found or other error occurred"
        
    - name: Continue with fallback actions
      cdot65.scm.application_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_app_groups
      
    - name: Log the error and continue
      debug:
        msg: "Continuing with list of all application groups instead of specific group"
```

## Best Practices

### Efficient Filtering

- Use specific filters to minimize the result set
- Use the exact_match parameter when you only want objects defined in the specific container
- Consider performance implications when retrieving large datasets
- Use exclusion filters to narrow down results when searching across multiple containers

### Container Selection

- Use folder, snippet, or device consistently across operations
- Verify container existence before querying
- Use exclusion filters to refine results when working with large containers
- Consider folder organization when retrieving application groups

### Information Handling

- Register results to variables for further processing
- Use Ansible's filtering capabilities (selectattr, map, etc.) on the returned lists
- Check if application_groups/application_group is defined before accessing properties
- Process member lists to identify application membership patterns
- Combine with application_info to get detailed information about member applications

### Security Analysis

- Use application group information to assess security policy consistency
- Identify overlapping or redundant application groups
- Analyze application group composition for security gaps
- Track application group changes over time
- Compare application groups across different environments

### Integration with Security Policies

- Use application group information to validate security policy configurations
- Verify application group membership before making policy changes
- Generate reports on application group usage across policies
- Identify unused application groups for cleanup

## Related Modules

- [application_group](application_group.md) - Manage application group objects (create, update,
  delete)
- [application](application.md) - Manage application objects
- [application_info](application_info.md) - Retrieve information about application objects
- [security_rule](security_rule.md) - Configure security policies that reference application groups
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules using
  application groups
