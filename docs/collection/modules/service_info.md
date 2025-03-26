# Service Information Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Service Info Parameters](#service-info-parameters)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Retrieving Service Information](#retrieving-service-information)
    - [Getting Information About a Specific Service](#getting-information-about-a-specific-service)
    - [Listing All Service Objects](#listing-all-service-objects)
    - [Filtering by Protocol Type](#filtering-by-protocol-type)
    - [Filtering by Tags](#filtering-by-tags)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `service_info` Ansible module provides functionality to gather information about service objects
in Palo Alto Networks' Strata Cloud Manager (SCM). This is a read-only module that can retrieve
detailed information about a specific service object by name, or list multiple service objects with
various filtering options. It supports advanced filtering capabilities including container-based
filtering, protocol type filtering, tag-based filtering, and exclusion filters.

## Core Methods

| Method    | Description                     | Parameters                    | Return Type                  |
| --------- | ------------------------------- | ----------------------------- | ---------------------------- |
| `fetch()` | Gets a specific service by name | `name: str`, `container: str` | `ServiceResponseModel`       |
| `list()`  | Lists services with filtering   | `folder: str`, `**filters`    | `List[ServiceResponseModel]` |

## Service Info Parameters

| Parameter          | Type | Required        | Description                                                               |
| ------------------ | ---- | --------------- | ------------------------------------------------------------------------- |
| `name`             | str  | No              | The name of a specific service object to retrieve                         |
| `gather_subset`    | list | No              | Determines which information to gather (default: ['config'])              |
| `folder`           | str  | One container\* | Filter services by folder container                                       |
| `snippet`          | str  | One container\* | Filter services by snippet container                                      |
| `device`           | str  | One container\* | Filter services by device container                                       |
| `exact_match`      | bool | No              | When True, only return objects defined exactly in the specified container |
| `exclude_folders`  | list | No              | List of folder names to exclude from results                              |
| `exclude_snippets` | list | No              | List of snippet values to exclude from results                            |
| `exclude_devices`  | list | No              | List of device values to exclude from results                             |
| `protocol_types`   | list | No              | Filter by protocol types (["tcp"], ["udp"], or ["tcp", "udp"])            |
| `tags`             | list | No              | Filter by tags                                                            |

\*One container parameter is required when `name` is not specified.

### Provider Dictionary

| Parameter       | Type | Required | Description                             |
| --------------- | ---- | -------- | --------------------------------------- |
| `client_id`     | str  | Yes      | Client ID for SCM authentication        |
| `client_secret` | str  | Yes      | Client secret for SCM authentication    |
| `tsg_id`        | str  | Yes      | Tenant Service Group ID                 |
| `log_level`     | str  | No       | Log level for the SDK (default: "INFO") |

## Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid request data or format |
| `MissingQueryParameterError` | Missing required parameters    |
| `ObjectNotPresentError`      | Service not found              |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The Service Info module requires proper authentication credentials to access the Strata Cloud
Manager API.

```yaml
- name: Basic Service Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about services
      cdot65.scm.service_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: services_result
    
    - name: Display services
      debug:
        var: services_result.services
```

## Usage Examples

### Retrieving Service Information

You can retrieve information about service objects with various filtering options.

### Getting Information About a Specific Service

This example retrieves details about a specific service by name.

```yaml
- name: Get information about a specific service
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    name: "web-service"
    folder: "Texas"
  register: service_info

- name: Display service information
  debug:
    var: service_info.service
    
- name: Check if service has TCP protocol
  debug:
    msg: "Service has TCP protocol with ports: {{ service_info.service.protocol.tcp.port }}"
  when: service_info.service.protocol.tcp is defined
```

### Listing All Service Objects

This example lists all service objects in a specific folder.

```yaml
- name: List all service objects in a folder
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_services

- name: Display count of services
  debug:
    msg: "Found {{ all_services.services | length }} services in Texas folder"
    
- name: List all service names
  debug:
    msg: "{{ all_services.services | map(attribute='name') | list }}"
```

### Filtering by Protocol Type

This example demonstrates filtering services by protocol type (TCP or UDP).

```yaml
- name: List only TCP service objects
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    folder: "Texas"
    protocol_types: ["tcp"]
  register: tcp_services

- name: Count TCP services
  debug:
    msg: "Found {{ tcp_services.services | length }} TCP services"
    
- name: List only UDP service objects
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    folder: "Texas"
    protocol_types: ["udp"]
  register: udp_services
    
- name: Count UDP services
  debug:
    msg: "Found {{ udp_services.services | length }} UDP services"
```

### Filtering by Tags

This example shows how to filter services by tag values.

```yaml
- name: List services with specific tags
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["Production", "Web"]
  register: tagged_services

- name: Process tagged services
  debug:
    msg: "Service {{ item.name }} is tagged with Production and Web"
  loop: "{{ tagged_services.services }}"
  when: "'Production' in item.tag and 'Web' in item.tag"
```

## Managing Configuration Changes

As an info module, `service_info` does not make any configuration changes. However, you can use the
information it retrieves to make decisions about other configuration operations.

```yaml
- name: Use service information to create service groups
  block:
    - name: Get TCP web services
      cdot65.scm.service_info:
        provider: "{{ provider }}"
        folder: "Texas"
        protocol_types: ["tcp"]
        tags: ["Web"]
      register: web_services
      
    - name: Create web services group
      cdot65.scm.service_group:
        provider: "{{ provider }}"
        name: "Web-Services-Group"
        folder: "Texas"
        members: "{{ web_services.services | map(attribute='name') | list }}"
        description: "Group containing all web service objects"
        state: "present"
      when: web_services.services | length > 0
      
    - name: Commit changes if group was created
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Created service group for web services"
      when: web_services.services | length > 0
```

## Error Handling

It's important to handle potential errors when retrieving service information.

```yaml
- name: Get service information with error handling
  block:
    - name: Attempt to get service info
      cdot65.scm.service_info:
        provider: "{{ provider }}"
        name: "web-service"
        folder: "Texas"
      register: result
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a 'not found' error
      debug:
        msg: "Service web-service does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

## Best Practices

### Efficient Filtering

- Use specific filters to minimize the result set
- Combine protocol_types and tags filters for more precise results
- Consider performance implications when retrieving large datasets
- Use exact_match=true when you only want objects defined directly in the container
- Utilize exclusion filters to narrow down results in complex environments

### Container Management

- Use folder, snippet, or device consistently across operations
- Verify container existence before querying
- Use exclusion filters to refine results when working with large containers
- Document container structure for better organization
- Consider implementing a hierarchical folder structure for easier filtering

### Protocol Type Filtering

- Filter by "tcp" when working with web services and most application traffic
- Filter by "udp" for DNS, NTP, and other connectionless services
- Use protocol_types filter to identify services that might be affected by protocol-specific changes
- Document protocol usage patterns for better understanding of network traffic
- Regularly review protocol distribution across services

### Tag Management

- Use tags filter to find services belonging to specific applications or environments
- Combine tags filter with protocol_types for environment-specific service types
- Create consistent tagging strategies for better filtering capabilities
- Document tag usage and meaning for easier reference
- Implement tag governance to maintain consistency

### Data Processing

- Register results to variables for further processing
- Use Ansible's filtering capabilities (selectattr, map, etc.) on the returned lists
- Check if services/service is defined before accessing properties
- Process returned data to generate reports or populate templates
- Create meaningful variable names for better playbook readability

## Related Modules

- [service](service.md) - Manage service objects (create, update, delete)
- [service_group](service_group.md) - Manage service group objects
- [service_group_info](service_group_info.md) - Retrieve information about service groups
- [security_rule](security_rule.md) - Configure security policies that reference services
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules
