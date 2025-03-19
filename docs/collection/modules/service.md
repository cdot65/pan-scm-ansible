# Service Configuration Object

## 1. Overview
The Service module allows you to manage service objects within Strata Cloud Manager (SCM). It provides functionality to define TCP and UDP services with port specifications and timeout overrides. Service objects are essential components for configuring security policies.

## 2. Core Methods

| Method     | Description                 | Parameters                | Return Type            |
|------------|-----------------------------|---------------------------|------------------------|
| `create()` | Creates a new service       | `data: Dict[str, Any]`    | `ResponseModel`        |
| `get()`    | Retrieves service by name   | `name: str, folder: str`  | `ResponseModel`        |
| `update()` | Updates an existing service | `service: Model`          | `ResponseModel`        |
| `delete()` | Deletes a service           | `id: str`                 | `None`                 |

## 3. Model Attributes

| Attribute     | Type               | Required | Description                                 |
|---------------|-------------------|----------|---------------------------------------------|
| `name`        | str                | Yes      | The name of the service                     |
| `protocol`    | Dict               | Yes*     | Protocol configuration (TCP or UDP)         |
| `description` | str                | No       | Description of the service                  |
| `tag`         | List[str]          | No       | List of tags associated with the service    |
| `folder`      | str                | No**     | The folder in which the resource is defined |
| `snippet`     | str                | No**     | The snippet in which the resource is defined|
| `device`      | str                | No**     | The device in which the resource is defined |

\* Required when state is "present"  
\** Exactly one of folder, snippet, or device must be provided

### Protocol Structure

#### TCP Protocol

```yaml
protocol:
  tcp:
    port: "80,443"
    override:
      timeout: 30
      halfclose_timeout: 120
      timewait_timeout: 15
```

#### UDP Protocol

```yaml
protocol:
  udp:
    port: "53"
    override:
      timeout: 30
```

## 4. Basic Configuration

<div class="termy">

<!-- termynal -->

```yaml
- name: Create TCP service
  cdot65.scm.service:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "web-service"
    protocol:
      tcp:
        port: "80,443"
    description: "Web service ports"
    folder: "Texas"
    state: "present"
```

</div>

## 5. Usage Examples

### Creating a TCP Service

<div class="termy">

<!-- termynal -->

```yaml
- name: Create TCP service with timeout overrides
  cdot65.scm.service:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "web-service"
    protocol:
      tcp:
        port: "80,443"
        override:
          timeout: 30
          halfclose_timeout: 120
          timewait_timeout: 15
    description: "Web service ports"
    folder: "Texas"
    state: "present"
```

</div>

### Creating a UDP Service

<div class="termy">

<!-- termynal -->

```yaml
- name: Create UDP service
  cdot65.scm.service:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "dns-service"
    protocol:
      udp:
        port: "53"
    description: "DNS service"
    folder: "Texas"
    state: "present"
```

</div>

### Updating a Service

<div class="termy">

<!-- termynal -->

```yaml
- name: Update service ports
  cdot65.scm.service:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "web-service"
    protocol:
      tcp:
        port: "80,443,8080"
    folder: "Texas"
    state: "present"
```

</div>

### Deleting a Service

<div class="termy">

<!-- termynal -->

```yaml
- name: Remove service
  cdot65.scm.service:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "web-service"
    folder: "Texas"
    state: "absent"
```

</div>

## 6. Error Handling

<div class="termy">

<!-- termynal -->

```yaml
- name: Create service with error handling
  block:
    - name: Attempt to create service
      cdot65.scm.service:
        provider: "{{ provider }}"
        name: "web-service"
        # Missing protocol specification
        folder: "Texas"
        state: "present"
  rescue:
    - name: Handle validation error
      debug:
        msg: "Failed to create service. Protocol configuration is required."
```

</div>

## 7. Best Practices

1. **Service Naming**
   - Use descriptive names that indicate the service purpose
   - Include protocol and port information in the name when relevant
   - Follow a consistent naming convention across services

2. **Port Configuration**
   - Use comma-separated ranges for related ports (e.g., "80,443")
   - Document non-standard ports in the description field
   - Keep port lists focused on functionally related services

3. **Override Settings**
   - Only modify timeout values when necessary for specific application requirements
   - Document the reason for custom timeout values in the description
   - Test thoroughly when modifying default timeout values

4. **Organization**
   - Group related services in the same folder
   - Use tags to categorize services by application, environment, or purpose
   - Document service dependencies to aid in change management

## 8. Related Models

- [Service Group](service_group.md) - Group related service objects
- [Security Rule](security_rule.md) - Reference services in security policies
- [Application](application.md) - Define application objects that can use service objects