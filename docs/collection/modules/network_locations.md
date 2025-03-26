# Network Locations Configuration Object

## 1. Overview

The Network Locations module allows you to manage network location objects within Strata Cloud Manager (SCM). Network
locations represent geographic regions and are used for routing decisions, service connectivity, and resource
allocation. This module primarily provides read capabilities and limited management functions, as network locations are
often system-defined.

## 2. Core Methods

| Method    | Description                       | Parameters                | Return Type           |
|-----------|-----------------------------------|---------------------------|-----------------------|
| `list()`  | Lists available network locations | `filters: Dict[str, Any]` | `List[ResponseModel]` |
| `get()`   | Retrieves location by ID          | `location_id: str`        | `ResponseModel`       |
| `fetch()` | Retrieves location by value       | `value: str`              | `ResponseModel`       |

## 3. Model Attributes

| Attribute   | Type  | Description                                    |
|-------------|-------|------------------------------------------------|
| `id`        | str   | Unique identifier for the network location     |
| `value`     | str   | Location value/code (e.g., "us-east-1")        |
| `display`   | str   | Display name of the location (e.g., "US East") |
| `continent` | str   | Continent where the location is situated       |
| `country`   | str   | Country code where the location is situated    |
| `city`      | str   | City where the location is situated            |
| `state`     | str   | State/province where the location is situated  |
| `latitude`  | float | Latitude coordinates                           |
| `longitude` | float | Longitude coordinates                          |
| `tier`      | int   | Service tier of the location                   |
| `type`      | str   | Type of location ("default", "custom", etc.)   |
| `status`    | str   | Current status of the location                 |

## 4. Basic Usage

<div class="termy">

<!-- termynal -->

```yaml
- name: Get network locations
  cdot65.scm.network_locations_info:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
  register: locations

- name: Display available locations
  debug:
    var: locations.network_locations
```

</div>

## 5. Usage Examples

### Listing All Network Locations

<div class="termy">

<!-- termynal -->

```yaml
- name: List all network locations
  cdot65.scm.network_locations_info:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
  register: all_locations

- name: Display location information
  debug:
    msg: "{{ item.display }} ({{ item.value }}) - {{ item.continent }}, {{ item.country }}"
  loop: "{{ all_locations.network_locations }}"
```

</div>

### Filtering Network Locations by Continent

<div class="termy">

<!-- termynal -->

```yaml
- name: Get European network locations
  cdot65.scm.network_locations_info:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    continent: "Europe"
  register: europe_locations

- name: Display European locations
  debug:
    msg: "{{ europe_locations.network_locations | map(attribute='display') | list }}"
```

</div>

### Finding a Specific Location

<div class="termy">

<!-- termynal -->

```yaml
- name: Find specific network location
  cdot65.scm.network_locations_info:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    value: "us-east-1"
  register: location_info

- name: Display location details
  debug:
    var: location_info.network_locations[0]
  when: location_info.network_locations | length > 0
```

</div>

### Using Location Information in Other Resources

<div class="termy">

<!-- termynal -->

```yaml
- name: Get available network locations
  cdot65.scm.network_locations_info:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
  register: locations

- name: Set location variable
  set_fact:
    primary_location: "{{ locations.network_locations | selectattr('display', 'eq', 'US East') | map(attribute='value') | first }}"

- name: Configure remote network using location
  cdot65.scm.remote_networks:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "branch-office"
    region: "{{ primary_location }}"
    # Other parameters...
    state: "present"
```

</div>

## 6. Error Handling

<div class="termy">

<!-- termynal -->

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

</div>

## 7. Best Practices

1. **Location Selection**
    - Choose network locations based on geographic proximity to your users and resources
    - Consider latency requirements when selecting locations
    - Use locations with tier 1 for critical workloads for better performance

2. **Redundancy Planning**
    - Select multiple locations for redundancy
    - Choose locations in different geographic regions for disaster recovery
    - Understand the capabilities and limitations of each location

3. **Integration with Other Resources**
    - Use location information when configuring remote networks
    - Reference location values correctly in other resources
    - Validate location values before using them in configurations

4. **Automation**
    - Use variables or facts to store location information
    - Create a centralized location selection strategy
    - Document which locations are used and why

5. **Monitoring**
    - Regularly check the status of network locations
    - Have a plan for location unavailability
    - Automate failover to alternative locations when needed

## 8. Related Models

- [Remote Networks](remote_networks.md) - Configure remote networks in specific locations
- [BGP Routing](bgp_routing.md) - Configure routing preferences that may be location-dependent
- [Service Connections](service_connections.md) - Configure service connections in specific locations