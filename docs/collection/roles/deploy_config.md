# Deploy Configuration Role

The `deploy_config` role provides a standardized way to manage, push, and deploy SCM configurations to managed firewalls. This role combines configuration management, commit operations, and deployment in a single workflow.

## Role Overview

The deploy_config role offers three main capabilities:

1. **Configuration Management**: Create and update SCM objects based on structured definitions
2. **Commit Operations**: Commit pending changes to specified folders
3. **Deployment Control**: Push configurations to managed devices with robust job monitoring

## Role Variables

### Authentication Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `scm_client_id` | OAuth2 client ID | Yes | - |
| `scm_client_secret` | OAuth2 client secret | Yes | - |
| `scm_tsg_id` | Tenant Service Group ID | Yes | - |
| `scm_log_level` | Log level for SDK | No | `"INFO"` |

### Configuration Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `scm_configs` | Dictionary of configuration objects to create | No | `{}` |
| `deploy_config_validate_only` | Validate but don't apply changes | No | `false` |

### Commit Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `deploy_folders` | List of folders to deploy | No | `["Shared"]` |
| `deploy_commit_message` | Message for commit operation | No | `"Configuration deployed by Ansible"` |
| `deploy_should_commit` | Whether to commit changes | No | `true` |
| `deploy_compare_versions` | Compare version before commit | No | `true` |

### Deployment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `deploy_device_groups` | List of device groups to deploy to | No | `[]` |
| `deploy_devices` | List of specific devices to deploy to | No | `[]` |
| `deploy_wait_for_job` | Wait for deploy job to complete | No | `true` |
| `deploy_timeout` | Timeout in seconds for job completion | No | `600` |
| `deploy_force` | Force deployment even with warnings | No | `false` |
| `deploy_push_config` | Whether to push config to devices | No | `true` |

## Configuration Structure

The `scm_configs` variable uses a structured format to define SCM objects:

```yaml
scm_configs:
  addresses:            # Address objects
    - name: "web-server"
      folder: "Production"
      description: "Web server"
      ip_netmask: "10.1.1.1/32"
  address_groups:       # Address groups
    - name: "web-servers"
      folder: "Production"
      static:
        - "web-server"
  services:             # Service objects
    - name: "http-service"
      folder: "Production"
      protocol:
        tcp:
          port: "80"
  security_rules:       # Security rules
    - name: "Allow Web Traffic"
      folder: "Production"
      source_zone: ["untrust"]
      destination_zone: ["trust"]
      source_address: ["any"]
      destination_address: ["web-servers"]
      application: ["web-browsing"]
      service: ["http-service"]
      action: "allow"
```

## Example Playbook

```yaml
---
- name: Deploy SCM Configurations
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml  # Contains encrypted credentials
  
  roles:
    - role: cdot65.scm.deploy_config
      vars:
        scm_client_id: "{{ client_id }}"
        scm_client_secret: "{{ client_secret }}"
        scm_tsg_id: "{{ tsg_id }}"
        deploy_commit_message: "Network security policy update"
        deploy_folders:
          - "Production"
          - "Development"
        deploy_device_groups:
          - "US-East-Firewalls"
        deploy_wait_for_job: true
        deploy_timeout: 1200  # 20 minutes
        scm_configs:
          addresses:
            - name: "web-server"
              folder: "Production"
              description: "Web server"
              ip_netmask: "10.1.1.1/32"
            - name: "db-server"
              folder: "Production"
              description: "Database server"
              ip_netmask: "10.1.1.2/32"
          security_rules:
            - name: "Allow Web Traffic"
              folder: "Production"
              source_zone: ["untrust"]
              destination_zone: ["trust"]
              source_address: ["any"]
              destination_address: ["web-server"]
              application: ["web-browsing"]
              service: ["application-default"]
              action: "allow"
```

## Deployment Workflow

The role performs these tasks in order:

1. Validate input parameters and authentication
2. Create or update SCM objects defined in `scm_configs`
3. Commit any pending changes to specified folders (if `deploy_should_commit` is true)
4. Create a deployment job for specified device groups or devices (if `deploy_push_config` is true)
5. Push the candidate configuration
6. Optionally wait for job completion with progress updates
7. Report deployment results

## Configuration Management Only

If you want to manage configurations without committing or deploying:

```yaml
- name: Manage SCM Configurations Only
  hosts: localhost
  roles:
    - role: cdot65.scm.deploy_config
      vars:
        scm_client_id: "{{ client_id }}"
        scm_client_secret: "{{ client_secret }}"
        scm_tsg_id: "{{ tsg_id }}"
        deploy_should_commit: false
        deploy_push_config: false
        scm_configs:
          addresses:
            - name: "test-server"
              folder: "Production"
              description: "Test server"
              ip_netmask: "10.1.1.10/32"
```

## Validation Only Mode

You can validate configurations without applying changes:

```yaml
- name: Validate SCM Configurations
  hosts: localhost
  roles:
    - role: cdot65.scm.deploy_config
      vars:
        scm_client_id: "{{ client_id }}"
        scm_client_secret: "{{ client_secret }}"
        scm_tsg_id: "{{ tsg_id }}"
        deploy_config_validate_only: true
        scm_configs:
          # Configuration objects to validate
```

## Job Monitoring

When `deploy_wait_for_job` is enabled (default), the role will monitor the deployment job until completion or timeout:

```yaml
- name: Deploy with detailed job monitoring
  hosts: localhost
  roles:
    - role: cdot65.scm.deploy_config
      vars:
        scm_client_id: "{{ client_id }}"
        scm_client_secret: "{{ client_secret }}"
        scm_tsg_id: "{{ tsg_id }}"
        deploy_wait_for_job: true
        deploy_timeout: 1800  # 30 minutes
        deploy_folders:
          - "Production"
```

## Partial Deployments

You can perform partial deployments by specifying particular folders, device groups, or devices:

```yaml
- name: Partial deployment to specific devices
  hosts: localhost
  roles:
    - role: cdot65.scm.deploy_config
      vars:
        scm_client_id: "{{ client_id }}"
        scm_client_secret: "{{ client_secret }}"
        scm_tsg_id: "{{ tsg_id }}"
        deploy_folders:
          - "Emergency-Changes"
        deploy_devices:
          - "firewall-1.example.com"
          - "firewall-2.example.com"
```

## Error Handling

The role includes comprehensive error handling with informative error messages. If any step fails, the role will stop and report the specific error.

Common deployment issues include:
- Configuration validation errors
- Device connectivity issues
- Timeout during deployment
- Permission issues

## Dependencies

This role depends on the following collection modules:
- `cdot65.scm.address` and related object modules
- `cdot65.scm.commit`
- `cdot65.scm.push_config`
- `cdot65.scm.job_info`

## Role Tags

The deploy_config role provides the following tags:

- `config`: Configuration management tasks
- `commit`: Configuration commit tasks
- `deploy`: Deployment tasks
- `validate`: Validation tasks
- `addresses`: Address object tasks
- `address_groups`: Address group tasks
- `services`: Service object tasks
- `security_rules`: Security rule tasks

## Best Practices

1. **Use Structured Variables**: Keep configurations organized in separate variable files
2. **Start with Validation**: Use `deploy_config_validate_only: true` to validate changes first
3. **Implement CI/CD**: Integrate this role into CI/CD pipelines for automated deployments
4. **Version Control**: Store your configuration variables in version control
5. **Use Tags**: Use the role's tags to selectively run parts of the deployment
