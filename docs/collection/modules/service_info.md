# Service Information Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
   - [Getting Information About a Specific Service](#getting-information-about-a-specific-service)
   - [Listing All Service Objects](#listing-all-service-objects)
   - [Filtering by Protocol Type](#filtering-by-protocol-type)
   - [Filtering by Tags](#filtering-by-tags)
   - [Using Advanced Filtering Options](#using-advanced-filtering-options)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `service_info` module provides functionality to gather information about service objects in Palo
Alto Networks' Strata Cloud Manager. This is a read-only module that can retrieve detailed
information about a specific service object by name, or list multiple service objects with various
filtering options. It supports advanced filtering capabilities including container-based filtering,
protocol type filtering, tag-based filtering, and exclusion filters.

## Module Parameters

| Parameter              | Required | Type | Choices           | Default    | Comments                                                                   |
| ---------------------- | -------- | ---- | ----------------- | ---------- | -------------------------------------------------------------------------- |
| name                   | no       | str  |                   |            | The name of a specific service object to retrieve.                         |
| gather_subset          | no       | list | ['all', 'config'] | ['config'] | Determines which information to gather about services.                     |
| folder                 | no       | str  |                   |            | Filter services by folder container.                                       |
| snippet                | no       | str  |                   |            | Filter services by snippet container.                                      |
| device                 | no       | str  |                   |            | Filter services by device container.                                       |
| exact_match            | no       | bool |                   | false      | When True, only return objects defined exactly in the specified container. |
| exclude_folders        | no       | list |                   |            | List of folder names to exclude from results.                              |
| exclude_snippets       | no       | list |                   |            | List of snippet values to exclude from results.                            |
| exclude_devices        | no       | list |                   |            | List of device values to exclude from results.                             |
| protocol_types         | no       | list | ["tcp", "udp"]    |            | Filter by protocol types.                                                  |
| tags                   | no       | list |                   |            | Filter by tags.                                                            |
| provider               | yes      | dict |                   |            | Authentication credentials.                                                |
| provider.client_id     | yes      | str  |                   |            | Client ID for authentication.                                              |
| provider.client_secret | yes      | str  |                   |            | Client secret for authentication.                                          |
| provider.tsg_id        | yes      | str  |                   |            | Tenant Service Group ID.                                                   |
| provider.log_level     | no       | str  |                   | INFO       | Log level for the SDK.                                                     |

!!! note

- Exactly one container type (`folder`, `snippet`, or `device`) must be provided when not specifying
  a name.
- When `name` is specified, the module will retrieve a single service object.
- When `name` is not specified, the module will return a list of services based on filter criteria.
- This is a read-only module that does not make any changes to the system.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Getting Information About a Specific Service



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
```


### Listing All Service Objects



```yaml
- name: List all service objects in a folder
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_services

- name: Display count of services
  debug:
    msg: "Found {{ all_services.services | length }} services in Texas folder"
```


### Filtering by Protocol Type

You can filter services by protocol type (TCP or UDP):



```yaml
- name: List only TCP service objects
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    folder: "Texas"
    protocol_types: ["tcp"]
  register: tcp_services

- name: List only UDP service objects
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    folder: "Texas"
    protocol_types: ["udp"]
  register: udp_services
```


### Filtering by Tags



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


### Using Advanced Filtering Options



```yaml
- name: List services with exact match and exclusions
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_services

- name: Use complex filtering with tags and protocol types
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["Production"]
    protocol_types: ["tcp"]
    exclude_devices: ["DeviceA"]
  register: complex_filtered_services
```


## Return Values

| Name     | Description                                                                | Type | Returned                            | Sample                                                                                                                                                                                                                                                                                                                                                                    |
| -------- | -------------------------------------------------------------------------- | ---- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| services | List of service objects matching the filter criteria                       | list | success, when name is not specified | \[{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-service", "description": "Web service ports", "protocol": {"tcp": {"port": "80,443", "override": {"timeout": 30, "halfclose_timeout": 15}}}, "folder": "Texas", "tag": ["Web", "Production"]}, {"id": "234e5678-e89b-12d3-a456-426655440001", "name": "dns-service", "protocol": {"udp": {"port": "53"}}}\] |
| service  | Information about the requested service (when querying a specific service) | dict | success, when name is specified     | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-service", "description": "Web service ports", "protocol": {"tcp": {"port": "80,443", "override": {"timeout": 30, "halfclose_timeout": 15}}}, "folder": "Texas", "tag": ["Web", "Production"]}                                                                                                                 |

## Error Handling

Common errors you might encounter when using this module:

| Error                      | Description                                                | Resolution                                                   |
| -------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| Service not found          | The specified service name does not exist in the container | Verify the service name and container location               |
| Missing required parameter | Required container parameter not provided                  | Ensure a container (folder, snippet, or device) is specified |
| Invalid filter parameters  | Incorrect filter values or format                          | Check the format and validity of filter parameters           |



```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to retrieve service information
      cdot65.scm.service_info:
        provider: "{{ provider }}"
        name: "web-service"
        folder: "Texas"
      register: service_info
  rescue:
    - name: Handle service not found error
      debug:
        msg: "Service web-service not found in Texas folder"
    - name: Continue with other tasks
      # Additional recovery tasks
```


## Best Practices

1. **Efficient Filtering**

   - Use specific filters to minimize the result set
   - Combine protocol_types and tags filters for more precise results
   - Consider performance implications when retrieving large datasets
   - Use exact_match=true when you only want objects defined directly in the container

2. **Container Selection**

   - Use folder, snippet, or device consistently across operations
   - Verify container existence before querying
   - Use exclusion filters to refine results when working with large containers

3. **Using Protocol Types**

   - Filter by "tcp" when working with web services and most application traffic
   - Filter by "udp" for DNS, NTP, and other connectionless services
   - Use protocol_types filter to identify services that might be affected by protocol-specific
     changes

4. **Tag-Based Organization**

   - Use tags filter to find services belonging to specific applications or environments
   - Combine tags filter with protocol_types for environment-specific service types
   - Create consistent tagging strategies for better filtering capabilities

5. **Using Results**

   - Register results to variables for further processing
   - Use Ansible's filtering capabilities (selectattr, map, etc.) on the returned lists
   - Check if services/service is defined before accessing properties
   - Process returned data to generate reports or populate templates

## Related Modules

- [service](service.md) - Manage service objects (create, update, delete)
- [service_group_info](service_group_info.md) - Retrieve information about service groups
- [service_group](service_group.md) - Manage service group objects
- [security_rule](security_rule.md) - Configure security policies that reference services

## Author

- Calvin Remsburg (@cdot65)
