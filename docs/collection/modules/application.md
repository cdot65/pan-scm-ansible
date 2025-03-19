# Application Configuration Object

## 1. Overview
The Application module allows you to manage custom application objects within Strata Cloud Manager (SCM). It provides capabilities to define application-specific attributes such as category, subcategory, technology, and risk levels, along with various behavioral characteristics.

## 2. Core Methods

| Method     | Description                    | Parameters                | Return Type            |
|------------|--------------------------------|---------------------------|------------------------|
| `create()` | Creates a new application      | `data: Dict[str, Any]`    | `ResponseModel`        |
| `get()`    | Retrieves application by name  | `name: str, folder: str`  | `ResponseModel`        |
| `update()` | Updates an existing application| `application: Model`      | `ResponseModel`        |
| `delete()` | Deletes an application         | `id: str`                 | `None`                 |

## 3. Model Attributes

| Attribute                 | Type     | Required | Description                                   |
|---------------------------|----------|----------|-----------------------------------------------|
| `name`                    | str      | Yes      | The name of the application                   |
| `category`                | str      | Yes*     | High-level category to which app belongs      |
| `subcategory`             | str      | Yes*     | Sub-category within the high-level category   |
| `technology`              | str      | Yes*     | Underlying technology used by the application |
| `risk`                    | int      | Yes*     | Risk level (1-5)                              |
| `description`             | str      | No       | Description of the application                |
| `ports`                   | List[str]| No       | List of TCP/UDP ports used by the application |
| `folder`                  | str      | No**     | Folder where configuration is stored          |
| `snippet`                 | str      | No**     | Configuration snippet                         |
| `evasive`                 | bool     | No       | Uses evasive techniques                       |
| `pervasive`               | bool     | No       | Is widely used                                |
| `excessive_bandwidth_use` | bool     | No       | Uses excessive bandwidth                      |
| `used_by_malware`         | bool     | No       | Commonly used by malware                      |
| `transfers_files`         | bool     | No       | Transfers files                               |
| `has_known_vulnerabilities` | bool   | No       | Has known vulnerabilities                     |
| `tunnels_other_apps`      | bool     | No       | Tunnels other applications                    |
| `prone_to_misuse`         | bool     | No       | Prone to misuse                               |
| `no_certifications`       | bool     | No       | Lacks certifications                          |

\* Required when state is "present"  
\** Exactly one of folder or snippet must be provided

## 4. Basic Configuration

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a custom application
  cdot65.scm.application:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "custom-app"
    category: "business-systems"
    subcategory: "database"
    technology: "client-server"
    risk: 3
    description: "Custom database application"
    folder: "Texas"
    state: "present"
```

</div>

## 5. Usage Examples

### Creating an Application

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a custom application with ports and characteristics
  cdot65.scm.application:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "custom-app"
    category: "business-systems"
    subcategory: "database"
    technology: "client-server"
    risk: 3
    description: "Custom database application"
    ports:
      - "tcp/1521"
    folder: "Texas"
    transfers_files: true
    state: "present"
```

</div>

### Updating an Application

<div class="termy">

<!-- termynal -->

```yaml
- name: Update application risk level and vulnerability status
  cdot65.scm.application:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "custom-app"
    category: "business-systems"
    subcategory: "database"
    technology: "client-server"
    risk: 4
    folder: "Texas"
    has_known_vulnerabilities: true
    state: "present"
```

</div>

### Deleting an Application

<div class="termy">

<!-- termynal -->

```yaml
- name: Remove application
  cdot65.scm.application:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "custom-app"
    folder: "Texas"
    state: "absent"
```

</div>

## 6. Error Handling

<div class="termy">

<!-- termynal -->

```yaml
- name: Create an application with error handling
  block:
    - name: Attempt to create application
      cdot65.scm.application:
        provider: "{{ provider }}"
        name: "custom-app"
        # Missing required fields: category, subcategory, technology, risk
        folder: "Texas"
        state: "present"
  rescue:
    - name: Handle validation error
      debug:
        msg: "Failed to create application. Check if all required parameters are provided."
```

</div>

## 7. Best Practices

1. **Application Definition**
   - Use clear, descriptive names that identify the application's purpose
   - Provide accurate category, subcategory, and technology values
   - Assign appropriate risk levels based on security assessment

2. **Risk Management**
   - Set risk levels based on:
     - Sensitivity of data handled
     - Potential impact of compromise
     - Compliance requirements
     - Known vulnerabilities
   - Review and update risk levels regularly as application security posture changes

3. **Application Characteristic Flags**
   - Set behavioral flags accurately to enable proper security controls
   - Document the basis for each characteristic setting
   - Review characteristics when application versions change

4. **Port Configuration**
   - Specify all ports required by the application
   - Use the format `protocol/port_number` (e.g., "tcp/443", "udp/53")
   - Only define ports that are actually needed by the application

## 8. Related Models

- [Application Group](application_group.md) - Group applications together
- [Security Rule](security_rule.md) - Configure security policies that reference applications
- [Service](service.md) - Define service objects that can be used with applications