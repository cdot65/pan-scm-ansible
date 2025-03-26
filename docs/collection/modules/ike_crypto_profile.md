# Ike Crypto Profile Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [IKE Crypto Profile Model Attributes](#ike-crypto-profile-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating IKE Crypto Profiles](#creating-ike-crypto-profiles)
    - [Basic IKE Crypto Profile](#basic-ike-crypto-profile)
    - [Strong Encryption IKE Crypto Profile](#strong-encryption-ike-crypto-profile)
    - [Updating IKE Crypto Profiles](#updating-ike-crypto-profiles)
    - [Deleting IKE Crypto Profiles](#deleting-ike-crypto-profiles)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `ike_crypto_profile` Ansible module provides functionality to manage Internet Key Exchange (IKE)
Crypto Profiles in Palo Alto Networks' Strata Cloud Manager (SCM). IKE Crypto Profiles define the
encryption and authentication algorithms to be used during the IKE Phase-1 negotiation when
establishing a secure VPN tunnel.

## Core Methods

| Method     | Description                      | Parameters                             | Return Type                           |
| ---------- | -------------------------------- | -------------------------------------- | ------------------------------------- |
| `create()` | Creates a new IKE Crypto Profile | `data: Dict[str, Any]`                 | `IkeCryptoProfileResponseModel`       |
| `update()` | Updates an existing profile      | `profile: IkeCryptoProfileUpdateModel` | `IkeCryptoProfileResponseModel`       |
| `delete()` | Removes a profile                | `object_id: str`                       | `None`                                |
| `fetch()`  | Gets a profile by name           | `name: str`, `container: str`          | `IkeCryptoProfileResponseModel`       |
| `list()`   | Lists profiles with filtering    | `folder: str`, `**filters`             | `List[IkeCryptoProfileResponseModel]` |

## IKE Crypto Profile Model Attributes

| Attribute        | Type | Required      | Description                                                |
| ---------------- | ---- | ------------- | ---------------------------------------------------------- |
| `name`           | str  | Yes           | Name of the IKE Crypto Profile                             |
| `description`    | str  | No            | Description of the profile                                 |
| `encryption`     | list | Yes           | List of encryption algorithms                              |
| `authentication` | list | Yes           | List of authentication algorithms                          |
| `dh_group`       | list | Yes           | List of Diffie-Hellman groups                              |
| `lifetime`       | dict | No            | IKE SA lifetime settings                                   |
| `folder`         | str  | One container | The folder in which the profile is defined (max 64 chars)  |
| `snippet`        | str  | One container | The snippet in which the profile is defined (max 64 chars) |
| `device`         | str  | One container | The device in which the profile is defined (max 64 chars)  |

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

The IKE Crypto Profile module requires proper authentication credentials to access the Strata Cloud
Manager API.

```yaml
- name: Basic IKE Crypto Profile Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure an IKE Crypto Profile exists
      cdot65.scm.ike_crypto_profile:
        provider: "{{ provider }}"
        name: "Standard-Encryption"
        description: "Standard encryption profile for VPN tunnels"
        encryption: 
          - "aes-256-cbc"
          - "aes-256-gcm"
        authentication: 
          - "sha384"
        dh_group: 
          - "group14"
          - "group19"
        lifetime:
          days: 1
        folder: "Texas"
        state: "present"
```

## Usage Examples

### Creating IKE Crypto Profiles

IKE Crypto Profiles define the security parameters for IKE negotiation when establishing a VPN
tunnel. Different profiles can be created for different security requirements.

### Basic IKE Crypto Profile

This example creates a standard IKE Crypto Profile with moderate security settings.

```yaml
- name: Create a basic IKE Crypto Profile
  cdot65.scm.ike_crypto_profile:
    provider: "{{ provider }}"
    name: "Standard-Encryption"
    description: "Standard encryption profile for general VPN tunnels"
    encryption: 
      - "aes-128-cbc"
      - "aes-256-cbc"
    authentication: 
      - "sha1"
      - "sha256"
    dh_group: 
      - "group14"
      - "group2"
    lifetime:
      days: 1
    folder: "Texas"
    state: "present"
```

### Strong Encryption IKE Crypto Profile

This example creates a high-security IKE Crypto Profile with stronger algorithms.

```yaml
- name: Create a strong encryption IKE Crypto Profile
  cdot65.scm.ike_crypto_profile:
    provider: "{{ provider }}"
    name: "Strong-Encryption"
    description: "Strong encryption profile for sensitive VPN tunnels"
    encryption: 
      - "aes-256-gcm"
    authentication: 
      - "sha512"
    dh_group: 
      - "group20"
    lifetime:
      hours: 8
    folder: "Texas"
    state: "present"
```

### Updating IKE Crypto Profiles

This example updates an existing IKE Crypto Profile with new algorithms and settings.

```yaml
- name: Update an IKE Crypto Profile
  cdot65.scm.ike_crypto_profile:
    provider: "{{ provider }}"
    name: "Standard-Encryption"
    description: "Updated standard encryption profile"
    encryption: 
      - "aes-128-gcm"
      - "aes-256-gcm"
    authentication: 
      - "sha256"
      - "sha384"
    dh_group: 
      - "group14"
      - "group19"
    lifetime:
      hours: 12
    folder: "Texas"
    state: "present"
```

### Deleting IKE Crypto Profiles

This example removes an IKE Crypto Profile.

```yaml
- name: Delete an IKE Crypto Profile
  cdot65.scm.ike_crypto_profile:
    provider: "{{ provider }}"
    name: "Standard-Encryption"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting IKE Crypto Profiles, you need to commit your changes to apply
them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated IKE Crypto Profiles"
```

## Error Handling

It's important to handle potential errors when working with IKE Crypto Profiles.

```yaml
- name: Create or update IKE Crypto Profile with error handling
  block:
    - name: Ensure IKE Crypto Profile exists
      cdot65.scm.ike_crypto_profile:
        provider: "{{ provider }}"
        name: "Standard-Encryption"
        description: "Standard encryption profile for VPN tunnels"
        encryption: 
          - "aes-256-cbc"
          - "aes-256-gcm"
        authentication: 
          - "sha384"
        dh_group: 
          - "group14"
          - "group19"
        lifetime:
          days: 1
        folder: "Texas"
        state: "present"
      register: profile_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated IKE Crypto Profiles"
      when: profile_result.changed
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's an algorithm error
      debug:
        msg: "Please check the encryption, authentication, or DH group settings"
      when: "'algorithm' in ansible_failed_result.msg"
```

## Best Practices

### Algorithm Selection

- Use strong encryption algorithms (AES-256-GCM) where possible
- Avoid using deprecated or weak algorithms (DES, MD5)
- Use larger DH groups (14 or higher) for better security
- Balance security requirements with compatibility needs
- Follow industry standards and compliance requirements

### Lifetime Management

- Set reasonable lifetimes based on your security requirements
- Shorter lifetimes increase security but also increase rekeying overhead
- Consider the performance impact of frequent rekeying
- Document your lifetime decisions and rationale

### Profile Organization

- Create different profiles for different security levels needed by various connections
- Use high-security profiles for sensitive networks
- Use standard profiles for general-purpose connections
- Document profile usage to track where each profile is applied
- Use descriptive names that indicate security level or purpose

### Implementation Strategy

- Test profiles in a non-production environment before deployment
- Verify compatibility with peer devices before implementation
- Implement changes during maintenance windows
- Have a rollback plan for unsuccessful implementations
- Monitor VPN connections after implementation

### Audit and Compliance

- Regularly review profiles for outdated or weak algorithms
- Update profiles as new security vulnerabilities are discovered
- Document profiles for compliance and audit purposes
- Maintain an inventory of profiles and their applications

## Related Modules

- [ike_gateway](ike_gateway.md) - Configure IKE gateways that reference IKE Crypto profiles
- [ipsec_crypto_profile](ipsec_crypto_profile.md) - Configure IPsec Crypto profiles for Phase-2
  negotiations
- [ipsec_tunnel](ipsec_tunnel.md) - Configure IPsec tunnels that use IKE gateways and crypto
  profiles
