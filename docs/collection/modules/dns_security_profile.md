# DNS Security Profile Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [DNS Security Profile Model Attributes](#dns-security-profile-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating DNS Security Profiles](#creating-dns-security-profiles)
    - [Basic DNS Security Profile](#basic-dns-security-profile)
    - [Comprehensive DNS Security Profile](#comprehensive-dns-security-profile)
    - [Updating DNS Security Profiles](#updating-dns-security-profiles)
    - [Deleting DNS Security Profiles](#deleting-dns-security-profiles)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `dns_security_profile` Ansible module provides functionality to manage DNS security profiles in
Palo Alto Networks' Strata Cloud Manager (SCM). These profiles define DNS security settings including
botnet domain filtering, DNS security categories, and sinkhole configurations to protect networks from
DNS-based threats and malicious activities.

## Core Methods

| Method     | Description                       | Parameters                             | Return Type                       |
| ---------- | --------------------------------- | -------------------------------------- | --------------------------------- |
| `create()` | Creates a new DNS security profile| `data: Dict[str, Any]`                 | `DnsSecurityProfileResponseModel` |
| `update()` | Updates an existing profile       | `profile: DnsSecurityProfileUpdateModel` | `DnsSecurityProfileResponseModel` |
| `delete()` | Removes a profile                 | `object_id: str`                       | `None`                            |
| `fetch()`  | Gets a profile by name            | `name: str`, `container: str`          | `DnsSecurityProfileResponseModel` |
| `list()`   | Lists profiles with filtering     | `folder: str`, `**filters`             | `List[DnsSecurityProfileResponseModel]` |

## DNS Security Profile Model Attributes

| Attribute        | Type | Required      | Description                                                |
| ---------------- | ---- | ------------- | ---------------------------------------------------------- |
| `name`           | str  | Yes           | Profile name. Must match pattern: ^[a-zA-Z0-9.\_-]+$       |
| `description`    | str  | No            | Description of the profile                                 |
| `botnet_domains` | dict | No            | Botnet domains configuration                               |
| `folder`         | str  | One container | The folder in which the profile is defined (max 64 chars)  |
| `snippet`        | str  | One container | The snippet in which the profile is defined (max 64 chars) |
| `device`         | str  | One container | The device in which the profile is defined (max 64 chars)  |

### Botnet Domains Attributes

| Attribute               | Type | Required | Description                           |
| ----------------------- | ---- | -------- | ------------------------------------- |
| `dns_security_categories` | list | No       | List of DNS security categories       |
| `sinkhole`              | dict | No       | Sinkhole configuration                |
| `whitelist`             | list | No       | List of whitelisted domains           |

### DNS Security Category Attributes

| Attribute        | Type | Required | Description                      | Choices                                                      |
| ---------------- | ---- | -------- | -------------------------------- | ------------------------------------------------------------ |
| `name`           | str  | Yes      | DNS security category name       |                                                              |
| `action`         | str  | No       | Action to take for the category  | `default`, `allow`, `block`, `sinkhole`                      |
| `log_level`      | str  | No       | Log level for the category       | `default`, `none`, `low`, `informational`, `medium`, `high`, `critical` |
| `packet_capture` | str  | No       | Packet capture option            | `disable`, `single-packet`, `extended-capture`               |

### Sinkhole Attributes

| Attribute       | Type | Required | Description                 | Choices                                |
| --------------- | ---- | -------- | --------------------------- | -------------------------------------- |
| `ipv4_address`  | str  | No       | IPv4 address for sinkhole   | `pan-sinkhole-default-ip`, `127.0.0.1` |
| `ipv6_address`  | str  | No       | IPv6 address for sinkhole   | `::1`                                  |

### Whitelist Domain Attributes

| Attribute     | Type | Required | Description                           |
| ------------- | ---- | -------- | ------------------------------------- |
| `name`        | str  | Yes      | Name of the whitelisted domain        |
| `description` | str  | No       | Description of the whitelisted domain |

## Exceptions

| Exception                    | Description                        |
| ---------------------------- | ---------------------------------- |
| `InvalidObjectError`         | Invalid profile data or format     |
| `NameNotUniqueError`         | Profile name already exists        |
| `ObjectNotPresentError`      | Profile not found                  |
| `MissingQueryParameterError` | Missing required parameters        |
| `InvalidCategoryError`       | Invalid DNS security category      |
| `AuthenticationError`        | Authentication failed              |
| `ServerError`                | Internal server error              |

## Basic Configuration

The DNS Security Profile module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic DNS Security Profile Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a DNS security profile exists
      cdot65.scm.dns_security_profile:
        provider: "{{ provider }}"
        name: "Basic-DNS-Security"
        description: "Basic DNS security profile"
        folder: "Texas"
        state: "present"
```

## Usage Examples

### Creating DNS Security Profiles

DNS security profiles help protect your network from DNS-based threats by detecting and blocking malicious domains.

### Basic DNS Security Profile

This example creates a simple DNS security profile without specific configurations.

```yaml
- name: Create a basic DNS security profile
  cdot65.scm.dns_security_profile:
    provider: "{{ provider }}"
    name: "Basic-DNS-Security"
    description: "Basic DNS security profile"
    folder: "Texas"
    state: "present"
```

### Comprehensive DNS Security Profile

This example creates a more comprehensive DNS security profile with botnet domain protection, security categories, and whitelist domains.

```yaml
- name: Create a comprehensive DNS security profile
  cdot65.scm.dns_security_profile:
    provider: "{{ provider }}"
    name: "Advanced-DNS-Security"
    description: "Advanced DNS security profile with botnet protection"
    botnet_domains:
      dns_security_categories:
        - name: "command-and-control"
          action: "block"
          log_level: "high"
          packet_capture: "single-packet"
        - name: "malware"
          action: "sinkhole"
          log_level: "critical"
        - name: "phishing"
          action: "block"
          log_level: "high"
      sinkhole:
        ipv4_address: "pan-sinkhole-default-ip"
        ipv6_address: "::1"
      whitelist:
        - name: "trusted-domain.com"
          description: "Trusted internal domain"
        - name: "example-partner.com"
          description: "Trusted partner domain"
    folder: "Texas"
    state: "present"
```

### Updating DNS Security Profiles

This example updates an existing DNS security profile with modified security categories and settings.

```yaml
- name: Update an existing DNS security profile
  cdot65.scm.dns_security_profile:
    provider: "{{ provider }}"
    name: "Advanced-DNS-Security"
    description: "Updated DNS security profile"
    botnet_domains:
      dns_security_categories:
        - name: "command-and-control"
          action: "sinkhole"
          log_level: "critical"
        - name: "malware"
          action: "block"
          log_level: "critical"
        - name: "spyware"
          action: "block"
          log_level: "high"
      sinkhole:
        ipv4_address: "127.0.0.1"
        ipv6_address: "::1"
      whitelist:
        - name: "trusted-domain.com"
          description: "Updated trusted domain"
    folder: "Texas"
    state: "present"
```

### Deleting DNS Security Profiles

This example removes a DNS security profile.

```yaml
- name: Delete a DNS security profile
  cdot65.scm.dns_security_profile:
    provider: "{{ provider }}"
    name: "Advanced-DNS-Security"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting DNS security profiles, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated DNS security profiles"
```

## Error Handling

It's important to handle potential errors when working with DNS security profiles.

```yaml
- name: Create or update DNS security profile with error handling
  block:
    - name: Ensure DNS security profile exists
      cdot65.scm.dns_security_profile:
        provider: "{{ provider }}"
        name: "Basic-DNS-Security"
        description: "Basic DNS security profile"
        botnet_domains:
          dns_security_categories:
            - name: "command-and-control"
              action: "block"
          sinkhole:
            ipv4_address: "pan-sinkhole-default-ip"
        folder: "Texas"
        state: "present"
      register: profile_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated DNS security profiles"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```

## Best Practices

### Security Category Configuration

- Block critical threat categories like command-and-control and malware
- Use sinkhole action for threats that require further analysis
- Set appropriate log levels based on the severity of the threat category
- Enable packet capture only for categories requiring detailed analysis
- Review and update category actions regularly based on threat intelligence

### Sinkhole Configuration

- Use pan-sinkhole-default-ip for standard deployments
- Configure custom sinkhole IPs when specific analysis infrastructure exists
- Ensure sinkhole servers are properly configured to collect and analyze traffic
- Monitor sinkhole traffic for threat analysis and incident response
- Document the purpose and configuration of the sinkhole

### Whitelist Management

- Only whitelist domains that are known to be safe and necessary
- Document the purpose of each whitelisted domain
- Regularly review the whitelist to ensure it remains current
- Implement a rigorous approval process for adding domains to the whitelist
- Consider using tags or descriptions to categorize whitelist entries

### Profile Organization

- Create profiles based on security requirements of different network segments
- Use descriptive names that reflect the profile's purpose
- Apply strict profiles to high-security zones
- Consider creating baseline profiles that can be referenced by other profiles
- Test profiles in a non-production environment before deployment

### Monitoring and Maintenance

- Regularly review logs for blocked domains and sinkhole activity
- Update profiles based on emerging threats and changing security requirements
- Monitor false positives and adjust whitelist accordingly
- Configure alerts for high-priority DNS security events
- Perform periodic audits of DNS security configurations

## Related Modules

- [dns_security_profile_info](dns_security_profile_info.md) - Retrieve information about DNS security profiles
- [security_rule](security_rule.md) - Configure security policies that use DNS security profiles
- [security_profiles_group](security_profiles_group.md) - Manage security profile groups that include DNS security profiles
- [external_dynamic_lists](external_dynamic_lists.md) - Manage external lists that can be used with DNS security