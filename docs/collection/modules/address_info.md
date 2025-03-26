# Address Information Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
   - [Getting Information About a Specific Address](#getting-information-about-a-specific-address)
   - [Listing All Address Objects](#listing-all-address-objects)
   - [Filtering by Address Type](#filtering-by-address-type)
   - [Filtering by Tags](#filtering-by-tags)
   - [Using Advanced Filtering Options](#using-advanced-filtering-options)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `address_info` module provides functionality to gather information about address objects in Palo
Alto Networks' Strata Cloud Manager. This is a read-only module that can retrieve detailed
information about a specific address object by name, or list multiple address objects with various
filtering options. It supports advanced filtering capabilities including container-based filtering,
address type filtering, tag-based filtering, and exclusion filters.

## Module Parameters

| Parameter              | Required | Type | Choices                                  | Default    | Comments                                                                   |
| ---------------------- | -------- | ---- | ---------------------------------------- | ---------- | -------------------------------------------------------------------------- |
| name                   | no       | str  |                                          |            | The name of a specific address object to retrieve.                         |
| gather_subset          | no       | list | ['all', 'config']                        | ['config'] | Determines which information to gather about addresses.                    |
| folder                 | no       | str  |                                          |            | Filter addresses by folder container.                                      |
| snippet                | no       | str  |                                          |            | Filter addresses by snippet container.                                     |
| device                 | no       | str  |                                          |            | Filter addresses by device container.                                      |
| exact_match            | no       | bool |                                          | false      | When True, only return objects defined exactly in the specified container. |
| exclude_folders        | no       | list |                                          |            | List of folder names to exclude from results.                              |
| exclude_snippets       | no       | list |                                          |            | List of snippet values to exclude from results.                            |
| exclude_devices        | no       | list |                                          |            | List of device values to exclude from results.                             |
| types                  | no       | list | ["netmask", "range", "wildcard", "fqdn"] |            | Filter by address types.                                                   |
| values                 | no       | list |                                          |            | Filter by address values.                                                  |
| tags                   | no       | list |                                          |            | Filter by tags.                                                            |
| provider               | yes      | dict |                                          |            | Authentication credentials.                                                |
| provider.client_id     | yes      | str  |                                          |            | Client ID for authentication.                                              |
| provider.client_secret | yes      | str  |                                          |            | Client secret for authentication.                                          |
| provider.tsg_id        | yes      | str  |                                          |            | Tenant Service Group ID.                                                   |
| provider.log_level     | no       | str  |                                          | INFO       | Log level for the SDK.                                                     |

!!! note

- Exactly one container type (`folder`, `snippet`, or `device`) must be provided when not specifying
  a name.
- When `name` is specified, the module will retrieve a single address object.
- When `name` is not specified, the module will return a list of addresses based on filter criteria.
- This is a read-only module that does not make any changes to the system.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Getting Information About a Specific Address



```yaml
- name: Get information about a specific address
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    name: "web-server"
    folder: "Texas"
  register: address_info

- name: Display address information
  debug:
    var: address_info.address
```


### Listing All Address Objects



```yaml
- name: List all address objects in a folder
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_addresses

- name: Display count of addresses
  debug:
    msg: "Found {{ all_addresses.addresses | length }} addresses in Texas folder"
```


### Filtering by Address Type



```yaml
- name: List only FQDN address objects
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
    types: ["fqdn"]
  register: fqdn_addresses

- name: List all IP/Netmask address objects
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
    types: ["netmask"]
  register: netmask_addresses
```


### Filtering by Tags



```yaml
- name: List addresses with specific tags
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["Production", "Web"]
  register: tagged_addresses

- name: Process tagged addresses
  debug:
    msg: "Address {{ item.name }} is tagged with Production and Web"
  loop: "{{ tagged_addresses.addresses }}"
  when: "'Production' in item.tag and 'Web' in item.tag"
```


### Using Advanced Filtering Options



```yaml
- name: List addresses with exact match and exclusions
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_addresses

- name: Use complex filtering with tags and address types
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["Dev"]
    types: ["netmask", "fqdn"]
    exclude_devices: ["DeviceA"]
  register: complex_filtered_addresses
```


## Return Values

| Name      | Description                                                                | Type | Returned                            | Sample                                                                                                                                                                                                                                                                                                                                                                                                 |
| --------- | -------------------------------------------------------------------------- | ---- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| addresses | List of address objects matching the filter criteria                       | list | success, when name is not specified | \[{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-server", "description": "Web server address", "ip_netmask": "192.168.1.100/32", "folder": "Texas", "tag": ["Web", "Production"]}, {"id": "234e5678-e89b-12d3-a456-426655440001", "name": "app-server", "description": "Application server address", "ip_netmask": "192.168.1.101/32", "folder": "Texas", "tag": ["App", "Production"]}\] |
| address   | Information about the requested address (when querying a specific address) | dict | success, when name is specified     | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-server", "description": "Web server address", "ip_netmask": "192.168.1.100/32", "folder": "Texas", "tag": ["Web", "Production"]}                                                                                                                                                                                                           |

## Error Handling

Common errors you might encounter when using this module:

| Error                      | Description                                                | Resolution                                                   |
| -------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------ |
| Address not found          | The specified address name does not exist in the container | Verify the address name and container location               |
| Missing required parameter | Required container parameter not provided                  | Ensure a container (folder, snippet, or device) is specified |
| Invalid filter parameters  | Incorrect filter values or format                          | Check the format and validity of filter parameters           |



```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to retrieve address information
      cdot65.scm.address_info:
        provider: "{{ provider }}"
        name: "web-server"
        folder: "Texas"
      register: address_info
  rescue:
    - name: Handle address not found error
      debug:
        msg: "Address web-server not found in Texas folder"
    - name: Continue with other tasks
      # Additional recovery tasks
```


## Best Practices

1. **Efficient Filtering**

   - Use specific filters to minimize the result set
   - Combine multiple filters for more precise results
   - Consider performance implications when retrieving large datasets

2. **Container Selection**

   - Use folder, snippet, or device consistently across operations
   - Verify container existence before querying
   - Use exclusion filters to refine results when working with large containers

3. **Using Results**

   - Register results to variables for further processing
   - Use Ansible's filtering capabilities (selectattr, map, etc.) on the returned lists
   - Check if addresses/address is defined before accessing properties

4. **Error Handling**

   - Implement proper error handling with block/rescue
   - Provide meaningful error messages
   - Have fallback actions when objects are not found

5. **Security Considerations**

   - Protect sensitive information in filter criteria
   - Store credentials securely using Ansible Vault
   - Limit information gathering to necessary objects only

## Related Modules

- [address](address.md) - Manage address objects (create, update, delete)
- [address_group_info](address_group_info.md) - Retrieve information about address groups
- [address_group](address_group.md) - Manage address group objects
- [tag_info](tag_info.md) - Retrieve information about tags used with address objects

## Author

- Calvin Remsburg (@cdot65)
