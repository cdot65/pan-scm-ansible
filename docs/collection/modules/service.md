# Service Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Service Model Attributes](#service-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating Service Objects](#creating-service-objects)
    - [Creating TCP Services](#creating-tcp-services)
    - [Creating UDP Services](#creating-udp-services)
    - [Updating Services](#updating-services)
    - [Deleting Services](#deleting-services)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `service` Ansible module provides functionality to manage service objects in Palo Alto Networks' Strata Cloud Manager (SCM). This module allows you to create, update, and delete service objects for both TCP and UDP protocols with port specifications and timeout override settings. Service objects are essential components for defining application traffic in security policies.

## Core Methods

| Method     | Description                    | Parameters                    | Return Type                 |
| ---------- | ------------------------------ | ----------------------------- | --------------------------- |
| `create()` | Creates a new service object   | `data: Dict[str, Any]`        | `ServiceResponseModel`       |
| `update()` | Updates an existing service    | `service: ServiceUpdateModel` | `ServiceResponseModel`       |
| `delete()` | Removes a service              | `object_id: str`              | `None`                       |
| `fetch()`  | Gets a service by name         | `name: str`, `container: str` | `ServiceResponseModel`       |
| `list()`   | Lists services with filtering  | `folder: str`, `**filters`    | `List[ServiceResponseModel]` |

## Service Model Attributes

| Attribute    | Type | Required      | Description                                                    |
| ------------ | ---- | ------------- | -------------------------------------------------------------- |
| `name`       | str  | Yes           | Service name. Must match pattern: ^[a-zA-Z0-9.\_-]+$          |
| `protocol`   | dict | Yes           | Protocol configuration (TCP or UDP). Exactly one required.     |
| `description`| str  | No            | Description of the service (max 1023 chars)                    |
| `tag`        | list | No            | List of tags associated with the service (max 64 chars each)   |
| `folder`     | str  | One container | The folder in which the service is defined (max 64 chars)      |
| `snippet`    | str  | One container | The snippet in which the service is defined (max 64 chars)     |
| `device`     | str  | One container | The device in which the service is defined (max 64 chars)      |

### TCP Protocol Attributes

| Attribute           | Type | Required | Description                                        |
| ------------------- | ---- | -------- | -------------------------------------------------- |
| `port`              | str  | Yes      | TCP port(s) for the service (e.g., '80' or '80,443') |
| `override`          | dict | No       | Override settings for TCP timeouts                 |
| `override.timeout`  | int  | No       | Connection timeout in seconds (default: 3600)      |
| `override.halfclose_timeout` | int | No | Half-close timeout in seconds (default: 120)    |
| `override.timewait_timeout`  | int | No | Time-wait timeout in seconds (default: 15)      |

### UDP Protocol Attributes

| Attribute          | Type | Required | Description                                        |
| ------------------ | ---- | -------- | -------------------------------------------------- |
| `port`             | str  | Yes      | UDP port(s) for the service (e.g., '53' or '67,68') |
| `override`         | dict | No       | Override settings for UDP timeouts                 |
| `override.timeout` | int  | No       | Connection timeout in seconds (default: 30)        |

### Provider Dictionary

| Parameter       | Type | Required | Description                             |
| --------------- | ---- | -------- | --------------------------------------- |
| `client_id`     | str  | Yes      | Client ID for SCM authentication         |
| `client_secret` | str  | Yes      | Client secret for SCM authentication     |
| `tsg_id`        | str  | Yes      | Tenant Service Group ID                  |
| `log_level`     | str  | No       | Log level for the SDK (default: "INFO")  |

## Exceptions

| Exception                    | Description                     |
| ---------------------------- | ------------------------------- |
| `InvalidObjectError`         | Invalid service data or format  |
| `NameNotUniqueError`         | Service name already exists     |
| `ObjectNotPresentError`      | Service not found               |
| `MissingQueryParameterError` | Missing required parameters     |
| `AuthenticationError`        | Authentication failed           |
| `ServerError`                | Internal server error           |

## Basic Configuration

The Service module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Service Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure TCP service exists
      cdot65.scm.service:
        provider: "{{ provider }}"
        name: "Web-Service"
        protocol:
          tcp:
            port: "80,443"
        description: "Web server ports"
        folder: "Texas"
        state: "present"
```

## Usage Examples

### Creating Service Objects

Service objects define protocols and ports for use in security policies and other objects.

### Creating TCP Services

This example creates a TCP service with port specifications and timeout overrides.

```yaml
- name: Create TCP service with port and timeout overrides
  cdot65.scm.service:
    provider: "{{ provider }}"
    name: "Test-TCP-Service"
    protocol:
      tcp:
        port: "80,443"
        override:
          timeout: 60
          halfclose_timeout: 30
          timewait_timeout: 10
    description: "Test TCP service with ports 80 and 443"
    folder: "Texas"
    tag: ["dev-ansible", "dev-test"]
    state: "present"
```

You can specify multiple ports as a comma-separated list:

```yaml
- name: Create web service with multiple ports
  cdot65.scm.service:
    provider: "{{ provider }}"
    name: "web-service"
    protocol:
      tcp:
        port: "80,443,8080,8443"
    description: "Web server ports"
    folder: "Texas"
    state: "present"
```

### Creating UDP Services

This example creates a UDP service with port specification and timeout override.

```yaml
- name: Create UDP service with port and timeout override
  cdot65.scm.service:
    provider: "{{ provider }}"
    name: "Test-UDP-Service"
    protocol:
      udp:
        port: "53"
        override:
          timeout: 120
    description: "Test UDP service for DNS"
    folder: "Texas"
    tag: ["dev-automation", "dev-cicd"]
    state: "present"
```

The UDP protocol supports a simpler override configuration with just the timeout parameter:

```yaml
- name: Create DHCP service
  cdot65.scm.service:
    provider: "{{ provider }}"
    name: "dhcp-service"
    protocol:
      udp:
        port: "67,68"
    description: "DHCP service"
    folder: "Texas"
    state: "present"
```

### Updating Services

When updating a service, you only need to include the parameters you want to change. Existing values for other parameters will be preserved.

```yaml
- name: Update TCP service with additional port and changed description
  cdot65.scm.service:
    provider: "{{ provider }}"
    name: "Test-TCP-Service"
    protocol:
      tcp:
        port: "80,443,8080"
    description: "Updated TCP service with additional port 8080"
    folder: "Texas"
    tag: ["dev-ansible", "dev-test", "dev-cicd"]
    state: "present"
```

You can also update just the description without changing other parameters:

```yaml
- name: Update just the description of UDP service
  cdot65.scm.service:
    provider: "{{ provider }}"
    name: "Test-UDP-Service"
    protocol:
      udp:
        port: "53"
    description: "Updated description for DNS service"
    folder: "Texas"
    state: "present"
```

### Deleting Services

This example removes a service object.

```yaml
- name: Delete the TCP service
  cdot65.scm.service:
    provider: "{{ provider }}"
    name: "Test-TCP-Service"
    folder: "Texas"
    state: "absent"
```

You can also delete multiple services using a loop:

```yaml
- name: Remove multiple services
  cdot65.scm.service:
    provider: "{{ provider }}"
    name: "{{ item }}"
    folder: "Texas"
    state: "absent"
  loop:
    - "web-service"
    - "dns-service"
    - "dhcp-service"
```

## Managing Configuration Changes

After creating, updating, or deleting service objects, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated service objects"
```

## Error Handling

It's important to handle potential errors when working with service objects.

```yaml
- name: Create or update service with error handling
  block:
    - name: Ensure service exists
      cdot65.scm.service:
        provider: "{{ provider }}"
        name: "Web-Service"
        protocol:
          tcp:
            port: "80,443"
        description: "Web server ports"
        folder: "Texas"
        state: "present"
      register: service_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated service objects"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```

## Best Practices

### Service Naming

- Use descriptive names that indicate the service purpose
- Include protocol and port information when relevant
- Follow a consistent naming convention across services
- Keep names concise but meaningful
- Consider using prefixes for service categories

### Port Configuration

- Use comma-separated lists for related ports (e.g., "80,443")
- Document non-standard ports in the description field
- Keep port lists focused on functionally related services
- Consider service groups for complex port arrangements
- Avoid overly broad port ranges that may introduce security risks

### Timeout Settings

- Only modify timeout values when required by specific application needs
- Document the reason for custom timeout values in the description
- Test thoroughly when modifying default timeout values
- Be aware of the impact on established connections when changing timeouts
- Balance between security and operational requirements when setting timeouts

### Organization

- Group related services in the same folder
- Use tags to categorize services by application, environment, or purpose
- Document service dependencies to aid in change management
- Maintain a consistent organization scheme across your infrastructure
- Consider using a naming convention that makes services easy to find

### Security Considerations

- Limit services to only the required ports for applications
- Avoid using overly permissive port definitions
- Document the business purpose for each service object
- Regularly review service objects for unused or redundant definitions
- Consider the impact of service definitions on security policy effectiveness

## Related Modules

- [service_info](service_info.md) - Retrieve information about service objects
- [service_group](service_group.md) - Manage service group objects
- [service_group_info](service_group_info.md) - Retrieve information about service groups
- [security_rule](security_rule.md) - Configure security policies that reference services