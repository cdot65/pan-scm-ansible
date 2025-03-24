# Security Rule

Manage security rules in Palo Alto Networks Strata Cloud Manager.

## Synopsis

The `security_rule` module allows you to create, update, and delete security rules in SCM.

Security rules define the traffic control policies for your network, determining what traffic is allowed or denied
between different zones, addresses, users, and applications.

## Requirements

- `pan-scm-sdk` Python package
- Authentication credentials for Strata Cloud Manager

## Parameters

| Parameter                   | Type    | Required | Default                   | Choices                    | Description                                                        |
|-----------------------------|---------|----------|---------------------------|----------------------------|--------------------------------------------------------------------|
| `name`                      | string  | yes      |                           |                            | Name of the security rule                                          |
| `folder`                    | string  | yes      |                           |                            | SCM folder path where the security rule is located                 |
| `description`               | string  | no       |                           |                            | Description for the security rule                                  |
| `source_zones`              | list    | no       |                           |                            | List of source zones                                               |
| `destination_zones`         | list    | no       |                           |                            | List of destination zones                                          |
| `source_addresses`          | list    | no       | `["any"]`                 |                            | List of source addresses                                           |
| `destination_addresses`     | list    | no       | `["any"]`                 |                            | List of destination addresses                                      |
| `source_users`              | list    | no       | `["any"]`                 |                            | List of source users                                               |
| `applications`              | list    | no       |                           |                            | List of applications                                               |
| `services`                  | list    | no       | `["application-default"]` |                            | List of services                                                   |
| `categories`                | list    | no       | `["any"]`                 |                            | List of URL categories                                             |
| `action`                    | string  | no       | `allow`                   | allow, deny, drop          | Action to take when traffic matches the rule                       |
| `log_setting`               | string  | no       |                           |                            | Log forwarding profile to use                                      |
| `log_start`                 | boolean | no       | `false`                   |                            | Whether to log at session start                                    |
| `log_end`                   | boolean | no       | `true`                    |                            | Whether to log at session end                                      |
| `disabled`                  | boolean | no       | `false`                   |                            | Whether the rule is disabled                                       |
| `tags`                      | list    | no       |                           |                            | List of tags to apply to the rule                                  |
| `position`                  | string  | no       | `bottom`                  | top, bottom, before, after | Position where to place the rule                                   |
| `reference_rule`            | string  | no       |                           |                            | Name of the reference rule when using 'before' or 'after' position |
| `profile_type`              | string  | no       | `profiles`                | profiles, group, none      | Type of security profile setting                                   |
| `profile_group`             | string  | no       |                           |                            | Name of the profile group when profile_type is 'group'             |
| `antivirus_profile`         | string  | no       |                           |                            | Name of the antivirus profile                                      |
| `anti_spyware_profile`      | string  | no       |                           |                            | Name of the anti-spyware profile                                   |
| `vulnerability_profile`     | string  | no       |                           |                            | Name of the vulnerability profile                                  |
| `url_filtering_profile`     | string  | no       |                           |                            | Name of the URL filtering profile                                  |
| `file_blocking_profile`     | string  | no       |                           |                            | Name of the file blocking profile                                  |
| `wildfire_analysis_profile` | string  | no       |                           |                            | Name of the WildFire analysis profile                              |
| `state`                     | string  | no       | present                   | present, absent            | Desired state of the rule                                          |
| `username`                  | string  | no       |                           |                            | SCM username (can use environment variable)                        |
| `password`                  | string  | no       |                           |                            | SCM password (can use environment variable)                        |
| `tenant`                    | string  | no       |                           |                            | SCM tenant ID (can use environment variable)                       |

## Examples

### Create a basic security rule

```yaml
- name: Create a basic web traffic security rule
  cdot65.scm.security_rule:
    name: "Allow-Web-Traffic"
    folder: "SharedFolder"
    description: "Allow web traffic to web servers"
    source_zones: 
      - "untrust"
    destination_zones:
      - "trust"
    source_addresses: 
      - "any"
    destination_addresses:
      - "web-server-group"
    applications:
      - "web-browsing"
      - "ssl"
    services:
      - "application-default"
    action: "allow"
    log_setting: "default"
    log_end: true
```

### Create a rule with security profiles

```yaml
- name: Create a rule with security profiles
  cdot65.scm.security_rule:
    name: "Allow-Inspected-Web"
    folder: "SharedFolder"
    description: "Allow and inspect web traffic"
    source_zones: 
      - "untrust"
    destination_zones:
      - "trust"
    applications:
      - "web-browsing"
      - "ssl"
    action: "allow"
    profile_type: "profiles"
    antivirus_profile: "default-antivirus"
    anti_spyware_profile: "default-anti-spyware"
    vulnerability_profile: "default-vulnerability"
    url_filtering_profile: "default-url-filtering"
```

### Create a rule with a security profile group

```yaml
- name: Create a rule with a security profile group
  cdot65.scm.security_rule:
    name: "Allow-Inspected-Traffic"
    folder: "SharedFolder"
    description: "Allow traffic with profile group inspection"
    source_zones: 
      - "untrust"
    destination_zones:
      - "trust"
    applications:
      - "any"
    action: "allow"
    profile_type: "group"
    profile_group: "default-profile-group"
```

### Position a rule relative to another rule

```yaml
- name: Add a rule before an existing rule
  cdot65.scm.security_rule:
    name: "Allow-HTTPS-Traffic"
    folder: "SharedFolder"
    description: "Allow HTTPS traffic"
    source_zones: 
      - "untrust"
    destination_zones:
      - "trust"
    applications:
      - "ssl"
    action: "allow"
    position: "before"
    reference_rule: "Allow-Web-Traffic"
```

### Delete a security rule

```yaml
- name: Delete a security rule
  cdot65.scm.security_rule:
    name: "Old-Rule"
    folder: "SharedFolder"
    state: absent
```

## Return Values

| Name         | Description                   | Type       | Sample                                                               |
|--------------|-------------------------------|------------|----------------------------------------------------------------------|
| `changed`    | Whether changes were made     | boolean    | `true`                                                               |
| `scm_object` | The SCM security rule details | dictionary | `{"id": "123", "name": "Allow-Web-Traffic", "action": "allow", ...}` |
| `response`   | The raw API response          | dictionary | `{"status": "success", "data": {...}}`                               |

## Notes

- Security rule names must be unique within a folder
- Rules are processed in order, with the first match determining the action
- Consider rule order carefully when creating or positioning rules
- Complex rules with many conditions may impact performance
- This module is idempotent; running it multiple times with the same parameters will result in the same state

## Status

This module is flagged as **stable**
