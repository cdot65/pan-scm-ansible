# Security Rule Information Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Security Rule Info Parameters](#security-rule-info-parameters)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Retrieving Security Rule Information](#retrieving-security-rule-information)
    - [Getting Information About a Specific Rule](#getting-information-about-a-specific-rule)
    - [Listing All Security Rules](#listing-all-security-rules)
    - [Filtering by Rule Properties](#filtering-by-rule-properties)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `security_rule_info` Ansible module provides functionality to gather information about security rule objects in Palo Alto Networks' Strata Cloud Manager (SCM). This module allows you to retrieve detailed information about a specific security rule by name or list multiple security rules with various filtering options. As an info module, it only retrieves information and does not modify any configuration.

## Core Methods

| Method    | Description                      | Parameters                                   | Return Type                     |
| --------- | -------------------------------- | -------------------------------------------- | ------------------------------- |
| `fetch()` | Gets a specific rule by name     | `name: str`, `container: str`, `rulebase: str` | `SecurityRuleResponseModel`     |
| `list()`  | Lists rules with filtering       | `folder: str`, `rulebase: str`, `**filters`    | `List[SecurityRuleResponseModel]` |

## Security Rule Info Parameters

| Parameter          | Type   | Required      | Description                                                               |
| ------------------ | ------ | ------------- | ------------------------------------------------------------------------- |
| `name`             | str    | No            | The name of a specific security rule to retrieve                          |
| `gather_subset`    | list   | No            | Determines which information to gather (default: ['config'])              |
| `folder`           | str    | One container* | Filter security rules by folder container                                 |
| `snippet`          | str    | One container* | Filter security rules by snippet container                                |
| `device`           | str    | One container* | Filter security rules by device container                                 |
| `rulebase`         | str    | No            | Which rulebase to query (pre or post) (default: "pre")                    |
| `exact_match`      | bool   | No            | When True, only return objects defined exactly in the specified container |
| `exclude_folders`  | list   | No            | List of folder names to exclude from results                              |
| `exclude_snippets` | list   | No            | List of snippet values to exclude from results                            |
| `exclude_devices`  | list   | No            | List of device values to exclude from results                             |
| `action`           | list   | No            | Filter by action ("allow", "deny", "drop", etc.)                          |
| `category`         | list   | No            | Filter by URL categories                                                  |
| `service`          | list   | No            | Filter by services                                                        |
| `application`      | list   | No            | Filter by applications                                                    |
| `destination`      | list   | No            | Filter by destinations                                                    |
| `to_`              | list   | No            | Filter by to zones                                                        |
| `source`           | list   | No            | Filter by sources                                                         |
| `from_`            | list   | No            | Filter by from zones                                                      |
| `tag`              | list   | No            | Filter by tags                                                            |
| `disabled`         | bool   | No            | Filter by disabled status                                                 |
| `profile_setting`  | dict   | No            | Filter by profile setting groups                                          |
| `log_setting`      | str    | No            | Filter by log setting                                                     |

*One container parameter is required when `name` is not specified.

### Provider Dictionary

| Parameter       | Type | Required | Description                             |
| --------------- | ---- | -------- | --------------------------------------- |
| `client_id`     | str  | Yes      | Client ID for SCM authentication         |
| `client_secret` | str  | Yes      | Client secret for SCM authentication     |
| `tsg_id`        | str  | Yes      | Tenant Service Group ID                  |
| `log_level`     | str  | No       | Log level for the SDK (default: "INFO")  |

## Exceptions

| Exception                    | Description                      |
| ---------------------------- | -------------------------------- |
| `InvalidObjectError`         | Invalid request data or format   |
| `MissingQueryParameterError` | Missing required parameters      |
| `ObjectNotPresentError`      | Security rule not found          |
| `AuthenticationError`        | Authentication failed            |
| `ServerError`                | Internal server error            |

## Basic Configuration

The Security Rule Info module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Security Rule Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about security rules
      cdot65.scm.security_rule_info:
        provider: "{{ provider }}"
        folder: "Texas"
        rulebase: "pre"
      register: rules_result
    
    - name: Display security rules
      debug:
        var: rules_result.security_rules
```

## Usage Examples

### Retrieving Security Rule Information

You can retrieve information about security rules with various filtering options.

### Getting Information About a Specific Rule

This example retrieves details about a specific security rule by name.

```yaml
- name: Get information about a specific security rule
  cdot65.scm.security_rule_info:
    provider: "{{ provider }}"
    name: "Allow_Web_Traffic"
    folder: "Texas"
    rulebase: "pre"
  register: rule_info

- name: Display rule information
  debug:
    var: rule_info.security_rule
    
- name: Check rule action
  debug:
    msg: "Rule action is {{ rule_info.security_rule.action }}"
  when: rule_info.security_rule is defined
```

### Listing All Security Rules

This example lists all security rules in a specific folder and rulebase.

```yaml
- name: List all security rules in a folder
  cdot65.scm.security_rule_info:
    provider: "{{ provider }}"
    folder: "Texas"
    rulebase: "pre"
  register: all_rules

- name: Display count of rules
  debug:
    msg: "Found {{ all_rules.security_rules | length }} security rules in pre-rulebase"
    
- name: List all rule names
  debug:
    msg: "{{ all_rules.security_rules | map(attribute='name') | list }}"
```

### Filtering by Rule Properties

This example demonstrates filtering security rules by various properties like action, tags, and zones.

```yaml
- name: List only allow action security rules
  cdot65.scm.security_rule_info:
    provider: "{{ provider }}"
    folder: "Texas"
    rulebase: "pre"
    action: ["allow"]
  register: allow_rules

- name: Count allow rules
  debug:
    msg: "Found {{ allow_rules.security_rules | length }} allow rules"
    
- name: List security rules with specific tags
  cdot65.scm.security_rule_info:
    provider: "{{ provider }}"
    folder: "Texas"
    rulebase: "pre"
    tag: ["web", "internet"]
  register: tagged_rules
    
- name: List security rules for specific zones
  cdot65.scm.security_rule_info:
    provider: "{{ provider }}"
    folder: "Texas"
    rulebase: "pre"
    from_: ["Internet"]
    to_: ["DMZ"]
  register: zone_rules
```

### Using Advanced Filtering Options

This example shows how to use advanced filtering options to refine query results.

```yaml
- name: List security rules with exact match and exclusions
  cdot65.scm.security_rule_info:
    provider: "{{ provider }}"
    folder: "Texas"
    rulebase: "post"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_rules

- name: List security rules with multiple filters
  cdot65.scm.security_rule_info:
    provider: "{{ provider }}"
    folder: "Texas"
    rulebase: "pre"
    source: ["any"]
    destination: ["Web-Servers"]
    application: ["web-browsing", "ssl"]
  register: web_server_rules
```

## Managing Configuration Changes

As an info module, `security_rule_info` does not make any configuration changes. However, you can use the information it retrieves to make decisions about other configuration operations.

```yaml
- name: Use security rule information to create address groups
  block:
    - name: Get security rules referencing specific destinations
      cdot65.scm.security_rule_info:
        provider: "{{ provider }}"
        folder: "Texas"
        rulebase: "pre"
        destination: ["Web-Servers"]
      register: web_rules
      
    - name: Create address group for additional web servers
      cdot65.scm.address_group:
        provider: "{{ provider }}"
        name: "Additional-Web-Servers"
        folder: "Texas"
        static_addresses: ["Web-Server-3", "Web-Server-4"]
        description: "Additional web servers for existing rules"
        state: "present"
      when: web_rules.security_rules | length > 0
      
    - name: Update security rules to include new address group
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "{{ item.name }}"
        folder: "Texas"
        rulebase: "pre"
        destination: "{{ item.destination + ['Additional-Web-Servers'] }}"
        state: "present"
      when: web_rules.security_rules | length > 0
      loop: "{{ web_rules.security_rules }}"
      
    - name: Commit changes if any rules were updated
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated security rules to include additional web servers"
      when: web_rules.security_rules | length > 0
```

## Error Handling

It's important to handle potential errors when retrieving security rule information.

```yaml
- name: Get security rule information with error handling
  block:
    - name: Attempt to get security rule info
      cdot65.scm.security_rule_info:
        provider: "{{ provider }}"
        name: "Allow_Web_Traffic"
        folder: "Texas"
        rulebase: "pre"
      register: result
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a 'not found' error
      debug:
        msg: "Security rule 'Allow_Web_Traffic' does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

## Best Practices

### Efficient Filtering

- Use specific filters to minimize the result set
- Combine multiple filters for more precise results
- Consider performance implications when retrieving large datasets
- Use exact_match=true when you only want rules defined directly in the container
- Utilize exclusion filters to narrow down results in complex environments

### Rulebase Management

- Specify the appropriate rulebase (pre or post) for your query
- Be consistent in your rulebase usage across related operations
- Document which rules belong to which rulebase
- Consider querying both rulebases when generating comprehensive reports
- Understand the processing order implications of pre vs post rulebase

### Container Management

- Use folder, snippet, or device consistently across operations
- Verify container existence before querying
- Use exclusion filters to refine results when working with large containers
- Document container structure for better organization
- Implement appropriate access controls for each container

### Data Processing

- Register results to variables for further processing
- Use Ansible's filtering capabilities (selectattr, map, etc.) on the returned lists
- Check if security_rules/security_rule is defined before accessing properties
- Process returned data to generate reports or populate templates
- Create meaningful variable names for better playbook readability

### Integration with Other Modules

- Use the info module to check for existing rules before creating new ones
- Combine with the security_rule module for complete rule management
- Use the retrieved information to make decisions in your playbooks
- Check rule dependencies before making changes
- Generate reports on security policy coverage and gaps

## Related Modules

- [security_rule](security_rule.md) - Create, update, and delete security rules
- [security_zone](security_zone.md) - Manage security zones referenced in rules
- [address_info](address_info.md) - Retrieve information about address objects
- [service_info](service_info.md) - Retrieve information about service objects
- [application_info](application_info.md) - Retrieve information about application objects