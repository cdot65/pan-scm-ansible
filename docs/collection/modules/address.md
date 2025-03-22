# Address

## Synopsis

Manage address objects in Strata Cloud Manager (SCM).

## Parameters

| Parameter              | Required | Type | Choices         | Default | Comments                                                             |
|------------------------|----------|------|-----------------|---------|----------------------------------------------------------------------|
| name                   | yes      | str  |                 |         | The name of the address object (max 63 chars).                       |
| description            | no       | str  |                 |         | Description of the address object (max 1023 chars).                  |
| tag                    | no       | list |                 |         | List of tags associated with the address object (max 64 chars each). |
| fqdn                   | no       | str  |                 |         | Fully Qualified Domain Name (FQDN) of the address (max 255 chars).   |
| ip_netmask             | no       | str  |                 |         | IP address with CIDR notation (e.g. "192.168.1.0/24").               |
| ip_range               | no       | str  |                 |         | IP address range (e.g. "192.168.1.100-192.168.1.200").               |
| ip_wildcard            | no       | str  |                 |         | IP wildcard mask format (e.g. "10.20.1.0/0.0.248.255").              |
| folder                 | no       | str  |                 |         | The folder in which the resource is defined (max 64 chars).          |
| snippet                | no       | str  |                 |         | The snippet in which the resource is defined (max 64 chars).         |
| device                 | no       | str  |                 |         | The device in which the resource is defined (max 64 chars).          |
| provider               | yes      | dict |                 |         | Authentication credentials.                                          |
| provider.client_id     | yes      | str  |                 |         | Client ID for authentication.                                        |
| provider.client_secret | yes      | str  |                 |         | Client secret for authentication.                                    |
| provider.tsg_id        | yes      | str  |                 |         | Tenant Service Group ID.                                             |
| provider.log_level     | no       | str  |                 | INFO    | Log level for the SDK.                                               |
| state                  | yes      | str  | present, absent |         | Desired state of the address object.                                 |

> **Note**:
>
> - Exactly one address type (`ip_netmask`, `ip_range`, `ip_wildcard`, or `fqdn`) must be provided when state is
    present.
> - Exactly one container type (`folder`, `snippet`, or `device`) must be provided.

## Requirements

- SCM Python SDK

## Examples

### Create an address object with ip_netmask

```yaml
- name: Create an address object with ip_netmask
  cdot65.scm.address:
    provider: "{{ provider }}"
    name: "Test_Address_Netmask"
    description: "An address object with ip_netmask"
    ip_netmask: "192.168.1.0/24"
    folder: "Texas"
    tag: [ "Network", "Internal" ]
    state: "present"
```

### Create an address object with ip_range

```yaml
- name: Create an address object with ip_range
  cdot65.scm.address:
    provider: "{{ provider }}"
    name: "Test_Address_Range"
    description: "An address object with ip_range"
    ip_range: "192.168.2.1-192.168.2.254"
    folder: "Texas"
    state: "present"
```

### Create an address object with ip_wildcard

```yaml
- name: Create an address object with ip_wildcard
  cdot65.scm.address:
    provider: "{{ provider }}"
    name: "Test_Address_Wildcard"
    description: "An address object with ip_wildcard"
    ip_wildcard: "10.20.1.0/0.0.248.255"
    folder: "Texas"
    state: "present"
```

### Create an address object with fqdn

```yaml
- name: Create an address object with fqdn
  cdot65.scm.address:
    provider: "{{ provider }}"
    name: "Test_Address_FQDN"
    description: "An address object with fqdn"
    fqdn: "example.com"
    folder: "Texas"
    state: "present"
```

### Update an address object with new description and tags

```yaml
- name: Update an address object with new description and tags
  cdot65.scm.address:
    provider: "{{ provider }}"
    name: "Test_Address_Netmask"
    description: "Updated description for netmask address"
    ip_netmask: "192.168.1.0/24"
    folder: "Texas"
    tag: [ "Network", "Internal", "Updated" ]
    state: "present"
```

### Delete an address object

```yaml
- name: Delete address object
  cdot65.scm.address:
    provider: "{{ provider }}"
    name: "Test_Address_FQDN"
    folder: "Texas"
    state: "absent"
```

## Return Values

| Name    | Description                      | Type | Returned              | Sample                                                                                                                                                                                                                |
|---------|----------------------------------|------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| changed | Whether any changes were made    | bool | always                | true                                                                                                                                                                                                                  |
| address | Details about the address object | dict | when state is present | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Test_Address_Netmask", "description": "An address object with ip_netmask", "ip_netmask": "192.168.1.0/24", "folder": "Texas", "tag": ["Network", "Internal"]} |

## Author

- Calvin Remsburg (@cdot65)
