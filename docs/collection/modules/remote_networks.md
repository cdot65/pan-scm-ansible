# Remote Networks Configuration Object

## 1. Overview
The Remote Networks module allows you to manage remote network connections within Strata Cloud Manager (SCM). Remote networks enable secure connectivity between your SCM-managed infrastructure and external networks, typically through IPsec VPN tunnels. This module helps you create, configure, and manage these connections.

## 2. Core Methods

| Method     | Description                    | Parameters                | Return Type            |
|------------|--------------------------------|---------------------------|------------------------|
| `create()` | Creates a new remote network   | `data: Dict[str, Any]`    | `ResponseModel`        |
| `get()`    | Retrieves network by name      | `name: str`               | `ResponseModel`        |
| `update()` | Updates an existing network    | `network: Model`          | `ResponseModel`        |
| `delete()` | Deletes a remote network       | `id: str`                 | `None`                 |
| `list()`   | Lists remote networks          | `filters: Dict[str, Any]` | `List[ResponseModel]`  |

## 3. Model Attributes

| Attribute               | Type              | Required | Description                                    |
|-------------------------|-------------------|----------|------------------------------------------------|
| `name`                  | str               | Yes      | Name of the remote network                     |
| `description`           | str               | No       | Description of the remote network              |
| `status`                | str               | No       | Status of the remote network (read-only)       |
| `license_type`          | str               | No       | License type for the remote network            |
| `region`                | str               | Yes      | Region where the network is located            |
| `spn_name`              | str               | No       | Service provider name                          |
| `ike_gateway`           | str               | Yes      | IKE gateway for the VPN connection             |
| `ipsec_crypto_profile`  | str               | Yes      | IPsec crypto profile for encryption            |
| `tunnel_interface`      | str               | Yes      | Tunnel interface name                          |
| `subnets`               | List[str]         | No       | Subnets within the remote network              |
| `bgp_peer`              | Dict              | No       | BGP peer configuration                         |
| `ecmp_load_balancing`   | bool              | No       | Enable ECMP load balancing                     |
| `protocol`              | Dict              | No       | Protocol configuration for the connection      |
| `secondary_wan_config`  | Dict              | No       | Secondary WAN configuration                     |

## 4. Basic Configuration

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a remote network
  cdot65.scm.remote_networks:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "branch-office"
    description: "Branch Office VPN Connection"
    region: "us-east-1"
    ike_gateway: "branch-gateway"
    ipsec_crypto_profile: "standard-ipsec-profile"
    tunnel_interface: "tunnel.1"
    subnets:
      - "192.168.10.0/24"
      - "192.168.11.0/24"
    state: "present"
```

</div>

## 5. Usage Examples

### Creating a Basic Remote Network

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a basic remote network
  cdot65.scm.remote_networks:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "site-a-vpn"
    description: "Site A VPN Connection"
    region: "us-east-1"
    ike_gateway: "site-a-gateway"
    ipsec_crypto_profile: "default-ipsec-crypto-profile"
    tunnel_interface: "tunnel.1"
    subnets:
      - "10.1.0.0/16"
    state: "present"
```

</div>

### Creating a Remote Network with BGP

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a remote network with BGP peering
  cdot65.scm.remote_networks:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "site-b-vpn"
    description: "Site B VPN with BGP"
    region: "us-west-1"
    ike_gateway: "site-b-gateway"
    ipsec_crypto_profile: "strong-ipsec-profile"
    tunnel_interface: "tunnel.2"
    protocol:
      bgp:
        enable: true
        peer_as: 65001
        local_address_ip: "169.254.0.1/30"
        peer_address_ip: "169.254.0.2"
    state: "present"
```

</div>

### Updating a Remote Network

<div class="termy">

<!-- termynal -->

```yaml
- name: Update a remote network
  cdot65.scm.remote_networks:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "site-a-vpn"
    description: "Updated Site A VPN Connection"
    region: "us-east-1"
    ike_gateway: "site-a-gateway"
    ipsec_crypto_profile: "default-ipsec-crypto-profile"
    tunnel_interface: "tunnel.1"
    subnets:
      - "10.1.0.0/16"
      - "10.2.0.0/16"  # Added subnet
    state: "present"
```

</div>

### Deleting a Remote Network

<div class="termy">

<!-- termynal -->

```yaml
- name: Delete a remote network
  cdot65.scm.remote_networks:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "decommissioned-site"
    state: "absent"
```

</div>

### Listing Remote Networks

<div class="termy">

<!-- termynal -->

```yaml
- name: List all remote networks
  cdot65.scm.remote_networks_info:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
  register: networks

- name: Display remote networks
  debug:
    msg: "{{ item.name }} - {{ item.status }}"
  loop: "{{ networks.remote_networks }}"
```

</div>

## 6. Error Handling

<div class="termy">

<!-- termynal -->

```yaml
- name: Create remote network with error handling
  block:
    - name: Attempt to create remote network
      cdot65.scm.remote_networks:
        provider: "{{ provider }}"
        name: "new-branch"
        region: "us-east-1"
        ike_gateway: "non-existent-gateway"  # Gateway doesn't exist
        ipsec_crypto_profile: "default-ipsec-crypto-profile"
        tunnel_interface: "tunnel.1"
        state: "present"
  rescue:
    - name: Handle error
      debug:
        msg: "Failed to create remote network. Check if all referenced objects exist."
```

</div>

## 7. Best Practices

1. **Planning and Design**
   - Plan IP addressing to avoid overlaps between remote networks
   - Design BGP peering relationships carefully
   - Choose appropriate regions based on geographic proximity
   - Document network topology and VPN configuration details

2. **Security Configuration**
   - Use strong IPsec crypto profiles
   - Configure appropriate security rules for remote network traffic
   - Implement principle of least privilege for remote network access
   - Regularly review and audit remote network connections

3. **High Availability**
   - Consider redundant tunnels for critical connections
   - Implement secondary WAN configurations where needed
   - Monitor tunnel status and connectivity
   - Create backup plans for connection failures

4. **BGP Configuration**
   - Use private AS numbers for BGP peering
   - Configure route filters to control route advertisements
   - Consider BGP authentication mechanisms
   - Test BGP routing changes before implementation

5. **Maintenance**
   - Schedule maintenance windows for configuration changes
   - Test changes in a staging environment when possible
   - Keep IKE and IPsec settings in sync with remote endpoints
   - Maintain documentation of remote network configurations

## 8. Related Models

- [IKE Gateway](ike_gateway.md) - Configure IKE gateways used by remote networks
- [IPsec Crypto Profile](ipsec_crypto_profile.md) - Configure encryption profiles for IPsec tunnels
- [BGP Routing](bgp_routing.md) - Configure BGP routing used with remote networks
- [Network Locations](network_locations.md) - Configure network locations for remote networks