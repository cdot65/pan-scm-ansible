# Using Roles

This guide covers how to effectively use the pre-built roles included in the Palo Alto Networks SCM Ansible Collection.

## Available Roles

The collection includes these roles:

| Role | Description |
|------|-------------|
| `bootstrap` | Initialize SCM with base configuration |
| `deploy_config` | Deploy configurations to managed devices |

## Role Benefits

Using these roles provides several advantages:

- **Simplified Workflows**: Complex tasks reduced to a few variables
- **Best Practices**: Follows recommended patterns for SCM management
- **Error Handling**: Built-in validation and error management
- **Idempotency**: Safe to run multiple times
- **Consistency**: Standardized approach across environments

## Common Role Variables

All roles accept these common variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `scm_username` | SCM username | No | Environment variable |
| `scm_password` | SCM password | No | Environment variable |
| `scm_tenant` | SCM tenant ID | No | Environment variable |
| `scm_debug` | Enable debug logging | No | `false` |

## Using the Bootstrap Role

The `bootstrap` role initializes a new SCM environment with baseline configurations:

```yaml
---
- name: Bootstrap SCM Environment
  hosts: localhost
  connection: local
  
  roles:
    - role: cdot65.scm.bootstrap
      vars:
        bootstrap_folder: "MyCompany"
        bootstrap_tags:
          - name: "web"
            color: "color13"  # Red
          - name: "database"
            color: "color7"   # Blue
        bootstrap_address_objects:
          - name: "web-server-1"
            description: "Production web server"
            ip_netmask: "10.1.1.10/32"
            tags:
              - "web"
        bootstrap_security_zones:
          - name: "Web-Zone"
            description: "Zone for web servers"
```

### Bootstrap Role Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `bootstrap_folder` | Main folder to create | Yes | - |
| `bootstrap_tags` | List of tags to create | No | `[]` |
| `bootstrap_address_objects` | List of address objects | No | `[]` |
| `bootstrap_service_objects` | List of service objects | No | `[]` |
| `bootstrap_security_zones` | List of security zones | No | `[]` |

## Using the Deploy Config Role

The `deploy_config` role handles committing and pushing configurations to managed firewalls:

```yaml
---
- name: Deploy SCM Configurations
  hosts: localhost
  connection: local
  
  roles:
    - role: cdot65.scm.deploy_config
      vars:
        deploy_commit_message: "Weekly security policy update"
        deploy_folders:
          - "Production"
        deploy_device_groups:
          - "US-East-Firewalls"
        deploy_wait_for_job: true
        deploy_timeout: 1200  # 20 minutes
```

### Deploy Config Role Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `deploy_commit_message` | Message for commit | No | "Deployed by Ansible" |
| `deploy_folders` | List of folders to deploy | No | `["Shared"]` |
| `deploy_device_groups` | List of device groups | No | `[]` |
| `deploy_devices` | List of specific devices | No | `[]` |
| `deploy_wait_for_job` | Wait for job completion | No | `true` |
| `deploy_timeout` | Timeout in seconds | No | `600` |
| `deploy_force` | Force deployment | No | `false` |

## Role Dependencies

These roles don't have external dependencies, but they rely on modules from this collection. Ensure the collection is properly installed before using the roles.

## Customizing Roles

You can customize role behavior by overriding variables:

```yaml
- name: Customized Bootstrap
  hosts: localhost
  vars:
    bootstrap_folder: "CustomEnvironment"
    # Custom variable overrides
  roles:
    - role: cdot65.scm.bootstrap
```

## Creating Role Defaults

For consistent settings, create a defaults file:

```yaml
# group_vars/all.yml
bootstrap_folder: "MyCompany"
bootstrap_tags:
  - name: "web"
    color: "color13"
  - name: "database"
    color: "color7"
```

## Combining Roles

Roles can be combined in sequence for a complete workflow:

```yaml
---
- name: Complete SCM Management
  hosts: localhost
  connection: local
  
  roles:
    # First bootstrap the environment
    - role: cdot65.scm.bootstrap
      vars:
        bootstrap_folder: "Production"
        # ... bootstrap variables
    
    # Then deploy the configuration
    - role: cdot65.scm.deploy_config
      vars:
        deploy_folders:
          - "Production"
        deploy_device_groups:
          - "ALL"
```

## Using Role Tags

Use Ansible tags to selectively run parts of roles:

```yaml
- name: SCM Management with Tags
  hosts: localhost
  roles:
    - role: cdot65.scm.bootstrap
      tags: 
        - setup
        - bootstrap
```

Then run with specific tags:

```bash
ansible-playbook playbook.yml --tags bootstrap
```

## Role Error Handling

All roles include error handling for common issues:

- Authentication failures
- Missing required parameters
- Object creation failures
- Deployment issues

If errors occur, check the error message for details on how to resolve the issue.

## Example: Complete Environment Setup

This example shows how to use roles for a complete environment setup:

```yaml
---
- name: Complete SCM Setup
  hosts: localhost
  connection: local
  vars_files:
    - scm_credentials.yml
  
  roles:
    # Setup base environment
    - role: cdot65.scm.bootstrap
      vars:
        scm_username: "{{ scm_username }}"
        scm_password: "{{ scm_password }}"
        scm_tenant: "{{ scm_tenant }}"
        bootstrap_folder: "Production"
        bootstrap_tags:
          - name: "web"
            color: "color13"
          - name: "app"
            color: "color7"
          - name: "db"
            color: "color20"
        bootstrap_address_objects:
          - name: "web-vip"
            description: "Web VIP"
            ip_netmask: "203.0.113.10/32"
            tags: ["web"]
          - name: "app-server-1"
            description: "Application Server 1"
            ip_netmask: "10.0.1.10/32"
            tags: ["app"]
          - name: "db-server-1"
            description: "Database Server 1"
            ip_netmask: "10.0.2.10/32"
            tags: ["db"]
        bootstrap_security_zones:
          - name: "Internet"
            description: "Internet Zone"
          - name: "DMZ"
            description: "DMZ Zone"
          - name: "Internal"
            description: "Internal Zone"
    
    # Deploy configuration
    - role: cdot65.scm.deploy_config
      vars:
        scm_username: "{{ scm_username }}"
        scm_password: "{{ scm_password }}"
        scm_tenant: "{{ scm_tenant }}"
        deploy_commit_message: "Initial environment setup"
        deploy_folders:
          - "Production"
        deploy_device_groups:
          - "Production-Firewalls"
```

## Next Steps

- Explore [Playbook Examples](playbook-examples.md) for common use cases
- Learn about [Advanced Topics](advanced-topics.md) for complex deployments
