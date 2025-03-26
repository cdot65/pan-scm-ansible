# Ike Crypto Profile Configuration Object

## Overview

The `ike_crypto_profile` module enables management of Internet Key Exchange (IKE) Crypto Profiles in
Palo Alto Networks Strata Cloud Manager (SCM). IKE Crypto Profiles define the encryption and
authentication algorithms to be used during the IKE Phase-1 negotiation when establishing a secure
VPN tunnel.

## Core Methods

| Method   | Description                                               |
| -------- | --------------------------------------------------------- |
| `create` | Creates a new IKE Crypto Profile in SCM                   |
| `update` | Modifies an existing IKE Crypto Profile                   |
| `delete` | Removes an IKE Crypto Profile from SCM                    |
| `get`    | Retrieves information about a specific IKE Crypto Profile |
| `list`   | Returns a list of all configured IKE Crypto Profiles      |

## Model Attributes

| Attribute        | Type   | Description                       | Required |
| ---------------- | ------ | --------------------------------- | -------- |
| `name`           | String | Name of the IKE Crypto Profile    | Yes      |
| `description`    | String | Description of the profile        | No       |
| `encryption`     | List   | List of encryption algorithms     | Yes      |
| `authentication` | List   | List of authentication algorithms | Yes      |
| `dh_group`       | List   | List of Diffie-Hellman groups     | Yes      |
| `lifetime`       | Dict   | IKE SA lifetime settings          | No       |

## Configuration Examples

### Creating an IKE Crypto Profile

```yaml
- name: Create IKE Crypto Profile
  cdot65.pan_scm.ike_crypto_profile:
    provider: "{{ scm_provider }}"
    state: present
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
      hours: 0
      minutes: 0
      seconds: 0
```

### Deleting an IKE Crypto Profile

```yaml
- name: Delete IKE Crypto Profile
  cdot65.pan_scm.ike_crypto_profile:
    provider: "{{ scm_provider }}"
    state: absent
    name: "Standard-Encryption"
```

## Usage Examples

### Complete Example

```yaml
---
- name: IKE Crypto Profile Management
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
    - name: Create Strong Encryption IKE Profile
      cdot65.pan_scm.ike_crypto_profile:
        provider: "{{ scm_provider }}"
        state: present
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
      register: profile_result
    
    - name: Display Profile Result
      debug:
        var: profile_result

    - name: Create Standard Encryption IKE Profile
      cdot65.pan_scm.ike_crypto_profile:
        provider: "{{ scm_provider }}"
        state: present
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

- Use strong encryption algorithms (AES-256-GCM) where possible
- Avoid using deprecated or weak algorithms (DES, MD5)
- Use larger DH groups (14 or higher) for better security
- Set reasonable lifetimes based on your security requirements
- Create different profiles for different security levels needed by various connections
- Document profile usage to track where each profile is applied

## Related Models

- [IKE Gateway](ike_gateway.md) - References IKE Crypto profiles during tunnel establishment
- [IPSec Crypto Profile](ipsec_crypto_profile.md) - Used alongside IKE Crypto profiles for VPN
  tunnels
- [IPSec Tunnel](ipsec_tunnel.md) - VPN tunnel configurations that utilize IKE Crypto profiles
