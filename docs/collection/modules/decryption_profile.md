# Decryption Profile Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Decryption Profile Model Attributes](#decryption-profile-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating Decryption Profiles](#creating-decryption-profiles)
    - [Basic Decryption Profile](#basic-decryption-profile)
    - [Comprehensive Decryption Profile](#comprehensive-decryption-profile)
    - [Updating Decryption Profiles](#updating-decryption-profiles)
    - [Deleting Decryption Profiles](#deleting-decryption-profiles)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `decryption_profile` Ansible module provides functionality to manage decryption profiles in 
Palo Alto Networks' Strata Cloud Manager (SCM). These profiles define SSL/TLS decryption settings 
including SSL forward proxy, inbound inspection, and protocol configurations. Decryption profiles 
enable visibility into encrypted traffic while maintaining security controls.

## Core Methods

| Method     | Description                       | Parameters                           | Return Type                      |
| ---------- | --------------------------------- | ------------------------------------ | -------------------------------- |
| `create()` | Creates a new decryption profile  | `data: Dict[str, Any]`               | `DecryptionProfileResponseModel` |
| `update()` | Updates an existing profile       | `profile: DecryptionProfileUpdateModel` | `DecryptionProfileResponseModel` |
| `delete()` | Removes a profile                 | `object_id: str`                     | `None`                           |
| `fetch()`  | Gets a profile by name            | `name: str`, `container: str`        | `DecryptionProfileResponseModel` |
| `list()`   | Lists profiles with filtering     | `folder: str`, `**filters`           | `List[DecryptionProfileResponseModel]` |

## Decryption Profile Model Attributes

| Attribute              | Type | Required      | Description                                                |
| ---------------------- | ---- | ------------- | ---------------------------------------------------------- |
| `name`                 | str  | Yes           | Profile name. Must match pattern: ^[a-zA-Z0-9.\_-]+$       |
| `description`          | str  | No            | Description of the profile                                 |
| `ssl_forward_proxy`    | dict | No            | SSL Forward Proxy settings                                 |
| `ssl_inbound_inspection` | dict | No          | SSL Inbound Inspection settings                            |
| `ssl_no_proxy`         | dict | No            | SSL No Proxy settings                                      |
| `ssl_protocol_settings` | dict | No           | SSL Protocol settings                                      |
| `folder`               | str  | One container | The folder in which the profile is defined (max 64 chars)  |
| `snippet`              | str  | One container | The snippet in which the profile is defined (max 64 chars) |
| `device`               | str  | One container | The device in which the profile is defined (max 64 chars)  |

### SSL Forward Proxy Attributes

| Attribute                  | Type | Required | Description                                        |
| -------------------------- | ---- | -------- | -------------------------------------------------- |
| `enabled`                  | bool | No       | Enable SSL Forward Proxy (default: false)          |
| `block_unsupported_cipher` | bool | No       | Block sessions with unsupported ciphers            |
| `block_unknown_cert`       | bool | No       | Block sessions with unknown certificates           |
| `block_expired_cert`       | bool | No       | Block sessions with expired certificates           |
| `block_timeoff_cert`       | bool | No       | Block sessions with certificates not yet valid     |
| `block_untrusted_issuer`   | bool | No       | Block sessions with untrusted issuer certificates  |
| `block_unknown_status`     | bool | No       | Block sessions with unknown certificate status     |

### SSL No Proxy Attributes

| Attribute                        | Type | Required | Description                                      |
| -------------------------------- | ---- | -------- | ------------------------------------------------ |
| `enabled`                        | bool | No       | Enable SSL No Proxy (default: false)             |
| `block_session_expired_cert`     | bool | No       | Block sessions with expired certificates         |
| `block_session_untrusted_issuer` | bool | No       | Block sessions with untrusted issuer certificates|

### SSL Inbound Inspection Attributes

| Attribute | Type | Required | Description                           |
| --------- | ---- | -------- | ------------------------------------- |
| `enabled` | bool | No       | Enable SSL Inbound Inspection (default: false) |

### SSL Protocol Settings Attributes

| Attribute          | Type | Required | Description                    | Choices                                              |
| ------------------ | ---- | -------- | ------------------------------ | ---------------------------------------------------- |
| `min_version`      | str  | No       | Minimum TLS version to support | `"tls1-0"`, `"tls1-1"`, `"tls1-2"`, `"tls1-3"`       |
| `max_version`      | str  | No       | Maximum TLS version to support | `"tls1-0"`, `"tls1-1"`, `"tls1-2"`, `"tls1-3"`       |
| `keyxchg_algorithm` | list | No      | Key exchange algorithms        | `"dhe"`, `"ecdhe"`                                   |
| `encrypt_algorithm` | list | No      | Encryption algorithms          | `"rc4"`, `"rc4-md5"`, `"aes-128-cbc"`, `"aes-128-gcm"`, `"aes-256-cbc"`, `"aes-256-gcm"`, `"3des"` |
| `auth_algorithm`   | list | No       | Authentication algorithms      | `"sha1"`, `"sha256"`, `"sha384"`                     |

## Exceptions

| Exception                    | Description                           |
| ---------------------------- | ------------------------------------- |
| `InvalidObjectError`         | Invalid profile data or format        |
| `NameNotUniqueError`         | Profile name already exists           |
| `ObjectNotPresentError`      | Profile not found                     |
| `MissingQueryParameterError` | Missing required parameters           |
| `InvalidSSLConfigError`      | Invalid SSL configuration             |
| `AuthenticationError`        | Authentication failed                 |
| `ServerError`                | Internal server error                 |

## Basic Configuration

The Decryption Profile module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Decryption Profile Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a decryption profile exists
      cdot65.scm.decryption_profile:
        provider: "{{ provider }}"
        name: "Basic-Decryption-Profile"
        description: "Basic SSL decryption profile"
        folder: "Production"
        ssl_forward_proxy:
          enabled: true
          block_expired_cert: true
        ssl_protocol_settings:
          min_version: "tls1-2"
          max_version: "tls1-3"
        state: "present"
```

## Usage Examples

### Creating Decryption Profiles

Decryption profiles define how SSL/TLS traffic should be decrypted and what certificate validation checks should be performed.

### Basic Decryption Profile

This example creates a simple decryption profile with SSL Forward Proxy enabled.

```yaml
- name: Create a basic decryption profile
  cdot65.scm.decryption_profile:
    provider: "{{ provider }}"
    name: "Basic-Decryption-Profile"
    description: "Basic SSL decryption profile with forward proxy"
    folder: "Production"
    ssl_forward_proxy:
      enabled: true
      block_expired_cert: true
      block_untrusted_issuer: true
    ssl_protocol_settings:
      min_version: "tls1-2"
      max_version: "tls1-3"
    state: "present"
```

### Comprehensive Decryption Profile

This example creates a more comprehensive decryption profile with multiple proxy types and extensive protocol settings.

```yaml
- name: Create a comprehensive decryption profile
  cdot65.scm.decryption_profile:
    provider: "{{ provider }}"
    name: "Advanced-Decryption-Profile"
    description: "Advanced SSL decryption profile with multiple proxy types"
    folder: "Production"
    ssl_forward_proxy:
      enabled: true
      block_expired_cert: true
      block_untrusted_issuer: true
      block_unknown_cert: true
      block_timeoff_cert: true
    ssl_no_proxy:
      enabled: true
      block_session_expired_cert: true
      block_session_untrusted_issuer: true
    ssl_protocol_settings:
      min_version: "tls1-2"
      max_version: "tls1-3"
      keyxchg_algorithm: ["ecdhe"]
      encrypt_algorithm: ["aes-128-gcm", "aes-256-gcm"]
      auth_algorithm: ["sha256", "sha384"]
    state: "present"
```

### Updating Decryption Profiles

This example updates an existing decryption profile with additional security settings.

```yaml
- name: Update a decryption profile
  cdot65.scm.decryption_profile:
    provider: "{{ provider }}"
    name: "Basic-Decryption-Profile"
    description: "Updated decryption profile with enhanced security"
    folder: "Production"
    ssl_forward_proxy:
      enabled: true
      block_expired_cert: true
      block_untrusted_issuer: true
      block_unknown_cert: true
      block_unknown_status: true
    ssl_protocol_settings:
      min_version: "tls1-2"
      max_version: "tls1-3"
      keyxchg_algorithm: ["ecdhe"]
      encrypt_algorithm: ["aes-256-gcm"]  # Only use the strongest encryption
      auth_algorithm: ["sha384"]          # Only use the strongest authentication
    state: "present"
```

### Deleting Decryption Profiles

This example removes a decryption profile.

```yaml
- name: Delete a decryption profile
  cdot65.scm.decryption_profile:
    provider: "{{ provider }}"
    name: "Basic-Decryption-Profile"
    folder: "Production"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting decryption profiles, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Production"]
    description: "Updated decryption profiles"
```

## Error Handling

It's important to handle potential errors when working with decryption profiles.

```yaml
- name: Create or update decryption profile with error handling
  block:
    - name: Ensure decryption profile exists
      cdot65.scm.decryption_profile:
        provider: "{{ provider }}"
        name: "Basic-Decryption-Profile"
        description: "Basic SSL decryption profile"
        folder: "Production"
        ssl_forward_proxy:
          enabled: true
          block_expired_cert: true
        ssl_protocol_settings:
          min_version: "tls1-2"
          max_version: "tls1-3"
        state: "present"
      register: profile_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Production"]
        description: "Updated decryption profiles"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```

## Best Practices

### Proxy Type Selection

- Choose SSL Forward Proxy for outbound traffic inspection
- Use SSL Inbound Inspection for servers under your control
- Enable SSL No Proxy for traffic that should be inspected but not decrypted
- Consider using multiple proxy types based on different security zones
- Document the purpose and usage scenario for each decryption profile

### Certificate Validation

- Enable blocking of expired certificates to prevent potential security risks
- Consider blocking certificates with untrusted issuers for sensitive traffic
- Balance security requirements with potential impact on legitimate traffic
- Implement more stringent certificate validation for high-security zones
- Create separate profiles with different validation settings for different security requirements

### Protocol Security

- Set minimum TLS version to at least TLS 1.2 for modern security standards
- Avoid enabling older TLS versions unless absolutely necessary for legacy systems
- Select strong encryption algorithms (AES-GCM) and phase out weaker ones
- Choose secure key exchange algorithms (ECDHE preferred over DHE)
- Regularly review and update protocol settings as security standards evolve

### Performance Considerations

- Balance security benefits with potential performance impact
- Monitor decryption performance and adjust settings if needed
- Consider hardware requirements for SSL decryption at scale
- Test decryption profiles with representative traffic before deploying to production
- Implement bypass mechanisms for applications that cannot tolerate decryption

### Compliance Considerations

- Document decryption policies for compliance requirements
- Ensure privacy regulations are addressed in your decryption strategy
- Consider legal implications of decrypting certain types of traffic
- Implement appropriate logging and notification mechanisms
- Create specialized decryption profiles for regulated traffic

## Related Modules

- [decryption_profile_info](decryption_profile_info.md) - Retrieve information about decryption profiles
- [security_rule](security_rule.md) - Configure security policies that use decryption profiles
- [security_profiles_group](security_profiles_group.md) - Manage security profile groups that can include decryption settings