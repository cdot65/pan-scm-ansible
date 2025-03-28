# IPsec Crypto Profile Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [IPsec Crypto Profile Model Attributes](#ipsec-crypto-profile-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating IPsec Crypto Profiles](#creating-ipsec-crypto-profiles)
    - [IPsec Crypto Profile with ESP Configuration](#ipsec-crypto-profile-with-esp-configuration)
    - [IPsec Crypto Profile with AH Configuration](#ipsec-crypto-profile-with-ah-configuration)
    - [Updating IPsec Crypto Profiles](#updating-ipsec-crypto-profiles)
    - [Deleting IPsec Crypto Profiles](#deleting-ipsec-crypto-profiles)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `ipsec_crypto_profile` Ansible module provides functionality to manage IPsec Crypto Profiles in
Palo Alto Networks' Strata Cloud Manager (SCM). IPsec Crypto Profiles define the encryption and
authentication algorithms to be used during the IPsec Phase-2 negotiation when establishing a secure
VPN tunnel.

## Core Methods

| Method     | Description                        | Parameters                               | Return Type                             |
| ---------- | ---------------------------------- | ---------------------------------------- | --------------------------------------- |
| `create()` | Creates a new IPsec Crypto Profile | `data: Dict[str, Any]`                   | `IpsecCryptoProfileResponseModel`       |
| `update()` | Updates an existing profile        | `profile: IpsecCryptoProfileUpdateModel` | `IpsecCryptoProfileResponseModel`       |
| `delete()` | Removes a profile                  | `object_id: str`                         | `None`                                  |
| `fetch()`  | Gets a profile by name             | `name: str`, `container: str`            | `IpsecCryptoProfileResponseModel`       |
| `list()`   | Lists profiles with filtering      | `folder: str`, `**filters`               | `List[IpsecCryptoProfileResponseModel]` |

## IPsec Crypto Profile Model Attributes

| Attribute            | Type    | Required      | Description                                      |
| -------------------- | ------- | ------------- | ------------------------------------------------ |
| `name`               | str     | Yes           | Name of the IPsec Crypto Profile                 |
| `description`        | str     | No            | Description of the IPsec Crypto Profile          |
| `esp`                | dict    | ESP or AH     | ESP configuration settings                       |
| `esp.encryption`     | list    | If ESP        | List of ESP encryption algorithms                |
| `esp.authentication` | list    | If ESP        | List of ESP authentication algorithms            |
| `ah`                 | dict    | ESP or AH     | AH configuration settings                        |
| `ah.authentication`  | list    | If AH         | List of AH authentication algorithms             |
| `dh_group`           | str     | No            | DH group for Perfect Forward Secrecy             |
| `lifetime`           | dict    | No            | SA lifetime configuration                        |
| `lifetime.seconds`   | int     | One unit      | Lifetime in seconds (180-65535)                  |
| `lifetime.minutes`   | int     | One unit      | Lifetime in minutes (3-1092)                     |
| `lifetime.hours`     | int     | One unit      | Lifetime in hours (1-18)                         |
| `lifetime.days`      | int     | One unit      | Lifetime in days (1-30)                          |
| `lifesize`           | dict    | No            | SA lifesize configuration                        |
| `lifesize.kb`        | int     | One unit      | Lifesize in kilobytes                            |
| `lifesize.mb`        | int     | One unit      | Lifesize in megabytes                            |
| `lifesize.gb`        | int     | One unit      | Lifesize in gigabytes                            |
| `lifesize.tb`        | int     | One unit      | Lifesize in terabytes                            |
| `folder`             | str     | One container | Folder in which to create the profile            |
| `snippet`            | str     | One container | Snippet in which to create the profile           |
| `device`             | str     | One container | Device in which to create the profile            |
| `state`              | str     | No            | State of the IPsec Crypto Profile (present/absent)|

*Exactly one of `esp` or `ah` must be provided.*  
*Only one lifetime unit (seconds, minutes, hours, days) can be specified.*  
*Only one lifesize unit (kb, mb, gb, tb) can be specified.*  
*Exactly one container (`folder`, `snippet`, or `device`) must be specified.*

### Provider Dictionary Attributes

| Attribute       | Type   | Required | Default | Description                      |
| --------------- | ------ | -------- | ------- | -------------------------------- |
| `client_id`     | str    | Yes      |         | Client ID for authentication     |
| `client_secret` | str    | Yes      |         | Client secret for authentication |
| `tsg_id`        | str    | Yes      |         | Tenant Service Group ID          |
| `log_level`     | str    | No       | "INFO"  | Log level for the SDK            |

## Exceptions

| Exception                    | Description                     |
| ---------------------------- | ------------------------------- |
| `ObjectNotPresentError`      | Profile not found               |
| `InvalidObjectError`         | Invalid parameter format        |
| `MissingQueryParameterError` | Missing required parameters     |
| `AuthenticationError`        | Authentication failed           |
| `ServerError`                | Internal server error           |
| `InvalidAlgorithmError`      | Invalid algorithm specified     |

## Basic Configuration

```yaml
- name: Create basic IPsec Crypto Profile
  cdot65.scm.ipsec_crypto_profile:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
    name: "Standard-IPsec-Profile"
    description: "Standard IPsec crypto settings"
    esp:
      encryption:
        - "aes-256-cbc"
      authentication:
        - "sha256"
    dh_group: "group14"
    folder: "Shared"
    state: "present"
```

## Usage Examples

### Creating IPsec Crypto Profiles

IPsec Crypto Profiles can be created with either ESP or AH configuration, but not both simultaneously.

#### IPsec Crypto Profile with ESP Configuration

```yaml
- name: Create IPsec Crypto Profile with ESP configuration
  cdot65.scm.ipsec_crypto_profile:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "ESP-AES256-SHA256"
    description: "ESP profile with AES-256-CBC and SHA-256"
    esp:
      encryption:
        - "aes-256-cbc"
      authentication:
        - "sha256"
    dh_group: "group14"
    lifetime:
      seconds: 28800
    lifesize:
      mb: 20000
    folder: "Prisma Access"
    state: "present"
```

#### IPsec Crypto Profile with AH Configuration

```yaml
- name: Create IPsec Crypto Profile with AH configuration
  cdot65.scm.ipsec_crypto_profile:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "AH-SHA512"
    description: "AH profile with SHA-512"
    ah:
      authentication:
        - "sha512"
    dh_group: "group14"
    lifetime:
      seconds: 65535
    folder: "Prisma Access"
    state: "present"
```

### Updating IPsec Crypto Profiles

To update an existing IPsec Crypto Profile, specify the name and the attributes to change:

```yaml
- name: Update IPsec Crypto Profile DH group
  cdot65.scm.ipsec_crypto_profile:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "ESP-AES256-SHA256"
    dh_group: "group19"
    lifetime:
      hours: 8
    folder: "Prisma Access"
    state: "present"
```

### Deleting IPsec Crypto Profiles

To delete an IPsec Crypto Profile:

```yaml
- name: Delete IPsec Crypto Profile
  cdot65.scm.ipsec_crypto_profile:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "ESP-AES256-SHA256"
    folder: "Prisma Access"
    state: "absent"
```

## Managing Configuration Changes

### Change Detection

The module performs change detection by comparing the existing profile configuration to the requested configuration:

1. The module fetches the existing IPsec Crypto Profile from SCM using its name and container
2. It compares the existing profile's attributes to the requested configuration
3. If differences are found, the module updates the profile
4. If no differences are found, the module reports no changes needed

### Idempotence

This module is idempotent, meaning it will only make changes when necessary:

- If creating a profile that already exists with identical settings, no change is reported
- If updating a profile with settings that match the current configuration, no change is reported
- If deleting a profile that doesn't exist, no change is reported

## Error Handling

Common errors and how to handle them:

| Error                                     | Possible Cause                                    | Solution                                                       |
| ----------------------------------------- | ------------------------------------------------- | -------------------------------------------------------------- |
| "Authentication failed"                    | Invalid client_id, client_secret, or tsg_id       | Verify the authentication parameters                            |
| "Profile not found"                        | The specified profile doesn't exist               | Check the profile name and container                            |
| "Multiple containers specified"            | More than one container type was specified        | Specify exactly one of folder, snippet, or device               |
| "Both ESP and AH specified"                | Both ESP and AH configurations were provided      | Specify only one of ESP or AH                                   |
| "Multiple lifetime units specified"        | More than one lifetime unit was specified         | Specify only one lifetime unit (seconds, minutes, hours, days)  |
| "Multiple lifesize units specified"        | More than one lifesize unit was specified         | Specify only one lifesize unit (kb, mb, gb, tb)                 |
| "Validation error for encryption algorithm"| Invalid encryption algorithm specified            | Use only supported encryption algorithms                        |
| "Validation error for authentication algorithm"| Invalid authentication algorithm specified    | Use only supported authentication algorithms                    |

Error handling best practices:

```yaml
- name: Create or update IPsec Crypto Profile with error handling
  block:
    - name: Attempt to create IPsec Crypto Profile
      cdot65.scm.ipsec_crypto_profile:
        provider: "{{ provider }}"
        name: "Standard-IPsec-Profile"
        esp:
          encryption:
            - "aes-256-cbc"
          authentication:
            - "sha256"
        dh_group: "group14"
        folder: "Shared"
        state: "present"
      register: result
  rescue:
    - name: Handle error
      debug:
        msg: "Failed to create or update IPsec Crypto Profile: {{ ansible_failed_result.msg }}"
```

## Best Practices

### Security Considerations

- Use strong encryption and authentication algorithms:
  - Prefer AES-256 over weaker encryption options
  - Use SHA-256 or stronger for authentication
  - Avoid using deprecated algorithms like MD5 or DES

- DH Group selection:
  - For most environments, use group14 (2048-bit MODP) or higher
  - For high-security environments, use group19 (256-bit ECP) or group20 (384-bit ECP)
  - Avoid using no-pfs except when compatibility with legacy systems is required

### Performance Considerations

- Balance security and performance:
  - For high-throughput environments, consider the performance impact of stronger algorithms
  - GCM-based encryption (aes-128-gcm, aes-256-gcm) provides both strong security and better performance

- Lifetime and lifesize settings:
  - Shorter lifetimes increase security but also increase key negotiation overhead
  - Set appropriate lifetimes based on your security requirements and traffic patterns

### Compliance Considerations

- Follow industry standards and compliance requirements:
  - FIPS 140-2 compliance may restrict algorithm choices
  - Industry regulations may dictate minimum security requirements

### Documentation

- Document your IPsec crypto profile choices and rationale
- Include references to security policies or compliance requirements that informed your configuration

## Related Modules

- [cdot65.scm.ipsec_crypto_profile_info](ipsec_crypto_profile_info.md) - Gather information about IPsec crypto profiles
- [cdot65.scm.ike_crypto_profile](ike_crypto_profile.md) - Manage IKE crypto profiles
- [cdot65.scm.ike_gateway](ike_gateway.md) - Manage IKE gateways
- [cdot65.scm.ipsec_tunnel](ipsec_tunnel.md) - Manage IPsec tunnels
