# Roles Overview

The Palo Alto Networks Strata Cloud Manager Ansible Collection includes pre-built roles that simplify common configuration tasks. These roles provide a more structured way to manage SCM configurations compared to using individual modules directly.

## Available Roles

| Role Name | Description |
|-----------|-------------|
| [bootstrap](bootstrap.md) | Initialize SCM configurations with basic settings |
| [deploy_config](deploy_config.md) | Deploy configurations to SCM using a structured approach |

## Using Roles

To use a role in your playbook:

```yaml
- name: Deploy SCM Configuration
  hosts: localhost
  roles:
    - role: cdot65.scm.deploy_config
      vars:
        scm_client_id: "{{ client_id }}"
        scm_client_secret: "{{ client_secret }}"
        scm_tsg_id: "{{ tsg_id }}"
        scm_configs:
          addresses:
            - name: "web-server"
              folder: "Texas"
              ip_netmask: "10.1.1.1/32"
            - name: "db-server"
              folder: "Texas"
              ip_netmask: "10.1.1.2/32"
          services:
            - name: "web-service"
              folder: "Texas"
              protocol:
                tcp:
                  port: "80,443"
```

## Role Variables

Each role has its own set of variables that control its behavior. These variables can be set in your playbook, in group/host variables, or in defaults.

To view the variables for a specific role, refer to its documentation:

- [Bootstrap Role Variables](bootstrap.md#role-variables)
- [Deploy Configuration Role Variables](deploy_config.md#role-variables)

## Common Variables

All roles share these common variables:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `scm_client_id` | OAuth2 client ID | Yes | |
| `scm_client_secret` | OAuth2 client secret | Yes | |
| `scm_tsg_id` | Tenant Service Group ID | Yes | |
| `scm_log_level` | Log level for SDK | No | INFO |

## Role Customization

You can customize role behavior by:

1. **Overriding Variables**: Set variables in your playbook or inventory
2. **Using Role Defaults**: Create a `defaults/main.yml` file with your preferred defaults
3. **Creating Custom Templates**: Override templates by placing them in your playbook's `templates` directory

### Example: Customizing the deploy_config Role

```yaml
- name: Deploy SCM Configuration with Custom Settings
  hosts: localhost
  roles:
    - role: cdot65.scm.deploy_config
      vars:
        scm_client_id: "{{ client_id }}"
        scm_client_secret: "{{ client_secret }}"
        scm_tsg_id: "{{ tsg_id }}"
        # Custom settings
        deploy_config_commit_description: "Deployed by Ansible on {{ ansible_date_time.date }}"
        deploy_config_backup: true
        deploy_config_wait_time: 60
        # Configuration to deploy
        scm_configs:
          addresses:
            - name: "web-server"
              folder: "Texas"
              ip_netmask: "10.1.1.1/32"
```

## Role Tags

Roles use tags to allow you to run specific parts of the role:

```bash
# Run only address configuration tasks
ansible-playbook scm_deploy.yml --tags "addresses"

# Skip the commit task
ansible-playbook scm_deploy.yml --skip-tags "commit"
```

Common tags used across roles:

- `bootstrap`: Bootstrap tasks
- `deploy`: Deployment tasks
- `addresses`: Address configuration
- `services`: Service configuration
- `security_rules`: Security rule configuration
- `commit`: Commit configuration changes
- `backup`: Configuration backup tasks
- `validation`: Configuration validation tasks

## Best Practices

1. **Define Variables in Vault Files**:
   Store sensitive variables like client credentials in encrypted files using Ansible Vault.

2. **Use Structured Variable Files**:
   Keep configuration data in separate YAML files organized by object type:

   ```
   group_vars/
   ├── all/
   │   ├── vault.yml          # Encrypted credentials
   │   ├── addresses.yml      # Address objects
   │   ├── services.yml       # Service objects
   │   └── security_rules.yml # Security rules
   ```

3. **Validate Before Deployment**:
   Use the `validate_only` variable to check configurations without making changes.

4. **Tag Your Tasks**:
   Add tags to your playbooks for more selective execution:

   ```yaml
   - name: Deploy SCM Configuration
     hosts: localhost
     roles:
       - role: cdot65.scm.deploy_config
         vars:
           # Role variables...
         tags:
           - deploy
           - config
   ```

5. **Include Dependencies**:
   Ensure required collections are declared in your playbook:

   ```yaml
   - name: Deploy SCM Configuration
     hosts: localhost
     collections:
       - cdot65.scm
     roles:
       - role: deploy_config
         # Role variables...
   ```