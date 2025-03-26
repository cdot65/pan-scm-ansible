# Service Group Information Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Service Group Info Parameters](#service-group-info-parameters)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Retrieving Specific Service Group Information](#retrieving-specific-service-group-information)
    - [Listing All Service Groups](#listing-all-service-groups)
    - [Filtering by Members](#filtering-by-members)
    - [Filtering by Tags](#filtering-by-tags)
    - [Advanced Filtering with Ansible](#advanced-filtering-with-ansible)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `service_group_info` module provides functionality to gather information about service group
objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is an information-gathering module
that doesn't make any changes to the system. It supports retrieving a specific service group by name
or listing all service groups with various filter options including members, tags, and container
filters. The module is useful for inventory management, dependency analysis, and preparing for
configuration changes.

## Core Methods

| Method    | Description                           | Parameters                    | Return Type                       |
| --------- | ------------------------------------- | ----------------------------- | --------------------------------- |
| `fetch()` | Gets a specific service group by name | `name: str`, `container: str` | `ServiceGroupResponseModel`       |
| `list()`  | Lists service groups with filtering   | `folder: str`, `**filters`    | `List[ServiceGroupResponseModel]` |

## Service Group Info Parameters

| Parameter          | Type | Required        | Description                                                    |
| ------------------ | ---- | --------------- | -------------------------------------------------------------- |
| `name`             | str  | No              | The name of a specific service group object to retrieve        |
| `gather_subset`    | list | No              | Determines which information to gather (default: ['config'])   |
| `folder`           | str  | One container\* | Filter service groups by folder container                      |
| `snippet`          | str  | One container\* | Filter service groups by snippet container                     |
| `device`           | str  | One container\* | Filter service groups by device container                      |
| `exact_match`      | bool | No              | Only return objects defined exactly in the specified container |
| `exclude_folders`  | list | No              | List of folder names to exclude from results                   |
| `exclude_snippets` | list | No              | List of snippet values to exclude from results                 |
| `exclude_devices`  | list | No              | List of device values to exclude from results                  |
| `members`          | list | No              | Filter by service members contained in the groups              |
| `tags`             | list | No              | Filter by tags associated with service groups                  |

\*One container parameter is required when `name` is not specified.

### Provider Dictionary

| Parameter       | Type | Required | Description                             |
| --------------- | ---- | -------- | --------------------------------------- |
| `client_id`     | str  | Yes      | Client ID for SCM authentication        |
| `client_secret` | str  | Yes      | Client secret for SCM authentication    |
| `tsg_id`        | str  | Yes      | Tenant Service Group ID                 |
| `log_level`     | str  | No       | Log level for the SDK (default: "INFO") |

### Requirements

- SCM Python SDK (`pan-scm-sdk>=0.3.22`)
- Python 3.12 or higher
- Ansible 2.17 or higher

## Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid request data or format |
| `MissingQueryParameterError` | Missing required parameters    |
| `ObjectNotPresentError`      | Service group not found        |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The Service Group Info module requires proper authentication credentials to access the Strata Cloud
Manager API.

```yaml
- name: Basic Service Group Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about service groups
      cdot65.scm.service_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: service_groups_result
    
    - name: Display service groups
      debug:
        var: service_groups_result.service_groups
```

### Return Values

| Name           | Description                                                 | Type | Returned                   | Sample                                                                                                                                                                                |
| -------------- | ----------------------------------------------------------- | ---- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| service_groups | List of service group objects matching the filter criteria. | list | when name is not specified | \[{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-services", "members": ["HTTPS", "SSH", "web-custom-service"], "folder": "Texas", "tag": ["Web", "Production"]}, {...}\] |
| service_group  | Information about the requested service group.              | dict | when name is specified     | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-services", "members": ["HTTPS", "SSH", "web-custom-service"], "folder": "Texas", "tag": ["Web", "Production"]}            |

## Usage Examples

### Retrieving Specific Service Group Information

```yaml
- name: Get information about a specific service group
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    name: "web-services"
    folder: "Texas"
  register: service_group_info
```

### Listing All Service Groups

```yaml
- name: List all service group objects in a folder
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_service_groups
```

### Filtering by Members

```yaml
- name: List service groups containing a specific member
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    members: ["HTTPS"]
  register: https_service_groups
```

### Filtering by Tags

```yaml
- name: List service groups with specific tags
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["Production", "Web"]
  register: tagged_service_groups
```

### Advanced Filtering with Ansible

```yaml
# Since the module doesn't support filtering by name prefix directly,
# we can use Ansible's built-in filters to achieve this
- name: Get all service groups for name prefix filtering
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_groups_for_filtering
  
# Filter service groups for names starting with "dev-" in memory
- name: Filter service groups for dev- prefix in memory
  set_fact:
    dev_groups: 
      service_groups: "{{ all_groups_for_filtering.service_groups | selectattr('name', 'match', '^dev-.*') | list }}"

# Work with the filtered results
- name: Display filtered service groups
  debug:
    var: dev_groups
```

## Managing Configuration Changes

As an info module, `service_group_info` does not make any configuration changes. However, you can
use the information it retrieves to make decisions about other configuration operations.

```yaml
- name: Use service group information for security rule creation
  block:
    - name: Get service groups with specific tags
      cdot65.scm.service_group_info:
        provider: "{{ provider }}"
        folder: "Texas"
        tags: ["Production", "Web"]
      register: web_service_groups
      
    - name: Create security rule using service groups
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Allow-Web-Services"
        folder: "Texas"
        source_zones: ["Trust"]
        destination_zones: ["Untrust"]
        source_addresses: ["any"]
        destination_addresses: ["any"]
        service_groups: "{{ web_service_groups.service_groups | map(attribute='name') | list }}"
        action: "allow"
        description: "Allow web service groups traffic"
        state: "present"
      when: web_service_groups.service_groups | length > 0
      
    - name: Commit changes if rule was created
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Created security rule for web service groups"
      when: web_service_groups.service_groups | length > 0
```

## Error Handling

Common errors you might encounter when using this module:

| Error                     | Description                                                   | Resolution                                           |
| ------------------------- | ------------------------------------------------------------- | ---------------------------------------------------- |
| Service group not found   | Specified service group does not exist in the given container | Verify the service group name and container location |
| Missing query parameter   | Required parameter not provided                               | Ensure all required parameters are specified         |
| Invalid filter parameters | Filter parameters in incorrect format                         | Check parameter format requirements                  |

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to retrieve service group information
      cdot65.scm.service_group_info:
        provider: "{{ provider }}"
        name: "NonExistentGroup"
        folder: "Texas"
      register: service_group_info_result
  rescue:
    - name: Handle service group not found error
      debug:
        msg: "Service group could not be found, continuing with other tasks"
    - name: Continue with other tasks
      # Additional recovery tasks
```

## Best Practices

### Querying Strategies

- Use name parameter for querying specific service groups
- Use container filters (folder, snippet, device) for listing service groups
- Combine with JMESPath filters in Ansible for advanced filtering
- Create a consistent approach to information gathering across playbooks
- Document query patterns for better maintenance

### Performance Optimization

- Include specific container parameters to narrow search scope
- Use exact_match parameter when possible to improve performance
- Use exclusion filters to narrow down results when querying large systems
- Consider using more specific filters for large deployments
- Optimize performance by retrieving only what you need

### Member-Based Filtering

- Filter by members to find groups containing specific services
- Use member-based filtering to trace service dependencies
- Identify all groups that would be affected by changes to a specific service
- Maintain service group dependency documentation
- Implement change control procedures for member changes

### Tag-Based Filtering

- Use tag filtering to group service groups by function or environment
- Combine multiple tags with AND logic to narrow results
- Create consistent tagging conventions for easier filtering
- Document tag governance and meaning
- Implement tag standardization across the organization

### Naming and Uniqueness

- Consider using timestamps in object names for test environments
- Use Ansible's `lookup('pipe', 'date +%Y%m%d%H%M%S')` to generate timestamps
- Store dynamic object names in variables for easier reference and cleanup
- Ensure unique names to avoid conflicts when testing
- Document naming conventions for better collaboration

### Integration with Other Modules

- Use service_group_info module output as input for service_group module operations
- Chain info queries with security policy modules to see where service groups are used
- Leverage the registered variables for conditional tasks and reporting
- Create workflows that combine info modules with configuration modules
- Use returned data for comprehensive documentation and reports

## Related Modules

- [service_group](service_group.md) - Manage service group objects (create, update, delete)
- [service](service.md) - Manage individual service objects
- [service_info](service_info.md) - Retrieve information about service objects
- [security_rule](security_rule.md) - Configure security policies that reference service groups
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules
- [tag](tag.md) - Manage tags used with service group objects

## Author

- Calvin Remsburg (@cdot65)
