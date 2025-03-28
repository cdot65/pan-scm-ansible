# IKE Crypto Profile Info Module

## Table of Contents

- [IKE Crypto Profile Info Module](#ike-crypto-profile-info-module)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [Module Parameters](#module-parameters)
  - [Return Values](#return-values)
  - [Exceptions](#exceptions)
  - [Basic Usage](#basic-usage)
  - [Usage Examples](#usage-examples)
    - [Get a Specific Profile](#get-a-specific-profile)
    - [List All Profiles in a Folder](#list-all-profiles-in-a-folder)
    - [Use Filtering Options](#use-filtering-options)
    - [Handle Non-Existent Profiles](#handle-non-existent-profiles)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Efficient Querying](#efficient-querying)
    - [Data Processing](#data-processing)
    - [Error Handling](#error-handling-1)
    - [Inventory Management](#inventory-management)
  - [Related Modules](#related-modules)

## Overview

The `ike_crypto_profile_info` Ansible module allows you to retrieve information about Internet Key Exchange (IKE) 
Crypto Profiles in Palo Alto Networks' Strata Cloud Manager (SCM). This module supports retrieving details of a specific
profile or listing profiles with various filtering options. This is an information module that only retrieves data and 
does not modify any configuration.

## Core Methods

| Method | Description | Parameters | Return Type |
| ------ | ----------- | ---------- | ----------- |
| `fetch()` | Gets a profile by name | `name: str`, `container: str` | `IkeCryptoProfileResponseModel` |
| `list()` | Lists profiles with filtering | `folder: str`, `**filters` | `List[IkeCryptoProfileResponseModel]` |

## Module Parameters

| Parameter | Type | Required | Default | Description |
| --------- | ---- | -------- | ------- | ----------- |
| `name` | str | No | | The name of a specific IKE crypto profile to retrieve |
| `gather_subset` | list | No | ["config"] | Determines which information to gather about IKE crypto profiles |
| `folder` | str | One container | | Filter IKE crypto profiles by folder container |
| `snippet` | str | One container | | Filter IKE crypto profiles by snippet container |
| `device` | str | One container | | Filter IKE crypto profiles by device container |
| `exact_match` | bool | No | false | When True, only return objects defined exactly in the specified container |
| `exclude_folders` | list | No | | List of folder names to exclude from results |
| `exclude_snippets` | list | No | | List of snippet values to exclude from results |
| `exclude_devices` | list | No | | List of device values to exclude from results |
| `provider` | dict | Yes | | Authentication credentials |
| &nbsp;&nbsp;&nbsp;&nbsp;`client_id` | str | Yes | | Client ID for authentication |
| &nbsp;&nbsp;&nbsp;&nbsp;`client_secret` | str | Yes | | Client secret for authentication |
| &nbsp;&nbsp;&nbsp;&nbsp;`tsg_id` | str | Yes | | Tenant Service Group ID |
| &nbsp;&nbsp;&nbsp;&nbsp;`log_level` | str | No | "INFO" | Log level for the SDK |

## Return Values

When requesting a specific profile by name:

| Value | Description | Type |
| ----- | ----------- | ---- |
| `profile` | Information about the requested IKE crypto profile | dict |

With fields:

| Field | Description |
| ----- | ----------- |
| `id` | Unique identifier of the profile |
| `name` | Name of the profile |
| `description` | Description of the profile (if any) |
| `folder`/`snippet`/`device` | Container information |
| `hash` | List of hash algorithms configured |
| `encryption` | List of encryption algorithms configured |
| `dh_group` | List of Diffie-Hellman groups configured |
| `lifetime` | Lifetime settings for the profile |
| `authentication_multiple` | Authentication multiple value (if configured) |

When listing profiles:

| Value | Description | Type |
| ----- | ----------- | ---- |
| `profiles` | List of IKE crypto profile objects matching the filter criteria | list |

## Exceptions

| Exception | Description |
| --------- | ----------- |
| `ObjectNotPresentError` | Profile not found |
| `MissingQueryParameterError` | Missing required parameters |
| `InvalidObjectError` | Invalid parameter format |
| `AuthenticationError` | Authentication failed |
| `ServerError` | Internal server error |

## Basic Usage

```yaml
- name: Get information about an IKE crypto profile
  cdot65.scm.ike_crypto_profile_info:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
    name: "Standard-IKE-Profile"
    folder: "SharedFolder"
  register: profile_info
```

## Usage Examples

### Get a Specific Profile

Retrieve information about a specific IKE crypto profile by name:

```yaml
- name: Get information about a specific IKE crypto profile
  cdot65.scm.ike_crypto_profile_info:
    provider: "{{ provider }}"
    name: "Strong-Encryption-Profile"
    folder: "SharedFolder"
  register: profile_info

- name: Display profile information
  debug:
    var: profile_info.profile
```

### List All Profiles in a Folder

List all IKE crypto profiles in a specific folder:

```yaml
- name: List all IKE crypto profiles in a folder
  cdot65.scm.ike_crypto_profile_info:
    provider: "{{ provider }}"
    folder: "SharedFolder"
  register: all_profiles

- name: Count profiles
  debug:
    msg: "Found {{ all_profiles.profiles | length }} IKE crypto profiles"

- name: Display profile names
  debug:
    msg: "Profile names: {{ all_profiles.profiles | map(attribute='name') | list }}"
```

### Use Filtering Options

Use filtering options to narrow down the results:

```yaml
- name: List profiles with filtering
  cdot65.scm.ike_crypto_profile_info:
    provider: "{{ provider }}"
    folder: "SharedFolder"
    exact_match: true
    exclude_folders: ["Templates", "DefaultFolder"]
  register: filtered_profiles

- name: Find strong encryption profiles
  set_fact:
    strong_profiles: "{{ filtered_profiles.profiles | selectattr('encryption', 'contains', 'aes-256-gcm') | list }}"

- name: Display strong encryption profiles
  debug:
    var: strong_profiles
```

### Handle Non-Existent Profiles

Handle cases where a profile doesn't exist:

```yaml
- name: Try to get a non-existent profile
  cdot65.scm.ike_crypto_profile_info:
    provider: "{{ provider }}"
    name: "Non-Existent-Profile"
    folder: "SharedFolder"
  register: profile_result
  failed_when: false

- name: Display result or error
  debug:
    msg: "{{ profile_result.msg if profile_result.failed else profile_result.profile }}"
```

## Error Handling

It's important to handle potential errors when retrieving information:

```yaml
- name: Get IKE crypto profile information with error handling
  block:
    - name: Get profile info
      cdot65.scm.ike_crypto_profile_info:
        provider: "{{ provider }}"
        name: "Standard-IKE-Profile"
        folder: "SharedFolder"
      register: profile_info
      
    - name: Display profile information
      debug:
        var: profile_info.profile
        
  rescue:
    - name: Handle profile not found
      debug:
        msg: "Profile not found: {{ ansible_failed_result.msg }}"
      when: "'not found' in ansible_failed_result.msg"
        
    - name: Handle other errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
      when: "'not found' not in ansible_failed_result.msg"
```

## Best Practices

### Efficient Querying

- Use specific parameters to narrow your query scope
- Use the `name` parameter when you know the exact profile you need
- Use container parameters (`folder`, `snippet`, `device`) to limit the search scope
- Use `exact_match: true` when you only want profiles directly in the specified container

### Data Processing

- Use Ansible's filters and conditionals to process returned data
- Use register and set_fact to store and manipulate returned data
- Use debug with appropriate verbosity for troubleshooting

### Error Handling

- Always use error handling with block/rescue when retrieving profile information
- Handle specific error cases like "profile not found" differently from other errors
- Use the `failed_when: false` pattern for non-critical queries

### Inventory Management

- Use the module to generate dynamic inventories of profiles
- Create reports of profiles with specific algorithms or settings
- Audit profiles for compliance with security standards

## Related Modules

- [ike_crypto_profile](ike_crypto_profile.md) - Create, update, and delete IKE crypto profiles
- [ike_gateway](ike_gateway.md) - Configure IKE gateways that reference IKE Crypto profiles
- [ipsec_crypto_profile](ipsec_crypto_profile.md) - Configure IPsec Crypto profiles
- [ipsec_crypto_profile_info](ipsec_crypto_profile_info.md) - Get information about IPsec crypto profiles