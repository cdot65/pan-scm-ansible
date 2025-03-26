# Anti Spyware Profile Module

## Overview

The `anti_spyware_profile` module enables management of Anti-Spyware profiles in Palo Alto Networks Strata Cloud
Manager (SCM). Anti-Spyware profiles are security components that detect and block spyware and other malicious software
on the network.

## Core Methods

| Method   | Description                                                 |
|----------|-------------------------------------------------------------|
| `create` | Creates a new Anti-Spyware profile in SCM                   |
| `update` | Modifies an existing Anti-Spyware profile                   |
| `delete` | Removes an Anti-Spyware profile from SCM                    |
| `get`    | Retrieves information about a specific Anti-Spyware profile |
| `list`   | Returns a list of all configured Anti-Spyware profiles      |

## Model Attributes

| Attribute           | Type    | Description                      | Required |
|---------------------|---------|----------------------------------|----------|
| `name`              | String  | Name of the Anti-Spyware profile | Yes      |
| `description`       | String  | Description of the profile       | No       |
| `threat_exceptions` | List    | List of threat exceptions        | No       |
| `rules`             | List    | List of Anti-Spyware rules       | Yes      |
| `botnet_lists`      | List    | Botnet domain lists to use       | No       |
| `packet_capture`    | Boolean | Enable/disable packet capture    | No       |

## Configuration Examples

### Creating an Anti-Spyware Profile

```yaml
- name: Create Anti-Spyware Profile
  cdot65.pan_scm.anti_spyware_profile:
    provider: "{{ scm_provider }}"
    state: present
    name: "Block-High-Risk-Threats"
    description: "Block threats with high risk levels"
    rules:
      - name: "rule1"
        threat_level: "high"
        action: "block"
        packet_capture: "disable"
```

### Deleting an Anti-Spyware Profile

```yaml
- name: Delete Anti-Spyware Profile
  cdot65.pan_scm.anti_spyware_profile:
    provider: "{{ scm_provider }}"
    state: absent
    name: "Block-High-Risk-Threats"
```

## Usage Examples

### Complete Example

```yaml
---
- name: Anti-Spyware Profile Management
  hosts: localhost
  gather_facts: false
  connection: local
  
  vars:
    scm_provider:
      client_id: "{{ lookup('env', 'SCM_CLIENT_ID') }}"
      client_secret: "{{ lookup('env', 'SCM_CLIENT_SECRET') }}"
      scope: "profile tsg_id:9876"
      token_url: "{{ lookup('env', 'SCM_TOKEN_URL') }}"
  
  tasks:
    - name: Create Anti-Spyware Profile
      cdot65.pan_scm.anti_spyware_profile:
        provider: "{{ scm_provider }}"
        state: present
        name: "Custom-AS-Profile"
        description: "Custom Anti-Spyware profile for critical servers"
        packet_capture: true
        rules:
          - name: "block-critical"
            threat_level: "critical"
            action: "block"
            packet_capture: "single-packet"
          - name: "block-high"
            threat_level: "high"
            action: "block"
            packet_capture: "disable"
          - name: "alert-medium"
            threat_level: "medium"
            action: "alert"
            packet_capture: "disable"
      register: profile_result
    
    - name: Display Profile Result
      debug:
        var: profile_result
```

## Error Handling

The module will fail with proper error messages if:

- Authentication with SCM fails
- The profile already exists when trying to create it
- The profile doesn't exist when trying to update or delete it
- Required parameters are missing
- Action fails due to API errors or permission issues

## Best Practices

- Use descriptive names for Anti-Spyware profiles
- Create different profiles for different security postures
- Enable packet capture only where needed due to performance impact
- Always test profiles in pre-production environments before deploying to production
- Use variables to store common settings across playbooks

## Related Models

- [Security Policy](security_rule.md) - References Anti-Spyware profiles in security rules
- [Security Profiles Group](security_profiles_group.md) - Can include Anti-Spyware profiles
