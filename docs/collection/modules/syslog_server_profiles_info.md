# Syslog Server Profiles Information

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
    - [Retrieving a Specific Syslog Server Profile](#retrieving-a-specific-syslog-server-profile)
    - [Listing Syslog Server Profiles](#listing-syslog-server-profiles)
    - [Filtering Syslog Server Profiles](#filtering-syslog-server-profiles)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `syslog_server_profiles_info` module provides functionality to retrieve information about syslog server profile objects in Palo Alto Networks' Strata Cloud Manager. This module allows you to fetch details about a specific syslog server profile by name or list multiple profiles with various filtering options.

## Module Parameters

| Parameter          | Required | Type     | Choices        | Default     | Comments                                                             |
|--------------------|----------|----------|---------------|-------------|----------------------------------------------------------------------|
| name               | no       | str      |               |             | The name of a specific syslog server profile to retrieve.             |
| gather_subset      | no       | list     | all, config   | ['config']  | Determines which information to gather about syslog server profiles.  |
| folder             | no*      | str      |               |             | Filter syslog server profiles by folder container.                    |
| snippet            | no*      | str      |               |             | Filter syslog server profiles by snippet container.                   |
| device             | no*      | str      |               |             | Filter syslog server profiles by device container.                    |
| exact_match        | no       | bool     |               | false       | When True, only return objects defined exactly in the container.      |
| exclude_folders    | no       | list     |               |             | List of folder names to exclude from results.                         |
| exclude_snippets   | no       | list     |               |             | List of snippet values to exclude from results.                       |
| exclude_devices    | no       | list     |               |             | List of device values to exclude from results.                        |
| transport          | no       | list     | UDP, TCP      |             | Filter by transport protocol used by the syslog servers.              |
| provider           | yes      | dict     |               |             | Authentication credentials.                                           |
| provider.client_id | yes      | str      |               |             | Client ID for authentication.                                         |
| provider.client_secret | yes  | str      |               |             | Client secret for authentication.                                     |
| provider.tsg_id    | yes      | str      |               |             | Tenant Service Group ID.                                              |
| provider.log_level | no       | str      |               | INFO        | Log level for the SDK.                                                |

!!! note
- At least one container type (`folder`, `snippet`, or `device`) is required when `name` is not specified.
- Only one container type can be specified at a time.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.11 or higher
- Ansible 2.15 or higher

## Usage Examples

### Retrieving a Specific Syslog Server Profile

<div class="termy">

<!-- termynal -->

```yaml
- name: Get information about a specific syslog server profile
  cdot65.scm.syslog_server_profiles_info:
    provider: "{{ provider }}"
    name: "test-syslog-profile"
    folder: "Texas"
  register: profile_info

- name: Display profile details
  debug:
    var: profile_info.syslog_server_profile
```

</div>

### Listing Syslog Server Profiles

<div class="termy">

<!-- termynal -->

```yaml
- name: List all syslog server profiles in a folder
  cdot65.scm.syslog_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_profiles

- name: Display all profiles
  debug:
    var: all_profiles.syslog_server_profiles
```

</div>

### Filtering Syslog Server Profiles

<div class="termy">

<!-- termynal -->

```yaml
- name: List only UDP profiles
  cdot65.scm.syslog_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    transport: ["UDP"]
  register: udp_profiles

- name: List profiles with exact match and exclusions
  cdot65.scm.syslog_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_profiles
```

</div>

## Return Values

| Name                  | Description                                                             | Type | Returned                            | Sample                                                                                                                                                          |
|-----------------------|-------------------------------------------------------------------------|------|-------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| syslog_server_profile | Information about the requested syslog server profile                   | dict | when name is specified and found    | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "test-syslog-profile", "servers": {"name": "primary-syslog", "server": "10.0.0.1", "transport": "UDP"}} |
| syslog_server_profiles | List of syslog server profile objects matching the filter criteria     | list | when name is not specified          | [{"id": "123...", "name": "profile1", ...}, {"id": "456...", "name": "profile2", ...}]                                                                         |

## Error Handling

Common errors you might encounter when using this module:

| Error                         | Description                                                  | Resolution                                                   |
|-------------------------------|--------------------------------------------------------------|------------------------------------------------------------|
| Syslog server profile not found | Attempt to retrieve a profile that doesn't exist            | Verify the profile name and container location              |
| Missing query parameter       | Required parameter not provided for filtering                | Ensure required container parameters are specified           |
| Invalid filter parameters     | Invalid filter values provided                               | Check filter values for proper format and supported options |

<div class="termy">

<!-- termynal -->

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to retrieve syslog server profile
      cdot65.scm.syslog_server_profiles_info:
        provider: "{{ provider }}"
        name: "test-syslog-profile"
        folder: "Texas"
      register: result
  rescue:
    - name: Handle profile not found error
      debug:
        msg: "Syslog server profile not found or invalid input provided"
    - name: Continue with other tasks
      # Additional recovery tasks
```

</div>

## Best Practices

1. **Efficient Filtering**
    - Use specific filters to reduce the number of results
    - Utilize the transport filter to find profiles with specific server types
    - Combine multiple filters for precise results

2. **Container Management**
    - Only specify one container type (folder, snippet, or device) at a time
    - Use the same container type consistently across operations

3. **Result Handling**
    - Check if results are empty before processing
    - Handle potential errors with try/except or block/rescue
    - Register results for further processing

4. **Performance Optimization**
    - Use exact_match for faster, more specific queries
    - Include exclusion filters to eliminate unwanted results
    - Fetch specific profiles by name when possible instead of filtering large lists

5. **Integration with Other Modules**
    - Use the info module to verify existence before creating or updating profiles
    - Chain tasks to create conditional workflows based on query results
    - Use returned data as input for other tasks

## Related Modules

- [syslog_server_profiles](syslog_server_profiles.md) - Manage syslog server profiles
- [log_forwarding_profile](log_forwarding_profile.md) - Manage log forwarding profiles that might use syslog server profiles
- [log_forwarding_profile_info](log_forwarding_profile_info.md) - Retrieve information about log forwarding profiles

## Author

- Calvin Remsburg (@cdot65)