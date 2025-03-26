# Application Group Information Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
   - [Getting Information About a Specific Application Group](#getting-information-about-a-specific-application-group)
   - [Listing All Application Group Objects](#listing-all-application-group-objects)
   - [Using Advanced Filtering Options](#using-advanced-filtering-options)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `application_group_info` module provides functionality to gather information about application
group objects in Palo Alto Networks' Strata Cloud Manager. This is a read-only module that can
retrieve detailed information about a specific application group by name, or list multiple
application groups with various filtering options. It supports advanced filtering capabilities
including container-based filtering and exclusion filters.

## Module Parameters

| Parameter              | Required | Type | Choices           | Default    | Comments                                                                   |
| ---------------------- | -------- | ---- | ----------------- | ---------- | -------------------------------------------------------------------------- |
| name                   | no       | str  |                   |            | The name of a specific application group object to retrieve.               |
| gather_subset          | no       | list | ['all', 'config'] | ['config'] | Determines which information to gather about application groups.           |
| folder                 | no       | str  |                   |            | Filter application groups by folder container.                             |
| snippet                | no       | str  |                   |            | Filter application groups by snippet container.                            |
| device                 | no       | str  |                   |            | Filter application groups by device container.                             |
| exact_match            | no       | bool |                   | false      | When True, only return objects defined exactly in the specified container. |
| exclude_folders        | no       | list |                   |            | List of folder names to exclude from results.                              |
| exclude_snippets       | no       | list |                   |            | List of snippet values to exclude from results.                            |
| provider               | yes      | dict |                   |            | Authentication credentials.                                                |
| provider.client_id     | yes      | str  |                   |            | Client ID for authentication.                                              |
| provider.client_secret | yes      | str  |                   |            | Client secret for authentication.                                          |
| provider.tsg_id        | yes      | str  |                   |            | Tenant Service Group ID.                                                   |
| provider.log_level     | no       | str  |                   | INFO       | Log level for the SDK.                                                     |

!!! note

- Exactly one container type (`folder`, `snippet`, or `device`) must be provided when not specifying
  a name.
- When `name` is specified, the module will retrieve a single application group object.
- When `name` is not specified, the module will return a list of application groups based on filter
  criteria.
- This is a read-only module that does not make any changes to the system.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Getting Information About a Specific Application Group



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


### Listing All Application Group Objects



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


### Using Advanced Filtering Options



```yaml
- name: List application groups with exact match and exclusions
  cdot65.scm.application_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_app_groups

- name: Process filtered application groups
  debug:
    msg: "Application group {{ item.name }} contains {{ item.members | length }} applications"
  loop: "{{ filtered_app_groups.application_groups }}"
```


## Return Values

| Name               | Description                                                               | Type | Returned                            | Sample                                                                                                                                                                                                                                               |
| ------------------ | ------------------------------------------------------------------------- | ---- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| application_groups | List of application group objects matching the filter criteria            | list | success, when name is not specified | \[{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-apps", "members": ["ssl", "web-browsing"], "folder": "Texas"}, {"id": "234e5678-e89b-12d3-a456-426655440001", "name": "network-apps", "members": ["dns", "dhcp"], "folder": "Texas"}\] |
| application_group  | Information about the requested application group (when querying by name) | dict | success, when name is specified     | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-apps", "members": ["ssl", "web-browsing"], "folder": "Texas"}                                                                                                                            |

## Error Handling

Common errors you might encounter when using this module:

| Error                       | Description                                                          | Resolution                                                   |
| --------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------ |
| Application group not found | The specified application group name does not exist in the container | Verify the application group name and container location     |
| Missing required parameter  | Required container parameter not provided                            | Ensure a container (folder, snippet, or device) is specified |
| Invalid filter parameters   | Incorrect filter values or format                                    | Check the format and validity of filter parameters           |



```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to retrieve application group information
      cdot65.scm.application_group_info:
        provider: "{{ provider }}"
        name: "web-apps"
        folder: "Texas"
      register: app_group_info
  rescue:
    - name: Handle application group not found error
      debug:
        msg: "Application group web-apps not found in Texas folder"
    - name: Continue with other tasks
      # Additional recovery tasks
```


## Best Practices

1. **Efficient Filtering**

   - Use specific filters to minimize the result set
   - Use the exact_match parameter when you only want objects defined in the specific container
   - Consider performance implications when retrieving large datasets

2. **Container Selection**

   - Use folder, snippet, or device consistently across operations
   - Verify container existence before querying
   - Use exclusion filters to refine results when working with large containers

3. **Using Results**

   - Register results to variables for further processing
   - Use Ansible's filtering capabilities (selectattr, map, etc.) on the returned lists
   - Check if application_groups/application_group is defined before accessing properties
   - Process member lists to identify application membership patterns

4. **Integration with Security Policies**

   - Use application group information to validate security policy configurations
   - Verify application group membership before making policy changes
   - Generate reports on application group usage across policies

5. **Error Handling**

   - Implement proper error handling with block/rescue
   - Provide meaningful error messages
   - Have fallback actions when objects are not found

## Related Modules

- [application_group](application_group.md) - Manage application group objects (create, update,
  delete)
- [application](application.md) - Manage application objects
- [application_info](application_info.md) - Retrieve information about application objects
- [security_rule](security_rule.md) - Configure security policies that reference application groups

## Author

- Calvin Remsburg (@cdot65)
