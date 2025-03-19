# Lookup Plugins

Lookup plugins allow Ansible to access external data sources. The Palo Alto Networks SCM Ansible Collection provides several lookup plugins to retrieve data from SCM.

## Available Lookup Plugins

| Plugin Name | Description |
|-------------|-------------|
| `scm_address` | Lookup address objects |
| `scm_tag` | Lookup tag objects |
| `scm_service` | Lookup service objects |
| `scm_security_rule` | Lookup security rule objects |

## General Usage

Lookup plugins are used in Ansible playbooks to fetch data from external sources. Here's the general syntax:

```yaml
- name: Example of lookup plugin usage
  debug:
    msg: "{{ lookup('cdot65.scm.scm_address', name='web-server', folder='SharedFolder') }}"
```

## Authentication

All lookup plugins require authentication to SCM. You can provide credentials in three ways:

1. **Environment Variables** (Recommended):
   ```bash
   export PAN_SCM_USERNAME="your-username"
   export PAN_SCM_PASSWORD="your-password"
   export PAN_SCM_TENANT="your-tenant-id"
   ```

2. **Explicit Parameters**:
   ```yaml
   - name: Lookup with explicit credentials
     debug:
       msg: "{{ lookup('cdot65.scm.scm_address', 
                      name='web-server', 
                      folder='SharedFolder',
                      username='your-username',
                      password='your-password',
                      tenant='your-tenant-id') }}"
   ```

3. **Ansible Variables**:
   ```yaml
   - name: Lookup with ansible variables
     vars:
       ansible_scm_username: "your-username"
       ansible_scm_password: "your-password"
       ansible_scm_tenant: "your-tenant-id"
     debug:
       msg: "{{ lookup('cdot65.scm.scm_address', name='web-server', folder='SharedFolder') }}"
   ```

## scm_address Lookup

Retrieves address object information from SCM.

### Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `name` | Name of the address object | Yes | |
| `folder` | SCM folder path | Yes | |
| `username` | SCM username | No | Environment variable |
| `password` | SCM password | No | Environment variable |
| `tenant` | SCM tenant ID | No | Environment variable |

### Examples

```yaml
- name: Get IP address from an address object
  debug:
    msg: "The IP address is {{ lookup('cdot65.scm.scm_address', name='web-server', folder='SharedFolder').value }}"

- name: Check if address is in use
  when: lookup('cdot65.scm.scm_address', name='old-server', folder='SharedFolder').references|length > 0
  debug:
    msg: "This address is referenced by other objects and cannot be deleted"
```

## scm_tag Lookup

Retrieves tag information from SCM.

### Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `name` | Name of the tag | Yes | |
| `folder` | SCM folder path | Yes | |
| `username` | SCM username | No | Environment variable |
| `password` | SCM password | No | Environment variable |
| `tenant` | SCM tenant ID | No | Environment variable |

### Examples

```yaml
- name: Get tag color
  debug:
    msg: "The tag color is {{ lookup('cdot65.scm.scm_tag', name='web-servers', folder='SharedFolder').color }}"

- name: Get all objects with a specific tag
  debug:
    msg: "Objects with this tag: {{ lookup('cdot65.scm.scm_tag', name='production', folder='SharedFolder').references }}"
```

## scm_service Lookup

Retrieves service object information from SCM.

### Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `name` | Name of the service | Yes | |
| `folder` | SCM folder path | Yes | |
| `username` | SCM username | No | Environment variable |
| `password` | SCM password | No | Environment variable |
| `tenant` | SCM tenant ID | No | Environment variable |

### Examples

```yaml
- name: Get service ports
  debug:
    msg: "Service port: {{ lookup('cdot65.scm.scm_service', name='web-service', folder='SharedFolder').destination_port }}"

- name: Check service protocol
  debug:
    msg: "Service protocol: {{ lookup('cdot65.scm.scm_service', name='web-service', folder='SharedFolder').protocol }}"
```

## scm_security_rule Lookup

Retrieves security rule information from SCM.

### Parameters

| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `name` | Name of the security rule | Yes | |
| `folder` | SCM folder path | Yes | |
| `username` | SCM username | No | Environment variable |
| `password` | SCM password | No | Environment variable |
| `tenant` | SCM tenant ID | No | Environment variable |

### Examples

```yaml
- name: Get security rule action
  debug:
    msg: "Rule action: {{ lookup('cdot65.scm.scm_security_rule', name='Allow-Web', folder='SharedFolder').action }}"

- name: Check if rule is enabled
  debug:
    msg: "Rule is {{ 'disabled' if lookup('cdot65.scm.scm_security_rule', name='Allow-Web', folder='SharedFolder').disabled else 'enabled' }}"
```

## Advanced Usage

### Filtering Lists

You can use Jinja2 filters with lookup results:

```yaml
- name: Get all TCP services
  vars:
    all_services: "{{ lookup('cdot65.scm.scm_service', folder='SharedFolder', list=true) }}"
    tcp_services: "{{ all_services | selectattr('protocol', 'equalto', 'tcp') | list }}"
  debug:
    msg: "TCP services: {{ tcp_services | map(attribute='name') | list }}"
```

### Error Handling

Handle potential lookup errors:

```yaml
- name: Handle lookup errors gracefully
  block:
    - name: Try to lookup an object
      set_fact:
        address_info: "{{ lookup('cdot65.scm.scm_address', name='missing-server', folder='SharedFolder') }}"
  rescue:
    - name: Handle the error
      debug:
        msg: "Address object not found, creating it now"
    - name: Create the missing address
      cdot65.scm.address:
        name: "missing-server"
        folder: "SharedFolder"
        ip_netmask: "10.1.1.1/32"
```

### Using with Templates

Lookups can be used in template files:

```yaml
# template.j2
security_rule:
  name: {{ security_rule_name }}
  action: {{ lookup('cdot65.scm.scm_security_rule', name=security_rule_name, folder=folder).action }}
  source_zones: {{ lookup('cdot65.scm.scm_security_rule', name=security_rule_name, folder=folder).source_zones | to_yaml }}
```

```yaml
# playbook.yml
- name: Use lookup in a template
  template:
    src: template.j2
    dest: /tmp/rule_info.yml
  vars:
    security_rule_name: "Allow-Web"
    folder: "SharedFolder"
```
