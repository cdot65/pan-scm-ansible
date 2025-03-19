# IPSec Crypto Profile Module

## Overview

The `ipsec_crypto_profile` module enables management of IPSec Crypto Profiles in Palo Alto Networks Strata Cloud Manager (SCM). IPSec Crypto Profiles define the encryption and authentication algorithms to be used during the IPSec Phase-2 negotiation when establishing a secure VPN tunnel.

## Core Methods

| Method | Description |
|--------|-------------|
| `create` | Creates a new IPSec Crypto Profile in SCM |
| `update` | Modifies an existing IPSec Crypto Profile |
| `delete` | Removes an IPSec Crypto Profile from SCM |
| `get` | Retrieves information about a specific IPSec Crypto Profile |
| `list` | Returns a list of all configured IPSec Crypto Profiles |

## Model Attributes

| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| `name` | String | Name of the IPSec Crypto Profile | Yes |
| `description` | String | Description of the profile | No |
| `esp_encryption` | List | List of ESP encryption algorithms | Yes |
| `esp_authentication` | List | List of ESP authentication algorithms | No |
| `ah_authentication` | List | List of AH authentication algorithms | No |
| `dh_group` | String | Diffie-Hellman group for Perfect Forward Secrecy | No |
| `lifetime` | Dict | IPSec SA lifetime settings | No |

## Configuration Examples

### Creating an IPSec Crypto Profile

```yaml
- name: Create IPSec Crypto Profile
  cdot65.pan_scm.ipsec_crypto_profile:
    provider: "{{ scm_provider }}"
    state: present
    name: "Standard-IPSec"
    description: "Standard IPSec encryption profile for VPN tunnels"
    esp_encryption: 
      - "aes-256-gcm"
    dh_group: "group14"
    lifetime:
      hours: 1
```

### Deleting an IPSec Crypto Profile

```yaml
- name: Delete IPSec Crypto Profile
  cdot65.pan_scm.ipsec_crypto_profile:
    provider: "{{ scm_provider }}"
    state: absent
    name: "Standard-IPSec"
```

## Usage Examples

### Complete Example

```yaml
---
- name: IPSec Crypto Profile Management
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
    - name: Create Strong IPSec Crypto Profile
      cdot65.pan_scm.ipsec_crypto_profile:
        provider: "{{ scm_provider }}"
        state: present
        name: "Strong-IPSec"
        description: "Strong encryption profile for sensitive VPN tunnels"
        esp_encryption: 
          - "aes-256-gcm"
        esp_authentication: 
          - "sha512"
        dh_group: "group20"
        lifetime:
          hours: 1
      register: profile_result
    
    - name: Display Profile Result
      debug:
        var: profile_result

    - name: Create Suite-B IPSec Crypto Profile
      cdot65.pan_scm.ipsec_crypto_profile:
        provider: "{{ scm_provider }}"
        state: present
        name: "Suite-B-GCM-128"
        description: "Suite-B compliance profile for IPSec"
        esp_encryption: 
          - "aes-128-gcm"
        dh_group: "group19"
        lifetime:
          hours: 4
```

## Error Handling

The module will fail with proper error messages if:

- Authentication with SCM fails
- The profile already exists when trying to create it
- The profile doesn't exist when trying to update or delete it
- Required parameters are missing
- Invalid encryption, authentication, or DH group options are specified
- Action fails due to API errors or permission issues

## Best Practices

- Use AES-GCM algorithms where possible as they provide both encryption and authentication
- Set appropriate SA lifetimes based on security requirements and traffic volume
- Use Perfect Forward Secrecy (PFS) with strong DH groups where security is critical
- Create profiles for different security levels based on the sensitivity of traffic
- Consider compliance requirements (FIPS, Suite-B) when selecting algorithms
- Document profile usage to track where each profile is applied

## Related Models

- [IKE Gateway](ike_gateway.md) - Used alongside IPSec Crypto profiles for VPN tunnels
- [IKE Crypto Profile](ike_crypto_profile.md) - Used for Phase-1 negotiation of VPN tunnels
- [IPSec Tunnel](ipsec_tunnel.md) - VPN tunnel configurations that utilize IPSec Crypto profiles
- [Remote Networks](remote_networks.md) - References IPSec Crypto profiles for site-to-cloud connections
