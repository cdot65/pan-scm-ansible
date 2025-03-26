# Address Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Address Model Attributes](#address-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating Address Objects](#creating-address-objects)
    - [Basic IP/Netmask Address](#basic-ipnetmask-address)
    - [IP Range Address](#ip-range-address)
    - [IP Wildcard Address](#ip-wildcard-address)
    - [FQDN Address](#fqdn-address)
    - [Updating Address Objects](#updating-address-objects)
    - [Deleting Address Objects](#deleting-address-objects)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `address` Ansible module provides functionality to manage address objects in Palo Alto Networks' Strata 
Cloud Manager (SCM). This module allows you to create, update, and delete address objects of various types 
including IP/Netmask, IP Range, IP Wildcard, and FQDN (Fully Qualified Domain Name).

## Core Methods

| Method     | Description                    | Parameters                     | Return Type                 |
| ---------- | ------------------------------ | ------------------------------ | --------------------------- |
| `create()` | Creates a new address object   | `data: Dict[str, Any]`         | `AddressResponseModel`      |
| `update()` | Updates an existing address    | `address: AddressUpdateModel`  | `AddressResponseModel`      |
| `delete()` | Removes an address             | `object_id: str`               | `None`                      |
| `fetch()`  | Gets an address by name        | `name: str`, `container: str`  | `AddressResponseModel`      |
| `list()`   | Lists addresses with filtering | `folder: str`, `**filters`     | `List[AddressResponseModel]`|

## Address Model Attributes

| Attribute      | Type | Required      | Description                                               |
| -------------- | ---- | ------------- | --------------------------------------------------------- |
| `name`         | str  | Yes           | The name of the address object (max 63 chars)             |
| `description`  | str  | No            | Description of the address object (max 1023 chars)        |
| `tag`          | list | No            | List of tags associated with the address object           |
| `fqdn`         | str  | One type only | Fully Qualified Domain Name (max 255 chars)               |
| `ip_netmask`   | str  | One type only | IP address with CIDR notation (e.g. "192.168.1.0/24")     |
| `ip_range`     | str  | One type only | IP address range (e.g. "192.168.1.100-192.168.1.200")     |
| `ip_wildcard`  | str  | One type only | IP wildcard mask format (e.g. "10.20.1.0/0.0.248.255")    |
| `folder`       | str  | One container | The folder in which the address is defined (max 64 chars) |
| `snippet`      | str  | One container | The snippet in which the address is defined (max 64 chars)|
| `device`       | str  | One container | The device in which the address is defined (max 64 chars) |

## Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid address data or format |
| `NameNotUniqueError`         | Address name already exists    |
| `ObjectNotPresentError`      | Address not found              |
| `MissingQueryParameterError` | Missing required parameters    |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The Address module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Address Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure an IP/Netmask address exists
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "Web-Server"
        description: "Web server network"
        folder: "Texas"
        ip_netmask: "192.168.1.0/24"
        tag: ["Web", "Internal"]
        state: "present"
```

## Usage Examples

### Creating Address Objects

Address objects can be created with different types to match specific network addressing needs.

### Basic IP/Netmask Address

This example creates a simple address object with an IP/Netmask.

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

### IP Range Address

This example creates an address object with an IP range.

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

### IP Wildcard Address

This example creates an address object with an IP wildcard mask.

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

### FQDN Address

This example creates an address object with a fully qualified domain name.

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

### Updating Address Objects

This example updates an existing address object with a new description and tags.

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

### Deleting Address Objects

This example removes an address object.

```yaml
- name: Delete address object
  cdot65.scm.address:
    provider: "{{ provider }}"
    name: "Test_Address_FQDN"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting address objects, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated address objects"
```

## Error Handling

It's important to handle potential errors when working with address objects.

```yaml
- name: Create or update address object with error handling
  block:
    - name: Ensure address object exists
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "Web-Server"
        description: "Web server network"
        folder: "Texas"
        ip_netmask: "192.168.1.0/24"
        tag: ["Web", "Internal"]
        state: "present"
      register: address_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated address objects"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```

## Best Practices

### Address Type Selection

- Choose the appropriate address type for your specific use case
- Use IP/Netmask for subnets and network segments
- Use IP Range when specific ranges of addresses need to be defined
- Use IP Wildcard for more complex network matching requirements
- Use FQDN for domain-based addressing that may resolve to different IPs

### Container Management

- Always specify exactly one container (folder, snippet, or device)
- Use consistent container names across operations
- Validate container existence before operations

### Using Tags

- Leverage tags for classification and filtering
- Keep tag names consistent across objects
- Consider creating tag conventions (environment, purpose, etc.)

### Naming Conventions

- Develop a consistent naming convention for address objects
- Make names descriptive of the address's purpose or location
- Use a consistent format like "Location-Function-Number"
- Document naming standards for team consistency

### Module Usage

- Use idempotent operations to safely run playbooks multiple times
- Leverage check mode (`--check`) to preview changes before executing them
- Implement proper error handling with block/rescue
- Generate unique names when creating multiple similar objects

### Performance Optimization

- Use loops efficiently when creating multiple address objects
- Consider using roles for standardized address object creation
- Organize related address objects in the same folders

## Related Modules

- [address_info](address_info.md) - Retrieve information about address objects
- [address_group](address_group.md) - Manage address group objects
- [tag](tag.md) - Manage tags used with address objects
- [security_rule](security_rule.md) - Manage security rules that use address objects