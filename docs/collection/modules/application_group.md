# Application Group Configuration Object

## 1. Overview
The Application Group module allows you to manage application group objects within Strata Cloud Manager (SCM). These groups logically combine related application objects to simplify policy configuration and improve administration efficiency.

## 2. Core Methods

| Method     | Description                        | Parameters                | Return Type            |
|------------|------------------------------------|---------------------------|------------------------|
| `create()` | Creates a new application group    | `data: Dict[str, Any]`    | `ResponseModel`        |
| `get()`    | Retrieves group by name            | `name: str, folder: str`  | `ResponseModel`        |
| `update()` | Updates an existing group          | `app_group: Model`        | `ResponseModel`        |
| `delete()` | Deletes an application group       | `id: str`                 | `None`                 |

## 3. Model Attributes

| Attribute     | Type              | Required | Description                                    |
|---------------|-------------------|----------|------------------------------------------------|
| `name`        | str               | Yes      | The name of the application group              |
| `description` | str               | No       | Description of the application group           |
| `members`     | List[str]         | Yes      | List of application names in the group         |
| `tag`         | List[str]         | No       | List of tags associated with the group         |
| `folder`      | str               | No*      | The folder in which the resource is defined    |
| `snippet`     | str               | No*      | The snippet in which the resource is defined   |
| `device`      | str               | No*      | The device in which the resource is defined    |

\* Exactly one of `folder`, `snippet`, or `device` must be provided.

## 4. Basic Configuration

<div class="termy">

<!-- termynal -->

```yaml
- name: Create an application group
  cdot65.scm.application_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "web-applications"
    members:
      - "web-browsing"
      - "ssl"
    folder: "Texas"
    state: "present"
```

</div>

## 5. Usage Examples

### Creating an Application Group

<div class="termy">

<!-- termynal -->

```yaml
- name: Create an application group with multiple applications
  cdot65.scm.application_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "collaboration-apps"
    description: "Collaboration applications"
    members:
      - "ms-teams"
      - "webex"
      - "zoom"
    folder: "Texas"
    state: "present"
```

</div>

### Updating an Application Group

<div class="termy">

<!-- termynal -->

```yaml
- name: Update an application group
  cdot65.scm.application_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "collaboration-apps"
    description: "Updated collaboration applications"
    members:
      - "ms-teams"
      - "webex"
      - "zoom"
      - "slack"
    folder: "Texas"
    state: "present"
```

</div>

### Deleting an Application Group

<div class="termy">

<!-- termynal -->

```yaml
- name: Delete an application group
  cdot65.scm.application_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "collaboration-apps"
    folder: "Texas"
    state: "absent"
```

</div>

## 6. Error Handling

<div class="termy">

<!-- termynal -->

```yaml
- name: Create an application group with error handling
  block:
    - name: Attempt to create application group
      cdot65.scm.application_group:
        provider: "{{ provider }}"
        name: "web-applications"
        members:
          - "web-browsing"
          - "non-existent-app"  # This app doesn't exist
        folder: "Texas"
        state: "present"
  rescue:
    - name: Handle error
      debug:
        msg: "Failed to create application group. Verify all applications exist."
```

</div>

## 7. Best Practices

1. **Naming and Organization**
   - Use descriptive names that indicate the function of the group
   - Group applications with similar functions or purposes
   - Use a consistent naming convention across application groups

2. **Member Management**
   - Verify all member applications exist before creating the group
   - Avoid creating excessively large groups with too many applications
   - Group applications logically based on function (web, database, collaboration, etc.)

3. **Security Considerations**
   - Use application groups in security policies to improve policy clarity
   - Review application group membership regularly
   - Document the purpose of each application group

4. **Efficiency**
   - Minimize the number of application groups by grouping related applications
   - Use application groups to simplify security policy configuration

## 8. Related Models

- [Application](application.md) - Manage individual application objects
- [Security Rule](security_rule.md) - Configure security policies that use application groups
- [Tag](tag.md) - Manage tags for resource organization