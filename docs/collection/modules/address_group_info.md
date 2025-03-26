# Address Group Information Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
   - [Getting Information About a Specific Address Group](#getting-information-about-a-specific-address-group)
   - [Listing All Address Groups](#listing-all-address-groups)
   - [Filtering by Address Group Type](#filtering-by-address-group-type)
   - [Filtering by Tags](#filtering-by-tags)
   - [Using Advanced Filtering Options](#using-advanced-filtering-options)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `address_group_info` module provides functionality to gather information about address group
objects in Palo Alto Networks' Strata Cloud Manager. This is a read-only module that can retrieve
detailed information about a specific address group object by name, or list multiple address group
objects with various filtering options. It supports advanced filtering capabilities including group
type filtering (static or dynamic), tag-based filtering, and exclusion filters.

## Module Parameters

| Parameter              | Required | Type | Choices               | Default    | Comments                                                                   |
| ---------------------- | -------- | ---- | --------------------- | ---------- | -------------------------------------------------------------------------- |
| name                   | no       | str  |                       |            | The name of a specific address group object to retrieve.                   |
| gather_subset          | no       | list | ['all', 'config']     | ['config'] | Determines which information to gather about address groups.               |
| folder                 | no       | str  |                       |            | Filter address groups by folder container.                                 |
| snippet                | no       | str  |                       |            | Filter address groups by snippet container.                                |
| device                 | no       | str  |                       |            | Filter address groups by device container.                                 |
| exact_match            | no       | bool |                       | false      | When True, only return objects defined exactly in the specified container. |
| exclude_folders        | no       | list |                       |            | List of folder names to exclude from results.                              |
| exclude_snippets       | no       | list |                       |            | List of snippet values to exclude from results.                            |
| exclude_devices        | no       | list |                       |            | List of device values to exclude from results.                             |
| types                  | no       | list | ["static", "dynamic"] |            | Filter by address group types.                                             |
| values                 | no       | list |                       |            | Filter by address group values (static members or dynamic filter).         |
| tags                   | no       | list |                       |            | Filter by tags.                                                            |
| provider               | yes      | dict |                       |            | Authentication credentials.                                                |
| provider.client_id     | yes      | str  |                       |            | Client ID for authentication.                                              |
| provider.client_secret | yes      | str  |                       |            | Client secret for authentication.                                          |
| provider.tsg_id        | yes      | str  |                       |            | Tenant Service Group ID.                                                   |
| provider.log_level     | no       | str  |                       | INFO       | Log level for the SDK.                                                     |

!!! note

- Exactly one container type (`folder`, `snippet`, or `device`) must be provided when not specifying
  a name.
- When `name` is specified, the module will retrieve a single address group object.
- When `name` is not specified, the module will return a list of address groups based on filter
  criteria.
- This is a read-only module that does not make any changes to the system.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Getting Information About a Specific Address Group



```yaml
- name: Get information about a specific address group
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    name: "Test_Static_Group_Info"
    folder: "Texas"
  register: specific_info

- name: Display specific address group information
  debug:
    var: specific_info.address_group
```


### Listing All Address Groups



```yaml
- name: List all address groups in the folder
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_groups

- name: Display count of address groups
  debug:
    msg: "Found {{ all_groups.address_groups | length }} address groups in Texas folder"
```


### Filtering by Address Group Type



```yaml
- name: List only static address groups
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    types: ["static"]
  register: static_groups

- name: List only dynamic address groups
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    types: ["dynamic"]
  register: dynamic_groups
```


### Filtering by Tags



```yaml
- name: List address groups with specific tag
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["dev-test"]
  register: tagged_groups

- name: Process tagged address groups
  debug:
    msg: "Address group {{ item.name }} is tagged with dev-test"
  loop: "{{ tagged_groups.address_groups }}"
  when: "'dev-test' in item.tag"
```


### Using Advanced Filtering Options



```yaml
- name: List address groups with exact match and exclusions
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_groups

- name: Use complex filtering with tags and group types
  cdot65.scm.address_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["dev-automation"]
    types: ["dynamic"]
    exclude_devices: ["DeviceA"]
  register: complex_filtered_groups
```


## Return Values

| Name           | Description                                                                    | Type | Returned                            | Sample                                                                                                                                                                                                                                                                                                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------ | ---- | ----------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| address_groups | List of address group objects matching the filter criteria                     | list | success, when name is not specified | \[{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-servers", "description": "Web server group", "static": ["web1", "web2"], "folder": "Texas", "tag": ["Web", "Production"]}, {"id": "234e5678-e89b-12d3-a456-426655440001", "name": "app-servers", "description": "Application server group", "dynamic": {"filter": "'app' and 'server'"}, "folder": "Texas", "tag": ["App", "Production"]}\] |
| address_group  | Information about the requested address group (when querying a specific group) | dict | success, when name is specified     | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-servers", "description": "Web server group", "static": ["web1", "web2"], "folder": "Texas", "tag": ["Web", "Production"]}                                                                                                                                                                                                                     |

## Error Handling

Common errors you might encounter when using this module:

| Error                      | Description                                                      | Resolution                                                   |
| -------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------ |
| Address group not found    | The specified address group name does not exist in the container | Verify the address group name and container location         |
| Missing required parameter | Required container parameter not provided                        | Ensure a container (folder, snippet, or device) is specified |
| Invalid filter parameters  | Incorrect filter values or format                                | Check the format and validity of filter parameters           |



```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to retrieve address group information
      cdot65.scm.address_group_info:
        provider: "{{ provider }}"
        name: "non_existent_group"
        folder: "Texas"
      register: group_info
  rescue:
    - name: Handle group not found error
      debug:
        msg: "Address group non_existent_group not found in Texas folder"
    - name: Continue with other tasks
      # Additional recovery tasks
```


## Best Practices

1. **Efficient Filtering**

   - Use specific filters to minimize the result set
   - Filter by group type when you only need static or dynamic groups
   - Combine multiple filters for more precise results
   - Consider performance implications when retrieving large datasets

2. **Container Selection**

   - Use folder, snippet, or device consistently across operations
   - Verify container existence before querying
   - Use exclusion filters to refine results when working with large containers

3. **Using Results**

   - Register results to variables for further processing
   - Use Ansible's filtering capabilities (selectattr, map, etc.) on the returned lists
   - Check if address_groups/address_group is defined before accessing properties
   - Process static and dynamic groups differently as they have different structure

4. **Error Handling**

   - Implement proper error handling with block/rescue
   - Provide meaningful error messages
   - Have fallback actions when objects are not found

5. **Security Considerations**

   - Protect sensitive information in filter criteria
   - Store credentials securely using Ansible Vault
   - Limit information gathering to necessary objects only

## Related Modules

- [address_group](address_group.md) - Manage address group objects (create, update, delete)
- [address](address.md) - Manage address objects
- [address_info](address_info.md) - Retrieve information about address objects
- [tag](tag.md) - Manage tags used with address groups
- [security_rule](security_rule.md) - Manage security rules that use address groups

## Author

- Calvin Remsburg (@cdot65)
