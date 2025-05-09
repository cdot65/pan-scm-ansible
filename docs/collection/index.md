# Collection Documentation

The Palo Alto Networks Strata Cloud Manager Ansible Collection provides a comprehensive set of
modules, roles, and plugins for managing SCM configurations. Built on top of the `pan-scm-sdk`
Python SDK, this collection enables automation of network security objects and policies in Strata
Cloud Manager.

## Collection Structure

```
cdot65.scm/
├── docs/                # Documentation
├── meta/                # Collection metadata
├── plugins/             # Collection plugins
│   ├── modules/         # Ansible modules
│   ├── inventory/       # Inventory plugins
│   ├── lookup/          # Lookup plugins
│   └── module_utils/    # Shared utilities
├── roles/               # Ansible roles
│   ├── bootstrap/       # SCM bootstrap role
│   └── deploy_config/   # Configuration deployment role
└── tests/               # Tests for collection
```

## Collection Namespace

All modules in this collection use the `cdot65.scm` namespace. To use a module:

```yaml
- name: Create an address object
  cdot65.scm.address:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "test-address"
    folder: "Texas"
    ip_netmask: "192.168.1.1/32"
    state: "present"
```

## Authentication

All modules in this collection require authentication to SCM using OAuth2 client credentials. The
recommended approach is to store credentials securely using Ansible Vault:

1. **Create a vault-encrypted variables file**:

   ```bash
   ansible-vault create vault.yaml
   ```

2. **Add your credentials to the file**:

   ```yaml
   client_id: "your-client-id"
   client_secret: "your-client-secret"
   tsg_id: "your-tenant-service-group-id"
   ```

3. **Reference the vault file in your playbook**:

   ```yaml
   - name: Configure SCM resources
     hosts: localhost
     vars_files:
       - vault.yaml
     vars:
       provider:
         client_id: "{{ client_id }}"
         client_secret: "{{ client_secret }}"
         tsg_id: "{{ tsg_id }}"
         log_level: "INFO"
     tasks:
       - name: Create address object
         cdot65.scm.address:
           provider: "{{ provider }}"
           name: "web-server"
           folder: "Texas"
           ip_netmask: "10.1.1.1/32"
           state: "present"
   ```

## Provider Configuration

The `provider` parameter is required for all modules and contains the following fields:

| Parameter       | Type   | Required | Description                     |
| --------------- | ------ | -------- | ------------------------------- |
| `client_id`     | string | Yes      | OAuth2 client ID                |
| `client_secret` | string | Yes      | OAuth2 client secret            |
| `tsg_id`        | string | Yes      | Tenant Service Group ID         |
| `log_level`     | string | No       | SDK log level (default: "INFO") |

## Key Collection Components

### Modules

The collection includes modules for managing various SCM configuration objects:

#### Network Objects

| Module                                                      | Description                              | Info Module                                                           |
| ----------------------------------------------------------- | ---------------------------------------- | --------------------------------------------------------------------- |
| [Address](modules/address.md)                               | Manage address objects                   | [Address Info](modules/address_info.md)                               |
| [Address Group](modules/address_group.md)                   | Manage address groups                    | [Address Group Info](modules/address_group_info.md)                   |
| [Application](modules/application.md)                       | Manage applications                      | [Application Info](modules/application_info.md)                       |
| [Application Group](modules/application_group.md)           | Manage application groups                | [Application Group Info](modules/application_group_info.md)           |
| [Dynamic User Group](modules/dynamic_user_group.md)         | Manage dynamic user groups               | [Dynamic User Group Info](modules/dynamic_user_group_info.md)         |
| [External Dynamic Lists](modules/external_dynamic_lists.md) | Manage external dynamic lists            | [External Dynamic Lists Info](modules/external_dynamic_lists_info.md) |
| [HIP Object](modules/hip_object.md)                         | Manage Host Information Profile objects  | [HIP Object Info](modules/hip_object_info.md)                         |
| [HIP Profile](modules/hip_profile.md)                       | Manage Host Information Profile profiles | [HIP Profile Info](modules/hip_profile_info.md)                       |
| [HTTP Server Profiles](modules/http_server_profiles.md)     | Manage HTTP server profiles              | [HTTP Server Profiles Info](modules/http_server_profiles_info.md)     |
| [Log Forwarding Profile](modules/log_forwarding_profile.md) | Manage log forwarding profiles           | [Log Forwarding Profile Info](modules/log_forwarding_profile_info.md) |
| [Quarantined Devices](modules/quarantined_devices.md)       | Manage quarantined devices               | [Quarantined Devices Info](modules/quarantined_devices_info.md)       |
| [Region](modules/region.md)                                 | Manage geographic region objects         | [Region Info](modules/region_info.md)                                 |
| [Service](modules/service.md)                               | Manage service objects                   | [Service Info](modules/service_info.md)                               |
| [Service Group](modules/service_group.md)                   | Manage service groups                    | [Service Group Info](modules/service_group_info.md)                   |
| [Syslog Server Profiles](modules/syslog_server_profiles.md) | Manage syslog server profiles            | [Syslog Server Profiles Info](modules/syslog_server_profiles_info.md) |
| [Tag](modules/tag.md)                                       | Manage tag objects                       | [Tag Info](modules/tag_info.md)                                       |

