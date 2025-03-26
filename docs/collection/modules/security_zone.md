# Security Zone Configuration Object

## 1. Overview

The Security Zone module allows you to manage security zone objects within Strata Cloud Manager
(SCM). Security zones are logical boundaries that segment the network and provide security policy
enforcement points. By defining zones, you can create security rules that control traffic between
different network segments.

## 2. Core Methods

| Method     | Description                 | Parameters               | Return Type     |
| ---------- | --------------------------- | ------------------------ | --------------- |
| `create()` | Creates a new security zone | `data: Dict[str, Any]`   | `ResponseModel` |
| `get()`    | Retrieves zone by name      | `name: str, folder: str` | `ResponseModel` |
| `update()` | Updates an existing zone    | `zone: Model`            | `ResponseModel` |
| `delete()` | Deletes a security zone     | `id: str`                | `None`          |

## 3. Model Attributes

| Attribute          | Type      | Required | Description                                  |
| ------------------ | --------- | -------- | -------------------------------------------- |
| `name`             | str       | Yes      | The name of the security zone                |
| `description`      | str       | No       | Description of the security zone             |
| `tag`              | List[str] | No       | List of tags associated with the zone        |
| `user_id_mappings` | Dict      | No       | User ID mapping settings                     |
| `log_setting`      | str       | No       | Log forwarding profile                       |
| `enable_user_id`   | bool      | No       | Enable User-ID for this zone                 |
| `exclude_ip`       | List[str] | No       | List of IP addresses to exclude from User-ID |
| `include_ip`       | List[str] | No       | List of IP addresses to include for User-ID  |
| `folder`           | str       | No\*     | The folder in which the resource is defined  |
| `snippet`          | str       | No\*     | The snippet in which the resource is defined |
| `device`           | str       | No\*     | The device in which the resource is defined  |

\* Exactly one of `folder`, `snippet`, or `device` must be provided.

## 4. Basic Configuration



```yaml
- name: Create a security zone
  cdot65.scm.security_zone:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "trust"
    description: "Internal trusted zone"
    folder: "Texas"
    state: "present"
```


## 5. Usage Examples

### Creating Basic Security Zones



```yaml
- name: Create standard security zones
  cdot65.scm.security_zone:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "{{ item.name }}"
    description: "{{ item.description }}"
    folder: "Texas"
    state: "present"
  loop:
    - { name: "trust", description: "Internal trusted zone" }
    - { name: "untrust", description: "External untrusted zone" }
    - { name: "dmz", description: "Demilitarized zone" }
```


### Creating Zone with User-ID Features



```yaml
- name: Create security zone with User-ID
  cdot65.scm.security_zone:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "internal"
    description: "Internal zone with User-ID"
    enable_user_id: true
    include_ip:
      - "10.0.0.0/8"
    exclude_ip:
      - "10.1.1.0/24"  # Server subnet without users
    folder: "Texas"
    state: "present"
```


### Updating a Security Zone



```yaml
- name: Update security zone settings
  cdot65.scm.security_zone:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "trust"
    description: "Updated trusted zone"
    log_setting: "detailed-logging"
    tag:
      - "internal"
    folder: "Texas"
    state: "present"
```


### Deleting a Security Zone



```yaml
- name: Delete a security zone
  cdot65.scm.security_zone:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "deprecated-zone"
    folder: "Texas"
    state: "absent"
```


## 6. Error Handling



```yaml
- name: Create security zone with error handling
  block:
    - name: Attempt to create security zone
      cdot65.scm.security_zone:
        provider: "{{ provider }}"
        name: "trust"
        description: "Internal trusted zone"
        log_setting: "non-existent-profile"  # This profile doesn't exist
        folder: "Texas"
        state: "present"
  rescue:
    - name: Handle error
      debug:
        msg: "Failed to create security zone. Check if all referenced objects exist."
```


## 7. Best Practices

1. **Zone Naming and Design**

   - Use descriptive names for zones that reflect their security purpose
   - Follow a consistent naming convention across all zones
   - Include the purpose of the zone in the description field
   - Design zones based on security requirements, not just network topology

2. **Zone Structure**

   - Create a clear separation between trusted (internal) and untrusted (external) zones
   - Use a DMZ for publicly accessible resources
   - Segment internal networks into multiple zones based on security requirements
   - Consider creating dedicated zones for sensitive systems or regulated data

3. **User-ID Configuration**

   - Only enable User-ID on zones with user traffic
   - Use include/exclude lists to optimize User-ID processing
   - Configure appropriate User-ID timeouts for your environment

4. **Security Policy Design**

   - Create clear security policies between zones
   - Follow the principle of least privilege when allowing traffic between zones
   - Use appropriate logging settings for inter-zone traffic

5. **Documentation**

   - Document the purpose and scope of each zone
   - Maintain documentation of which interfaces belong to which zones
   - Document security policy requirements between zones

## 8. Related Models

- [Security Rule](security_rule.md) - Configure security policies between zones
- [Address](address.md) - Define network objects within zones
- [Tag](tag.md) - Apply tags to zones for organization
