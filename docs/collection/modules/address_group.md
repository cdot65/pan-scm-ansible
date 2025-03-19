# Address Group Configuration Object

## 1. Overview
The Address Group module allows you to manage address group objects within Strata Cloud Manager (SCM). It supports both static and dynamic address groups, with comprehensive validation through Pydantic models.

## 2. Core Methods

| Method     | Description                    | Parameters                | Return Type            |
|------------|--------------------------------|---------------------------|------------------------|
| `create()` | Creates a new address group    | `data: Dict[str, Any]`    | `ResponseModel`        |
| `get()`    | Retrieves group by name        | `name: str, folder: str`  | `ResponseModel`        |
| `update()` | Updates an existing group      | `address_group: Model`    | `ResponseModel`        |
| `delete()` | Deletes an address group       | `id: str`                 | `None`                 |

## 3. Model Attributes

| Attribute     | Type              | Required | Description                                    |
|---------------|-------------------|----------|------------------------------------------------|
| `name`        | str               | Yes      | The name of the address group                  |
| `description` | str               | No       | Description of the address group               |
| `tag`         | List[str]         | No       | List of tags associated with the address group |
| `static`      | List[str]         | No*      | List of static addresses in the group          |
| `dynamic`     | Dict[str, str]    | No*      | Dynamic filter defining group membership       |
| `folder`      | str               | No**     | The folder in which the resource is defined    |
| `snippet`     | str               | No**     | The snippet in which the resource is defined   |
| `device`      | str               | No**     | The device in which the resource is defined    |

\* Exactly one of `static` or `dynamic` must be provided.  
\** Exactly one of `folder`, `snippet`, or `device` must be provided.

## 4. Basic Configuration

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a static address group
  cdot65.scm.address_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "Test Address Group"
    static:
      - "test_network1"
      - "test_network2"
    folder: "Shared"
    state: "present"
```

</div>

## 5. Usage Examples

### Creating a Static Address Group

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a static address group
  cdot65.scm.address_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "Test_Static_Group"
    description: "A static address group"
    static:
      - "test_network1"
      - "test_network2"
    folder: "Texas"
    state: "present"
```

</div>

### Creating a Dynamic Address Group

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a dynamic address group
  cdot65.scm.address_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "Test_Dynamic_Group"
    description: "A dynamic address group"
    dynamic:
      filter: "'tag1' or 'tag2'"
    folder: "Texas"
    state: "present"
```

</div>

### Updating an Address Group

<div class="termy">

<!-- termynal -->

```yaml
- name: Update the static address group
  cdot65.scm.address_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "Test_Static_Group"
    description: "An updated static address group"
    static:
      - "test_network1"
    folder: "Texas"
    state: "present"
```

</div>

### Deleting an Address Group

<div class="termy">

<!-- termynal -->

```yaml
- name: Delete an address group
  cdot65.scm.address_group:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "Test Address Group"
    folder: "Shared"
    state: "absent"
```

</div>

## 6. Error Handling

<div class="termy">

<!-- termynal -->

```yaml
- name: Create an address group with error handling
  block:
    - name: Attempt to create address group
      cdot65.scm.address_group:
        provider: "{{ provider }}"
        name: "Test_Group"
        # Missing either static or dynamic parameter
        folder: "Texas"
        state: "present"
  rescue:
    - name: Handle validation error
      debug:
        msg: "Failed to create address group. Ensure either static or dynamic is provided."
```

</div>

## 7. Best Practices

1. **Group Organization**
   - Use descriptive names for address groups
   - Include purpose in the description field
   - Apply consistent tagging strategies

2. **Static vs Dynamic Groups**
   - Use static groups for fixed sets of addresses
   - Use dynamic groups for addresses that share attributes
   - Use clear, understandable filter expressions for dynamic groups

3. **Security Considerations**
   - Review address groups regularly to ensure they include only necessary addresses
   - Document the purpose of each address group
   - Limit the number of addresses in a group to improve performance

4. **Management Efficiency**
   - Leverage tags to organize and categorize address groups
   - Use folders consistently to organize address groups by function, region, or environment
   - Document dependencies between address groups and security policies

## 8. Related Models

- [Address](address.md) - Manage individual address objects
- [Security Rule](security_rule.md) - Configure security policies that use address groups
- [Tag](tag.md) - Create and manage tags used in dynamic address groups