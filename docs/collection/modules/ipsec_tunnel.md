# IPsec Tunnel Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [IPsec Tunnel Model Attributes](#ipsec-tunnel-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating IPsec Tunnels](#creating-ipsec-tunnels)
    - [Basic IPsec Tunnel](#basic-ipsec-tunnel)
    - [IPsec Tunnel with Proxy IDs](#ipsec-tunnel-with-proxy-ids)
    - [IPsec Tunnel with Monitoring](#ipsec-tunnel-with-monitoring)
    - [Updating IPsec Tunnels](#updating-ipsec-tunnels)
    - [Deleting IPsec Tunnels](#deleting-ipsec-tunnels)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `ipsec_tunnel` Ansible module provides functionality to manage IPsec tunnels in Palo Alto
Networks' Strata Cloud Manager (SCM). IPsec tunnels define secure connections between networks and
leverage IKE Gateway and Crypto Profile configurations to establish encrypted communications for
site-to-site VPNs, remote access, and cloud connectivity.

## Core Methods

| Method     | Description                  | Parameters                       | Return Type                      |
| ---------- | ---------------------------- | -------------------------------- | -------------------------------- |
| `create()` | Creates a new IPsec tunnel   | `data: Dict[str, Any]`           | `IPsecTunnelResponseModel`       |
| `update()` | Updates an existing tunnel   | `tunnel: IPsecTunnelUpdateModel` | `IPsecTunnelResponseModel`       |
| `delete()` | Removes a tunnel             | `object_id: str`                 | `None`                           |
| `fetch()`  | Gets a tunnel by name        | `name: str`, `container: str`    | `IPsecTunnelResponseModel`       |
| `list()`   | Lists tunnels with filtering | `folder: str`, `**filters`       | `List[IPsecTunnelResponseModel]` |

## IPsec Tunnel Model Attributes

| Attribute                  | Type | Required      | Description                                                      |
| -------------------------- | ---- | ------------- | ---------------------------------------------------------------- |
| `name`                     | str  | Yes           | Name of the IPsec tunnel. Must match pattern: ^[a-zA-Z0-9.\_-]+$ |
| `tunnel_interface`         | str  | Yes           | Tunnel interface to use (e.g., "tunnel.1")                       |
| `ike_gateway`              | str  | Yes           | Name of the IKE Gateway to use                                   |
| `ipsec_crypto_profile`     | str  | Yes           | Name of the IPSec Crypto Profile to use                          |
| `tunnel_monitor`           | dict | No            | Tunnel monitoring configuration                                  |
| `anti_replay`              | bool | No            | Enable/disable anti-replay protection                            |
| `copy_tos`                 | bool | No            | Copy TOS field from inner packet to IPSec packet                 |
| `enable_gre_encapsulation` | bool | No            | Enable GRE encapsulation                                         |
| `proxy_ids`                | list | No            | List of Proxy IDs for this tunnel                                |
| `folder`                   | str  | One container | The folder in which the tunnel is defined (max 64 chars)         |
| `snippet`                  | str  | One container | The snippet in which the tunnel is defined (max 64 chars)        |
| `device`                   | str  | One container | The device in which the tunnel is defined (max 64 chars)         |

### Tunnel Monitor Attributes

| Attribute        | Type | Required | Description                                        |
| ---------------- | ---- | -------- | -------------------------------------------------- |
| `enable`         | bool | Yes      | Enable or disable tunnel monitoring                |
| `destination_ip` | str  | No       | Destination IP address to monitor                  |
| `source_ip`      | str  | No       | Source IP address for monitoring packets           |
| `proxy_id`       | str  | No       | Proxy ID to use for monitoring                     |
| `interval`       | int  | No       | Interval between monitoring probes (seconds)       |
| `threshold`      | int  | No       | Number of consecutive failures to mark tunnel down |
| `action`         | str  | No       | Action to take when tunnel is down                 |

### Proxy ID Attributes

| Attribute  | Type | Required | Description                                      |
| ---------- | ---- | -------- | ------------------------------------------------ |
| `name`     | str  | Yes      | Name of the proxy ID                             |
| `local`    | str  | Yes      | Local subnet (e.g., "10.0.0.0/24")               |
| `remote`   | str  | Yes      | Remote subnet (e.g., "192.168.0.0/24")           |
| `protocol` | str  | No       | Protocol for this proxy ID (any, tcp, udp, etc.) |

## Exceptions

| Exception                    | Description                      |
| ---------------------------- | -------------------------------- |
| `InvalidObjectError`         | Invalid tunnel data or format    |
| `NameNotUniqueError`         | Tunnel name already exists       |
| `ObjectNotPresentError`      | Tunnel not found                 |
| `MissingQueryParameterError` | Missing required parameters      |
| `AuthenticationError`        | Authentication failed            |
| `ServerError`                | Internal server error            |
| `ReferenceNotFoundError`     | Referenced object does not exist |

## Basic Configuration

The IPsec Tunnel module requires proper authentication credentials to access the Strata Cloud
Manager API.

```yaml
- name: Basic IPsec Tunnel Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure an IPsec tunnel exists
      cdot65.scm.ipsec_tunnel:
        provider: "{{ provider }}"
        name: "Branch-Office-Tunnel"
        tunnel_interface: "tunnel.1"
        ike_gateway: "Branch-Office-Gateway"
        ipsec_crypto_profile: "Standard-IPSec"
        folder: "Texas"
        anti_replay: true
        copy_tos: true
        state: "present"
```

## Usage Examples

### Creating IPsec Tunnels

IPsec tunnels provide secure connectivity between networks and can be configured with various
options to meet specific security and operational requirements.

### Basic IPsec Tunnel

This example creates a simple IPsec tunnel with minimal configuration.

```yaml
- name: Create a basic IPsec tunnel
  cdot65.scm.ipsec_tunnel:
    provider: "{{ provider }}"
    name: "Branch-Office-Tunnel"
    tunnel_interface: "tunnel.1"
    ike_gateway: "Branch-Office-Gateway"
    ipsec_crypto_profile: "Standard-IPSec"
    folder: "Texas"
    anti_replay: true
    copy_tos: true
    state: "present"
```

### IPsec Tunnel with Proxy IDs

This example creates an IPsec tunnel with multiple proxy IDs to specify which traffic should flow
through the tunnel.

```yaml
- name: Create an IPsec tunnel with proxy IDs
  cdot65.scm.ipsec_tunnel:
    provider: "{{ provider }}"
    name: "Datacenter-Tunnel"
    tunnel_interface: "tunnel.2"
    ike_gateway: "Datacenter-Gateway"
    ipsec_crypto_profile: "Strong-IPSec"
    folder: "Texas"
    anti_replay: true
    copy_tos: true
    proxy_ids:
      - name: "LAN-Traffic"
        local: "10.0.0.0/24"
        remote: "192.168.0.0/24"
        protocol: "any"
      - name: "Voice-Traffic"
        local: "10.1.0.0/24"
        remote: "192.168.1.0/24"
        protocol: "udp"
    state: "present"
```

### IPsec Tunnel with Monitoring

This example creates an IPsec tunnel with tunnel monitoring enabled for high availability.

```yaml
- name: Create an IPsec tunnel with monitoring
  cdot65.scm.ipsec_tunnel:
    provider: "{{ provider }}"
    name: "Critical-Connection"
    tunnel_interface: "tunnel.3"
    ike_gateway: "Critical-Gateway"
    ipsec_crypto_profile: "High-Security-IPSec"
    folder: "Texas"
    anti_replay: true
    copy_tos: true
    tunnel_monitor:
      enable: true
      destination_ip: "192.168.1.1"
      source_ip: "10.2.2.2"
      interval: 10
      threshold: 3
      action: "restart"
    state: "present"
```

### Updating IPsec Tunnels

This example updates an existing IPsec tunnel with new proxy IDs and tunnel monitoring settings.

```yaml
- name: Update an IPsec tunnel
  cdot65.scm.ipsec_tunnel:
    provider: "{{ provider }}"
    name: "Branch-Office-Tunnel"
    tunnel_interface: "tunnel.1"
    ike_gateway: "Branch-Office-Gateway"
    ipsec_crypto_profile: "Standard-IPSec"
    folder: "Texas"
    anti_replay: true
    copy_tos: true
    enable_gre_encapsulation: true
    tunnel_monitor:
      enable: true
      destination_ip: "10.1.1.1"
      source_ip: "10.2.2.2"
      interval: 5
      threshold: 3
    proxy_ids:
      - name: "Updated-Traffic"
        local: "10.0.0.0/16"
        remote: "192.168.0.0/16"
        protocol: "any"
    state: "present"
```

### Deleting IPsec Tunnels

This example removes an IPsec tunnel.

```yaml
- name: Delete an IPsec tunnel
  cdot65.scm.ipsec_tunnel:
    provider: "{{ provider }}"
    name: "Branch-Office-Tunnel"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting IPsec tunnels, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated IPsec tunnel configurations"
```

## Error Handling

It's important to handle potential errors when working with IPsec tunnels.

```yaml
- name: Create or update IPsec tunnel with error handling
  block:
    - name: Ensure IPsec tunnel exists
      cdot65.scm.ipsec_tunnel:
        provider: "{{ provider }}"
        name: "Branch-Office-Tunnel"
        tunnel_interface: "tunnel.1"
        ike_gateway: "Branch-Office-Gateway"
        ipsec_crypto_profile: "Standard-IPSec"
        folder: "Texas"
        anti_replay: true
        copy_tos: true
        state: "present"
      register: tunnel_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated IPsec tunnel configurations"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```

## Best Practices

### Tunnel Configuration

- Use descriptive names for IPsec tunnels that indicate their purpose or endpoint
- Establish a consistent naming convention for all VPN components
- Configure appropriate interfaces to segregate VPN traffic
- Balance security requirements with operational needs
- Reference existing security zones for tunnel interfaces

### Security Settings

- Enable anti-replay protection to prevent replay attacks
- Use strong IPsec crypto profiles for sensitive connections
- Match IPsec settings to organizational security policies
- Consider implementation of Perfect Forward Secrecy (PFS)
- Regularly review and update cryptographic settings

### Traffic Management

- Configure specific proxy IDs to match traffic that should flow through the tunnel
- Avoid overly broad proxy IDs that might route unintended traffic
- Use protocol-specific proxy IDs for better traffic control
- Consider using QoS markings with the copy_tos option for critical traffic
- Document intended traffic flows for each tunnel

### High Availability

- Enable tunnel monitoring for critical connections to quickly detect failures
- Configure appropriate monitoring intervals and thresholds
- Consider active/passive or active/active tunnel configurations
- Implement redundant tunnels for mission-critical connections
- Test failover scenarios regularly

### Documentation and Management

- Document tunnel configurations including IP addresses and connected networks
- Maintain an inventory of all VPN connections and their purposes
- Implement proper change management for tunnel modifications
- Regularly verify tunnel status using built-in monitoring tools
- Develop and test disaster recovery procedures

## Related Modules

- [ike_gateway](ike_gateway.md) - Manage IKE gateways referenced by IPsec tunnels
- [ike_crypto_profile](ike_crypto_profile.md) - Configure IKE crypto profiles for Phase-1
  negotiation
- [ipsec_crypto_profile](ipsec_crypto_profile.md) - Manage IPsec crypto profiles for Phase-2
  negotiation
- [security_zone](security_zone.md) - Configure security zones for tunnel interfaces
- [remote_networks](remote_networks.md) - Manage remote networks using IPsec tunnels
