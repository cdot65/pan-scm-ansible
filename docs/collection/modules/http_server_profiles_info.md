# Http Server Profiles Information Object

## Table of Contents

1. [Overview](#overview)
2. [Parameters](#parameters)
3. [Filter Parameters](#filter-parameters)
4. [Examples](#examples)
   - [Retrieving a Specific HTTP Server Profile](#retrieving-a-specific-http-server-profile)
   - [Listing All HTTP Server Profiles](#listing-all-http-server-profiles)
   - [Filtering HTTP Server Profiles](#filtering-http-server-profiles)
5. [Return Values](#return-values)
6. [Status Codes](#status-codes)

## Overview

The `http_server_profiles_info` module retrieves information about HTTP server profile objects from
Palo Alto Networks' Strata Cloud Manager (SCM). This module enables you to query both specific
profiles and lists of profiles with various filtering options without making any changes to the
system.

## Parameters

| Parameter       | Type   | Required | Description                                                                    |
| --------------- | ------ | -------- | ------------------------------------------------------------------------------ |
| `name`          | string | No       | Name of a specific HTTP server profile to retrieve                             |
| `gather_subset` | list   | No       | Determines which information to gather (default: ['config'])                   |
| `folder`        | string | Yes\*    | Filter by folder container (\*one container required if name is not provided)  |
| `snippet`       | string | Yes\*    | Filter by snippet container (\*one container required if name is not provided) |
| `device`        | string | Yes\*    | Filter by device container (\*one container required if name is not provided)  |
| `provider`      | dict   | Yes      | Authentication credentials (see [Provider](#provider))                         |

### Provider

| Parameter       | Type   | Required | Description                      |
| --------------- | ------ | -------- | -------------------------------- |
| `client_id`     | string | Yes      | Client ID for authentication     |
| `client_secret` | string | Yes      | Client secret for authentication |
| `tsg_id`        | string | Yes      | Tenant Service Group ID          |
| `log_level`     | string | No       | SDK log level (default: "INFO")  |

## Filter Parameters

When listing HTTP server profiles, you can use the following parameters to filter the results:

| Parameter          | Type    | Required | Description                                                                 |
| ------------------ | ------- | -------- | --------------------------------------------------------------------------- |
| `exact_match`      | boolean | No       | Only return objects defined exactly in specified container (default: false) |
| `exclude_folders`  | list    | No       | List of folder names to exclude from results                                |
| `exclude_snippets` | list    | No       | List of snippet values to exclude from results                              |
| `exclude_devices`  | list    | No       | List of device values to exclude from results                               |
| `protocol`         | list    | No       | Filter by server protocols: ["HTTP"], ["HTTPS"], or ["HTTP", "HTTPS"]       |
| `tag_registration` | boolean | No       | Filter by tag registration status                                           |

## Examples

### Retrieving a Specific HTTP Server Profile



```yaml
- name: Get information about a specific HTTP server profile
  cdot65.scm.http_server_profiles_info:
    provider: "{{ provider }}"
    name: "test-http-profile"
    folder: "Texas"
  register: profile_info
  
- name: Display profile information
  debug:
    var: profile_info
```


### Listing All HTTP Server Profiles



```yaml
- name: List all HTTP server profiles in a folder
  cdot65.scm.http_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_profiles
  
- name: Display all profiles
  debug:
    var: all_profiles
```


### Filtering HTTP Server Profiles



```yaml
- name: List only HTTPS profiles
  cdot65.scm.http_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    protocol: ["HTTPS"]
  register: https_profiles

- name: List profiles with tag registration enabled
  cdot65.scm.http_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tag_registration: true
  register: tagged_profiles

- name: List profiles with exact match and exclusions
  cdot65.scm.http_server_profiles_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_profiles
```


## Return Values

When retrieving a specific profile by name:

| Name                  | Type | Description                        | Sample                                                                             |
| --------------------- | ---- | ---------------------------------- | ---------------------------------------------------------------------------------- |
| `http_server_profile` | dict | Details of the HTTP server profile | `{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "test-http-profile", ...}` |

When listing profiles:

| Name                   | Type | Description                         | Sample                                                                                   |
| ---------------------- | ---- | ----------------------------------- | ---------------------------------------------------------------------------------------- |
| `http_server_profiles` | list | List of HTTP server profile objects | `[{"id": "123...", "name": "profile1", ...}, {"id": "456...", "name": "profile2", ...}]` |

## Status Codes

| Code | Description                  |
| ---- | ---------------------------- |
| 200  | Success                      |
| 400  | Invalid input data or format |
| 401  | Authentication error         |
| 404  | Resource not found           |
| 500  | Server error                 |
