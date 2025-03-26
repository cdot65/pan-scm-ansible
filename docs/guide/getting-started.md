# Getting Started with SCM Ansible Collection

This guide provides a comprehensive introduction to using the Palo Alto Networks Strata Cloud
Manager (SCM) Ansible Collection. It walks through the initial setup, authentication, and basic
operations.

## Prerequisites

Before you begin, ensure you have:

1. **Ansible** installed (version 2.13 or higher)
2. **Python** installed (version 3.8 or higher)
3. **SCM Access** with appropriate permissions
4. **API Credentials** for SCM

## Installation

1. Install the SCM Python SDK:

```bash
pip install pan-scm-sdk
```

2. Install the Ansible Collection:

```bash
ansible-galaxy collection install cdot65.scm
```

## Authentication Setup

There are several ways to authenticate with SCM:

### Environment Variables (Recommended)

Set up environment variables for authentication:

```bash
export PAN_SCM_USERNAME="your-username"
export PAN_SCM_PASSWORD="your-password"
export PAN_SCM_TENANT="your-tenant-id"
```

### Ansible Vault

Store credentials securely using Ansible Vault:

1. Create a vault file:

```bash
ansible-vault create scm_credentials.yml
```

2. Add your credentials:

```yaml
---
scm_username: "your-username"
scm_password: "your-password"
scm_tenant: "your-tenant-id"
```

3. Reference in your playbook:

```yaml
- name: SCM Operations
  hosts: localhost
  vars_files:
    - scm_credentials.yml
  tasks:
    - name: Create an address object
      cdot65.scm.address:
        name: "web-server"
        folder: "SharedFolder"
        ip_netmask: "192.168.1.1/32"
        username: "{{ scm_username }}"
        password: "{{ scm_password }}"
        tenant: "{{ scm_tenant }}"
```

## Creating Your First Playbook

Let's create a simple playbook to verify connectivity and create some basic objects:

```yaml
---
# scm_basics.yml
- name: SCM Basics
  hosts: localhost
  connection: local
  gather_facts: false
  
  tasks:
    - name: Create a tag
      cdot65.scm.tag:
        name: "web-servers"
        color: "color13"  # Red
        folder: "SharedFolder"
      register: tag_result
      
    - name: Show tag result
      debug:
        var: tag_result
        
    - name: Create an address object
      cdot65.scm.address:
        name: "web-server-1"
        folder: "SharedFolder"
        description: "Web Server 1"
        ip_netmask: "10.1.1.1/32"
        tags:
          - "web-servers"
      register: address_result
      
    - name: Show address result
      debug:
        var: address_result
        
    - name: Commit changes
      cdot65.scm.commit:
        description: "Initial configuration"
      register: commit_result
      
    - name: Show commit result
      debug:
        var: commit_result
```

Run the playbook:

```bash
ansible-playbook scm_basics.yml
```

## Understanding the Workflow

When working with SCM Ansible Collection, you typically follow this workflow:

1. **Create/Modify Objects**: Use modules to create or modify SCM objects
2. **Commit Changes**: Use the `commit` module to commit changes
3. **Push Configuration**: Use the `push_config` module to push changes to devices
4. **Monitor Jobs**: Use the `job_info` module to monitor job status

### Example Workflow Playbook

```yaml
---
# scm_workflow.yml
- name: SCM Complete Workflow
  hosts: localhost
  connection: local
  gather_facts: false
  
  tasks:
    # 1. Create objects
    - name: Create security zone
      cdot65.scm.security_zone:
        name: "Web-Zone"
        folder: "SharedFolder"
        description: "Zone for web servers"
      
    - name: Create address objects
      cdot65.scm.address:
        name: "{{ item.name }}"
        folder: "SharedFolder"
        description: "{{ item.desc }}"
        ip_netmask: "{{ item.ip }}"
      loop:
        - { name: "web-server-1", desc: "Web Server 1", ip: "10.1.1.1/32" }
        - { name: "web-server-2", desc: "Web Server 2", ip: "10.1.1.2/32" }
    
    - name: Create security rule
      cdot65.scm.security_rule:
        name: "Allow-Web-Traffic"
        folder: "SharedFolder"
        description: "Allow web traffic"
        source_zones: ["untrust"]
        destination_zones: ["Web-Zone"]
        source_addresses: ["any"]
        destination_addresses: ["web-server-1", "web-server-2"]
        applications: ["web-browsing", "ssl"]
        action: "allow"
    
    # 2. Commit changes
    - name: Commit configuration changes
      cdot65.scm.commit:
        description: "Web server configuration"
      register: commit_result
    
    # 3. Push configuration to devices
    - name: Push configuration to firewalls
      cdot65.scm.push_config:
        device_groups:
          - "Firewall-Group-1"
      register: push_result
    
    # 4. Monitor job status
    - name: Check job status
      cdot65.scm.job_info:
        job_id: "{{ push_result.job_id }}"
      register: job_status
      until: job_status.status == "COMPLETED"
      retries: 30
      delay: 10
      
    - name: Show final job status
      debug:
        var: job_status
```

## Using Roles

The collection includes pre-built roles for common tasks:

```yaml
---
# scm_with_roles.yml
- name: SCM with Roles
  hosts: localhost
  connection: local
  gather_facts: false
  
  roles:
    - role: cdot65.scm.bootstrap
      vars:
        bootstrap_folder: "Production"
        bootstrap_tags:
          - name: "web-servers"
            color: "color13"
          - name: "db-servers"
            color: "color7"
        bootstrap_address_objects:
          - name: "web-server-1"
            description: "Production web server"
            ip_netmask: "10.1.1.10/32"
            tags:
              - "web-servers"
```

## Next Steps

Now that you understand the basics, you can:

1. Explore the [Module Reference](../collection/modules/index.md) for all available modules
2. Learn about [Authentication](authentication.md) options in detail
3. See [Playbook Examples](playbook-examples.md) for common use cases
4. Understand [Using Roles](using-roles.md) for simplified management
