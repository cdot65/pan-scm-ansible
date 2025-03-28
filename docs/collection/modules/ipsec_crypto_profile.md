# Ipsec Crypto Profile Configuration Object

## Table of Contents

- [Ipsec Crypto Profile Configuration Object](#ipsec-crypto-profile-configuration-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [IPSec Crypto Profile Model Attributes](#ipsec-crypto-profile-model-attributes)
    - [Lifetime Attributes](#lifetime-attributes)
    - [Provider Dictionary Attributes](#provider-dictionary-attributes)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Creating IPSec Crypto Profiles](#creating-ipsec-crypto-profiles)
    - [Basic IPSec Crypto Profile](#basic-ipsec-crypto-profile)
    - [Suite-B IPSec Crypto Profile](#suite-b-ipsec-crypto-profile)
    - [Updating IPSec Crypto Profiles](#updating-ipsec-crypto-profiles)
    - [Deleting IPSec Crypto Profiles](#deleting-ipsec-crypto-profiles)
  - [Managing Configuration Changes](#managing-configuration-changes)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Algorithm Selection](#algorithm-selection)
    - [Perfect Forward Secrecy](#perfect-forward-secrecy)
    - [Lifetime Management](#lifetime-management)
    - [Profile Organization](#profile-organization)
    - [Compliance Requirements](#compliance-requirements)
    - [Implementation Strategy](#implementation-strategy)
  - [Related Modules](#related-modules)

## Overview

The `ipsec_crypto_profile` Ansible module provides functionality to manage IPSec Crypto Profiles in
Palo Alto Networks' Strata Cloud Manager (SCM). IPSec Crypto Profiles define the encryption and
authentication algorithms to be used during the IPSec Phase-2 negotiation when establishing a secure
VPN tunnel.

## Core Methods

| Method     | Description                        | Parameters                               | Return Type                             |
| ---------- | ---------------------------------- | ---------------------------------------- | --------------------------------------- |
| `create()` | Creates a new IPSec Crypto Profile | `data: Dict[str, Any]`                   | `IpsecCryptoProfileResponseModel`       |
| `update()` | Updates an existing profile        | `profile: IpsecCryptoProfileUpdateModel` | `IpsecCryptoProfileResponseModel`       |
| `delete()` | Removes a profile                  | `object_id: str`                         | `None`                                  |
| `fetch()`  | Gets a profile by name             | `name: str`, `container: str`            | `IpsecCryptoProfileResponseModel`       |
| `list()`   | Lists profiles with filtering      | `folder: str`, `**filters`               | `List[IpsecCryptoProfileResponseModel]` |

## IPSec Crypto Profile Model Attributes

| Attribute            | Type | Required      | Description                                      |
| -------------------- | ---- | ------------- | ------------------------------------------------ |
| `name`               | str  | Yes           | Name of the IPSec Crypto Profile                 |
| `description`        | str  | No            | Description of the profile                       |
| `esp_encryption`     | list | Yes           | List of ESP encryption algorithms                |
| `esp_authentication` | list | No\*          | List of ESP authentication algorithms            |
| `ah_authentication`  | list | No\*          | List of AH authentication algorithms             |
| `dh_group`           | str  | No            | Diffie-Hellman group for Perfect Forward Secrecy |
| `lifetime`           | dict | No            | IPSec SA lifetime settings                       |
| `folder`             | str  | One container | The folder in which the profile is defined       |
| `snippet`            | str  | One container | The snippet in which the profile is defined      |
| `device`             | str  | One container | The device in which the profile is defined       |

\*Note: When using GCM encryption algorithms, esp_authentication should not be specified as
authentication is built into GCM.

### Lifetime Attributes

| Attribute | Type | Required | Description                           |
| --------- | ---- | -------- | ------------------------------------- |
| `days`    | int  | No       | Number of days for lifetime (0-365)   |
| `hours`   | int  | No       | Number of hours for lifetime (0-24)   |
| `minutes` | int  | No       | Number of minutes for lifetime (0-60) |
| `seconds` | int  | No       | Number of seconds for lifetime (0-60) |

### Provider Dictionary Attributes

| Attribute       | Type | Required | Default | Description                      |
| --------------- | ---- | -------- | ------- | -------------------------------- |
| `client_id`     | str  | Yes      |         | Client ID for authentication     |
| `client_secret` | str  | Yes      |         | Client secret for authentication |
| `tsg_id`        | str  | Yes      |         | Tenant Service Group ID          |
| `log_level`     | str  | No       | "INFO"  | Log level for the SDK            |

## Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid profile data or format |
| `NameNotUniqueError`         | Profile name already exists    |
| `ObjectNotPresentError`      | Profile not found              |
| `MissingQueryParameterError` | Missing required parameters    |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |
| `InvalidAlgorithmError`      | Invalid algorithm specified    |

## Basic Configuration

The IPSec Crypto Profile module requires proper authentication credentials to access the Strata
Cloud Manager API.

```yaml
- name: Basic IPSec Crypto Profile Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure an IPSec Crypto Profile exists
      cdot65.scm.ipsec_crypto_profile:
        provider: "{{ provider }}"
        name: "Standard-IPSec"
        description: "Standard IPSec encryption profile for VPN tunnels"
        esp_encryption: 
          - "aes-256-cbc"
        esp_authentication:
          - "sha256"
        dh_group: "group14"
        lifetime:
          hours: 1
        folder: "Texas"
        state: "present"
```

## Usage Examples

### Creating IPSec Crypto Profiles

IPSec Crypto Profiles define the security parameters for Phase-2 IPSec negotiation when establishing
a VPN tunnel. Different profiles can be created for different security requirements.

### Basic IPSec Crypto Profile

This example creates a standard IPSec Crypto Profile with moderate security settings.

```yaml
- name: Create a basic IPSec Crypto Profile
  cdot65.scm.ipsec_crypto_profile:
    provider: "{{ provider }}"
    name: "Standard-IPSec"
    description: "Standard IPSec encryption profile for general VPN tunnels"
    esp_encryption: 
      - "aes-128-cbc"
      - "aes-256-cbc"
    esp_authentication: 
      - "sha1"
      - "sha256"
    dh_group: "group14"
    lifetime:
      hours: 8
    folder: "Texas"
    state: "present"
```

### Suite-B IPSec Crypto Profile

This example creates a Suite-B compliant IPSec Crypto Profile with high security settings.

```yaml
- name: Create a Suite-B compliant IPSec Crypto Profile
  cdot65.scm.ipsec_crypto_profile:
    provider: "{{ provider }}"
    name: "Suite-B-GCM-128"
    description: "Suite-B compliance profile for IPSec"
    esp_encryption: 
      - "aes-128-gcm"
    dh_group: "group19"
    lifetime:
      hours: 4
    folder: "Texas"
    state: "present"
```

### Updating IPSec Crypto Profiles

This example updates an existing IPSec Crypto Profile with new algorithms and settings.

```yaml
- name: Update an IPSec Crypto Profile
  cdot65.scm.ipsec_crypto_profile:
    provider: "{{ provider }}"
    name: "Standard-IPSec"
    description: "Updated standard IPSec profile"
    esp_encryption: 
      - "aes-256-gcm"
    dh_group: "group20"
    lifetime:
      hours: 2
    folder: "Texas"
    state: "present"
```

### Deleting IPSec Crypto Profiles

This example removes an IPSec Crypto Profile.

```yaml
- name: Delete an IPSec Crypto Profile
  cdot65.scm.ipsec_crypto_profile:
    provider: "{{ provider }}"
    name: "Standard-IPSec"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting IPSec Crypto Profiles, you need to commit your changes to
apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated IPSec Crypto Profiles"
```

## Error Handling

It's important to handle potential errors when working with IPSec Crypto Profiles.

```yaml
- name: Create or update IPSec Crypto Profile with error handling
  block:
    - name: Ensure IPSec Crypto Profile exists
      cdot65.scm.ipsec_crypto_profile:
        provider: "{{ provider }}"
        name: "Standard-IPSec"
        description: "Standard IPSec encryption profile"
        esp_encryption: 
          - "aes-256-gcm"
        dh_group: "group14"
        lifetime:
          hours: 1
        folder: "Texas"
        state: "present"
      register: profile_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated IPSec Crypto Profiles"
      when: profile_result.changed
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's an algorithm error
      debug:
        msg: "Please check the encryption or authentication algorithm settings"
      when: "'algorithm' in ansible_failed_result.msg"
```

## Best Practices

### Algorithm Selection

- Use AES-GCM algorithms where possible as they provide both encryption and authentication
- Avoid using deprecated or weak algorithms (DES, MD5)
- For non-GCM algorithms, always specify authentication algorithms
- Balance security requirements with performance considerations
- Follow industry standards and compliance requirements

### Perfect Forward Secrecy

- Enable Perfect Forward Secrecy (PFS) with strong DH groups where security is critical
- Use group14 (2048-bit) or higher for sensitive traffic
- Consider the performance impact of PFS on high-volume VPN tunnels
- Document PFS decisions and rationale

### Lifetime Management

- Set appropriate SA lifetimes based on security requirements and traffic volume
- Shorter lifetimes increase security but also increase rekeying overhead
- Consider the operational impact of frequent rekeying
- Document your lifetime decisions and rationale

### Profile Organization

- Create profiles for different security levels based on the sensitivity of traffic
- Use high-security profiles for sensitive networks
- Use standard profiles for general-purpose connections
- Document profile usage to track where each profile is applied
- Use descriptive names that indicate security level or purpose

### Compliance Requirements

- Consider compliance requirements (FIPS, Suite-B) when selecting algorithms
- Document compliance adherence for audit purposes
- Regularly review profiles against evolving compliance standards
- Test compliance-driven configurations thoroughly

### Implementation Strategy

- Test profiles in a non-production environment before deployment
- Verify compatibility with peer devices before implementation
- Implement changes during maintenance windows
- Have a rollback plan for unsuccessful implementations
- Monitor VPN connections after implementation

## Related Modules

- [ike_crypto_profile](ike_crypto_profile.md) - Configure IKE Crypto profiles for Phase-1
  negotiations
- [ike_gateway](ike_gateway.md) - Configure IKE gateways that use IPSec Crypto profiles
- [ipsec_tunnel](ipsec_tunnel.md) - Configure IPsec tunnels that reference IPSec Crypto profiles
- [remote_networks](remote_networks.md) - Configure remote networks that use IPSec tunnels
