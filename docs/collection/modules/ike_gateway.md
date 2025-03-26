# Ike Gateway Configuration Object

## 01. Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [IKE Gateway Model Attributes](#ike-gateway-model-attributes)
4. [Exceptions](#exceptions)
5. [Basic Configuration](#basic-configuration)
6. [Usage Examples](#usage-examples)
   - [Creating IKE Gateways](#creating-ike-gateways)
   - [IKE Gateway with Pre-Shared Key](#ike-gateway-with-pre-shared-key)
   - [IKE Gateway with Certificate Authentication](#ike-gateway-with-certificate-authentication)
   - [Updating IKE Gateways](#updating-ike-gateways)
   - [Deleting IKE Gateways](#deleting-ike-gateways)
7. [Managing Configuration Changes](#managing-configuration-changes)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## 02. Overview

The `ike_gateway` Ansible module provides functionality to manage Internet Key Exchange (IKE) gateway configuration objects in Palo Alto Networks' Strata Cloud Manager (SCM). IKE gateways define the parameters for establishing IPsec VPN tunnels with remote endpoints, including authentication methods, encryption settings, and peer identities.

## 03. Core Methods

| Method     | Description                         | Parameters                    | Return Type                 |
| ---------- | ----------------------------------- | ----------------------------- | --------------------------- |
| `create()` | Creates a new IKE gateway           | `data: Dict[str, Any]`        | `IkeGatewayResponseModel`   |
| `update()` | Updates an existing gateway         | `gateway: IkeGatewayUpdateModel` | `IkeGatewayResponseModel` |
| `delete()` | Removes an IKE gateway              | `object_id: str`              | `None`                      |
| `fetch()`  | Gets a gateway by name              | `name: str`, `container: str` | `IkeGatewayResponseModel`   |
| `list()`   | Lists gateways with filtering       | `folder: str`, `**filters`    | `List[IkeGatewayResponseModel]` |

## 04. IKE Gateway Model Attributes

| Attribute                           | Type   | Required      | Description                                        |
| ----------------------------------- | ------ | ------------- | -------------------------------------------------- |
| `name`                              | str    | Yes           | Name of the IKE gateway                            |
| `description`                       | str    | No            | Description of the IKE gateway                     |
| `version`                           | str    | Yes           | IKE version (ikev1, ikev2, or ikev2-preferred)     |
| `peer_address`                      | str    | Yes           | Peer IP address or FQDN                            |
| `interface`                         | str    | Yes           | Interface for the connection                       |
| `local_id_type`                     | str    | No            | Local identifier type (ipaddr, fqdn, ufqdn, keyid) |
| `local_id_value`                    | str    | No            | Local identifier value                             |
| `peer_id_type`                      | str    | No            | Peer identifier type (ipaddr, fqdn, ufqdn, keyid)  |
| `peer_id_value`                     | str    | No            | Peer identifier value                              |
| `pre_shared_key`                    | str    | Yes*          | Pre-shared key for authentication                  |
| `certificate_name`                  | str    | Yes*          | Certificate name for authentication                |
| `crypto_profile`                    | str    | No            | IKE crypto profile name                            |
| `enable_nat_traversal`              | bool   | No            | Enable NAT traversal                               |
| `nat_traversal_keep_alive`          | int    | No            | NAT traversal keepalive interval                   |
| `nat_traversal_enable_udp_checksum` | bool   | No            | Enable UDP checksum for NAT traversal              |
| `enable_fragmentation`              | bool   | No            | Enable IKE fragmentation                           |
| `enable_liveness_check`             | bool   | No            | Enable IKE liveness check                          |
| `liveness_check_interval`           | int    | No            | Liveness check interval                            |
| `folder`                            | str    | One container | The folder in which the resource is defined        |
| `snippet`                           | str    | One container | The snippet in which the resource is defined       |
| `device`                            | str    | One container | The device in which the resource is defined        |

*Exactly one of `pre_shared_key` or `certificate_name` must be provided.

### Provider Dictionary Attributes

| Attribute       | Type | Required | Default | Description                      |
| --------------- | ---- | -------- | ------- | -------------------------------- |
| `client_id`     | str  | Yes      |         | Client ID for authentication     |
| `client_secret` | str  | Yes      |         | Client secret for authentication |
| `tsg_id`        | str  | Yes      |         | Tenant Service Group ID          |
| `log_level`     | str  | No       | "INFO"  | Log level for the SDK            |

## 05. Exceptions

| Exception                    | Description                     |
| ---------------------------- | ------------------------------- |
| `InvalidObjectError`         | Invalid gateway data or format  |
| `NameNotUniqueError`         | Gateway name already exists     |
| `ObjectNotPresentError`      | Gateway not found               |
| `MissingQueryParameterError` | Missing required parameters     |
| `AuthenticationError`        | Authentication failed           |
| `ServerError`                | Internal server error           |
| `InvalidParameterError`      | Invalid parameter value         |

## 06. Basic Configuration

The IKE Gateway module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic IKE Gateway Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure an IKE gateway exists
      cdot65.scm.ike_gateway:
        provider: "{{ provider }}"
        name: "branch-office-gw"
        description: "Branch office VPN gateway"
        version: "ikev2"
        peer_address: "203.0.113.1"
        interface: "ethernet1/1"
        pre_shared_key: "{{ vpn_psk }}"
        folder: "Texas"
        state: "present"
```

## 07. Usage Examples

### Creating IKE Gateways

IKE gateways define the parameters for establishing VPN tunnels with remote endpoints. Different authentication methods and settings can be used based on requirements.

### IKE Gateway with Pre-Shared Key

This example creates an IKE gateway using pre-shared key authentication.

```yaml
- name: Create IKE gateway with PSK authentication
  cdot65.scm.ike_gateway:
    provider: "{{ provider }}"
    name: "remote-site-vpn"
    description: "Remote site VPN gateway"
    version: "ikev2"
    peer_address: "198.51.100.1"
    interface: "ethernet1/1"
    pre_shared_key: "{{ vpn_psk | default('securepassword') }}"
    local_id_type: "ipaddr"
    local_id_value: "203.0.113.2"
    peer_id_type: "ipaddr"
    peer_id_value: "198.51.100.1"
    crypto_profile: "default-ike-crypto-profile"
    enable_nat_traversal: true
    enable_liveness_check: true
    liveness_check_interval: 5
    folder: "Texas"
    state: "present"
```

### IKE Gateway with Certificate Authentication

This example creates an IKE gateway using certificate-based authentication.

```yaml
- name: Create IKE gateway with certificate authentication
  cdot65.scm.ike_gateway:
    provider: "{{ provider }}"
    name: "partner-vpn"
    description: "Partner VPN gateway with certificate authentication"
    version: "ikev2"
    peer_address: "partner.example.com"
    interface: "ethernet1/1"
    certificate_name: "partner-cert"
    local_id_type: "fqdn"
    local_id_value: "vpn.mycompany.com"
    peer_id_type: "fqdn"
    peer_id_value: "vpn.partner.com"
    crypto_profile: "strong-ike-crypto-profile"
    enable_fragmentation: true
    folder: "Texas"
    state: "present"
```

### Updating IKE Gateways

This example updates an existing IKE gateway with new settings.

```yaml
- name: Update IKE gateway settings
  cdot65.scm.ike_gateway:
    provider: "{{ provider }}"
    name: "remote-site-vpn"
    description: "Updated remote site VPN gateway"
    version: "ikev2"
    peer_address: "198.51.100.1"
    interface: "ethernet1/1"
    pre_shared_key: "{{ new_vpn_psk }}"
    enable_liveness_check: true
    liveness_check_interval: 10  # Updated interval
    folder: "Texas"
    state: "present"
```

### Deleting IKE Gateways

This example removes an IKE gateway.

```yaml
- name: Delete an IKE gateway
  cdot65.scm.ike_gateway:
    provider: "{{ provider }}"
    name: "deprecated-vpn"
    folder: "Texas"
    state: "absent"
```

## 08. Managing Configuration Changes

After creating, updating, or deleting IKE gateways, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated IKE gateways"
```

## 09. Error Handling

It's important to handle potential errors when working with IKE gateways.

```yaml
- name: Create or update IKE gateway with error handling
  block:
    - name: Attempt to create IKE gateway
      cdot65.scm.ike_gateway:
        provider: "{{ provider }}"
        name: "branch-vpn"
        version: "ikev2"
        peer_address: "198.51.100.1"
        interface: "ethernet1/1"
        crypto_profile: "strong-ike-crypto-profile"
        pre_shared_key: "{{ vpn_psk }}"
        folder: "Texas"
        state: "present"
      register: gateway_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated IKE gateways"
      when: gateway_result.changed
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a crypto profile error
      debug:
        msg: "Verify that the specified crypto profile exists"
      when: "'crypto_profile' in ansible_failed_result.msg"
```

## 10. Best Practices

### Authentication

- Use strong pre-shared keys or certificates for authentication
- Consider using certificates for higher security
- Rotate pre-shared keys periodically
- Store secrets securely using Ansible Vault
- Use long, complex pre-shared keys with a mix of character types

### IKE Version

- Use IKEv2 when possible for better security and features
- Only use IKEv1 for compatibility with legacy devices
- Consider ikev2-preferred for maximum compatibility
- Document any requirement for older IKE versions

### Identifiers

- Always configure explicit identifiers for both local and peer endpoints
- Use IP addresses as identifiers when possible for simplicity
- Ensure peer identifiers match exactly what the remote device uses
- Use descriptive FQDNs when IP addresses may change
- Test identifier configurations thoroughly

### Crypto Profiles

- Use strong encryption algorithms and DH groups
- Follow current security best practices for crypto settings
- Create custom crypto profiles instead of using defaults
- Reference named profiles for consistent configuration
- Document crypto profile selections and rationale

### High Availability

- Configure liveness checks to ensure tunnel availability
- Set appropriate liveness check intervals (not too short, not too long)
- Consider NAT traversal settings when tunnels cross NAT devices
- Enable fragmentation when needed for larger packets
- Test redundancy and failover mechanisms

### Organization

- Use descriptive names for IKE gateways
- Include purpose and remote site in gateway descriptions
- Organize gateways in appropriate folders
- Maintain consistent naming conventions
- Document IKE gateway configurations and their relationships to tunnels

## 11. Related Modules

- [ike_crypto_profile](ike_crypto_profile.md) - Configure encryption profiles for IKE gateways
- [ipsec_crypto_profile](ipsec_crypto_profile.md) - Configure encryption profiles for IPsec tunnels
- [ipsec_tunnel](ipsec_tunnel.md) - Configure IPsec tunnels that use IKE gateways
- [remote_networks](remote_networks.md) - Configure remote networks that use IKE gateways