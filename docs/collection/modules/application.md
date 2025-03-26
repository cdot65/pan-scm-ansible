# Application Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Application Model Attributes](#application-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating Applications](#creating-applications)
    - [Basic Application](#basic-application)
    - [Comprehensive Application](#comprehensive-application)
    - [Updating Applications](#updating-applications)
    - [Deleting Applications](#deleting-applications)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `application` Ansible module provides functionality to manage custom application objects in Palo Alto
Networks' Strata Cloud Manager (SCM). This module allows you to create, update, and delete application
objects with various attributes such as category, subcategory, technology, risk level, and
behavioral characteristics. Custom applications can be used in security policies to control
application-specific traffic.

## Core Methods

| Method     | Description                      | Parameters                      | Return Type                  |
| ---------- | -------------------------------- | ------------------------------- | ---------------------------- |
| `create()` | Creates a new application object | `data: Dict[str, Any]`          | `ApplicationResponseModel`    |
| `update()` | Updates an existing application  | `app: ApplicationUpdateModel`   | `ApplicationResponseModel`    |
| `delete()` | Removes an application           | `object_id: str`                | `None`                       |
| `fetch()`  | Gets an application by name      | `name: str`, `container: str`   | `ApplicationResponseModel`    |
| `list()`   | Lists applications with filtering| `folder: str`, `**filters`      | `List[ApplicationResponseModel]`|

## Application Model Attributes

| Attribute                  | Type | Required      | Description                                                |
| -------------------------- | ---- | ------------- | ---------------------------------------------------------- |
| `name`                     | str  | Yes           | The name of the application                                |
| `category`                 | str  | Yes           | High-level category to which the application belongs       |
| `subcategory`              | str  | Yes           | Specific sub-category within the high-level category       |
| `technology`               | str  | Yes           | The underlying technology utilized by the application      |
| `risk`                     | int  | Yes           | The risk level associated with the application (1-5)       |
| `description`              | str  | No            | Description for the application                            |
| `ports`                    | list | No            | List of TCP/UDP ports associated with the application      |
| `evasive`                  | bool | No            | Indicates if the application uses evasive techniques       |
| `pervasive`                | bool | No            | Indicates if the application is widely used                |
| `excessive_bandwidth_use`  | bool | No            | Indicates if the application uses excessive bandwidth      |
| `used_by_malware`          | bool | No            | Indicates if the application is commonly used by malware   |
| `transfers_files`          | bool | No            | Indicates if the application transfers files               |
| `has_known_vulnerabilities`| bool | No            | Indicates if the application has known vulnerabilities     |
| `tunnels_other_apps`       | bool | No            | Indicates if the application tunnels other applications    |
| `prone_to_misuse`          | bool | No            | Indicates if the application is prone to misuse            |
| `no_certifications`        | bool | No            | Indicates if the application lacks certifications          |
| `folder`                   | str  | One container | The folder in which the application is defined (max 64 chars) |
| `snippet`                  | str  | One container | The snippet in which the application is defined (max 64 chars)|

## Exceptions

| Exception                    | Description                         |
| ---------------------------- | ----------------------------------- |
| `InvalidObjectError`         | Invalid application data or format  |
| `NameNotUniqueError`         | Application name already exists     |
| `ObjectNotPresentError`      | Application not found               |
| `MissingQueryParameterError` | Missing required parameters         |
| `InvalidRiskLevelError`      | Invalid risk level (must be 1-5)    |
| `AuthenticationError`        | Authentication failed               |
| `ServerError`                | Internal server error               |

## Basic Configuration

The Application module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Application Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a custom application exists
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
        state: "present"
```

## Usage Examples

### Creating Applications

Applications can be created with various characteristics and port definitions to precisely control network traffic.

### Basic Application

This example creates a simple application with basic attributes.

```yaml
- name: Create a basic custom application
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
    state: "present"
```

### Comprehensive Application

This example creates a more comprehensive application with multiple ports and detailed characteristics.

```yaml
- name: Create a comprehensive application
  cdot65.scm.application:
    provider: "{{ provider }}"
    name: "advanced-web-app"
    category: "business-systems"
    subcategory: "web-application"
    technology: "browser-based"
    risk: 4
    description: "Advanced web application with file transfer capabilities"
    ports:
      - "tcp/80"
      - "tcp/443"
      - "tcp/8080"
    folder: "Texas"
    evasive: false
    pervasive: true
    excessive_bandwidth_use: false
    used_by_malware: false
    transfers_files: true
    has_known_vulnerabilities: true
    tunnels_other_apps: false
    prone_to_misuse: true
    no_certifications: false
    state: "present"
```

### Updating Applications

When updating an application, you must provide all required fields (category, subcategory,
technology, risk) along with any fields you want to change. All other fields will retain their
current values.

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

### Deleting Applications

This example removes applications from the system.

```yaml
- name: Remove applications
  cdot65.scm.application:
    provider: "{{ provider }}"
    name: "{{ item }}"
    folder: "Texas"
    state: "absent"
  loop:
    - "custom-app"
    - "advanced-web-app"
```

## Managing Configuration Changes

After creating, updating, or deleting applications, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated application definitions"
```

## Error Handling

It's important to handle potential errors when working with application objects.

```yaml
- name: Create or update application with error handling
  block:
    - name: Ensure application exists
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
        state: "present"
      register: app_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated application definitions"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```

## Best Practices

### Application Definition

- Use clear, descriptive names that identify the application's purpose
- Provide accurate category, subcategory, and technology values
- Assign appropriate risk levels based on security assessment
- Include detailed descriptions to document the application's purpose
- Be consistent with naming conventions across your environment

### Risk Management

- Set risk levels (1-5) based on:
  - Sensitivity of data handled
  - Potential impact of compromise
  - Compliance requirements
  - Known vulnerabilities
- Review and update risk levels regularly as application security posture changes
- Document the reasoning behind each risk level assignment

### Application Characteristic Flags

- Set behavioral flags accurately to enable proper security controls
- Document the basis for each characteristic setting
- Review characteristics when application versions change
- Only enable flags that are applicable to the application
- Be cautious with high-risk characteristics that might trigger additional scrutiny

### Port Configuration

- Specify all ports required by the application
- Use the format `protocol/port_number` (e.g., "tcp/443", "udp/53")
- Only define ports that are actually needed by the application
- Group related ports for the same application
- Consider security implications of ports (e.g., non-standard or high-number ports)

### Module Usage

- Be aware of known idempotency issues with this module
- Always provide all required parameters when updating
- Use check mode to preview changes before applying
- Implement error handling with block/rescue for production playbooks
- Organize applications into logical folders

## Related Modules

- [application_info](application_info.md) - Retrieve information about application objects
- [application_group](application_group.md) - Manage application group objects
- [application_group_info](application_group_info.md) - Retrieve information about application groups
- [security_rule](security_rule.md) - Configure security policies that reference applications
- [service](service.md) - Define service objects that can be used with applications