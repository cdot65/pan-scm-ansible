# External Dynamic Lists Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [External Dynamic List Model Attributes](#external-dynamic-list-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating External Dynamic Lists](#creating-external-dynamic-lists)
    - [Basic IP-Based External Dynamic List](#basic-ip-based-external-dynamic-list)
    - [Domain-Based External Dynamic List](#domain-based-external-dynamic-list)
    - [Advanced URL-Based External Dynamic List](#advanced-url-based-external-dynamic-list)
    - [Updating External Dynamic Lists](#updating-external-dynamic-lists)
    - [Deleting External Dynamic Lists](#deleting-external-dynamic-lists)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `external_dynamic_lists` Ansible module provides functionality to manage External Dynamic Lists
(EDLs) in Palo Alto Networks' Strata Cloud Manager (SCM). EDLs are used to dynamically fetch updated
lists of IPs, domains, URLs, IMSIs, or IMEIs from external sources to use in security policies. This
module enables you to create, update, and delete various types of external dynamic lists with
configurable update intervals.

## Core Methods

| Method     | Description                         | Parameters                            | Return Type                              |
| ---------- | ----------------------------------- | ------------------------------------- | ---------------------------------------- |
| `create()` | Creates a new external dynamic list | `data: Dict[str, Any]`                | `ExternalDynamicListResponseModel`       |
| `update()` | Updates an existing EDL             | `edl: ExternalDynamicListUpdateModel` | `ExternalDynamicListResponseModel`       |
| `delete()` | Removes an EDL                      | `object_id: str`                      | `None`                                   |
| `fetch()`  | Gets an EDL by name                 | `name: str`, `container: str`         | `ExternalDynamicListResponseModel`       |
| `list()`   | Lists EDLs with filtering           | `folder: str`, `**filters`            | `List[ExternalDynamicListResponseModel]` |

## External Dynamic List Model Attributes

| Attribute     | Type | Required        | Description                                                 |
| ------------- | ---- | --------------- | ----------------------------------------------------------- |
| `name`        | str  | Yes             | Name of the external dynamic list (max 63 chars)            |
| `description` | str  | No              | Description of the external dynamic list (max 255 chars)    |
| `ip_list`     | dict | One list type   | Configuration for an IP-based external dynamic list         |
| `domain_list` | dict | One list type   | Configuration for a domain-based external dynamic list      |
| `url_list`    | dict | One list type   | Configuration for a URL-based external dynamic list         |
| `imsi_list`   | dict | One list type   | Configuration for an IMSI-based external dynamic list       |
| `imei_list`   | dict | One list type   | Configuration for an IMEI-based external dynamic list       |
| `five_minute` | bool | One update type | Configure list to update every five minutes                 |
| `hourly`      | bool | One update type | Configure list to update hourly                             |
| `daily`       | dict | One update type | Configure list to update daily at specified hour            |
| `weekly`      | dict | One update type | Configure list to update weekly on specified day and time   |
| `monthly`     | dict | One update type | Configure list to update monthly on specified day and time  |
| `folder`      | str  | One container   | The folder in which the resource is defined (max 64 chars)  |
| `snippet`     | str  | One container   | The snippet in which the resource is defined (max 64 chars) |
| `device`      | str  | One container   | The device in which the resource is defined (max 64 chars)  |

### List Type Attributes

| Attribute             | Type | Required | Description                                               |
| --------------------- | ---- | -------- | --------------------------------------------------------- |
| `url`                 | str  | Yes      | URL to fetch the list content                             |
| `exception_list`      | list | No       | List of entries to exclude from the external dynamic list |
| `certificate_profile` | str  | No       | Client certificate profile for secure connections         |
| `auth`                | dict | No       | Authentication credentials for the list URL               |
| `expand_domain`       | bool | No       | Domain expansion (domain_list only)                       |

### Update Interval Attributes

| Parameter     | Sub-parameters                           | Description                                   |
| ------------- | ---------------------------------------- | --------------------------------------------- |
| `five_minute` | None (boolean flag)                      | Update every 5 minutes                        |
| `hourly`      | None (boolean flag)                      | Update every hour                             |
| `daily`       | `at`: Hour of day (00-23)                | Update once a day at the specified hour       |
| `weekly`      | `day_of_week`: Day of week<br>`at`: Hour | Update once a week on specified day and time  |
| `monthly`     | `day_of_month`: Day (1-31)<br>`at`: Hour | Update once a month on specified day and time |

### Provider Dictionary Attributes

| Attribute       | Type | Required | Default | Description                      |
| --------------- | ---- | -------- | ------- | -------------------------------- |
| `client_id`     | str  | Yes      |         | Client ID for authentication     |
| `client_secret` | str  | Yes      |         | Client secret for authentication |
| `tsg_id`        | str  | Yes      |         | Tenant Service Group ID          |
| `log_level`     | str  | No       | "INFO"  | Log level for the SDK            |

## Exceptions

| Exception                    | Description                 |
| ---------------------------- | --------------------------- |
| `InvalidObjectError`         | Invalid EDL data or format  |
| `NameNotUniqueError`         | EDL name already exists     |
| `ObjectNotPresentError`      | EDL not found               |
| `MissingQueryParameterError` | Missing required parameters |
| `AuthenticationError`        | Authentication failed       |
| `ServerError`                | Internal server error       |
| `InvalidURLError`            | Invalid URL format          |
| `InvalidIntervalError`       | Invalid update interval     |

## Basic Configuration

The External Dynamic Lists module requires proper authentication credentials to access the Strata
Cloud Manager API.

```yaml
- name: Basic External Dynamic List Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure an IP-based external dynamic list exists
      cdot65.scm.external_dynamic_lists:
        provider: "{{ provider }}"
        name: "malicious-ips"
        description: "Known malicious IPs"
        folder: "Texas"
        ip_list:
          url: "https://threatfeeds.example.com/ips.txt"
        hourly: true
        state: "present"
```

## Usage Examples

### Creating External Dynamic Lists

External dynamic lists can be created with different list types (IP, domain, URL, IMSI, IMEI) and
update intervals to meet various security requirements.

### Basic IP-Based External Dynamic List

This example creates a simple IP-based external dynamic list with hourly updates.

```yaml
- name: Create IP-based external dynamic list with hourly updates
  cdot65.scm.external_dynamic_lists:
    provider: "{{ provider }}"
    name: "malicious-ips"
    description: "Known malicious IPs"
    folder: "Texas"
    ip_list:
      url: "https://threatfeeds.example.com/ips.txt"
      auth:
        username: "user123"
        password: "pass123"
    hourly: true
    state: "present"
```

### Domain-Based External Dynamic List

This example creates a domain-based external dynamic list with daily updates.

```yaml
- name: Create domain-based external dynamic list with daily updates at 3 AM
  cdot65.scm.external_dynamic_lists:
    provider: "{{ provider }}"
    name: "blocked-domains"
    description: "Blocked domains list"
    folder: "Texas"
    domain_list:
      url: "https://threatfeeds.example.com/domains.txt"
      expand_domain: true
    daily:
      at: "03"
    state: "present"
```

### Advanced URL-Based External Dynamic List

This example creates a URL-based external dynamic list with weekly updates and exception list.

```yaml
- name: Create URL-based external dynamic list with weekly updates
  cdot65.scm.external_dynamic_lists:
    provider: "{{ provider }}"
    name: "malicious-urls"
    description: "Malicious URLs list"
    folder: "Texas"
    url_list:
      url: "https://threatfeeds.example.com/urls.txt"
      exception_list:
        - "example.com/allowed"
        - "example.org/allowed"
      certificate_profile: "default-certificate-profile"
    weekly:
      day_of_week: "monday"
      at: "12"
    state: "present"
```

### Updating External Dynamic Lists

This example updates an existing external dynamic list with a new update interval and
authentication.

```yaml
- name: Update external dynamic list with new description and auth
  cdot65.scm.external_dynamic_lists:
    provider: "{{ provider }}"
    name: "malicious-ips"
    description: "Updated malicious IPs list"
    folder: "Texas"
    ip_list:
      url: "https://threatfeeds.example.com/ips.txt"
      auth:
        username: "newuser"
        password: "newpass"
    five_minute: true
    state: "present"
```

### Deleting External Dynamic Lists

This example removes an external dynamic list from SCM.

```yaml
- name: Delete external dynamic list
  cdot65.scm.external_dynamic_lists:
    provider: "{{ provider }}"
    name: "blocked-domains"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting external dynamic lists, you need to commit your changes to
apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: [ "Texas" ]
    description: "Updated external dynamic lists"
```

## Error Handling

It's important to handle potential errors when working with external dynamic lists.

```yaml
- name: Create or update external dynamic list with error handling
  block:
    - name: Ensure external dynamic list exists
      cdot65.scm.external_dynamic_lists:
        provider: "{{ provider }}"
        name: "malicious-ips"
        description: "Known malicious IPs"
        folder: "Texas"
        ip_list:
          url: "https://threatfeeds.example.com/ips.txt"
        hourly: true
        state: "present"
      register: edl_result

    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: [ "Texas" ]
        description: "Updated external dynamic lists"
      when: edl_result.changed

  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"

    - name: Check if it's a URL error
      debug:
        msg: "Please check the URL format or accessibility"
      when: "'url' in ansible_failed_result.msg"
```

## Best Practices

### List Type Selection

- Choose the appropriate list type (IP, domain, URL, IMSI, IMEI) based on your security requirements
- Use IP lists for IP address filtering, domain lists for FQDN filtering, URL lists for specific
  path filtering
- Consider domain expansion settings for domain-based lists to improve coverage
- Document the purpose and source of each EDL

### Update Interval Selection

- Set update intervals based on the volatility of the threat intelligence source
- Use shorter intervals (five-minute, hourly) for frequently changing threat feeds
- Use longer intervals (daily, weekly) for more stable lists to reduce load
- Consider time zones when configuring specific update times

### Source Configuration

- Use trusted and reliable threat intelligence sources
- Implement proper authentication for secure access to EDL sources
- Use certificate profiles for HTTPS connections to verify source authenticity
- Test EDL sources before implementing in production

### Exception List Management

- Document all exceptions thoroughly with justification
- Review exception lists regularly to ensure they're still required
- Keep exception lists as small as possible to maintain security posture
- Implement change management for exception list modifications

### EDL Content Considerations

- Understand the format requirements for each list type
- Ensure source lists provide clean, well-formatted data
- Consider size limitations and performance impact of large lists
- Validate list content before using in production

### Performance and Scalability

- Monitor the impact of EDLs on firewall performance
- Consolidate similar EDLs to reduce management overhead
- Consider the frequency of updates and potential impact on resources
- Test large or frequently updated EDLs thoroughly before deployment

## Related Modules

- [external_dynamic_lists_info](external_dynamic_lists_info.md) - Retrieve information about
  external dynamic lists
- [security_rule](security_rule.md) - Configure security policies that use external dynamic lists
- [tag](tag.md) - Create, update, and delete tags for organizing external dynamic lists
- [security_profiles_group](security_profiles_group.md) - Manage security profile groups that might
  reference external dynamic lists
