# Application Information Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Application Info Model Attributes](#application-info-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Retrieving Application Information](#retrieving-application-information)
    - [Getting a Specific Application](#getting-a-specific-application)
    - [Listing All Applications](#listing-all-applications)
    - [Filtering by Category](#filtering-by-category)
    - [Filtering by Risk Level](#filtering-by-risk-level)
    - [Using Advanced Filtering Options](#using-advanced-filtering-options)
07. [Processing Retrieved Information](#processing-retrieved-information)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `application_info` Ansible module provides functionality to retrieve information about
application objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is a read-only module
that can retrieve detailed information about a specific application object by name, or list multiple
application objects with various filtering options including container-based filtering, category
filtering, technology filtering, risk level filtering, and exclusion filters.

## Core Methods

| Method     | Description                         | Parameters                                  | Return Type                      |
| ---------- | ----------------------------------- | ------------------------------------------- | -------------------------------- |
| `get()`    | Gets a specific application by name | `name: str`, `container: str`               | `ApplicationResponseModel`       |
| `list()`   | Lists applications with filtering   | `folder: str`, `**filters`                  | `List[ApplicationResponseModel]` |
| `filter()` | Applies filters to the results      | `applications: List`, `filter_params: Dict` | `List[ApplicationResponseModel]` |

## Application Info Model Attributes

| Attribute          | Type | Required      | Description                                                  |
| ------------------ | ---- | ------------- | ------------------------------------------------------------ |
| `name`             | str  | No            | The name of a specific application to retrieve               |
| `gather_subset`    | list | No            | Determines which information to gather (default: ['config']) |
| `folder`           | str  | One container | Filter applications by folder (max 64 chars)                 |
| `snippet`          | str  | One container | Filter applications by snippet (max 64 chars)                |
| `exact_match`      | bool | No            | When True, only return objects in the specified container    |
| `exclude_folders`  | list | No            | List of folder names to exclude from results                 |
| `exclude_snippets` | list | No            | List of snippet values to exclude from results               |
| `category`         | list | No            | Filter by application category                               |
| `subcategory`      | list | No            | Filter by application subcategory                            |
| `technology`       | list | No            | Filter by application technology                             |
| `risk`             | list | No            | Filter by application risk level (1-5)                       |

## Exceptions

| Exception                    | Description                          |
| ---------------------------- | ------------------------------------ |
| `ObjectNotPresentError`      | Application not found                |
| `MissingQueryParameterError` | Missing required parameters          |
| `InvalidFilterError`         | Invalid filter parameters            |
| `AuthenticationError`        | Authentication failed                |
| `ServerError`                | Internal server error                |
| `MultipleMatchesError`       | Multiple applications match criteria |

## Basic Configuration

The Application Info module requires proper authentication credentials to access the Strata Cloud
Manager API.

```yaml
- name: Basic Application Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about applications
      cdot65.scm.application_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: applications_info
      
    - name: Display retrieved information
      debug:
        var: applications_info.applications
```

## Usage Examples

### Retrieving Application Information

The module provides several ways to retrieve application information based on your specific needs.

### Getting a Specific Application

This example retrieves detailed information about a specific application by name.

```yaml
- name: Get information about a specific application
  cdot65.scm.application_info:
    provider: "{{ provider }}"
    name: "custom-app"
    folder: "Texas"
  register: application_info

- name: Display application information
  debug:
    var: application_info.application
```

### Listing All Applications

This example lists all application objects in a specific folder.

```yaml
- name: List all application objects in a folder
  cdot65.scm.application_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_applications

- name: Display count of applications
  debug:
    msg: "Found {{ all_applications.applications | length }} applications in Texas folder"
```

### Filtering by Category

This example demonstrates how to filter applications by their category.

```yaml
- name: List applications by category
  cdot65.scm.application_info:
    provider: "{{ provider }}"
    folder: "Texas"
    category: ["business-systems"]
  register: business_applications

- name: Process business applications
  debug:
    msg: "Business application: {{ item.name }} ({{ item.subcategory }})"
  loop: "{{ business_applications.applications }}"
```

### Filtering by Risk Level

This example shows how to filter applications by their risk level.

```yaml
- name: List high-risk applications
  cdot65.scm.application_info:
    provider: "{{ provider }}"
    folder: "Texas"
    risk: [4, 5]
  register: high_risk_applications

- name: Process high-risk applications
  debug:
    msg: "High-risk application: {{ item.name }} (Risk Level: {{ item.risk }})"
  loop: "{{ high_risk_applications.applications }}"
```

### Using Advanced Filtering Options

These examples illustrate more advanced filtering options including exact match, exclusions, and
combined filters.

```yaml
- name: List applications with exact match and exclusions
  cdot65.scm.application_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_applications

- name: Use complex filtering with category and technology
  cdot65.scm.application_info:
    provider: "{{ provider }}"
    folder: "Texas"
    category: ["collaboration"]
    technology: ["client-server"]
    subcategory: ["instant-messaging"]
  register: collaboration_applications
```

## Processing Retrieved Information

After retrieving application information, you can process the data for various purposes such as
security analysis, inventory management, or integration with other systems.

```yaml
- name: Create a security analysis of applications
  block:
    - name: Get all applications
      cdot65.scm.application_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_applications
      
    - name: Group applications by risk level
      set_fact:
        critical_risk_apps: "{{ all_applications.applications | selectattr('risk', 'equalto', 5) | list }}"
        high_risk_apps: "{{ all_applications.applications | selectattr('risk', 'equalto', 4) | list }}"
        medium_risk_apps: "{{ all_applications.applications | selectattr('risk', 'equalto', 3) | list }}"
        low_risk_apps: "{{ all_applications.applications | selectattr('risk', 'in', [1, 2]) | list }}"
        
    - name: Count applications with security flags
      set_fact:
        vulnerable_apps: "{{ all_applications.applications | selectattr('has_known_vulnerabilities', 'defined') | selectattr('has_known_vulnerabilities', 'equalto', true) | list }}"
        evasive_apps: "{{ all_applications.applications | selectattr('evasive', 'defined') | selectattr('evasive', 'equalto', true) | list }}"
        malware_apps: "{{ all_applications.applications | selectattr('used_by_malware', 'defined') | selectattr('used_by_malware', 'equalto', true) | list }}"
        
    - name: Display security analysis
      debug:
        msg: |
          Application Security Analysis:
          - Total Applications: {{ all_applications.applications | length }}
          
          Risk Distribution:
          - Critical Risk (5): {{ critical_risk_apps | length }}
          - High Risk (4): {{ high_risk_apps | length }}
          - Medium Risk (3): {{ medium_risk_apps | length }}
          - Low Risk (1-2): {{ low_risk_apps | length }}
          
          Security Flags:
          - Apps with Known Vulnerabilities: {{ vulnerable_apps | length }}
          - Apps with Evasive Behavior: {{ evasive_apps | length }}
          - Apps Used by Malware: {{ malware_apps | length }}
```

## Error Handling

It's important to handle potential errors when retrieving application information.

```yaml
- name: Retrieve application info with error handling
  block:
    - name: Attempt to retrieve application information
      cdot65.scm.application_info:
        provider: "{{ provider }}"
        name: "nonexistent-app"
        folder: "Texas"
      register: application_info
      
  rescue:
    - name: Handle application not found error
      debug:
        msg: "Application not found or other error occurred"
        
    - name: Continue with fallback actions
      cdot65.scm.application_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_applications
      
    - name: Log the error and continue
      debug:
        msg: "Continuing with list of all applications instead of specific application"
```

## Best Practices

### Efficient Filtering

- Use specific filters to minimize the result set
- Filter by category, subcategory, or technology when looking for application types
- Filter by risk level when performing security analysis
- Combine multiple filters for more precise results

### Container Selection

- Use folder or snippet consistently across operations
- Verify container existence before querying
- Use exclusion filters to refine results when working with large containers

### Risk-Based Analysis

- Filter applications by risk level to identify high-risk applications
- Combine risk filtering with category filtering for targeted risk assessment
- Regularly review high-risk applications for security policy adjustments
- Identify applications with security flags for additional scrutiny

### Information Handling

- Register results to variables for further processing
- Use Ansible's filtering capabilities (selectattr, map, etc.) on the returned lists
- Check if applications/application is defined before accessing properties
- Process different application characteristics separately for detailed analysis

### Performance Optimization

- Retrieve only the information you need
- Use name parameter when you need only one specific application
- Use filters to minimize result set size
- Consider caching results for repeated access within the same playbook

### Integration with Security Policies

- Use retrieved application information to inform security policy creation
- Identify high-risk applications that require stricter controls
- Group applications by category or risk level for policy development
- Track applications with security flags for special handling

## Related Modules

- [application](application.md) - Manage application objects (create, update, delete)
- [application_group](application_group.md) - Manage application group objects
- [application_group_info](application_group_info.md) - Retrieve information about application
  groups
- [security_rule](security_rule.md) - Configure security policies that reference applications
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules using
  applications