#### Network Configuration

| Module                                                  | Description                      | Info Module                                                      |
| ------------------------------------------------------- | -------------------------------- | ---------------------------------------------------------------- |
| [Security Zone](modules/security_zone.md)               | Manage security zones            |                                                                  |
| [IKE Crypto Profile](modules/ike_crypto_profile.md)     | Manage IKE crypto profiles       | [IKE Crypto Profile Info](modules/ike_crypto_profile_info.md)     |
| [IKE Gateway](modules/ike_gateway.md)                   | Manage IKE gateways              |                                                                  |
| [IPsec Crypto Profile](modules/ipsec_crypto_profile.md) | Manage IPsec crypto profiles     |                                                                  |
| [IPsec Tunnel](modules/ipsec_tunnel.md)                 | Manage IPsec tunnels             |                                                                  |
| [BGP Routing](modules/bgp_routing.md)                   | Manage BGP routing configuration | [BGP Routing Info](modules/bgp_routing_info.md)                   |

#### Deployment

| Module                                                    | Description                       | Info Module                                               |
| --------------------------------------------------------- | --------------------------------- | --------------------------------------------------------- |
| [Bandwidth Allocations](modules/bandwidth_allocations.md) | Manage bandwidth allocations      | [Bandwidth Allocations Info](modules/bandwidth_allocations_info.md) |
| [Internal DNS Servers](modules/internal_dns_servers.md)   | Manage internal DNS servers       | [Internal DNS Servers Info](modules/internal_dns_servers_info.md) |
| [Remote Networks](modules/remote_networks.md)             | Manage remote networks            | [Remote Networks Info](modules/remote_networks_info.md)   |
| [Network Locations](modules/network_locations.md)         | Manage network locations          |                                                           |
| [Service Connections](modules/service_connections.md)     | Manage service connections        | [Service Connections Info](modules/service_connections_info.md) |

#### Security Services

| Module                                                                          | Description                              | Info Module                                                                               |
| ------------------------------------------------------------------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------------- |
| [Security Rule](modules/security_rule.md)                                       | Manage security rules                    | [Security Rule Info](modules/security_rule_info.md)                                       |
| [Anti-Spyware Profile](modules/anti_spyware_profile.md)                         | Manage anti-spyware profiles             | [Anti-Spyware Profile Info](modules/anti_spyware_profile_info.md)                         |
| [Decryption Profile](modules/decryption_profile.md)                             | Manage decryption profiles               | [Decryption Profile Info](modules/decryption_profile_info.md)                             |
| [DNS Security Profile](modules/dns_security_profile.md)                         | Manage DNS security profiles             | [DNS Security Profile Info](modules/dns_security_profile_info.md)                         |
| [Security Profiles Group](modules/security_profiles_group.md)                   | Manage security profile groups           | [Security Profiles Group Info](modules/security_profiles_group_info.md)                   |
| [URL Categories](modules/url_categories.md)                                     | Manage URL categories                    | [URL Categories Info](modules/url_categories_info.md)                                     |
| [Vulnerability Protection Profile](modules/vulnerability_protection_profile.md) | Manage vulnerability protection profiles | [Vulnerability Protection Profile Info](modules/vulnerability_protection_profile_info.md) |
| [WildFire Antivirus Profiles](modules/wildfire_antivirus_profiles.md)           | Manage WildFire antivirus profiles       | [WildFire Antivirus Profiles Info](modules/wildfire_antivirus_profiles_info.md)           |

[View All Modules →](modules/index.md)

### Roles

Pre-built roles to simplify common tasks:

- **bootstrap**: Initialize SCM configurations
- **deploy_config**: Deploy configurations to SCM

[View All Roles →](roles/index.md)

### Plugins

Additional plugins to extend Ansible functionality:

- **Inventory Plugin**: Build dynamic inventories from SCM
- **Lookup Plugin**: Look up data from SCM

[View All Plugins →](plugins/index.md)

## Best Practices

1. **Idempotent Operations**:

   - All modules are designed to be idempotent
   - Running playbooks multiple times won't create duplicate resources

2. **Secure Credential Management**:

   - Always store credentials in Ansible Vault
   - Never hardcode secrets in playbooks

3. **Organize by Folder**:

   - Group related objects in the same SCM folder
   - Use consistent folder naming schemes

4. **Testing**:

   - Use `check_mode: yes` to validate changes before applying them
   - Create test environments before deploying to production
