# IPsec Crypto Profile Info Module

## Table of Contents
01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Module Parameters](#module-parameters)
04. [Return Values](#return-values)
05. [Exceptions](#exceptions)
06. [Basic Usage](#basic-usage)
07. [Usage Examples](#usage-examples)
    - [Get a Specific Profile](#get-a-specific-profile)
    - [List All Profiles in a Folder](#list-all-profiles-in-a-folder)
    - [Use Filtering Options](#use-filtering-options)
    - [Handle Non-Existent Profiles](#handle-non-existent-profiles)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview
The `ipsec_crypto_profile_info` Ansible module allows you to retrieve information about IPsec Crypto Profiles
in Palo Alto Networks' Strata Cloud Manager (SCM). This module supports retrieving details of a specific
profile or listing profiles with various filtering options. This is an information module that only retrieves data and
does not modify any configuration.

## Core Methods
| Method | Description | Parameters | Return Type |
| ------ | ----------- | ---------- | ----------- |
| `fetch()` | Gets a profile by name | `name: str`, `container: str` | `IpsecCryptoProfileResponseModel` |
| `list()` | Lists profiles with filtering | `folder: str`, `**filters` | `List[IpsecCryptoProfileResponseModel]` |

## Module Parameters
| Parameter | Type | Required | Default | Description |
| --------- | ---- | -------- | ------- | ----------- |
| `name` | str | No | | The name of a specific IPsec crypto profile to retrieve |
| `gather_subset` | list | No | ["config"] | Determines which information to gather about IPsec crypto profiles |
| `folder` | str | One container | | Filter IPsec crypto profiles by folder container |
| `snippet` | str | One container | | Filter IPsec crypto profiles by snippet container |
| `device` | str | One container | | Filter IPsec crypto profiles by device container |
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
| `profile` | Information about the requested IPsec crypto profile | dict |

With fields:
| Field | Description |
| ----- | ----------- |
| `id` | Unique identifier of the profile |
| `name` | Name of the profile |
| `description` | Description of the profile |
| `folder`/`snippet`/`device` | Container information |
| `esp` | ESP configuration details including encryption and authentication algorithms |
| `ah` | AH configuration details including authentication algorithms |
| `dh_group` | DH group for Perfect Forward Secrecy |
| `lifetime` | Lifetime settings for the Security Association (SA) |
| `lifesize` | Lifesize settings for the Security Association (SA) |
| `created_at` | Timestamp when the profile was created |
| `created_by` | User who created the profile |
| `modified_at` | Timestamp when the profile was last modified |
| `modified_by` | User who last modified the profile |

When listing profiles:
| Value | Description | Type |
| ----- | ----------- | ---- |
| `profiles` | List of IPsec crypto profile objects matching the filter criteria | list |

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
- name: Get information about an IPsec crypto profile
  cdot65.scm.ipsec_crypto_profile_info:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
    name: "Standard-IPsec-Profile"
    folder: "Shared"
  register: profile_info

- name: Display profile details
  debug:
    var: profile_info.profile
```

## Usage Examples

### Get a Specific Profile

This example retrieves information about a specific IPsec crypto profile by name:

```yaml
- name: Get a specific IPsec crypto profile
  cdot65.scm.ipsec_crypto_profile_info:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "ESP-AES256-SHA256"
    folder: "Prisma Access"
  register: profile_info

- name: Display profile information
  debug:
    msg: "Profile '{{ profile_info.profile.name }}' uses DH Group {{ profile_info.profile.dh_group }} with ESP encryption {{ profile_info.profile.esp.encryption | join(', ') }}"
  when: profile_info.profile is defined
```

### List All Profiles in a Folder

This example retrieves all IPsec crypto profiles in a specific folder:

```yaml
- name: List all IPsec crypto profiles in Prisma Access folder
  cdot65.scm.ipsec_crypto_profile_info:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    folder: "Prisma Access"
  register: profiles_info

- name: Display number of profiles
  debug:
    msg: "Found {{ profiles_info.profiles | length }} IPsec crypto profiles in Prisma Access folder"

- name: Display profile names
  debug:
    msg: "Profile names: {{ profiles_info.profiles | map(attribute='name') | list | join(', ') }}"
  when: profiles_info.profiles | length > 0
```

### Use Filtering Options

This example shows how to use additional filtering options when listing profiles:

```yaml
- name: List IPsec crypto profiles with filtering
  cdot65.scm.ipsec_crypto_profile_info:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    folder: "Shared"
    exact_match: true
    exclude_folders:
      - "Deprecated Profiles"
  register: filtered_profiles

- name: Process filtered profiles
  debug:
    msg: "Profile: {{ item.name }}, DH Group: {{ item.dh_group }}"
  loop: "{{ filtered_profiles.profiles }}"
  when: filtered_profiles.profiles | length > 0
```

### Handle Non-Existent Profiles

This example demonstrates error handling when a profile does not exist:

```yaml
- name: Try to get a non-existent profile
  cdot65.scm.ipsec_crypto_profile_info:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "Non-Existent-Profile"
    folder: "Shared"
  register: profile_info
  failed_when: false

- name: Display message if profile doesn't exist
  debug:
    msg: "Profile 'Non-Existent-Profile' does not exist"
  when: profile_info.failed or profile_info.profile is not defined
```

## Error Handling

Common errors and how to handle them:

| Error | Possible Cause | Solution |
| ----- | -------------- | -------- |
| "Authentication failed" | Invalid client_id, client_secret, or tsg_id | Verify the authentication parameters |
| "Profile not found" | The specified profile doesn't exist | Check the profile name and container |
| "Multiple containers specified" | More than one container type was specified | Specify exactly one of folder, snippet, or device |
| "Internal server error" | Issue with the SCM API | Try the request again or contact support |

Example of robust error handling:

```yaml
- name: Get IPsec crypto profile info with error handling
  block:
    - name: Attempt to retrieve IPsec crypto profile
      cdot65.scm.ipsec_crypto_profile_info:
        provider: "{{ provider }}"
        name: "Standard-IPsec-Profile"
        folder: "Shared"
      register: profile_info
  rescue:
    - name: Handle error
      debug:
        msg: "Failed to retrieve IPsec crypto profile info: {{ ansible_failed_result.msg }}"
    
    - name: Check if it's a not found error
      debug:
        msg: "Profile does not exist or you don't have permissions to view it"
      when: "'not found' in ansible_failed_result.msg | default('')"
```

## Best Practices

### Efficient Information Gathering

- Use the `gather_subset` parameter to control the level of detail in the response
- Retrieve only the specific profile you need by name when possible
- Use filtering options to reduce the number of profiles returned
- Consider using `exact_match: true` when you need profiles from a specific container only

### Handling Large Result Sets

- When working with a large number of profiles, process them in smaller batches
- Use templating to extract and format only the needed information

### Security Considerations

- Store authentication credentials securely (e.g., in Ansible Vault)
- Limit the scope of information gathering to only what is necessary
- Avoid exposing sensitive profile information in logs or debug output

### Performance Optimization

- Cache profile information when it will be used multiple times in a playbook
- Use conditional logic to avoid unnecessary API calls

## Related Modules

- [cdot65.scm.ipsec_crypto_profile](ipsec_crypto_profile.md) - Manage IPsec crypto profiles
- [cdot65.scm.ike_crypto_profile_info](ike_crypto_profile_info.md) - Gather information about IKE crypto profiles
- [cdot65.scm.ike_gateway_info](ike_gateway_info.md) - Gather information about IKE gateways
- [cdot65.scm.ipsec_tunnel_info](ipsec_tunnel_info.md) - Gather information about IPsec tunnels
