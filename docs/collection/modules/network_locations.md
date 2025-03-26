# Network Locations Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Network Locations Model Attributes](#network-locations-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Listing All Network Locations](#listing-all-network-locations)
    - [Filtering Network Locations by Continent](#filtering-network-locations-by-continent)
    - [Finding a Specific Location](#finding-a-specific-location)
    - [Using Location Information in Other Resources](#using-location-information-in-other-resources)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `network_locations` Ansible module provides functionality to manage network location objects
within Palo Alto Networks' Strata Cloud Manager (SCM). Network locations represent geographic
regions and are used for routing decisions, service connectivity, and resource allocation. This
module primarily provides read capabilities and limited management functions, as network locations
are often system-defined.

## Core Methods

| Method    | Description                       | Parameters                | Return Type                  |
| --------- | --------------------------------- | ------------------------- | ---------------------------- |
| `list()`  | Lists available network locations | `filters: Dict[str, Any]` | `List[NetworkLocationModel]` |
| `get()`   | Retrieves location by ID          | `location_id: str`        | `NetworkLocationModel`       |
| `fetch()` | Retrieves location by value       | `value: str`              | `NetworkLocationModel`       |

## Network Locations Model Attributes

| Attribute   | Type  | Required | Description                                    |
| ----------- | ----- | -------- | ---------------------------------------------- |
| `id`        | str   | System   | Unique identifier for the network location     |
| `value`     | str   | System   | Location value/code (e.g., "us-east-1")        |
| `display`   | str   | System   | Display name of the location (e.g., "US East") |
| `continent` | str   | System   | Continent where the location is situated       |
| `country`   | str   | System   | Country code where the location is situated    |
| `city`      | str   | System   | City where the location is situated            |
| `state`     | str   | System   | State/province where the location is situated  |
| `latitude`  | float | System   | Latitude coordinates                           |
| `longitude` | float | System   | Longitude coordinates                          |
| `tier`      | int   | System   | Service tier of the location                   |
| `type`      | str   | System   | Type of location ("default", "custom", etc.)   |
| `status`    | str   | System   | Current status of the location                 |

## Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid request data or format |
| `MissingQueryParameterError` | Missing required parameters    |
| `ObjectNotPresentError`      | Network location not found     |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The Network Locations module requires proper authentication credentials to access the Strata Cloud
Manager API.

```yaml
- name: Basic Network Locations Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get network locations
      cdot65.scm.network_locations_info:
        provider: "{{ provider }}"
      register: locations
    
    - name: Display available locations
      debug:
        var: locations.network_locations
```

## Usage Examples

### Listing All Network Locations

This example retrieves and displays all available network locations in the SCM environment.

```yaml
- name: List all network locations
  cdot65.scm.network_locations_info:
    provider: "{{ provider }}"
  register: all_locations

- name: Display location information
  debug:
    msg: "{{ item.display }} ({{ item.value }}) - {{ item.continent }}, {{ item.country }}"
  loop: "{{ all_locations.network_locations }}"
```

### Filtering Network Locations by Continent

This example retrieves network locations within a specific continent.

```yaml
- name: Get European network locations
  cdot65.scm.network_locations_info:
    provider: "{{ provider }}"
    continent: "Europe"
  register: europe_locations

- name: Display European locations
  debug:
    msg: "{{ europe_locations.network_locations | map(attribute='display') | list }}"
```

### Finding a Specific Location

This example searches for a specific network location by its value code.

```yaml
- name: Find specific network location
  cdot65.scm.network_locations_info:
    provider: "{{ provider }}"
    value: "us-east-1"
  register: location_info

- name: Display location details
  debug:
    var: location_info.network_locations[0]
  when: location_info.network_locations | length > 0
```

### Using Location Information in Other Resources

This example demonstrates how to use network location information to configure other resources.

```yaml
- name: Get available network locations
  cdot65.scm.network_locations_info:
    provider: "{{ provider }}"
  register: locations

- name: Set location variable
  set_fact:
    primary_location: "{{ locations.network_locations | selectattr('display', 'eq', 'US East') | map(attribute='value') | first }}"

- name: Configure remote network using location
  cdot65.scm.remote_networks:
    provider: "{{ provider }}"
    name: "branch-office"
    region: "{{ primary_location }}"
    # Other parameters...
    state: "present"
```

## Managing Configuration Changes

For information modules like `network_locations_info`, no commit is needed since these modules only
retrieve information and do not modify the configuration. However, you may need to commit changes if
you use the retrieved information to make configuration changes with other modules.

```yaml
- name: Use network location information and configure remote networks
  block:
    - name: Get network locations
      cdot65.scm.network_locations_info:
        provider: "{{ provider }}"
      register: locations
      
    - name: Configure remote networks
      cdot65.scm.remote_networks:
        provider: "{{ provider }}"
        name: "branch-office-{{ item.display | replace(' ', '-') | lower }}"
        region: "{{ item.value }}"
        # Other parameters...
        state: "present"
      loop: "{{ locations.network_locations | selectattr('continent', 'eq', 'North America') | list }}"
      register: remote_networks_result
      
    - name: Commit changes if remote networks were created
      cdot65.scm.commit:
        provider: "{{ provider }}"
        description: "Created remote networks in North American locations"
      when: remote_networks_result is changed
```

## Error Handling

It's important to handle potential errors when working with network locations.

```yaml
- name: Get network location with error handling
  block:
    - name: Attempt to get location information
      cdot65.scm.network_locations_info:
        provider: "{{ provider }}"
        value: "non-existent-location"
      register: location_result

    - name: Verify location exists
      assert:
        that: 
          - location_result.network_locations | length > 0
        fail_msg: "Specified location does not exist"
        success_msg: "Location found"
  rescue:
    - name: Handle error
      debug:
        msg: "Location not found. Using default location instead."

    - name: Use default location
      set_fact:
        location_value: "us-east-1"
```

## Best Practices

### Location Selection

- Choose network locations based on geographic proximity to your users and resources
- Consider latency requirements when selecting locations
- Use locations with tier 1 designation for critical workloads requiring better performance
- Balance cost considerations with performance needs when selecting locations
- Verify location availability before configuration

### Redundancy Planning

- Select multiple locations for redundancy and high availability
- Choose locations in different geographic regions for disaster recovery
- Understand the capabilities and limitations of each location
- Implement appropriate failover mechanisms between locations
- Test failover scenarios regularly to ensure reliability

### Integration with Other Resources

- Use location information when configuring remote networks
- Reference location values correctly in other resources
- Validate location values before using them in configurations
- Document location dependencies for each resource
- Consider creating location groups for similar geographic regions

### Automation

- Use variables or facts to store location information
- Create a centralized location selection strategy
- Document which locations are used and why
- Implement location selection logic based on business requirements
- Create playbooks that handle location-specific configurations

### Monitoring

- Regularly check the status of network locations
- Have a plan for location unavailability
- Automate failover to alternative locations when needed
- Monitor performance metrics for each location
- Adjust location selection based on performance data

## Related Modules

- [remote_networks](remote_networks.md) - Configure remote networks in specific locations
- [bgp_routing](bgp_routing.md) - Configure routing preferences that may be location-dependent
- [service_connections](service_connections.md) - Configure service connections in specific
  locations
- [region](region.md) - Configure regions that may include multiple network locations
- [region_info](region_info.md) - Retrieve information about configured regions
