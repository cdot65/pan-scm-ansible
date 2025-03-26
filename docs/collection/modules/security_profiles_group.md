# Security Profiles Group Module

## Overview

The `security_profiles_group` module enables management of Security Profiles Groups in Palo Alto Networks Strata Cloud
Manager (SCM). Security Profiles Groups allow you to bundle multiple security profiles (Anti-Spyware, Vulnerability
Protection, URL Filtering, etc.) into a single group that can be applied to security rules.

## Core Methods

| Method   | Description                                                    |
|----------|----------------------------------------------------------------|
| `create` | Creates a new Security Profiles Group in SCM                   |
| `update` | Modifies an existing Security Profiles Group                   |
| `delete` | Removes a Security Profiles Group from SCM                     |
| `get`    | Retrieves information about a specific Security Profiles Group |
| `list`   | Returns a list of all configured Security Profiles Groups      |

## Model Attributes

| Attribute                   | Type   | Description                                      | Required |
|-----------------------------|--------|--------------------------------------------------|----------|
| `name`                      | String | Name of the Security Profiles Group              | Yes      |
| `description`               | String | Description of the group                         | No       |
| `anti_spyware_profile`      | String | Name of the Anti-Spyware profile to include      | No       |
| `anti_virus_profile`        | String | Name of the Anti-Virus profile to include        | No       |
| `vulnerability_profile`     | String | Name of the Vulnerability profile to include     | No       |
| `url_filtering_profile`     | String | Name of the URL Filtering profile to include     | No       |
| `file_blocking_profile`     | String | Name of the File Blocking profile to include     | No       |
| `wildfire_analysis_profile` | String | Name of the WildFire Analysis profile to include | No       |
| `data_filtering_profile`    | String | Name of the Data Filtering profile to include    | No       |
| `tags`                      | List   | List of tags to apply to the group               | No       |

## Configuration Examples

### Creating a Security Profiles Group

```yaml
- name: Create Security Profiles Group
  cdot65.pan_scm.security_profiles_group:
    provider: "{{ scm_provider }}"
    state: present
    name: "Standard-Protection"
    description: "Standard protection profile for corporate assets"
    anti_spyware_profile: "Custom-AS-Profile"
    anti_virus_profile: "Default-AV"
    url_filtering_profile: "Corporate-URL-Filter"
    tags: 
      - "standard-security"
```

### Deleting a Security Profiles Group

```yaml
- name: Delete Security Profiles Group
  cdot65.pan_scm.security_profiles_group:
    provider: "{{ scm_provider }}"
    state: absent
    name: "Standard-Protection"
```

## Usage Examples

### Complete Example

```yaml
---
- name: Security Profiles Group Management
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
    - name: Create Enhanced Security Profiles Group
      cdot65.pan_scm.security_profiles_group:
        provider: "{{ scm_provider }}"
        state: present
        name: "Enhanced-Protection"
        description: "Enhanced protection profile for sensitive assets"
        anti_spyware_profile: "Enhanced-AS-Profile"
        anti_virus_profile: "Enhanced-AV"
        vulnerability_profile: "Enhanced-VP"
        url_filtering_profile: "Strict-URL-Filter"
        file_blocking_profile: "Block-Risky-Files"
        wildfire_analysis_profile: "Enhanced-WF"
        data_filtering_profile: "DLP-Strict"
        tags: 
          - "enhanced-security"
          - "sensitive-assets"
      register: group_result
    
    - name: Display Group Result
      debug:
        var: group_result
    
    - name: Create Standard Security Profiles Group
      cdot65.pan_scm.security_profiles_group:
        provider: "{{ scm_provider }}"
        state: present
        name: "Standard-Protection"
        description: "Standard protection profile for corporate assets"
        anti_spyware_profile: "Standard-AS-Profile"
        anti_virus_profile: "Standard-AV"
        url_filtering_profile: "Corporate-URL-Filter"
        tags: 
          - "standard-security"
```

## Error Handling

The module will fail with proper error messages if:

- Authentication with SCM fails
- The Security Profiles Group already exists when trying to create it
- The Security Profiles Group doesn't exist when trying to update or delete it
- Required parameters are missing
- Referenced security profiles don't exist
- Action fails due to API errors or permission issues

## Best Practices

- Create different Security Profiles Groups for different security postures or asset types
- Use descriptive names that indicate the security level or purpose
- Document which security rules use each group
- Regularly review and update the profiles included in each group
- Apply more stringent profiles to groups used for sensitive assets
- Use tags to categorize and organize groups
- Test changes to Security Profiles Groups in pre-production environments before applying to production

## Related Models

- [Anti-Spyware Profile](anti_spyware_profile.md) - Can be included in Security Profiles Groups
- [Security Rule](security_rule.md) - References Security Profiles Groups to determine which security profiles to apply