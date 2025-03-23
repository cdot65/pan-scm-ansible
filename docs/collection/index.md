# Collection Documentation

The Palo Alto Networks Strata Cloud Manager Ansible Collection provides a comprehensive set of modules, roles, and plugins for managing SCM configurations. Built on top of the `pan-scm-sdk` Python SDK, this collection enables automation of network security objects and policies in Strata Cloud Manager.

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

All modules in this collection require authentication to SCM using OAuth2 client credentials. The recommended approach is to store credentials securely using Ansible Vault:

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

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `client_id` | string | Yes | OAuth2 client ID |
| `client_secret` | string | Yes | OAuth2 client secret |
| `tsg_id` | string | Yes | Tenant Service Group ID |
| `log_level` | string | No | SDK log level (default: "INFO") |

## Key Collection Components

### Modules

The collection includes modules for managing various SCM configuration objects:

- **Network Objects**: 
  - [Address](modules/address.md), [Address Group](modules/address_group.md)
  - [Application](modules/application.md), [Application Group](modules/application_group.md)
  - [Service](modules/service.md), [Service Group](modules/service_group.md)
  - [Tag](modules/tag.md)
  
- **Info Modules**:
  - [Address Info](modules/address_info.md), [Address Group Info](modules/address_group_info.md)
  - [Application Info](modules/application_info.md), [Application Group Info](modules/application_group_info.md)
  - [Service Info](modules/service_info.md), [Service Group Info](modules/service_group_info.md)
  - [Tag Info](modules/tag_info.md)

- **Network Configuration**:
  - [Security Zone](modules/security_zone.md)
  - [IKE Crypto Profile](modules/ike_crypto_profile.md), [IKE Gateway](modules/ike_gateway.md)
  - [IPsec Crypto Profile](modules/ipsec_crypto_profile.md), [IPsec Tunnel](modules/ipsec_tunnel.md)
  - [BGP Routing](modules/bgp_routing.md)

- **Deployment**:
  - [Remote Networks](modules/remote_networks.md)
  - [Network Locations](modules/network_locations.md)
  - [Service Connections](modules/service_connections.md)

- **Security Services**:
  - [Anti-Spyware Profile](modules/anti_spyware_profile.md), [Anti-Spyware Profile Info](modules/anti_spyware_profile_info.md)
  - [Security Profiles Group](modules/security_profiles_group.md)
  - [Security Rule](modules/security_rule.md), [Security Rule Info](modules/security_rule_info.md)

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