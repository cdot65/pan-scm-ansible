# Getting Started

This guide will help you get started with the Palo Alto Networks SCM Ansible Collection by walking through basic authentication setup and your first playbook.

## Authentication

To authenticate with Strata Cloud Manager, you'll need to provide your SCM credentials. The recommended approach is to use environment variables for security:

```bash
export PAN_SCM_USERNAME="your-username"
export PAN_SCM_PASSWORD="your-password"
export PAN_SCM_TENANT="your-tenant-id"
```

Alternatively, you can store credentials in an Ansible vault file:

```yaml
# credentials.yml
---
scm_username: "your-username"
scm_password: "your-password"
scm_tenant: "your-tenant-id"
```

Then encrypt the file:

```bash
ansible-vault encrypt credentials.yml
```

## Your First Playbook

Here's a simple playbook that creates an address object in SCM:

```yaml
---
- name: Create SCM Address Objects
  hosts: localhost
  connection: local
  gather_facts: false
  vars_files:
    - credentials.yml  # If using vault for credentials
  
  tasks:
    - name: Create web server address
      cdot65.scm.address:
        name: "web-server"
        folder: "SharedFolder"
        description: "Web server address"
        ip_netmask: "10.1.1.10/32"
        # Use environment variables or specify here:
        # username: "{{ scm_username }}"
        # password: "{{ scm_password }}"
        # tenant: "{{ scm_tenant }}"
```

Save this as `create_address.yml` and run it:

```bash
ansible-playbook create_address.yml
```

If using vault:

```bash
ansible-playbook create_address.yml --ask-vault-pass
```

## Using Tags

Tags in SCM are used to organize and categorize objects. Here's an example of creating a tag and then applying it to an address object:

```yaml
---
- name: Create and Apply Tags
  hosts: localhost
  connection: local
  gather_facts: false
  
  tasks:
    - name: Create a web-servers tag
      cdot65.scm.tag:
        name: "web-servers"
        color: "color13"  # Red
        folder: "SharedFolder"
    
    - name: Create web server address with tag
      cdot65.scm.address:
        name: "web-server-prod"
        folder: "SharedFolder"
        description: "Production web server"
        ip_netmask: "10.1.1.11/32"
        tags:
          - "web-servers"
```

## Working with Security Rules

Security rules are a core component of network security. Here's an example that creates a basic security rule:

```yaml
---
- name: Configure Security Rules
  hosts: localhost
  connection: local
  gather_facts: false
  
  tasks:
    - name: Allow web traffic
      cdot65.scm.security_rule:
        name: "Allow-Web-Traffic"
        folder: "SharedFolder"
        description: "Allow HTTP/HTTPS to web servers"
        source_zones: ["untrust"]
        destination_zones: ["trust"]
        source_addresses: ["any"]
        destination_addresses: ["web-server-prod"]
        applications: ["web-browsing", "ssl"]
        services: ["application-default"]
        action: "allow"
        log_setting: "default"
```

## Next Steps

Now that you have the basics, explore the following resources:

- [Module Reference](../collection/modules/index.md): Documentation for all available modules
- [Playbook Examples](../guide/playbook-examples.md): More complex playbooks for common tasks
- [Roles Documentation](../collection/roles/index.md): Pre-built roles for SCM management
