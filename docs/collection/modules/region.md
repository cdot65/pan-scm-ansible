# Region Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
   - [Creating Region Objects](#creating-region-objects)
   - [Updating Region Objects](#updating-region-objects)
   - [Deleting Region Objects](#deleting-region-objects)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `region` module provides functionality to manage region objects in Palo Alto Networks' Strata
Cloud Manager. This module allows you to create, update, and delete region objects with geographic
locations and associated network addresses. Regions can be used to define geographic areas and their
associated networks for policy management.

!!! note Unlike other SCM objects, regions do not support 'description' or 'tag' fields. If these
fields are provided in the module parameters, they will be ignored by the SCM API.

## Module Parameters

| Parameter              | Required | Type  | Choices         | Default | Comments                                                     |
| ---------------------- | -------- | ----- | --------------- | ------- | ------------------------------------------------------------ |
| name                   | yes      | str   |                 |         | The name of the region object (max 31 chars).                |
| geo_location           | no       | dict  |                 |         | Geographic location of the region.                           |
| geo_location.latitude  | yes      | float |                 |         | The latitudinal position (must be between -90 and 90).       |
| geo_location.longitude | yes      | float |                 |         | The longitudinal position (must be between -180 and 180).    |
| address                | no       | list  |                 |         | List of IP addresses or networks associated with the region. |
| folder                 | no       | str   |                 |         | The folder in which the resource is defined (max 64 chars).  |
| snippet                | no       | str   |                 |         | The snippet in which the resource is defined (max 64 chars). |
| device                 | no       | str   |                 |         | The device in which the resource is defined (max 64 chars).  |
| provider               | yes      | dict  |                 |         | Authentication credentials.                                  |
| provider.client_id     | yes      | str   |                 |         | Client ID for authentication.                                |
| provider.client_secret | yes      | str   |                 |         | Client secret for authentication.                            |
| provider.tsg_id        | yes      | str   |                 |         | Tenant Service Group ID.                                     |
| provider.log_level     | no       | str   |                 | INFO    | Log level for the SDK.                                       |
| state                  | yes      | str   | present, absent |         | Desired state of the region object.                          |

!!! note

- Exactly one container type (`folder`, `snippet`, or `device`) must be provided.
- The geo_location's latitude must be between -90 and 90 degrees.
- The geo_location's longitude must be between -180 and 180 degrees.

## Requirements

## Requirements

- SCM Python SDK (`pan-scm-sdk>=0.3.22`)
- Python 3.12 or higher
- Ansible 2.17 or higher

## Usage Examples

### Creating Region Objects

```yaml
- name: Create a region with geo_location and addresses
  cdot65.scm.region:
    provider: "{{ provider }}"
    name: "us-west-region"
    geo_location:
      latitude: 37.7749
      longitude: -122.4194
    address:
      - "10.0.0.0/8"
      - "192.168.1.0/24"
    folder: "Global"
    state: "present"
```

```yaml
- name: Create a region with addresses only
  cdot65.scm.region:
    provider: "{{ provider }}"
    name: "internal-networks"
    address:
      - "172.16.0.0/16"
      - "192.168.0.0/16"
    folder: "Global"
    state: "present"
```

### Updating Region Objects

```yaml
- name: Update a region with new geo_location
  cdot65.scm.region:
    provider: "{{ provider }}"
    name: "us-west-region"
    geo_location:
      latitude: 40.7128
      longitude: -74.0060
    address:
      - "10.0.0.0/8"
      - "192.168.1.0/24"
      - "172.16.0.0/16"
    folder: "Global"
    state: "present"
```

### Deleting Region Objects

```yaml
- name: Delete a region
  cdot65.scm.region:
    provider: "{{ provider }}"
    name: "internal-networks"
    folder: "Global"
    state: "absent"
```

## Return Values

| Name    | Description                     | Type | Returned              | Sample                                                                                                                                                                                                   |
| ------- | ------------------------------- | ---- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| changed | Whether any changes were made   | bool | always                | true                                                                                                                                                                                                     |
| region  | Details about the region object | dict | when state is present | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "us-west-region", "geo_location": {"latitude": 37.7749, "longitude": -122.4194}, "address": ["10.0.0.0/8", "192.168.1.0/24"], "folder": "Global"} |

## Error Handling

Common errors you might encounter when using this module:

| Error                      | Description                                                 | Resolution                                                            |
| -------------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------- |
| Invalid geo_location data  | The latitude or longitude values are outside allowed ranges | Ensure latitude is between -90 and 90, longitude between -180 and 180 |
| Region name already exists | Attempt to create a region with a name that already exists  | Use a unique name or update the existing region                       |
| Region not found           | Attempt to update or delete a region that doesn't exist     | Verify the region name and container location                         |
| Missing required parameter | Required parameter not provided                             | Ensure all required parameters are specified                          |

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to create region
      cdot65.scm.region:
        provider: "{{ provider }}"
        name: "test_region"
        geo_location:
          latitude: 37.7749
          longitude: -122.4194
        folder: "Global"
        state: "present"
      register: result
  rescue:
    - name: Handle region already exists error
      debug:
        msg: "Region already exists or invalid input provided"
    - name: Continue with other tasks
      # Additional recovery tasks
```

## Best Practices

1. **Geographical Data Validation**

   - Always use valid latitude (-90 to 90) and longitude (-180 to 180) values
   - Use the appropriate level of precision for your geographic locations
   - Consider standardizing on a consistent coordinate format

2. **Container Management**

   - Always specify exactly one container (folder, snippet, or device)
   - Use consistent container names across operations
   - Validate container existence before operations

3. **Address Management**

   - Use standardized CIDR notation for network addresses
   - Organize related networks within the same region for easier management
   - Consider the policy implications of your region definitions

4. **Module Usage**

   - Use idempotent operations to safely run playbooks multiple times
   - Leverage check mode (`--check`) to preview changes before executing them
   - Implement proper error handling with block/rescue
   - Use consistent naming conventions for regions

5. **Performance Optimization**

   - Group related regions in the same folders
   - Use the region_info module to audit and manage existing regions

## Related Modules

- [region_info](region_info.md) - Retrieve information about region objects
- [address](address.md) - Manage address objects used within regions
- [address_group](address_group.md) - Manage address group objects
- [security_rule](security_rule.md) - Manage security rules that can use region-based criteria

## Author

- Calvin Remsburg (@cdot65)
