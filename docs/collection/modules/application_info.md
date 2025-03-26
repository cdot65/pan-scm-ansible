# Application Information Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
   - [Getting Information About a Specific Application](#getting-information-about-a-specific-application)
   - [Listing All Application Objects](#listing-all-application-objects)
   - [Filtering by Category](#filtering-by-category)
   - [Filtering by Risk Level](#filtering-by-risk-level)
   - [Using Advanced Filtering Options](#using-advanced-filtering-options)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `application_info` module provides functionality to gather information about application objects
in Palo Alto Networks' Strata Cloud Manager. This is a read-only module that can retrieve detailed
information about a specific application object by name, or list multiple application objects with
various filtering options. It supports advanced filtering capabilities including container-based
filtering, category filtering, technology filtering, risk level filtering, and exclusion filters.

## Module Parameters

| Parameter              | Required | Type | Choices           | Default    | Comments                                                                   |
| ---------------------- | -------- | ---- | ----------------- | ---------- | -------------------------------------------------------------------------- |
| name                   | no       | str  |                   |            | The name of a specific application object to retrieve.                     |
| gather_subset          | no       | list | ['all', 'config'] | ['config'] | Determines which information to gather about applications.                 |
| folder                 | no       | str  |                   |            | Filter applications by folder container.                                   |
| snippet                | no       | str  |                   |            | Filter applications by snippet container.                                  |
| exact_match            | no       | bool |                   | false      | When True, only return objects defined exactly in the specified container. |
| exclude_folders        | no       | list |                   |            | List of folder names to exclude from results.                              |
| exclude_snippets       | no       | list |                   |            | List of snippet values to exclude from results.                            |
| category               | no       | list |                   |            | Filter by application category.                                            |
| subcategory            | no       | list |                   |            | Filter by application subcategory.                                         |
| technology             | no       | list |                   |            | Filter by application technology.                                          |
| risk                   | no       | list |                   |            | Filter by application risk level (1-5).                                    |
| provider               | yes      | dict |                   |            | Authentication credentials.                                                |
| provider.client_id     | yes      | str  |                   |            | Client ID for authentication.                                              |
| provider.client_secret | yes      | str  |                   |            | Client secret for authentication.                                          |
| provider.tsg_id        | yes      | str  |                   |            | Tenant Service Group ID.                                                   |
| provider.log_level     | no       | str  |                   | INFO       | Log level for the SDK.                                                     |

!!! note

- Exactly one container type (`folder` or `snippet`) must be provided when not specifying a name.
- When `name` is specified, the module will retrieve a single application object.
- When `name` is not specified, the module will return a list of applications based on filter
  criteria.
- This is a read-only module that does not make any changes to the system.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Getting Information About a Specific Application



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


### Listing All Application Objects



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


## Return Values

| Name         | Description                                                                        | Type | Returned                            | Sample                                                                                                                                                                                                                                                                                                                                            |
| ------------ | ---------------------------------------------------------------------------------- | ---- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| applications | List of application objects matching the filter criteria                           | list | success, when name is not specified | \[{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "custom-app", "category": "business-systems", "subcategory": "database", "technology": "client-server", "risk": 3, "description": "Custom database application", "folder": "Texas", "ports": ["tcp/1521"]}, {"id": "234e5678-e89b-12d3-a456-426655440001", "name": "secure-chat", ...}\] |
| application  | Information about the requested application (when querying a specific application) | dict | success, when name is specified     | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "custom-app", "category": "business-systems", "subcategory": "database", "technology": "client-server", "risk": 3, "description": "Custom database application", "folder": "Texas", "ports": ["tcp/1521"]}                                                                                 |

## Error Handling

Common errors you might encounter when using this module:

| Error                      | Description                                                    | Resolution                                          |
| -------------------------- | -------------------------------------------------------------- | --------------------------------------------------- |
| Application not found      | The specified application name does not exist in the container | Verify the application name and container location  |
| Missing required parameter | Required container parameter not provided                      | Ensure a container (folder or snippet) is specified |
| Invalid filter parameters  | Incorrect filter values or format                              | Check the format and validity of filter parameters  |



```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to retrieve application information
      cdot65.scm.application_info:
        provider: "{{ provider }}"
        name: "custom-app"
        folder: "Texas"
      register: application_info
  rescue:
    - name: Handle application not found error
      debug:
        msg: "Application custom-app not found in Texas folder"
    - name: Continue with other tasks
      # Additional recovery tasks
```


## Best Practices

1. **Efficient Filtering**

   - Use specific filters like category, subcategory, and risk level to minimize the result set
   - Combine multiple filters for more precise results
   - Consider performance implications when retrieving large datasets

2. **Container Selection**

   - Use folder or snippet consistently across operations
   - Verify container existence before querying
   - Use exclusion filters to refine results when working with large containers

3. **Risk-Based Analysis**

   - Filter applications by risk level to identify high-risk applications
   - Combine risk filtering with category filtering for targeted risk assessment
   - Regularly review high-risk applications for security policy adjustments

4. **Using Results**

   - Register results to variables for further processing
   - Use Ansible's filtering capabilities (selectattr, map, etc.) on the returned lists
   - Check if applications/application is defined before accessing properties

5. **Security Considerations**

   - Identify applications with security flags like `used_by_malware` or `has_known_vulnerabilities`
   - Group applications by category and risk for security planning
   - Use the module for audit and compliance verification

## Related Modules

- [application](application.md) - Manage application objects (create, update, delete)
- [application_group_info](application_group_info.md) - Retrieve information about application
  groups
- [application_group](application_group.md) - Manage application group objects
- [security_rule](security_rule.md) - Configure security policies that reference applications

## Author

- Calvin Remsburg (@cdot65)
