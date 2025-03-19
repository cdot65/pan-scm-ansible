# Service Group Configuration Object

## 1. Overview
The Service Group module allows you to manage service group objects within Strata Cloud Manager (SCM). Service groups combine multiple service objects into a single reference that can be used in security policies, simplifying administration and policy management.

## 2. Core Methods

| Method     | Description                    | Parameters                | Return Type            |
|------------|--------------------------------|---------------------------|------------------------|
| `create()` | Creates a new service group    | `data: Dict[str, Any]`    | `ResponseModel`        |
| `get()`    | Retrieves group by name        | `name: str, folder: str`  | `ResponseModel`        |
| `update()` | Updates an existing group      | `service_group: Model`    | `ResponseModel`        |
| `delete()` | Deletes a service group        | `id: str`                 | `None`                 |

## 3. Model Attributes

| Attribute     | Type              | Required | Description                                    |
|---------------|-------------------|----------|------------------------------------------------|
| `name`        | str               | Yes      | The name of the service group                  |
| `description` | str               | No       | Description of the service group               |
| `members`     | List[str]         | Yes      | List of service names in the group             |
| `tag`         | List[str]         | No       | List of tags associated with the group         |
| `folder`      | str               | No*      | The folder in which the resource is defined    |
| `snippet`     | str               | No*      | The snippet in which the resource is defined   |
| `device`      | str               | No*      | The device in which the resource is defined    |

\* Exactly one of `folder`, `snippet`, or `device` must be provided.

## 4. Basic Configuration

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a service group
  cdot65.scm.service_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "web-services"
    members:
      - "http"
      - "https"
    folder: "Texas"
    state: "present"
```

</div>

## 5. Usage Examples

### Creating a Service Group

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a comprehensive service group
  cdot65.scm.service_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "database-services"
    description: "Common database service ports"
    members:
      - "mysql"
      - "postgresql"
      - "mongodb"
      - "oracle"
    folder: "Texas"
    state: "present"
```

</div>

### Updating a Service Group

<div class="termy">

<!-- termynal -->

```yaml
- name: Update a service group
  cdot65.scm.service_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "web-services"
    description: "Updated web services"
    members:
      - "http"
      - "https"
      - "http-alt"  # Adding port 8080
    folder: "Texas"
    state: "present"
```

</div>

### Deleting a Service Group

<div class="termy">

<!-- termynal -->

```yaml
- name: Delete a service group
  cdot65.scm.service_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "deprecated-services"
    folder: "Texas"
    state: "absent"
```

</div>

## 6. Error Handling

<div class="termy">

<!-- termynal -->

```yaml
- name: Create service group with error handling
  block:
    - name: Attempt to create service group
      cdot65.scm.service_group:
        provider: "{{ provider }}"
        name: "new-services"
        members:
          - "http"
          - "non-existent-service"  # This service doesn't exist
        folder: "Texas"
        state: "present"
  rescue:
    - name: Handle error
      debug:
        msg: "Failed to create service group. Verify all services exist."
```

</div>

## 7. Best Practices

1. **Naming and Organization**
   - Use descriptive names that indicate the function of the group
   - Use a consistent naming convention across service groups
   - Include the purpose of the service group in the description field

2. **Member Management**
   - Group services with related functions (web, database, email, etc.)
   - Verify all member services exist before creating the group
   - Avoid creating excessively large groups with too many services

3. **Security Policy Usage**
   - Use service groups in security policies to improve policy clarity and reduce maintenance
   - Reference service groups instead of individual services when possible
   - Document which policies reference each service group

4. **Maintenance**
   - Review service group membership regularly
   - Update service groups when adding or removing services
   - Consider the impact on existing policies when modifying service groups

## 8. Related Models

- [Service](service.md) - Manage individual service objects
- [Security Rule](security_rule.md) - Configure security policies that use service groups
- [Tag](tag.md) - Manage tags for resource organization