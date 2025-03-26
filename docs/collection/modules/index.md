# Index Configuration Object

The Palo Alto Networks Strata Cloud Manager Ansible Collection provides a comprehensive set of
modules for managing SCM configuration objects. These modules enable you to automate the creation,
modification, and deletion of various network and security components.

## Module Categories

The modules are organized into these categories:

### Network Objects

These modules manage the fundamental building blocks of your network security policy:

| Module                                              | Description                      | Info Module                                                   |
| --------------------------------------------------- | -------------------------------- | ------------------------------------------------------------- |
| [address](address.md)                               | Manage address objects           | [address_info](address_info.md)                               |
| [address_group](address_group.md)                   | Manage address groups            | [address_group_info](address_group_info.md)                   |
| [application](application.md)                       | Manage applications              | [application_info](application_info.md)                       |
| [application_group](application_group.md)           | Manage application groups        | [application_group_info](application_group_info.md)           |
| [dynamic_user_group](dynamic_user_group.md)         | Manage dynamic user groups       | [dynamic_user_group_info](dynamic_user_group_info.md)         |
| [external_dynamic_lists](external_dynamic_lists.md) | Manage external dynamic lists    | [external_dynamic_lists_info](external_dynamic_lists_info.md) |
| [hip_object](hip_object.md)                         | Manage HIP objects               | [hip_object_info](hip_object_info.md)                         |
| [hip_profile](hip_profile.md)                       | Manage HIP profiles              | [hip_profile_info](hip_profile_info.md)                       |
| [service](service.md)                               | Manage service objects           | [service_info](service_info.md)                               |
| [service_group](service_group.md)                   | Manage service groups            | [service_group_info](service_group_info.md)                   |
| [tag](tag.md)                                       | Manage tag objects               | [tag_info](tag_info.md)                                       |
| [http_server_profiles](http_server_profiles.md)     | Manage HTTP server profiles      | [http_server_profiles_info](http_server_profiles_info.md)     |
| [log_forwarding_profile](log_forwarding_profile.md) | Manage log forwarding profiles   | [log_forwarding_profile_info](log_forwarding_profile_info.md) |
| [quarantined_devices](quarantined_devices.md)       | Manage quarantined devices       | [quarantined_devices_info](quarantined_devices_info.md)       |
| [region](region.md)                                 | Manage geographic region objects | [region_info](region_info.md)                                 |
| [syslog_server_profiles](syslog_server_profiles.md) | Manage syslog server profiles    | [syslog_server_profiles_info](syslog_server_profiles_info.md) |

### Network Configuration

These modules configure the network infrastructure and connectivity:

| Module                                          | Description                      |
| ----------------------------------------------- | -------------------------------- |
| [security_zone](security_zone.md)               | Manage security zones            |
| [ike_crypto_profile](ike_crypto_profile.md)     | Manage IKE crypto profiles       |
| [ike_gateway](ike_gateway.md)                   | Manage IKE gateways              |
| [ipsec_crypto_profile](ipsec_crypto_profile.md) | Manage IPsec crypto profiles     |
| [ipsec_tunnel](ipsec_tunnel.md)                 | Manage IPsec tunnels             |
| [bgp_routing](bgp_routing.md)                   | Manage BGP routing configuration |

### Deployment

These modules manage deployment-related configurations:

| Module                                        | Description                |
| --------------------------------------------- | -------------------------- |
| [remote_networks](remote_networks.md)         | Manage remote networks     |
| [network_locations](network_locations.md)     | Manage network locations   |
| [service_connections](service_connections.md) | Manage service connections |

### Security Services

These modules configure security policies and profiles:

| Module                                                                  | Description                              | Info Module                                                                       |
| ----------------------------------------------------------------------- | ---------------------------------------- | --------------------------------------------------------------------------------- |
| [security_rule](security_rule.md)                                       | Manage security rules                    | [security_rule_info](security_rule_info.md)                                       |
| [anti_spyware_profile](anti_spyware_profile.md)                         | Manage anti-spyware profiles             | [anti_spyware_profile_info](anti_spyware_profile_info.md)                         |
| [decryption_profile](decryption_profile.md)                             | Manage decryption profiles               | [decryption_profile_info](decryption_profile_info.md)                             |
| [dns_security_profile](dns_security_profile.md)                         | Manage DNS security profiles             | [dns_security_profile_info](dns_security_profile_info.md)                         |
| [security_profiles_group](security_profiles_group.md)                   | Manage security profile groups           | -                                                                                 |
| [url_categories](url_categories.md)                                     | Manage URL categories                    | [url_categories_info](url_categories_info.md)                                     |
| [vulnerability_protection_profile](vulnerability_protection_profile.md) | Manage vulnerability protection profiles | [vulnerability_protection_profile_info](vulnerability_protection_profile_info.md) |
| [wildfire_antivirus_profiles](wildfire_antivirus_profiles.md)           | Manage WildFire antivirus profiles       | [wildfire_antivirus_profiles_info](wildfire_antivirus_profiles_info.md)           |

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

Information modules retrieve data without making changes:

- They follow the naming pattern `<resource>_info` (e.g., `address_info`)
- They support filters to narrow down results
- They return lists of matching objects or detailed information about specific objects

## Return Values

Most modules return these common values:

| Name         | Description               | Type       | Sample                                  |
| ------------ | ------------------------- | ---------- | --------------------------------------- |
| `changed`    | Whether changes were made | boolean    | `true`                                  |
| `scm_object` | The SCM object details    | dictionary | `{"id": "123", "name": "test-address"}` |

## Using Check Mode

All modules support Ansible's check mode. When run with `--check`, the module will report what
changes would be made without actually making them:

```yaml
- name: Check what would change (without making changes)
  cdot65.scm.address:
    name: "web-server"
    folder: "SharedFolder"
    ip_netmask: "10.1.1.1/32"
  check_mode: yes
```
