# Address Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
    - [Creating Address Objects](#creating-address-objects)
    - [Updating Address Objects](#updating-address-objects)
    - [Deleting Address Objects](#deleting-address-objects)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `address` module provides functionality to manage address objects in Palo Alto Networks' Strata Cloud Manager. This 
module allows you to create, update, and delete address objects of various types including IP/Netmask, IP Range, 
IP Wildcard, and FQDN (Fully Qualified Domain Name).

## Module Parameters

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

!!! note
    - Exactly one address type (`ip_netmask`, `ip_range`, `ip_wildcard`, or `fqdn`) must be provided when state is present.
    - Exactly one container type (`folder`, `snippet`, or `device`) must be provided.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Creating Address Objects

<div class="termy">

<!-- termynal -->

```yaml
- name: Create an address object with ip_netmask
  cdot65.scm.address:
    provider: "{{ provider }}"
    name: "Test_Address_Netmask"
    description: "An address object with ip_netmask"
    ip_netmask: "192.168.1.0/24"
    folder: "Texas"
    tag: ["Network", "Internal"]
    state: "present"
```

</div>

<div class="termy">

<!-- termynal -->

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

</div>

<div class="termy">

<!-- termynal -->

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

</div>

<div class="termy">

<!-- termynal -->

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

</div>

### Updating Address Objects

<div class="termy">

<!-- termynal -->

```yaml
- name: Update an address object with new description and tags
  cdot65.scm.address:
    provider: "{{ provider }}"
    name: "Test_Address_Netmask"
    description: "Updated description for netmask address"
    ip_netmask: "192.168.1.0/24"
    folder: "Texas"
    tag: ["Network", "Internal", "Updated"]
    state: "present"
```

</div>

### Deleting Address Objects

<div class="termy">

<!-- termynal -->

```yaml
- name: Delete address object
  cdot65.scm.address:
    provider: "{{ provider }}"
    name: "Test_Address_FQDN"
    folder: "Texas"
    state: "absent"
```

</div>

## Return Values

| Name    | Description                      | Type | Returned              | Sample                                                                                                                                                                                                                |
|---------|----------------------------------|------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| changed | Whether any changes were made    | bool | always                | true                                                                                                                                                                                                                  |
| address | Details about the address object | dict | when state is present | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Test_Address_Netmask", "description": "An address object with ip_netmask", "ip_netmask": "192.168.1.0/24", "folder": "Texas", "tag": ["Network", "Internal"]} |

## Error Handling

Common errors you might encounter when using this module:

| Error | Description | Resolution |
|-------|-------------|------------|
| Invalid address data | The address parameters don't match required formats | Verify the format of address values (e.g., correct CIDR notation) |
| Address name already exists | Attempt to create an address with a name that already exists | Use a unique name or update the existing address |
| Address not found | Attempt to update or delete an address that doesn't exist | Verify the address name and container location |
| Missing required parameter | Required parameter not provided | Ensure all required parameters are specified |

<div class="termy">

<!-- termynal -->

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to create address
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "test_address"
        ip_netmask: "192.168.1.0/24"
        folder: "Texas"
        state: "present"
      register: result
  rescue:
    - name: Handle address already exists error
      debug:
        msg: "Address already exists or invalid input provided"
    - name: Continue with other tasks
      # Additional recovery tasks
```

</div>

## Best Practices

1. **Container Management**
   - Always specify exactly one container (folder, snippet, or device)
   - Use consistent container names across operations
   - Validate container existence before operations

2. **Address Types**
   - Specify exactly one address type per object
   - Use appropriate address format for each type
   - Validate address formats before creation

3. **Using Tags**
   - Leverage tags for classification and filtering
   - Keep tag names consistent across objects
   - Consider creating tag conventions (environment, purpose, etc.)

4. **Module Usage**
   - Use idempotent operations to safely run playbooks multiple times
   - Leverage check mode (`--check`) to preview changes before executing them
   - Implement proper error handling with block/rescue
   - Generate unique names when creating multiple similar objects

5. **Performance Optimization**
   - Use loops efficiently when creating multiple address objects
   - Consider using roles for standardized address object creation
   - Organize related address objects in the same folders

## Related Modules

- [address_info](address_info.md) - Retrieve information about address objects
- [address_group](address_group.md) - Manage address group objects
- [tag](tag.md) - Manage tags used with address objects
- [security_rule](security_rule.md) - Manage security rules that use address objects

## Author

- Calvin Remsburg (@cdot65)