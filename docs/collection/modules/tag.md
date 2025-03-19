# Tag Configuration Object

## 1. Overview
The Tag module allows you to manage tag objects within Strata Cloud Manager (SCM). Tags are metadata labels that can be applied to various objects for categorization, filtering, and policy application. They are particularly useful for dynamic address group membership and organizational purposes.

## 2. Core Methods

| Method     | Description             | Parameters                | Return Type            |
|------------|-------------------------|---------------------------|------------------------|
| `create()` | Creates a new tag       | `data: Dict[str, Any]`    | `ResponseModel`        |
| `get()`    | Retrieves tag by name   | `name: str, folder: str`  | `ResponseModel`        |
| `update()` | Updates an existing tag | `tag: Model`              | `ResponseModel`        |
| `delete()` | Deletes a tag           | `id: str`                 | `None`                 |

## 3. Model Attributes

| Attribute     | Type              | Required | Description                                    |
|---------------|-------------------|----------|------------------------------------------------|
| `name`        | str               | Yes      | The name of the tag                            |
| `color`       | str               | Yes      | The color of the tag (e.g., "color1")          |
| `comments`    | str               | No       | Additional comments about the tag              |
| `folder`      | str               | No*      | The folder in which the resource is defined    |
| `snippet`     | str               | No*      | The snippet in which the resource is defined   |
| `device`      | str               | No*      | The device in which the resource is defined    |

\* Exactly one of `folder`, `snippet`, or `device` must be provided.

### Available Tag Colors

- `color1` - Red
- `color2` - Green
- `color3` - Blue
- `color4` - Yellow
- `color5` - Copper
- `color6` - Orange
- `color7` - Purple
- `color8` - Gray
- `color9` - Light Green
- `color10` - Cyan
- `color11` - Light Gray
- `color12` - Blue Gray
- `color13` - Lime
- `color14` - Black
- `color15` - Gold
- `color16` - Brown
- `color17` - Olive

## 4. Basic Configuration

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a tag
  cdot65.scm.tag:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "production"
    color: "color1"
    folder: "Texas"
    state: "present"
```

</div>

## 5. Usage Examples

### Creating Tags

<div class="termy">

<!-- termynal -->

```yaml
- name: Create multiple tags
  cdot65.scm.tag:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "{{ item.name }}"
    color: "{{ item.color }}"
    comments: "{{ item.description }}"
    folder: "Texas"
    state: "present"
  loop:
    - { name: "production", color: "color1", description: "Production systems" }
    - { name: "development", color: "color2", description: "Development systems" }
    - { name: "testing", color: "color3", description: "Testing systems" }
    - { name: "web-server", color: "color4", description: "Web servers" }
    - { name: "database", color: "color5", description: "Database servers" }
```

</div>

### Updating a Tag

<div class="termy">

<!-- termynal -->

```yaml
- name: Update a tag color and comments
  cdot65.scm.tag:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "production"
    color: "color15"  # Change to Gold
    comments: "Critical production systems - high priority"
    folder: "Texas"
    state: "present"
```

</div>

### Deleting a Tag

<div class="termy">

<!-- termynal -->

```yaml
- name: Delete a tag
  cdot65.scm.tag:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "deprecated-tag"
    folder: "Texas"
    state: "absent"
```

</div>

## 6. Using Tags with Other Objects

### Tagging Address Objects

<div class="termy">

<!-- termynal -->

```yaml
- name: Create address object with tags
  cdot65.scm.address:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "web-server-1"
    description: "Primary web server"
    ip_netmask: "10.1.1.10/32"
    tag:
      - "production"
      - "web-server"
    folder: "Texas"
    state: "present"
```

</div>

### Creating Dynamic Address Groups with Tags

<div class="termy">

<!-- termynal -->

```yaml
- name: Create dynamic address group using tags
  cdot65.scm.address_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "production-web-servers"
    description: "Dynamic group for production web servers"
    dynamic:
      filter: "'production' and 'web-server'"
    folder: "Texas"
    state: "present"
```

</div>

## 7. Best Practices

1. **Naming Convention**
   - Use descriptive names that indicate the tag's purpose
   - Keep tag names concise but clear
   - Use lowercase names for consistency

2. **Color Coding**
   - Use consistent colors for similar categories
   - Create a color scheme for your organization (e.g., red for production, green for development)
   - Document the meaning of each color

3. **Organization**
   - Create a hierarchical tagging system
   - Use tags for environment, function, location, compliance, etc.
   - Document your tagging strategy

4. **Dynamic Address Groups**
   - Design tags specifically for use with dynamic address groups
   - Use logical combinations of tags in dynamic address group filters
   - Test tag expressions before implementing in production

5. **Maintenance**
   - Regularly review and clean up unused tags
   - Ensure tags are applied consistently across objects
   - Document which objects use each tag

## 8. Related Models

- [Address](address.md) - Apply tags to address objects
- [Address Group](address_group.md) - Use tags in dynamic address group filters
- [Security Rule](security_rule.md) - Use tagged objects in security policies