# IPSec Tunnel Module

## Overview

The `ipsec_tunnel` module enables management of IPSec tunnels in Palo Alto Networks Strata Cloud Manager (SCM). IPSec
tunnels define secure connections between networks and leverage IKE Gateway and Crypto Profile configurations to
establish encrypted communications.

## Core Methods

| Method   | Description                                         |
|----------|-----------------------------------------------------|
| `create` | Creates a new IPSec tunnel in SCM                   |
| `update` | Modifies an existing IPSec tunnel                   |
| `delete` | Removes an IPSec tunnel from SCM                    |
| `get`    | Retrieves information about a specific IPSec tunnel |
| `list`   | Returns a list of all configured IPSec tunnels      |

## Model Attributes

| Attribute                  | Type    | Description                                      | Required |
|----------------------------|---------|--------------------------------------------------|----------|
| `name`                     | String  | Name of the IPSec tunnel                         | Yes      |
| `tunnel_interface`         | String  | Tunnel interface to use                          | Yes      |
| `ike_gateway`              | String  | Name of the IKE Gateway to use                   | Yes      |
| `ipsec_crypto_profile`     | String  | Name of the IPSec Crypto Profile to use          | Yes      |
| `tunnel_monitor`           | Dict    | Tunnel monitoring configuration                  | No       |
| `anti_replay`              | Boolean | Enable/disable anti-replay protection            | No       |
| `copy_tos`                 | Boolean | Copy TOS field from inner packet to IPSec packet | No       |
| `enable_gre_encapsulation` | Boolean | Enable GRE encapsulation                         | No       |
| `proxy_ids`                | List    | List of Proxy IDs for this tunnel                | No       |

## Configuration Examples

### Creating an IPSec Tunnel

```yaml
- name: Create IPSec Tunnel
  cdot65.pan_scm.ipsec_tunnel:
    provider: "{{ scm_provider }}"
    state: present
    name: "Branch-Office-Tunnel"
    tunnel_interface: "tunnel.1"
    ike_gateway: "Branch-Office-Gateway"
    ipsec_crypto_profile: "Standard-IPSec"
    anti_replay: true
    copy_tos: true
    tunnel_monitor:
      enable: true
      destination_ip: "10.1.1.1"
      source_ip: "10.2.2.2"
      proxy_id: "monitor-proxy"
```

### Deleting an IPSec Tunnel

```yaml
- name: Delete IPSec Tunnel
  cdot65.pan_scm.ipsec_tunnel:
    provider: "{{ scm_provider }}"
    state: absent
    name: "Branch-Office-Tunnel"
```

## Usage Examples

### Complete Example

```yaml
---
- name: IPSec Tunnel Management
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
    - name: Create IPSec Tunnel with Proxy IDs
      cdot65.pan_scm.ipsec_tunnel:
        provider: "{{ scm_provider }}"
        state: present
        name: "Datacenter-Tunnel"
        tunnel_interface: "tunnel.2"
        ike_gateway: "Datacenter-Gateway"
        ipsec_crypto_profile: "Strong-IPSec"
        anti_replay: true
        copy_tos: true
        tunnel_monitor:
          enable: true
          destination_ip: "192.168.1.1"
          interval: 10
          threshold: 3
        proxy_ids:
          - name: "LAN-Traffic"
            local: "10.0.0.0/24"
            remote: "192.168.0.0/24"
            protocol: "any"
          - name: "Voice-Traffic"
            local: "10.1.0.0/24"
            remote: "192.168.1.0/24"
            protocol: "udp"
      register: tunnel_result
    
    - name: Display Tunnel Result
      debug:
        var: tunnel_result
```

## Error Handling

The module will fail with proper error messages if:

- Authentication with SCM fails
- The tunnel already exists when trying to create it
- The tunnel doesn't exist when trying to update or delete it
- Required parameters are missing
- Referenced objects (IKE Gateway, IPSec Crypto Profile, Tunnel Interface) don't exist
- Action fails due to API errors or permission issues

## Best Practices

- Use descriptive names for IPSec tunnels that indicate their purpose or endpoint
- Enable tunnel monitoring for critical connections to quickly detect failures
- Configure appropriate Proxy IDs to match traffic that should flow through the tunnel
- Use strong IPSec crypto profiles for sensitive connections
- Document tunnel configurations including IP addresses and networks that are connected
- Configure redundant tunnels for critical connections where possible
- Regularly verify tunnel status using built-in monitoring tools

## Related Models

- [IKE Gateway](ike_gateway.md) - Referenced by IPSec tunnels for peer information
- [IKE Crypto Profile](ike_crypto_profile.md) - Used by IKE Gateway for Phase-1 negotiation
- [IPSec Crypto Profile](ipsec_crypto_profile.md) - Referenced by IPSec tunnels for Phase-2 negotiation
- [Remote Networks](remote_networks.md) - Often use IPSec tunnels for site-to-cloud connectivity
