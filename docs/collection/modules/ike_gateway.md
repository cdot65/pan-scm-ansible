# IKE Gateway Configuration Object

## 1. Overview
The IKE Gateway module allows you to manage Internet Key Exchange (IKE) gateway configuration objects within Strata Cloud Manager (SCM). IKE gateways define the parameters for establishing IPsec VPN tunnels with remote endpoints, including authentication methods, encryption settings, and peer identities.

## 2. Core Methods

| Method     | Description                    | Parameters                | Return Type            |
|------------|--------------------------------|---------------------------|------------------------|
| `create()` | Creates a new IKE gateway      | `data: Dict[str, Any]`    | `ResponseModel`        |
| `get()`    | Retrieves gateway by name      | `name: str, folder: str`  | `ResponseModel`        |
| `update()` | Updates an existing gateway    | `ike_gateway: Model`      | `ResponseModel`        |
| `delete()` | Deletes an IKE gateway         | `id: str`                 | `None`                 |

## 3. Model Attributes

| Attribute            | Type              | Required | Description                                           |
|----------------------|-------------------|----------|-------------------------------------------------------|
| `name`               | str               | Yes      | Name of the IKE gateway                               |
| `description`        | str               | No       | Description of the IKE gateway                        |
| `version`            | str               | Yes      | IKE version (ikev1, ikev2, or ikev2-preferred)        |
| `peer_address`       | str               | Yes      | Peer IP address or FQDN                               |
| `interface`          | str               | Yes      | Interface for the connection                          |
| `local_id_type`      | str               | No       | Local identifier type (ipaddr, fqdn, ufqdn, keyid)    |
| `local_id_value`     | str               | No       | Local identifier value                                |
| `peer_id_type`       | str               | No       | Peer identifier type (ipaddr, fqdn, ufqdn, keyid)     |
| `peer_id_value`      | str               | No       | Peer identifier value                                 |
| `pre_shared_key`     | str               | Yes*     | Pre-shared key for authentication                     |
| `certificate_name`   | str               | Yes*     | Certificate name for authentication                    |
| `crypto_profile`     | str               | No       | IKE crypto profile name                               |
| `enable_nat_traversal`| bool             | No       | Enable NAT traversal                                  |
| `nat_traversal_keep_alive`| int          | No       | NAT traversal keepalive interval                     |
| `nat_traversal_enable_udp_checksum`| bool | No      | Enable UDP checksum for NAT traversal                 |
| `enable_fragmentation`| bool             | No       | Enable IKE fragmentation                              |
| `enable_liveness_check`| bool            | No       | Enable IKE liveness check                             |
| `liveness_check_interval`| int           | No       | Liveness check interval                               |
| `folder`             | str               | No**     | The folder in which the resource is defined           |
| `snippet`            | str               | No**     | The snippet in which the resource is defined          |
| `device`             | str               | No**     | The device in which the resource is defined           |

\* Exactly one of `pre_shared_key` or `certificate_name` must be provided.  
\** Exactly one of `folder`, `snippet`, or `device` must be provided.

## 4. Basic Configuration

<div class="termy">

<!-- termynal -->

```yaml
- name: Create IKE gateway with PSK
  cdot65.scm.ike_gateway:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "branch-office-gw"
    description: "Branch office VPN gateway"
    version: "ikev2"
    peer_address: "203.0.113.1"
    interface: "ethernet1/1"
    pre_shared_key: "{{ vpn_psk }}"
    folder: "Texas"
    state: "present"
```

</div>

## 5. Usage Examples

### Creating an IKE Gateway with Pre-Shared Key

<div class="termy">

<!-- termynal -->

```yaml
- name: Create IKE gateway with PSK authentication
  cdot65.scm.ike_gateway:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
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

</div>

### Creating an IKE Gateway with Certificate Authentication

<div class="termy">

<!-- termynal -->

```yaml
- name: Create IKE gateway with certificate authentication
  cdot65.scm.ike_gateway:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
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

</div>

### Updating an IKE Gateway

<div class="termy">

<!-- termynal -->

```yaml
- name: Update IKE gateway settings
  cdot65.scm.ike_gateway:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
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

</div>

### Deleting an IKE Gateway

<div class="termy">

<!-- termynal -->

```yaml
- name: Delete an IKE gateway
  cdot65.scm.ike_gateway:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "deprecated-vpn"
    folder: "Texas"
    state: "absent"
```

</div>

## 6. Error Handling

<div class="termy">

<!-- termynal -->

```yaml
- name: Create IKE gateway with error handling
  block:
    - name: Attempt to create IKE gateway
      cdot65.scm.ike_gateway:
        provider: "{{ provider }}"
        name: "branch-vpn"
        version: "ikev2"
        peer_address: "198.51.100.1"
        interface: "ethernet1/1"
        crypto_profile: "non-existent-profile"  # Profile doesn't exist
        pre_shared_key: "{{ vpn_psk }}"
        folder: "Texas"
        state: "present"
  rescue:
    - name: Handle error
      debug:
        msg: "Failed to create IKE gateway. Check if all referenced objects exist."
```

</div>

## 7. Best Practices

1. **Authentication**
   - Use strong pre-shared keys or certificates for authentication
   - Consider using certificates for higher security
   - Rotate pre-shared keys periodically
   - Store secrets securely using Ansible Vault

2. **IKE Version**
   - Use IKEv2 when possible for better security and features
   - Only use IKEv1 for compatibility with legacy devices
   - Consider ikev2-preferred for maximum compatibility

3. **Identifiers**
   - Always configure explicit identifiers for both local and peer endpoints
   - Use IP addresses as identifiers when possible for simplicity
   - Ensure peer identifiers match exactly what the remote device uses

4. **Crypto Profiles**
   - Use strong encryption algorithms and DH groups
   - Follow current security best practices for crypto settings
   - Create custom crypto profiles instead of using defaults

5. **High Availability**
   - Configure liveness checks to ensure tunnel availability
   - Set appropriate liveness check intervals (not too short, not too long)
   - Consider NAT traversal settings when tunnels cross NAT devices

6. **Organization**
   - Use descriptive names for IKE gateways
   - Include purpose and remote site in gateway descriptions
   - Organize gateways in appropriate folders

## 8. Related Models

- [IKE Crypto Profile](ike_crypto_profile.md) - Configure encryption profiles for IKE gateways
- [IPsec Crypto Profile](ipsec_crypto_profile.md) - Configure encryption profiles for IPsec tunnels
- [IPsec Tunnel](ipsec_tunnel.md) - Configure IPsec tunnels that use IKE gateways
- [Remote Networks](remote_networks.md) - Configure remote networks that use IKE gateways