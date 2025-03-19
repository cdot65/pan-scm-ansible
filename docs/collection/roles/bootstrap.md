# Bootstrap Role

The bootstrap role provides a streamlined way to initialize a new Strata Cloud Manager (SCM) environment with basic configurations. It sets up foundational objects such as folders, address objects, service objects, and tags that form the basis for more complex configurations.

## Role Overview

The bootstrap role performs the following tasks:

1. Validate input parameters
2. Create organizational folders
3. Configure common address objects
4. Set up standard service objects
5. Create tags for resource categorization
6. Configure basic security zones
7. Set up initial security rules
8. Perform a commit operation

This role is typically run once when setting up a new SCM environment or tenant.

## Role Variables

### Required Variables

| Variable | Description | Type | Required |
|----------|-------------|------|----------|
| `scm_client_id` | OAuth2 client ID | String | Yes |
| `scm_client_secret` | OAuth2 client secret | String | Yes |
| `scm_tsg_id` | Tenant Service Group ID | String | Yes |
| `bootstrap_folder` | Main folder to create | String | Yes |

### Configuration Variables

| Variable | Description | Type | Default |
|----------|-------------|------|---------|
| `bootstrap_tags` | List of tags to create | List | `[]` |
| `bootstrap_address_objects` | List of address objects to create | List | `[]` |
| `bootstrap_service_objects` | List of service objects to create | List | `[]` |
| `bootstrap_security_zones` | List of security zones to create | List | `[]` |
| `bootstrap_security_rules` | Security rules to create | List | `[]` |
| `bootstrap_commit` | Whether to commit changes | Boolean | `true` |
| `bootstrap_commit_description` | Description for the commit | String | `"Initial bootstrap configuration"` |

## Example Playbook

```yaml
---
- name: Bootstrap SCM Environment
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml  # Contains encrypted credentials
  
  roles:
    - role: cdot65.scm.bootstrap
      vars:
        scm_client_id: "{{ client_id }}"
        scm_client_secret: "{{ client_secret }}"
        scm_tsg_id: "{{ tsg_id }}"
        bootstrap_folder: "Production"
        bootstrap_tags:
          - name: "web-servers"
            color: "color13"  # Red
          - name: "db-servers"
            color: "color7"   # Blue
        bootstrap_address_objects:
          - name: "web-server-1"
            description: "Production web server"
            ip_netmask: "10.1.1.10/32"
            tags:
              - "web-servers"
          - name: "db-server-1"
            description: "Production database server"
            ip_netmask: "10.1.2.10/32"
            tags:
              - "db-servers"
        bootstrap_security_zones:
          - name: "Web-Zone"
            description: "Zone for web servers"
          - name: "DB-Zone"
            description: "Zone for database servers"
```

## Customizing the Bootstrap Configuration

You can customize the bootstrap process by modifying the variables. There are multiple ways to do this:

### 1. Using Variable Files

Create a file with your custom variables:

```yaml
# custom_bootstrap_vars.yml
bootstrap_folder: "Texas"
bootstrap_address_objects:
  - name: "texas-server"
    description: "Texas regional server"
    ip_netmask: "192.168.1.1/32"
```

Then include it in your playbook:

```yaml
- name: Custom Bootstrap
  hosts: localhost
  vars_files:
    - vault.yaml
    - custom_bootstrap_vars.yml
  roles:
    - role: cdot65.scm.bootstrap
      vars:
        scm_client_id: "{{ client_id }}"
        scm_client_secret: "{{ client_secret }}"
        scm_tsg_id: "{{ tsg_id }}"
```

### 2. Using Role Variables

Define the variables directly in the role section:

```yaml
- name: Bootstrap with Inline Variables
  hosts: localhost
  vars_files:
    - vault.yaml
  roles:
    - role: cdot65.scm.bootstrap
      vars:
        scm_client_id: "{{ client_id }}"
        scm_client_secret: "{{ client_secret }}"
        scm_tsg_id: "{{ tsg_id }}"
        bootstrap_folder: "Development"
        bootstrap_tags:
          - name: "dev-servers"
            color: "color5"
        bootstrap_commit: false  # Skip commit for testing
```

## Role Tags

The bootstrap role provides the following tags to control which tasks are executed:

- `bootstrap`: All bootstrap tasks
- `folders`: Folder creation tasks
- `addresses`: Address object creation tasks
- `services`: Service object creation tasks
- `tags`: Tag creation tasks
- `zones`: Security zone creation tasks
- `rules`: Security rule creation tasks
- `commit`: Configuration commit tasks

Example of using tags:

```bash
# Only create folders and addresses
ansible-playbook scm_bootstrap.yml --tags "folders,addresses"

# Skip the commit task
ansible-playbook scm_bootstrap.yml --skip-tags "commit"
```

## Error Handling

The role includes comprehensive error handling with informative error messages. If any step fails, the role will stop and report the specific error.

Typical issues include:
- Authentication failures
- Permission issues
- Duplicate object names
- Invalid configuration values

## Dependencies

This role depends on the following collection modules:
- `cdot65.scm.tag`
- `cdot65.scm.address`
- `cdot65.scm.service`
- `cdot65.scm.security_zone`
- `cdot65.scm.security_rule`
- `cdot65.scm.commit`

## Best Practices

1. **Review Default Objects**: Before running the role, review the default objects to ensure they match your requirements
2. **Run in Check Mode First**: Use Ansible's check mode to preview changes
3. **Start with a Minimal Configuration**: Begin with a minimal set of objects and add more as needed
4. **Secure Credentials**: Use Ansible Vault to secure your SCM credentials
5. **Version Control**: Store your bootstrap configuration in version control
6. **Use Tags**: Use tags to run specific parts of the role during iterative development
