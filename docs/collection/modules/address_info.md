# Address Info

## Synopsis

Gather information about address objects in Strata Cloud Manager (SCM).

## Parameters

| Parameter              | Required | Type | Choices | Default | Comments                                                                        |
|------------------------|----------|------|---------|---------|---------------------------------------------------------------------------------|
| name                   | no       | str  |         |         | The name of a specific address object to retrieve.                              |
| folder                 | no       | str  |         |         | Filter addresses by folder container.                                           |
| snippet                | no       | str  |         |         | Filter addresses by snippet container.                                          |
| device                 | no       | str  |         |         | Filter addresses by device container.                                           |
| exact_match            | no       | bool |         | false   | When True, only return objects defined exactly in the specified container.      |
| exclude_folders        | no       | list |         |         | List of folder names to exclude from results.                                   |
| exclude_snippets       | no       | list |         |         | List of snippet values to exclude from results.                                 |
| exclude_devices        | no       | list |         |         | List of device values to exclude from results.                                  |
| types                  | no       | list |         |         | Filter by address types. Valid choices: "netmask", "range", "wildcard", "fqdn". |
| values                 | no       | list |         |         | Filter by address values.                                                       |
| tags                   | no       | list |         |         | Filter by tags.                                                                 |
| provider               | yes      | dict |         |         | Authentication credentials.                                                     |
| provider.client_id     | yes      | str  |         |         | Client ID for authentication.                                                   |
| provider.client_secret | yes      | str  |         |         | Client secret for authentication.                                               |
| provider.tsg_id        | yes      | str  |         |         | Tenant Service Group ID.                                                        |
| provider.log_level     | no       | str  |         | INFO    | Log level for the SDK.                                                          |

> **Note**:
>
> - Exactly one container type (`folder`, `snippet`, or `device`) must be provided.
> - When `name` is specified, the module will retrieve a single address object.
> - When `name` is not specified, the module will return a list of addresses based on filter criteria.

## Requirements

- SCM Python SDK

## Examples

### Get information about a specific address

```yaml
- name: Get information about a specific address
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    name: "web-server"
    folder: "Texas"
  register: address_info
```

### List all address objects in a folder

```yaml
- name: List all address objects in a folder
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_addresses
```

### List only FQDN address objects

```yaml
- name: List only FQDN address objects
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
    types: [ "fqdn" ]
  register: fqdn_addresses
```

### List addresses with specific tags

```yaml
- name: List addresses with specific tags
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: [ "Production", "Web" ]
  register: tagged_addresses
```

### List addresses with exact match and exclusions

```yaml
- name: List addresses with exact match and exclusions
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: [ "All" ]
    exclude_snippets: [ "default" ]
  register: filtered_addresses
```

## Return Values

| Name      | Description                                          | Type | Returned                            | Sample                                                                                                                                                                                                                                                                                                                                                                                               |
|-----------|------------------------------------------------------|------|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| addresses | List of address objects matching the filter criteria | list | success, when name is not specified | [{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-server", "description": "Web server address", "ip_netmask": "192.168.1.100/32", "folder": "Texas", "tag": ["Web", "Production"]}, {"id": "234e5678-e89b-12d3-a456-426655440001", "name": "app-server", "description": "Application server address", "ip_netmask": "192.168.1.101/32", "folder": "Texas", "tag": ["App", "Production"]}] |
| address   | Information about the requested address              | dict | success, when name is specified     | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "web-server", "description": "Web server address", "ip_netmask": "192.168.1.100/32", "folder": "Texas", "tag": ["Web", "Production"]}                                                                                                                                                                                                         |

## Author

- Calvin Remsburg (@cdot65)
