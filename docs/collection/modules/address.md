# address

Manage address objects in Palo Alto Networks Strata Cloud Manager.

## Synopsis

The `address` module allows you to create, update, and delete address objects in SCM.

Address objects are used to identify hosts and networks in security rules, NAT policies, and other configuration objects.

## Requirements

- `pan-scm-sdk` Python package
- Authentication credentials for Strata Cloud Manager

## Parameters

| Parameter | Type | Required | Default | Choices | Description |
|-----------|------|----------|---------|---------|-------------|
| `name` | string | yes | | | Name of the address object |
| `folder` | string | yes | | | SCM folder path where the address object is located |
| `description` | string | no | | | Description for the address object |
| `ip_netmask` | string | no | | | IPv4 or IPv6 address with CIDR (e.g., "192.168.1.1/32") |
| `ip_range` | string | no | | | IP address range (e.g., "192.168.1.1-192.168.1.10") |
| `fqdn` | string | no | | | Fully qualified domain name |
| `tags` | list | no | | | List of tags to apply to the address object |
| `state` | string | no | present | present, absent | Desired state of the address object |
| `username` | string | no | | | SCM username (can use environment variable) |
| `password` | string | no | | | SCM password (can use environment variable) |
| `tenant` | string | no | | | SCM tenant ID (can use environment variable) |

**Note**: You must specify exactly one of `ip_netmask`, `ip_range`, or `fqdn` for address objects.

## Examples

### Create an IPv4 address object

```yaml
- name: Create an IPv4 address object
  cdot65.scm.address:
    name: "web-server"
    folder: "SharedFolder"
    description: "Web server address"
    ip_netmask: "10.1.1.1/32"
    tags:
      - "web-servers"
      - "production"
```

### Create an IP range address object

```yaml
- name: Create an IP range address object
  cdot65.scm.address:
    name: "dhcp-pool"
    folder: "SharedFolder" 
    description: "DHCP address range"
    ip_range: "10.1.1.100-10.1.1.200"
```

### Create an FQDN address object

```yaml
- name: Create an FQDN address object
  cdot65.scm.address:
    name: "company-website"
    folder: "SharedFolder"
    description: "Company website"
    fqdn: "www.example.com"
```

### Delete an address object

```yaml
- name: Delete an address object
  cdot65.scm.address:
    name: "old-server"
    folder: "SharedFolder"
    state: absent
```

## Return Values

| Name | Description | Type | Sample |
|------|-------------|------|--------|
| `changed` | Whether changes were made | boolean | `true` |
| `scm_object` | The SCM address object details | dictionary | `{"id": "123", "name": "web-server", "type": "IP_NETMASK", "value": "10.1.1.1/32"}` |
| `response` | The raw API response | dictionary | `{"status": "success", "data": {...}}` |

## Notes

- Address object names must be unique within a folder
- For security best practices, use environment variables for authentication credentials
- This module is idempotent; running it multiple times with the same parameters will result in the same state

## Status

This module is flagged as **stable**
