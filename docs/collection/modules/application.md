# Application Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
    - [Creating Applications](#creating-applications)
    - [Updating Applications](#updating-applications)
    - [Deleting Applications](#deleting-applications)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `application` module provides functionality to manage custom application objects in Palo Alto Networks' Strata Cloud
Manager. This module allows you to create, update, and delete application objects with various attributes such as
category, subcategory, technology, risk level, and behavioral characteristics. Custom applications can be used in
security policies to control application-specific traffic.

## Module Parameters

| Parameter                 | Required | Type | Choices         | Default | Comments                                                  |
|---------------------------|----------|------|-----------------|---------|-----------------------------------------------------------|
| name                      | yes      | str  |                 |         | The name of the application.                              |
| category                  | yes*     | str  |                 |         | High-level category to which the application belongs.     |
| subcategory               | yes*     | str  |                 |         | Specific sub-category within the high-level category.     |
| technology                | yes*     | str  |                 |         | The underlying technology utilized by the application.    |
| risk                      | yes*     | int  |                 |         | The risk level associated with the application (1-5).     |
| description               | no       | str  |                 |         | Description for the application.                          |
| ports                     | no       | list |                 |         | List of TCP/UDP ports associated with the application.    |
| folder                    | no       | str  |                 |         | The folder where the application configuration is stored. |
| snippet                   | no       | str  |                 |         | The configuration snippet for the application.            |
| evasive                   | no       | bool |                 | false   | Indicates if the application uses evasive techniques.     |
| pervasive                 | no       | bool |                 | false   | Indicates if the application is widely used.              |
| excessive_bandwidth_use   | no       | bool |                 | false   | Indicates if the application uses excessive bandwidth.    |
| used_by_malware           | no       | bool |                 | false   | Indicates if the application is commonly used by malware. |
| transfers_files           | no       | bool |                 | false   | Indicates if the application transfers files.             |
| has_known_vulnerabilities | no       | bool |                 | false   | Indicates if the application has known vulnerabilities.   |
| tunnels_other_apps        | no       | bool |                 | false   | Indicates if the application tunnels other applications.  |
| prone_to_misuse           | no       | bool |                 | false   | Indicates if the application is prone to misuse.          |
| no_certifications         | no       | bool |                 | false   | Indicates if the application lacks certifications.        |
| provider                  | yes      | dict |                 |         | Authentication credentials.                               |
| provider.client_id        | yes      | str  |                 |         | Client ID for authentication.                             |
| provider.client_secret    | yes      | str  |                 |         | Client secret for authentication.                         |
| provider.tsg_id           | yes      | str  |                 |         | Tenant Service Group ID.                                  |
| provider.log_level        | no       | str  |                 | INFO    | Log level for the SDK.                                    |
| state                     | yes      | str  | present, absent |         | Desired state of the application object.                  |

!!! note
\* Category, subcategory, technology, and risk are required when state is "present".

    \* Exactly one of folder or snippet must be provided.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Creating Applications

<div class="termy">

<!-- termynal -->

```yaml
- name: Create a custom application
  cdot65.scm.application:
    provider: "{{ provider }}"
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

You can create applications with various characteristics and port definitions:

<div class="termy">

<!-- termynal -->

```yaml
- name: Create email application with multiple ports
  cdot65.scm.application:
    provider: "{{ provider }}"
    name: "test-app"
    category: "collaboration"
    subcategory: "email"
    technology: "client-server"
    risk: 2
    description: "Test email application"
    ports:
      - "tcp/25"
      - "tcp/143"
    folder: "Texas"
    state: "present"
```

</div>

### Updating Applications

When updating an application, you must provide all required fields (category, subcategory, technology, risk) along with
any fields you want to change. All other fields will retain their current values.

<div class="termy">

<!-- termynal -->

```yaml
- name: Update application risk level and add vulnerability flag
  cdot65.scm.application:
    provider: "{{ provider }}"
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

### Deleting Applications

<div class="termy">

<!-- termynal -->

```yaml
- name: Remove applications
  cdot65.scm.application:
    provider: "{{ provider }}"
    name: "{{ item }}"
    folder: "Texas"
    state: "absent"
  loop:
    - "custom-app"
    - "test-app"
```

</div>

## Return Values

| Name        | Description                   | Type | Returned              | Sample                                                                                                                                          |
|-------------|-------------------------------|------|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| changed     | Whether any changes were made | bool | always                | true                                                                                                                                            |
| application | Details about the application | dict | when state is present | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "custom-app", "category": "business-systems", "subcategory": "database", "risk": 3, ...} |

## Error Handling

Common errors you might encounter when using this module:

| Error                           | Description                                                         | Resolution                                                    |
|---------------------------------|---------------------------------------------------------------------|---------------------------------------------------------------|
| Invalid application data        | Required parameters missing or invalid format                       | Ensure all required parameters are provided with valid values |
| Application name already exists | Attempting to create an application with a name that already exists | Use a unique name or update the existing application          |
| Missing container               | Neither folder nor snippet is specified                             | Provide exactly one of folder or snippet                      |
| Invalid risk level              | Risk level must be between 1 and 5                                  | Provide a valid integer value between 1 and 5                 |

<div class="termy">

<!-- termynal -->

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to create application
      cdot65.scm.application:
        provider: "{{ provider }}"
        name: "custom-app"
        # Missing required fields: category, subcategory, technology, risk
        folder: "Texas"
        state: "present"
      register: result
  rescue:
    - name: Handle validation error
      debug:
        msg: "Failed to create application. Ensure all required parameters are provided."
    - name: Continue with other tasks
      # Additional recovery tasks
```

</div>

## Best Practices

1. **Application Definition**
    - Use clear, descriptive names that identify the application's purpose
    - Provide accurate category, subcategory, and technology values
    - Assign appropriate risk levels based on security assessment
    - Include detailed descriptions to document the application's purpose

2. **Risk Management**
    - Set risk levels (1-5) based on:
        - Sensitivity of data handled
        - Potential impact of compromise
        - Compliance requirements
        - Known vulnerabilities
    - Review and update risk levels regularly as application security posture changes

3. **Application Characteristic Flags**
    - Set behavioral flags accurately to enable proper security controls
    - Document the basis for each characteristic setting
    - Review characteristics when application versions change
    - Only enable flags that are applicable to the application

4. **Port Configuration**
    - Specify all ports required by the application
    - Use the format `protocol/port_number` (e.g., "tcp/443", "udp/53")
    - Only define ports that are actually needed by the application
    - Group related ports for the same application

5. **Module Usage**
    - Be aware of known idempotency issues with this module
    - Always provide all required parameters when updating
    - Use check mode to preview changes before applying
    - Implement error handling with block/rescue for production playbooks

## Related Modules

- [application_info](application_info.md) - Retrieve information about application objects
- [application_group](application_group.md) - Manage application group objects
- [application_group_info](application_group_info.md) - Retrieve information about application groups
- [security_rule](security_rule.md) - Configure security policies that reference applications
- [service](service.md) - Define service objects that can be used with applications

## Author

- Calvin Remsburg (@cdot65)