# Region Information Object

## Table of Contents

- [Region Information Object](#region-information-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Module Parameters](#module-parameters)
  - [Requirements](#requirements)
  - [Requirements](#requirements-1)
  - [Usage Examples](#usage-examples)
    - [Retrieving a Specific Region](#retrieving-a-specific-region)
    - [Listing All Regions](#listing-all-regions)
    - [Filtering by Geographic Location](#filtering-by-geographic-location)
    - [Filtering by Addresses](#filtering-by-addresses)
    - [Using Advanced Filters](#using-advanced-filters)
  - [Return Values](#return-values)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
  - [Related Modules](#related-modules)
  - [Author](#author)

## Overview

The `region_info` module provides functionality to retrieve information about region objects in Palo
Alto Networks' Strata Cloud Manager. This module allows you to fetch details about specific regions
by name or list multiple regions using various filter criteria, including geographic location ranges
and network addresses.

## Module Parameters

| Parameter                  | Required | Type  | Choices     | Default    | Comments                                                                   |
| -------------------------- | -------- | ----- | ----------- | ---------- | -------------------------------------------------------------------------- |
| name                       | no       | str   |             |            | The name of a specific region to retrieve.                                 |
| gather_subset              | no       | list  | all, config | ['config'] | Determines which information to gather about regions.                      |
| folder                     | no       | str   |             |            | Filter regions by folder container.                                        |
| snippet                    | no       | str   |             |            | Filter regions by snippet container.                                       |
| device                     | no       | str   |             |            | Filter regions by device container.                                        |
| exact_match                | no       | bool  |             | false      | When true, only return objects defined exactly in the specified container. |
| exclude_folders            | no       | list  |             |            | List of folder names to exclude from results.                              |
| exclude_snippets           | no       | list  |             |            | List of snippet values to exclude from results.                            |
| exclude_devices            | no       | list  |             |            | List of device values to exclude from results.                             |
| geo_location               | no       | dict  |             |            | Filter by geographic location range.                                       |
| geo_location.latitude      | no       | dict  |             |            | Latitude range for filtering.                                              |
| geo_location.latitude.min  | yes      | float |             |            | Minimum latitude value (range -90 to 90).                                  |
| geo_location.latitude.max  | yes      | float |             |            | Maximum latitude value (range -90 to 90).                                  |
| geo_location.longitude     | no       | dict  |             |            | Longitude range for filtering.                                             |
| geo_location.longitude.min | yes      | float |             |            | Minimum longitude value (range -180 to 180).                               |
| geo_location.longitude.max | yes      | float |             |            | Maximum longitude value (range -180 to 180).                               |
| addresses                  | no       | list  |             |            | Filter by addresses included in regions.                                   |
| provider                   | yes      | dict  |             |            | Authentication credentials.                                                |
| provider.client_id         | yes      | str   |             |            | Client ID for authentication.                                              |
| provider.client_secret     | yes      | str   |             |            | Client secret for authentication.                                          |
| provider.tsg_id            | yes      | str   |             |            | Tenant Service Group ID.                                                   |
| provider.log_level         | no       | str   |             | INFO       | Log level for the SDK.                                                     |

!!! note

- When fetching a specific region by name, a container parameter (`folder`, `snippet`, or `device`)
  is recommended.
- When listing regions, one container parameter is required.
- The geographic filtering ranges must use valid latitude (-90 to 90) and longitude (-180 to 180)
  values.

## Requirements

## Requirements

- SCM Python SDK (`pan-scm-sdk>=0.3.22`)
- Python 3.12 or higher
- Ansible 2.17 or higher

## Usage Examples

### Retrieving a Specific Region

```yaml
- name: Get information about a specific region
  cdot65.scm.region_info:
    provider: "{{ provider }}"
    name: "us-west-region"
    folder: "Global"
  register: region_info
```

### Listing All Regions

```yaml
- name: List all region objects in a folder
  cdot65.scm.region_info:
    provider: "{{ provider }}"
    folder: "Global"
  register: all_regions
```

### Filtering by Geographic Location

```yaml
- name: List regions with geographic filtering (west coast US)
  cdot65.scm.region_info:
    provider: "{{ provider }}"
    folder: "Global"
    geo_location:
      latitude:
        min: 30
        max: 50
      longitude:
        min: -130
        max: -110
  register: west_coast_regions
```

### Filtering by Addresses

```yaml
- name: List regions with specific addresses
  cdot65.scm.region_info:
    provider: "{{ provider }}"
    folder: "Global"
    addresses: ["10.0.0.0/8"]
  register: network_regions
```

### Using Advanced Filters

```yaml
- name: List regions with exact match and exclusions
  cdot65.scm.region_info:
    provider: "{{ provider }}"
    folder: "Global"
    exact_match: true
    exclude_folders: ["Test", "Development"]
  register: filtered_regions
```

## Return Values

| Name    | Description                                                                               | Type | Returned                   | Sample                                                                                                                                                                                                   |
| ------- | ----------------------------------------------------------------------------------------- | ---- | -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| region  | Information about the requested region (returned when name is specified)                  | dict | when name is specified     | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "us-west-region", "geo_location": {"latitude": 37.7749, "longitude": -122.4194}, "address": ["10.0.0.0/8", "192.168.1.0/24"], "folder": "Global"} |
| regions | List of region objects matching the filter criteria (returned when name is not specified) | list | when name is not specified | [{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "us-west-region", ...}, {"id": "234e5678-e89b-12d3-a456-426655440001", "name": "internal-networks", ...}]                                        |

## Error Handling

Common errors you might encounter when using this module:

| Error                       | Description                                                   | Resolution                                                            |
| --------------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------- |
| Invalid geo_location filter | The latitude or longitude values are outside allowed ranges   | Ensure latitude is between -90 and 90, longitude between -180 and 180 |
| Region not found            | Attempt to retrieve a region that doesn't exist               | Verify the region name and container location                         |
| Missing container parameter | No container parameter provided for listing operations        | Specify at least one container parameter (folder, snippet, device)    |
| Invalid filter parameters   | The filter parameters are malformed or contain invalid values | Check the format and values of the filter parameters                  |

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to retrieve region information
      cdot65.scm.region_info:
        provider: "{{ provider }}"
        name: "us-west-region" 
        folder: "Global"
      register: result
  rescue:
    - name: Handle region not found error
      debug:
        msg: "Region not found or invalid input provided"
    - name: Continue with other tasks
      # Additional recovery tasks
```

## Best Practices

1. **Efficient Filtering**

   - Use the most specific filters possible to reduce result set size
   - Combine multiple filters for more precise results
   - Consider using the `exact_match` parameter when searching within containers

2. **Geographic Filtering**

   - Use appropriate latitude and longitude ranges for the target area
   - Consider the precision needed for your geographic queries
   - Use smaller range windows for more precise results

3. **Address Filtering**

   - Use standardized CIDR notation for network addresses
   - Be aware that address filtering matches if any address in the region matches

4. **Performance Considerations**

   - Be specific with container parameters to limit search scope
   - Use exclusion lists to filter out known irrelevant containers
   - Consider pagination for large result sets (gathering subsets)

5. **Result Processing**

   - Use registration of results for post-processing and reporting
   - Leverage Ansible's filters to extract specific information from results
   - Consider using `debug` with appropriate verbosity levels

## Related Modules

- [region](region.md) - Create, update, and delete region objects
- [address_info](address_info.md) - Retrieve information about address objects
- [address_group_info](address_group_info.md) - Retrieve information about address group objects
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules that may
  use regions

## Author

- Calvin Remsburg (@cdot65)
