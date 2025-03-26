# Using Modules

This guide explains how to effectively use the modules in the Palo Alto Networks SCM Ansible
Collection.

## Module Structure

All modules in the collection follow a consistent structure:

1. **Authentication Parameters** - For connecting to SCM
2. **Object Identification** - Name and folder location
3. **Configuration Parameters** - Specific to each object type
4. **State Management** - For creating or removing objects

## Common Parameters

These parameters are available in most modules:

| Parameter  | Description          | Required | Default              |
| ---------- | -------------------- | -------- | -------------------- |
| `username` | SCM username         | No       | Environment variable |
| `password` | SCM password         | No       | Environment variable |
| `tenant`   | SCM tenant ID        | No       | Environment variable |
| `folder`   | SCM folder path      | Yes      |                      |
| `name`     | Object name          | Yes      |                      |
| `state`    | State of the object  | No       | `present`            |
| `debug`    | Enable debug logging | No       | `false`              |

## Module Categories

The collection includes several categories of modules:

### Object Management Modules

Manage configuration objects like addresses, services, and tags:

```yaml
- name: Create an address object
  cdot65.scm.address:
    name: "web-server"
    folder: "SharedFolder"
    ip_netmask: "10.1.1.1/32"
```

### Security Modules

Manage security-related configurations:

```yaml
- name: Create a security rule
  cdot65.scm.security_rule:
    name: "Allow-Web"
    folder: "SharedFolder"
    source_zones: [ "untrust" ]
    destination_zones: [ "trust" ]
    applications: [ "web-browsing", "ssl" ]
    action: "allow"
```

### Network Modules

Manage network configurations:

```yaml
- name: Create a security zone
  cdot65.scm.security_zone:
    name: "DMZ"
    folder: "SharedFolder"
    description: "DMZ Zone"
```

### Operational Modules

Manage operational aspects of SCM:

```yaml
- name: Commit changes
  cdot65.scm.commit:
    description: "Weekly security policy update"
```

## Object Creation and Modification

When creating or modifying objects, the modules automatically handle idempotency:

```yaml
- name: Ensure web server address exists
  cdot65.scm.address:
    name: "web-server"
    folder: "SharedFolder"
    ip_netmask: "10.1.1.1/32"
    description: "Primary web server"
```

Running this task multiple times will only make changes if necessary.

## Object Deletion

To delete objects, set the `state` parameter to `absent`:

```yaml
- name: Remove old address
  cdot65.scm.address:
    name: "old-server"
    folder: "SharedFolder"
    state: absent
```

## Working with Lists and Groups

Many modules support list parameters and group objects:

```yaml
- name: Create an address group
  cdot65.scm.address_group:
    name: "web-servers"
    folder: "SharedFolder"
    description: "Web server group"
    static_members:
      - "web-server-1"
      - "web-server-2"
```

## Working with Tags

Tags can be applied to most objects:

```yaml
- name: Create address with tags
  cdot65.scm.address:
    name: "db-server"
    folder: "SharedFolder"
    ip_netmask: "10.2.1.1/32"
    tags:
      - "database"
      - "production"
```

## Check Mode

All modules support Ansible's check mode:

```bash
ansible-playbook your_playbook.yml --check
```

This will report what changes would be made without actually making them.

## Using Filters and Loops

Use Ansible filters and loops for more powerful automations:

```yaml
- name: Create multiple address objects
  cdot65.scm.address:
    name: "{{ item.name }}"
    folder: "SharedFolder"
    description: "{{ item.description }}"
    ip_netmask: "{{ item.ip }}"
  loop: "{{ server_list }}"
```

## Handling Module Returns

Modules return useful information that you can capture and use:

```yaml
- name: Create address object
  cdot65.scm.address:
    name: "app-server"
    folder: "SharedFolder"
    ip_netmask: "10.3.1.1/32"
  register: address_result

- name: Use the registered result
  debug:
    msg: "Created address with ID: {{ address_result.scm_object.id }}"
```

## Error Handling

Handle potential errors in your playbooks:

```yaml
- name: Try to create an object
  block:
    - name: Create security rule
      cdot65.scm.security_rule:
        name: "Allow-App-Traffic"
        folder: "SharedFolder"
        source_zones: [ "untrust" ]
        destination_zones: [ "trust" ]
        destination_addresses: [ "app-server" ]
        applications: [ "web-browsing" ]
        action: "allow"
  rescue:
    - name: Handle the error
      debug:
        msg: "Failed to create security rule, see error above"
```

## Module Documentation

Each module has detailed documentation available:

- Use `ansible-doc` from the command line:

  ```bash
  ansible-doc cdot65.scm.address
  ```

- Check the [Module Reference](../collection/modules/index.md) in this documentation

## Performance Considerations

For better performance when making multiple changes:

- Group related changes together
- Perform a single commit operation at the end
- Use roles for common operations

```yaml
- name: Commit all changes at once
  cdot65.scm.commit:
    description: "Batch update of multiple objects"
  when: any_changes_made
```

## Next Steps

- Learn about [Playbook Examples](playbook-examples.md)
- Explore [Using Roles](using-roles.md) for simplified management
- Understand [Advanced Topics](advanced-topics.md) for complex deployments
