# Plugins Overview

This collection includes several Ansible plugins that extend functionality beyond what the modules provide. These plugins enable you to integrate SCM data into your automation workflows in various ways.

## Inventory Plugin

The inventory plugin allows you to dynamically generate Ansible inventory from SCM objects. This is particularly useful for automatically discovering and managing devices in your SCM environment.

[Learn more about the Inventory Plugin →](inventory.md)

### Key Features

- Discover devices managed by SCM
- Group devices by location, role, or custom attributes
- Filter devices based on tags, status, or other attributes
- Automatically populate variables with SCM-sourced data

### Example Configuration

```yaml
# inventory.yml
plugin: cdot65.scm.inventory
client_id: "{{ lookup('env', 'SCM_CLIENT_ID') }}"
client_secret: "{{ lookup('env', 'SCM_CLIENT_SECRET') }}"
tsg_id: "{{ lookup('env', 'SCM_TSG_ID') }}"
groups:
  firewall: "type == 'firewall'"
  prisma_access: "type == 'prisma_access'"
```

## Lookup Plugin

The lookup plugin allows you to query SCM for specific information during playbook execution. This enables you to make dynamic decisions based on current SCM state.

[Learn more about the Lookup Plugin →](lookup.md)

### Key Features

- Query address, service, and tag objects
- Look up security rules and policies
- Access and filter device information
- Retrieve status information from SCM

### Example Usage

```yaml
- name: Get address object information
  debug:
    msg: "{{ lookup('cdot65.scm.address', 'web-server', folder='Texas') }}"

- name: Get all service objects in a folder
  debug:
    msg: "{{ lookup('cdot65.scm.service', folder='Texas') }}"

- name: Get security rule IDs that reference an address
  debug:
    msg: "{{ lookup('cdot65.scm.reference', type='address', name='web-server', folder='Texas') }}"
```

## Filter Plugin

Filter plugins provide custom filters to transform and manipulate SCM data in your templates and playbooks.

### Available Filters

| Filter | Description |
|--------|-------------|
| `scm_format_address` | Format SCM address objects for display |
| `scm_format_service` | Format SCM service objects for display |
| `scm_extract_property` | Extract a specific property from SCM objects |
| `scm_filter_objects` | Filter a list of SCM objects by property |

### Example Usage

```yaml
- name: Format addresses for display
  debug:
    msg: "{{ addresses | scm_format_address }}"

- name: Filter objects by property
  debug:
    msg: "{{ services | scm_filter_objects('protocol.tcp') }}"
```

## Using Plugins Together

The real power of these plugins comes from using them together. For example:

```yaml
- name: Configure security rules for all devices
  hosts: "{{ lookup('cdot65.scm.inventory', 'type=firewall') }}"
  vars:
    address_objects: "{{ lookup('cdot65.scm.address', folder='Texas') }}"
    web_servers: "{{ address_objects | scm_filter_objects('name', 'web') }}"
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
        state: "present"
```

## Plugin Development

If you're interested in contributing plugins to this collection, see the [contributing guidelines](../../development/contributing.md) for development instructions and best practices.