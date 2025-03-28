# Security Rule Configuration Object

## Table of Contents

- [Security Rule Configuration Object](#security-rule-configuration-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [Security Rule Model Attributes](#security-rule-model-attributes)
    - [Profile Setting Attributes](#profile-setting-attributes)
    - [Action Options](#action-options)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Creating Security Rules](#creating-security-rules)
    - [Basic Security Rule](#basic-security-rule)
    - [Security Rule with Advanced Settings](#security-rule-with-advanced-settings)
    - [Post-Rulebase Security Rules](#post-rulebase-security-rules)
    - [Updating Security Rules](#updating-security-rules)
    - [Deleting Security Rules](#deleting-security-rules)
  - [Managing Configuration Changes](#managing-configuration-changes)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Rule Design](#rule-design)
    - [Security Controls](#security-controls)
    - [Rule Organization](#rule-organization)
    - [Policy Management](#policy-management)
    - [Performance Considerations](#performance-considerations)
  - [Related Modules](#related-modules)

## Overview

The `security_rule` Ansible module provides functionality to manage security rule objects in Palo
Alto Networks' Strata Cloud Manager (SCM). Security rules define the traffic control policies that
determine which traffic is allowed or denied between zones. This module enables you to create,
update, and delete security rules with various parameters such as source and destination zones,
addresses, applications, services, and more.

## Core Methods

| Method     | Description                 | Parameters                                     | Return Type                       |
| ---------- | --------------------------- | ---------------------------------------------- | --------------------------------- |
| `create()` | Creates a new security rule | `data: Dict[str, Any]`                         | `SecurityRuleResponseModel`       |
| `update()` | Updates an existing rule    | `rule: SecurityRuleUpdateModel`                | `SecurityRuleResponseModel`       |
| `delete()` | Removes a rule              | `object_id: str`                               | `None`                            |
| `fetch()`  | Gets a rule by name         | `name: str`, `container: str`, `rulebase: str` | `SecurityRuleResponseModel`       |
| `list()`   | Lists rules with filtering  | `folder: str`, `rulebase: str`, `**filters`    | `List[SecurityRuleResponseModel]` |

## Security Rule Model Attributes

| Attribute            | Type      | Required      | Description                                                    |
| -------------------- | --------- | ------------- | -------------------------------------------------------------- |
| `name`               | str       | Yes           | The name of the security rule                                  |
| `disabled`           | bool      | No            | Whether the security rule is disabled (default: false)         |
| `description`        | str       | No            | Description of the security rule                               |
| `tag`                | List[str] | No            | List of tags associated with the security rule                 |
| `from_`              | List[str] | No            | List of source security zones (default: ["any"])               |
| `source`             | List[str] | No            | List of source addresses (default: ["any"])                    |
| `negate_source`      | bool      | No            | Whether to negate the source addresses (default: false)        |
| `source_user`        | List[str] | No            | List of source users and/or groups (default: ["any"])          |
| `source_hip`         | List[str] | No            | List of source Host Integrity Profiles (default: ["any"])      |
| `to_`                | List[str] | No            | List of destination security zones (default: ["any"])          |
| `destination`        | List[str] | No            | List of destination addresses (default: ["any"])               |
| `negate_destination` | bool      | No            | Whether to negate the destination addresses (default: false)   |
| `destination_hip`    | List[str] | No            | List of destination Host Integrity Profiles (default: ["any"]) |
| `application`        | List[str] | No            | List of applications (default: ["any"])                        |
| `service`            | List[str] | No            | List of services (default: ["any"])                            |
| `category`           | List[str] | No            | List of URL categories (default: ["any"])                      |
| `action`             | str       | No            | Action for matched traffic (default: "allow")                  |
| `profile_setting`    | dict      | No            | Security profile settings for the rule                         |
| `log_setting`        | str       | No            | Log forwarding profile for the rule                            |
| `schedule`           | str       | No            | Schedule for the rule                                          |
| `log_start`          | bool      | No            | Whether to log at the start of the session                     |
| `log_end`            | bool      | No            | Whether to log at the end of the session                       |
| `folder`             | str       | One container | The folder in which the rule is defined (max 64 chars)         |
| `snippet`            | str       | One container | The snippet in which the rule is defined (max 64 chars)        |
| `device`             | str       | One container | The device in which the rule is defined (max 64 chars)         |
| `rulebase`           | str       | No            | Which rulebase to use (pre or post) (default: "pre")           |

### Profile Setting Attributes

| Attribute  | Type      | Required | Description                              |
| ---------- | --------- | -------- | ---------------------------------------- |
| `group`    | List[str] | No       | List of security profile groups to apply |
| `profiles` | dict      | No       | Individual security profiles to apply    |

### Action Options

| Value          | Description                                        |
| -------------- | -------------------------------------------------- |
| `allow`        | Allow the traffic and apply any security profiles  |
| `deny`         | Silently drop the traffic with an ICMP unreachable |
| `drop`         | Silently drop the traffic                          |
| `reset-client` | Send TCP reset to the client                       |
| `reset-server` | Send TCP reset to the server                       |
| `reset-both`   | Send TCP reset to both client and server           |

## Exceptions

| Exception                    | Description                          |
| ---------------------------- | ------------------------------------ |
| `InvalidObjectError`         | Invalid security rule data or format |
| `NameNotUniqueError`         | Security rule name already exists    |
| `ObjectNotPresentError`      | Security rule not found              |
| `MissingQueryParameterError` | Missing required parameters          |
| `AuthenticationError`        | Authentication failed                |
| `ServerError`                | Internal server error                |
| `ReferenceNotFoundError`     | Referenced object does not exist     |

## Basic Configuration

The Security Rule module requires proper authentication credentials to access the Strata Cloud
Manager API.

```yaml
- name: Basic Security Rule Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a security rule exists
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Allow_Internal_Traffic"
        description: "Allow traffic between internal zones"
        from_: ["trust"]
        to_: ["trust"]
        action: "allow"
        folder: "Texas"
        state: "present"
```

## Usage Examples

### Creating Security Rules

Security rules control which traffic is allowed to flow through the firewall based on various match
criteria.

### Basic Security Rule

This example creates a simple security rule to allow web traffic from the Internet to web servers in
the DMZ.

```yaml
- name: Create a basic security rule
  cdot65.scm.security_rule:
    provider: "{{ provider }}"
    name: "Allow_Web_Traffic"
    description: "Allow web traffic to the web servers"
    from_: ["Internet"]
    source: ["any"]
    to_: ["DMZ"]
    destination: ["Web-Servers"]
    application: ["web-browsing", "ssl"]
    service: ["application-default"]
    action: "allow"
    folder: "Texas"
    state: "present"
```

### Security Rule with Advanced Settings

This example creates a security rule with advanced settings including security profiles, logging,
and tags.

```yaml
- name: Create a security rule with advanced settings
  cdot65.scm.security_rule:
    provider: "{{ provider }}"
    name: "Allow_Web_Traffic_Advanced"
    description: "Allow web traffic with advanced security controls"
    from_: ["Internet"]
    source: ["any"]
    to_: ["DMZ"]
    destination: ["Web-Servers"]
    application: ["web-browsing", "ssl"]
    service: ["application-default"]
    action: "allow"
    profile_setting:
      group: ["strict-security"]
    log_setting: "detailed-logging"
    log_start: false
    log_end: true
    tag: ["web", "internet", "production"]
    folder: "Texas"
    state: "present"
```

### Post-Rulebase Security Rules

This example creates a security rule in the post-rulebase to block traffic to known malicious sites.

```yaml
- name: Create a post-rulebase security rule
  cdot65.scm.security_rule:
    provider: "{{ provider }}"
    name: "Block_Malicious_Traffic"
    description: "Block traffic to known malicious sites"
    from_: ["any"]
    source: ["any"]
    to_: ["any"]
    destination: ["any"]
    application: ["any"]
    service: ["any"]
    category: ["malware", "command-and-control"]
    action: "deny"
    folder: "Texas"
    rulebase: "post"
    log_setting: "default-log-profile"
    log_end: true
    state: "present"
```

### Updating Security Rules

This example updates an existing security rule with new settings.

```yaml
- name: Update a security rule
  cdot65.scm.security_rule:
    provider: "{{ provider }}"
    name: "Allow_Web_Traffic"
    description: "Allow web traffic to the web servers (updated)"
    from_: ["Internet"]
    source: ["any"]
    to_: ["DMZ"]
    destination: ["Web-Servers"]
    application: ["web-browsing", "ssl", "http2"]
    service: ["application-default"]
    action: "allow"
    profile_setting:
      group: ["strict-security"]
    tag: ["web", "internet", "updated"]
    folder: "Texas"
    state: "present"
```

### Deleting Security Rules

This example removes a security rule that is no longer needed.

```yaml
- name: Delete a security rule
  cdot65.scm.security_rule:
    provider: "{{ provider }}"
    name: "Allow_Web_Traffic"
    folder: "Texas"
    rulebase: "pre"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting security rules, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated security rule configurations"
```

## Error Handling

It's important to handle potential errors when working with security rules.

```yaml
- name: Create or update security rule with error handling
  block:
    - name: Ensure security rule exists
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Allow_Web_Traffic"
        description: "Allow web traffic to the web servers"
        from_: ["Internet"]
        source: ["any"]
        to_: ["DMZ"]
        destination: ["Web-Servers"]
        application: ["web-browsing", "ssl"]
        service: ["application-default"]
        action: "allow"
        folder: "Texas"
        state: "present"
      register: rule_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated security rule configurations"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Check if referenced object doesn't exist
      debug:
        msg: "Check if all referenced objects (zones, addresses, etc.) exist."
      when: "'referenced object does not exist' in ansible_failed_result.msg"
```

## Best Practices

### Rule Design

- Create specific, targeted rules instead of overly broad ones
- Order rules from most specific to most general
- Use appropriate applications instead of relying solely on ports
- Include clear descriptions that explain the rule's purpose
- Consider using "application-default" for service when appropriate

### Security Controls

- Apply appropriate security profiles to allow rules
- Enable logging for security-critical rules
- Consider logging at both session start and end for important traffic
- Use URL filtering categories to control web access
- Implement stricter controls for higher-risk traffic

### Rule Organization

- Use a consistent naming convention for rules
- Group related rules together
- Use tags to categorize and organize rules
- Maintain a clear separation between pre-rulebase and post-rulebase rules
- Document rule dependencies and relationships

### Policy Management

- Regularly review and clean up unused or redundant rules
- Test changes in a development environment before applying to production
- Document the business purpose for each rule
- Implement a rule review process for ongoing maintenance
- Utilize rule hit counts to identify unused rules

### Performance Considerations

- Minimize the use of "any" in heavily trafficked rules
- Place frequently hit rules earlier in the rulebase
- Use address groups and service groups for better manageability
- Consider impact of complex application dependencies
- Balance security requirements with performance needs

## Related Modules

- [security_rule_info](security_rule_info.md) - Retrieve information about security rules
- [security_zone](security_zone.md) - Manage security zones referenced in rules
- [address](address.md) - Manage address objects used in security rules
- [address_group](address_group.md) - Manage address groups referenced in security rules
- [service](service.md) - Manage service objects used in security rules
