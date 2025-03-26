# Plugins Overview

This collection includes several Ansible plugins that extend functionality beyond what the modules
provide. These plugins enable you to integrate SCM data into your automation workflows in various
ways.

### Key Features

- Discover devices managed by SCM
- Group devices by location, role, or custom attributes
- Filter devices based on tags, status, or other attributes
- Automatically populate variables with SCM-sourced data

<div class="termynal" data-termynal data-ty-typeDelay="40" data-ty-lineDelay="700">
    <span data-ty="input">cat inventory.yml</span>
    <span data-ty>---
plugin: cdot65.scm.inventory
client_id: "{{ lookup('env', 'SCM_CLIENT_ID') }}"
client_secret: "{{ lookup('env', 'SCM_CLIENT_SECRET') }}"
tsg_id: "{{ lookup('env', 'SCM_TSG_ID') }}"
groups:
  firewall: "type == 'firewall'"
  prisma_access: "type == 'prisma_access'"</span>
    <span data-ty="input">ansible-inventory -i inventory.yml --list</span>
    <span data-ty="progress" data-ty-progressChar="·"></span>
    <span data-ty>{
  "_meta": {
    "hostvars": {
      "pa-fw-01": {
        "ansible_host": "10.1.1.1",
        "device_type": "firewall",
        "location": "Texas"
      }
    }
  },
  "all": {
    "children": ["firewall", "prisma_access", "ungrouped"]
  },
  "firewall": {
    "hosts": ["pa-fw-01"]
  }
}</span>
</div>

### Key Features

- Query address, service, and tag objects
- Look up security rules and policies
- Access and filter device information
- Retrieve status information from SCM

<div class="termynal" data-termynal data-ty-typeDelay="40" data-ty-lineDelay="700">
    <span data-ty="input">cat lookup-example.yml</span>
    <span data-ty>---
- name: Lookup examples
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  tasks:
    - name: Get address object information
      debug:
        msg: "{{ lookup('cdot65.scm.address', 'web-server', folder='Texas') }}"

```
- name: Get all service objects in a folder
  debug:
    msg: "{{ lookup('cdot65.scm.service', folder='Texas') }}"</span>
```

</div>

## Using Plugins Together

The real power of these plugins comes from using them together:

<div class="termynal" data-termynal data-ty-typeDelay="40" data-ty-lineDelay="700">
    <span data-ty="input">cat integrated-example.yml</span>
    <span data-ty>---
- name: Configure security rules for all devices
  hosts: "{{ query('cdot65.scm.inventory', 'type=firewall') }}"
  vars:
    address_objects: "{{ lookup('cdot65.scm.address', folder='Texas') }}"
    web_servers: "{{ address_objects | selectattr('name', 'match', 'web') | list }}"
  tasks:
    - name: Configure security rule for web servers
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Allow Web Traffic"
        source_zone: ["untrust"]
        destination_zone: ["trust"]
        source_address: ["any"]
        destination_address: "{{ web_servers | map(attribute='name') | list }}"
        application: ["web-browsing", "ssl"]
        service: ["application-default"]
        action: "allow"
        folder: "Texas"
        state: "present"</span>
</div>

## Plugin Development

If you're interested in contributing plugins to this collection, see the
[contributing guidelines](../../development/contributing.md) for development instructions and best
practices.
