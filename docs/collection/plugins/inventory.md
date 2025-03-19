# Inventory Plugin

The SCM inventory plugin allows you to dynamically build your Ansible inventory from Palo Alto Networks Strata Cloud Manager.

## Synopsis

This plugin retrieves device information from SCM and makes it available as inventory hosts in Ansible. It can be used to automate tasks across all your managed firewalls without manually maintaining an inventory file.

## Requirements

- `pan-scm-sdk` Python package
- Authentication credentials for Strata Cloud Manager

## Configuration

### Enabling the Plugin

To enable the plugin, add it to your `ansible.cfg` file:

```ini
[inventory]
enable_plugins = cdot65.scm.inventory
```

### Plugin Configuration

Create a file named `scm_inventory.yml` (or any other name with `.yml` extension):

```yaml
# SCM Inventory Plugin Configuration
plugin: cdot65.scm.inventory
# Authentication (can use environment variables instead)
# username: "your-username"
# password: "your-password"
# tenant: "your-tenant-id"
# Configuration options
device_groups:
  - All Devices
keyed_groups:
  - prefix: version
    key: version
  - prefix: model
    key: model
  - prefix: location
    key: location
hostnames:
  - hostname
  - serial
  - id
compose:
  ansible_host: managementIp
filters:
  - "state == 'CONNECTED'"
```

## Plugin Options

| Option | Description | Default | Required |
|--------|-------------|---------|----------|
| `username` | SCM username | Environment variable | No |
| `password` | SCM password | Environment variable | No |
| `tenant` | SCM tenant ID | Environment variable | No |
| `device_groups` | List of device groups to include | All devices | No |
| `hostnames` | List of device attributes to use as hostnames (in order of preference) | `['hostname']` | No |
| `keyed_groups` | List of groups to create based on device attributes | `[]` | No |
| `compose` | Create custom host variables | `{}` | No |
| `filters` | Filter devices based on attributes | `[]` | No |
| `cache` | Enable inventory caching | `false` | No |
| `cache_plugin` | Cache plugin to use | `jsonfile` | No |
| `cache_timeout` | Cache timeout in seconds | `3600` | No |
| `cache_connection` | Path to cache file | `~/.ansible/tmp/scm_inventory_cache` | No |

## Usage Examples

### Basic Usage

Run a playbook using the dynamic inventory:

```bash
ansible-playbook -i scm_inventory.yml your_playbook.yml
```

### List Hosts

List all hosts from the inventory:

```bash
ansible-inventory -i scm_inventory.yml --list
```

### Filter by Group

Target specific device models:

```bash
ansible -i scm_inventory.yml 'model_PA_VM' -m ping
```

### Custom Inventory Variables

Access custom inventory variables in your playbook:

```yaml
- name: Use SCM device information
  hosts: all
  gather_facts: false
  tasks:
    - name: Display device information
      debug:
        msg: >
          Device: {{ inventory_hostname }}
          Model: {{ model }}
          Version: {{ version }}
          Management IP: {{ ansible_host }}
```

## Advanced Configuration

### Multiple Inventory Sources

You can combine the SCM inventory with other inventory sources:

```yaml
# scm_and_custom_inventory.yml
plugin: cdot65.scm.inventory
device_groups:
  - Production Firewalls
filters:
  - "state == 'CONNECTED'"
---
plugin: yaml
path: ./custom_inventory.yml
```

### Complex Filtering

Filter devices based on multiple criteria:

```yaml
plugin: cdot65.scm.inventory
filters:
  - "state == 'CONNECTED'"
  - "model.startswith('PA-')"
  - "'New York' in location"
```

### Custom Group Creation

Create custom groups based on device attributes:

```yaml
plugin: cdot65.scm.inventory
keyed_groups:
  - prefix: version
    key: version
  - prefix: model
    key: model
  - key: location
    prefix: ''
    separator: ''
```

## Caching

Enable caching to improve performance:

```yaml
plugin: cdot65.scm.inventory
cache: true
cache_plugin: jsonfile
cache_timeout: 7200  # 2 hours
cache_connection: ~/.ansible/tmp/scm_inventory_cache
```

## Troubleshooting

If you encounter issues:

1. Run with increased verbosity:
   ```bash
   ansible-inventory -i scm_inventory.yml --list -vvv
   ```

2. Check authentication:
   ```bash
   export PAN_SCM_USERNAME="your-username"
   export PAN_SCM_PASSWORD="your-password"
   export PAN_SCM_TENANT="your-tenant-id"
   ```

3. Verify network connectivity to SCM API

4. Check filters to ensure they're not excluding all devices

5. Clear the cache if using caching:
   ```bash
   rm -f ~/.ansible/tmp/scm_inventory_cache
   ```
