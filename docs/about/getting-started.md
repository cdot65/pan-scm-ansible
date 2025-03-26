# Getting Started with pan-scm-ansible

Welcome to the `cdot65.scm` Ansible Collection! This guide will walk you through the initial setup and basic usage of the collection to automate Palo Alto Networks Strata Cloud Manager configurations.

## Installation

**Requirements**:

- Python 3.11 or higher
- Ansible Core 2.17 or higher
- `pan-scm-sdk` version 0.3.22 or higher

<div class="termy">

```bash
$ pip install pan-scm-sdk
---> 100%
Successfully installed pan-scm-sdk-0.3.22

$ ansible-galaxy collection install cdot65.scm
---> 100%
Process completed successfully
```

</div>

## Authentication

Before using the collection, you need to set up authentication with Strata Cloud Manager using OAuth2 client credentials. The recommended approach is to store credentials securely using Ansible Vault:

1. **Create a vault-encrypted variables file**:

<div class="termy">

```bash
$ ansible-vault create vault.yaml
New Vault password: 
Confirm New Vault password: 
```

</div>

2. **Add your credentials to the file**:

<div class="termy">

```yaml
# Contents of vault.yaml
client_id: "your-client-id"
client_secret: "your-client-secret"
tsg_id: "your-tenant-service-group-id"
```

</div>

3. **Reference the vault file in your playbook**:

<div class="termy">

```yaml
# Example playbook with authentication
---
- name: SCM Configuration Example
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"  # Optional, defaults to INFO
  tasks:
    - name: Create an address object
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "web-server"
        description: "Web server"
        ip_netmask: "10.1.1.10/32"
        folder: "Texas"
        state: "present"
```

</div>

## Basic Usage

The collection provides modules for managing various SCM configuration objects. Here are some common examples:

### Managing Address Objects

<div class="termy">

```yaml
# Example: Creating different types of address objects
---
- name: Manage Address Objects
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
  tasks:
    # IP/Netmask address
    - name: Create an IP address object
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "internal-network"
        description: "Internal network segment"
        ip_netmask: "192.168.1.0/24"
        folder: "Texas"
        tag: ["Network", "Internal"]
        state: "present"
    
    # FQDN address
    - name: Create an FQDN address object
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "example-server"
        description: "Example server FQDN"
        fqdn: "server.example.com"
        folder: "Texas"
        state: "present"
        
    # IP Range address
    - name: Create an IP Range address object
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "dhcp-range"
        description: "DHCP address range"
        ip_range: "192.168.1.100-192.168.1.200"
        folder: "Texas"
        state: "present"
```

</div>

### Managing Tags

<div class="termy">

```yaml
# Example: Creating and managing tags
---
- name: Manage Tags
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
  tasks:
    - name: Create tags with different colors
      cdot65.scm.tag:
        provider: "{{ provider }}"
        name: "{{ item.name }}"
        color: "{{ item.color }}"
        folder: "Texas"
        state: "present"
      loop:
        - { name: "Production", color: "red" }
        - { name: "Testing", color: "green" }
        - { name: "Development", color: "blue" }
    
    - name: Get tag information
      cdot65.scm.tag_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: tags_result
    
    - name: Display all tags
      debug:
        var: tags_result
```

</div>

### Managing Security Rules

<div class="termy">

```yaml
# Example: Creating security rules
---
- name: Configure Security Rules
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
  tasks:
    - name: Create a web access rule
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Allow-Web-Traffic"
        folder: "Texas"
        description: "Allow HTTP/HTTPS traffic to web servers"
        source_zone: ["untrust"]
        destination_zone: ["trust"]
        source_address: ["any"]
        destination_address: ["web-server"]
        application: ["web-browsing", "ssl"]
        service: ["application-default"]
        action: "allow"
        log_end: true
        state: "present"
```

</div>

## Using Info Modules

Info modules allow you to retrieve information about objects in SCM:

<div class="termy">

```yaml
# Example: Using info modules
---
- name: Retrieve SCM Information
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
  tasks:
    - name: Get all address objects
      cdot65.scm.address_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: addresses
    
    - name: Display all addresses
      debug:
        var: addresses
    
    - name: Get specific address object
      cdot65.scm.address_info:
        provider: "{{ provider }}"
        name: "web-server"
        folder: "Texas"
      register: specific_address
    
    - name: Display specific address
      debug:
        var: specific_address
```

</div>

## Error Handling

Always implement proper error handling in your playbooks:

<div class="termy">

```yaml
# Example: Error handling
---
- name: Error Handling Example
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
  tasks:
    - name: Attempt to create an address
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "example-server"
        description: "Example server"
        fqdn: "server.example.com"
        folder: "Texas"
        state: "present"
      register: address_result
      failed_when: false
    
    - name: Handle potential errors
      debug:
        msg: "Failed to create address: {{ address_result.msg }}"
      when: address_result.failed
    
    - name: Continue with successful creation
      debug:
        msg: "Successfully created address with ID: {{ address_result.address.id }}"
      when: not address_result.failed
```

</div>

## Using Check Mode

All modules support Ansible's check mode, allowing you to see what changes would be made without actually making them:

<div class="termy">

```bash
$ ansible-playbook --check my_playbook.yml
```

</div>

## Next Steps

- Explore the [Collection Documentation](../collection/index.md) for detailed information on all available modules, roles, and plugins
- Check out the [User Guide](../guide/using-modules.md) for more advanced usage examples
- Refer to the [Playbook Examples](../guide/playbook-examples.md) for complete playbook examples