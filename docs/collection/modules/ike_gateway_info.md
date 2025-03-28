# IKE Gateway Info Module

## Table of Contents
- [IKE Gateway Info Module](#ike-gateway-info-module)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [Module Parameters](#module-parameters)
  - [Return Values](#return-values)
  - [Exceptions](#exceptions)
  - [Basic Usage](#basic-usage)
  - [Usage Examples](#usage-examples)
    - [Get a Specific Gateway](#get-a-specific-gateway)
    - [List All Gateways in a Folder](#list-all-gateways-in-a-folder)
    - [Use Filtering Options](#use-filtering-options)
    - [Handle Non-Existent Gateways](#handle-non-existent-gateways)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
  - [Related Modules](#related-modules)

## Overview
The `ike_gateway_info` Ansible module allows you to retrieve information about Internet Key Exchange (IKE)
Gateways in Palo Alto Networks' Strata Cloud Manager (SCM). This module supports retrieving details of a specific
gateway or listing gateways with various filtering options. This is an information module that only retrieves data and
does not modify any configuration.

## Core Methods
| Method | Description | Parameters | Return Type |
| ------ | ----------- | ---------- | ----------- |
| `fetch()` | Gets a gateway by name | `name: str`, `container: str` | `IKEGatewayResponseModel` |
| `list()` | Lists gateways with filtering | `folder: str`, `**filters` | `List[IKEGatewayResponseModel]` |

## Module Parameters
| Parameter | Type | Required | Default | Description |
| --------- | ---- | -------- | ------- | ----------- |
| `name` | str | No | | The name of a specific IKE gateway to retrieve |
| `gather_subset` | list | No | ["config"] | Determines which information to gather about IKE gateways |
| `folder` | str | One container | | Filter IKE gateways by folder container |
| `snippet` | str | One container | | Filter IKE gateways by snippet container |
| `device` | str | One container | | Filter IKE gateways by device container |
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
When requesting a specific gateway by name:
| Value | Description | Type |
| ----- | ----------- | ---- |
| `gateway` | Information about the requested IKE gateway | dict |

With fields:
| Field | Description |
| ----- | ----------- |
| `id` | Unique identifier of the gateway |
| `name` | Name of the gateway |
| `folder`/`snippet`/`device` | Container information |
| `authentication` | Authentication configuration details (pre_shared_key or certificate) |
| `peer_id` | Peer identification settings |
| `local_id` | Local identification settings |
| `protocol` | Protocol version and cryptographic settings |
| `protocol_common` | Common protocol settings like NAT traversal |
| `peer_address` | Peer address configuration (IP, FQDN, or dynamic) |
| `created_at` | Timestamp when the gateway was created |
| `created_by` | User who created the gateway |
| `modified_at` | Timestamp when the gateway was last modified |
| `modified_by` | User who last modified the gateway |

When listing gateways:
| Value | Description | Type |
| ----- | ----------- | ---- |
| `gateways` | List of IKE gateway objects matching the filter criteria | list |

## Exceptions
| Exception | Description |
| --------- | ----------- |
| `ObjectNotPresentError` | Gateway not found |
| `MissingQueryParameterError` | Missing required parameters |
| `InvalidObjectError` | Invalid parameter format |
| `AuthenticationError` | Authentication failed |
| `ServerError` | Internal server error |

## Basic Usage
```yaml
- name: Get information about an IKE gateway
  cdot65.scm.ike_gateway_info:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
    name: "Primary-VPN-Gateway"
    folder: "Service Connections"
  register: gateway_info

- name: Display gateway details
  debug:
    var: gateway_info.gateway
```

## Usage Examples
### Get a Specific Gateway
Retrieve detailed information about a specific IKE gateway in a folder:
```yaml
- name: Get information about a specific IKE gateway
  cdot65.scm.ike_gateway_info:
    provider: "{{ provider }}"
    name: "Primary-VPN-Gateway"
    folder: "Service Connections"
  register: gateway_info

- name: Display gateway information
  debug:
    msg: "Gateway '{{ gateway_info.gateway.name }}' uses {{ gateway_info.gateway.protocol.version }} with peer at {{ gateway_info.gateway.peer_address.ip }}"
  when: gateway_info.gateway is defined
```

### List All Gateways in a Folder
Retrieve a list of all IKE gateways in a specific folder:
```yaml
- name: List all IKE gateways in a folder
  cdot65.scm.ike_gateway_info:
    provider: "{{ provider }}"
    folder: "Service Connections"
  register: all_gateways

- name: Display gateway names
  debug:
    msg: "Found {{ all_gateways.gateways | length }} gateways: {{ all_gateways.gateways | map(attribute='name') | join(', ') }}"
  when: all_gateways.gateways is defined and all_gateways.gateways | length > 0
```

### Use Filtering Options
Filter the list of gateways by excluding specific folders or applying exact match:
```yaml
- name: List gateways with filtering options
  cdot65.scm.ike_gateway_info:
    provider: "{{ provider }}"
    folder: "Service Connections"
    exact_match: true
    exclude_folders: ["Default", "Shared"]
  register: filtered_gateways

- name: Print filtered gateway count
  debug:
    msg: "Found {{ filtered_gateways.gateways | length }} gateways defined exactly in Service Connections folder"
```

### Handle Non-Existent Gateways
Handle the case when a gateway does not exist:
```yaml
- name: Try to get information about a non-existent gateway
  cdot65.scm.ike_gateway_info:
    provider: "{{ provider }}"
    name: "NonExistentGateway"
    folder: "Service Connections"
  register: gateway_info
  failed_when: false

- name: Display message if gateway doesn't exist
  debug:
    msg: "Gateway does not exist: {{ gateway_info.msg }}"
  when: gateway_info.failed | default(false)
```

## Error Handling
Properly handle errors when using the IKE Gateway info module:
```yaml
- name: Get IKE gateway information with error handling
  block:
    - name: Attempt to retrieve gateway information
      cdot65.scm.ike_gateway_info:
        provider: "{{ provider }}"
        name: "Primary-VPN-Gateway"
        folder: "Service Connections"
      register: gateway_info

    - name: Display gateway information
      debug:
        var: gateway_info.gateway
  rescue:
    - name: Handle API or authentication errors
      debug:
        msg: "Failed to retrieve IKE gateway information: {{ ansible_failed_result.msg | default('Unknown error') }}"
```

## Best Practices
1. **Provider Configuration**: Store credentials in Ansible Vault for security.
2. **Error Handling**: Implement appropriate error handling as shown above.
3. **Filtering**: Use filtering options to limit results when working with large environments.
4. **Validation**: Validate that returned objects contain expected fields before accessing them.
5. **Logging**: Set appropriate log levels to help with troubleshooting.

## Related Modules
| Module | Description |
| ------ | ----------- |
| [ike_gateway](./ike_gateway.md) | Create, update, or delete IKE gateways |
| [ike_crypto_profile](./ike_crypto_profile.md) | Configure IKE crypto profiles used by IKE gateways |
| [ike_crypto_profile_info](./ike_crypto_profile_info.md) | Retrieve information about IKE crypto profiles |
| [ipsec_tunnel](./ipsec_tunnel.md) | Configure IPsec tunnels that use IKE gateways |
| [ipsec_crypto_profile](./ipsec_crypto_profile.md) | Configure IPsec crypto profiles used by IPsec tunnels |
