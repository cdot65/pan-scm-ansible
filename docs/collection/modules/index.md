# Modules Overview

The Palo Alto Networks Strata Cloud Manager Ansible Collection provides a comprehensive set of modules for managing SCM configuration objects. These modules enable you to automate the creation, modification, and deletion of various network and security components.

## Module Categories

The modules are organized into these categories:

- **Object Modules**: Manage address objects, address groups, services, tags, etc.
- **Security Modules**: Manage security rules, security profiles, etc.
- **Network Modules**: Manage zones, IKE gateways, IPsec tunnels, etc.
- **Deployment Modules**: Manage remote networks, service connections, etc.

## Available Modules

| Module Name | Description | Category |
|-------------|-------------|----------|
| [`address`](address.md) | Manage address objects | Object |
| [`address_group`](address_group.md) | Manage address groups | Object |
| [`application`](application.md) | Manage custom applications | Object |
| [`application_group`](application_group.md) | Manage application groups | Object | 
| [`anti_spyware_profile`](anti_spyware_profile.md) | Manage anti-spyware security profiles | Security |
| [`bgp_routing`](bgp_routing.md) | Manage BGP routing configurations | Network |
| [`ike_crypto_profile`](ike_crypto_profile.md) | Manage IKE crypto profiles | Network |
| [`ike_gateway`](ike_gateway.md) | Manage IKE gateways | Network |
| [`ipsec_crypto_profile`](ipsec_crypto_profile.md) | Manage IPSec crypto profiles | Network |
| [`ipsec_tunnel`](ipsec_tunnel.md) | Manage IPSec tunnels | Network |
| [`network_locations`](network_locations.md) | Manage network locations | Deployment |
| [`remote_networks`](remote_networks.md) | Manage remote networks | Deployment |
| [`security_rule`](security_rule.md) | Manage security rules | Security |
| [`security_zone`](security_zone.md) | Manage security zones | Network |
| [`service`](service.md) | Manage service objects | Object |
| [`service_group`](service_group.md) | Manage service groups | Object |
| [`tag`](tag.md) | Manage tags | Object |

## Common Module Parameters

All modules share the following common parameters:

### Provider

The provider parameter is required for all modules and contains SCM authentication credentials:

```yaml
provider:
  client_id: "your_client_id"
  client_secret: "your_client_secret"
  tsg_id: "your_tsg_id"
  log_level: "INFO"  # Optional, defaults to INFO
```

### State

Most modules support the following state parameters:

- `present`: Ensures the resource exists with the specified configuration
- `absent`: Ensures the resource does not exist

### Location Parameters

Most modules require exactly one of the following location parameters:

- `folder`: The folder where the resource is stored
- `snippet`: The configuration snippet for the resource
- `device`: The device where the resource is defined

## Information Modules

These modules retrieve information from SCM without making changes:

| Module Name | Description |
|-------------|-------------|
| [`address_info`](address_info.md) | Get information about address objects |
| [`address_group_info`](address_group_info.md) | Get information about address groups |
| [`anti_spyware_profile_info`](anti_spyware_profile_info.md) | Get information about anti-spyware profiles |
| [`application_info`](application_info.md) | Get information about applications |
| [`application_group_info`](application_group_info.md) | Get information about application groups |
| [`security_rule_info`](security_rule_info.md) | Get information about security rules |
| [`service_info`](service_info.md) | Get information about service objects |
| [`service_group_info`](service_group_info.md) | Get information about service groups |
| [`tag_info`](tag_info.md) | Get information about tags |

## Return Values

Most modules return these common values:

| Name | Description | Type | Sample |
|------|-------------|------|--------|
| `changed` | Whether changes were made | boolean | `true` |
| `scm_object` | The SCM object details | dictionary | `{"id": "123", "name": "test-address"}` |
| `response` | The raw API response | dictionary | `{"status": "success", "data": {...}}` |

## Using Check Mode

All modules support Ansible's check mode. When run with `--check`, the module will report what changes would be made without actually making them:

```yaml
- name: Check what would change (without making changes)
  cdot65.scm.address:
    name: "web-server"
    folder: "SharedFolder"
    ip_netmask: "10.1.1.1/32"
  check_mode: yes
```
