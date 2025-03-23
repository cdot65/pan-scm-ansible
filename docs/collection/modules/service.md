# Service Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
    - [Creating TCP Services](#creating-tcp-services)
    - [Creating UDP Services](#creating-udp-services)
    - [Updating Services](#updating-services)
    - [Deleting Services](#deleting-services)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `service` module provides functionality to manage service objects in Palo Alto Networks' Strata Cloud Manager. This module allows you to create, update, and delete service objects for both TCP and UDP protocols with port specifications and timeout override settings. Service objects are essential components for defining application traffic in security policies.

## Module Parameters

| Parameter                            | Required | Type | Choices         | Default | Comments                                                         |
|--------------------------------------|----------|------|-----------------|---------|------------------------------------------------------------------|
| name                                 | yes      | str  |                 |         | The name of the service (max 63 chars).                          |
| protocol                             | yes*     | dict |                 |         | Protocol configuration (TCP or UDP). Exactly one required.       |
| protocol.tcp                         | no       | dict |                 |         | TCP protocol configuration with port information.                |
| protocol.tcp.port                    | yes**    | str  |                 |         | TCP port(s) for the service (e.g., '80' or '80,443').           |
| protocol.tcp.override                | no       | dict |                 |         | Override settings for TCP timeouts.                              |
| protocol.tcp.override.timeout        | no       | int  |                 | 3600    | Connection timeout in seconds.                                   |
| protocol.tcp.override.halfclose_timeout | no    | int  |                 | 120     | Half-close timeout in seconds.                                   |
| protocol.tcp.override.timewait_timeout | no     | int  |                 | 15      | Time-wait timeout in seconds.                                    |
| protocol.udp                         | no       | dict |                 |         | UDP protocol configuration with port information.                |
| protocol.udp.port                    | yes***   | str  |                 |         | UDP port(s) for the service (e.g., '53' or '67,68').            |
| protocol.udp.override                | no       | dict |                 |         | Override settings for UDP timeouts.                              |
| protocol.udp.override.timeout        | no       | int  |                 | 30      | Connection timeout in seconds.                                   |
| description                          | no       | str  |                 |         | Description of the service (max 1023 chars).                     |
| tag                                  | no       | list |                 |         | List of tags associated with the service (max 64 chars each).    |
| folder                               | no       | str  |                 |         | The folder in which the resource is defined.                     |
| snippet                              | no       | str  |                 |         | The snippet in which the resource is defined.                    |
| device                               | no       | str  |                 |         | The device in which the resource is defined.                     |
| provider                             | yes      | dict |                 |         | Authentication credentials.                                      |
| provider.client_id                   | yes      | str  |                 |         | Client ID for authentication.                                    |
| provider.client_secret               | yes      | str  |                 |         | Client secret for authentication.                                |
| provider.tsg_id                      | yes      | str  |                 |         | Tenant Service Group ID.                                         |
| provider.log_level                   | no       | str  |                 | INFO    | Log level for the SDK.                                           |
| state                                | yes      | str  | present, absent |         | Desired state of the service object.                             |

!!! note
    \* Protocol is required when state is "present".
    
    \** Required when TCP protocol is specified.
    
    \*** Required when UDP protocol is specified.
    
    \* Exactly one of `folder`, `snippet`, or `device` must be provided.
    
    \* Exactly one protocol type (TCP or UDP) must be specified.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Creating TCP Services

<div class="termy">

<!-- termynal -->

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

</div>

You can specify multiple ports as a comma-separated list:

<div class="termy">

<!-- termynal -->

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

</div>

### Creating UDP Services

<div class="termy">

<!-- termynal -->

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

</div>

The UDP protocol supports a simpler override configuration with just the timeout parameter:

<div class="termy">

<!-- termynal -->

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

</div>

### Updating Services

When updating a service, you only need to include the parameters you want to change. Existing values for other parameters will be preserved.

<div class="termy">

<!-- termynal -->

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

</div>

You can also update just the description without changing other parameters:

<div class="termy">

<!-- termynal -->

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

</div>

### Deleting Services

<div class="termy">

<!-- termynal -->

```yaml
- name: Delete the TCP service
  cdot65.scm.service:
    provider: "{{ provider }}"
    name: "Test-TCP-Service"
    folder: "Texas"
    state: "absent"
```

</div>

You can also delete multiple services using a loop:

<div class="termy">

<!-- termynal -->

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

</div>

## Return Values

| Name    | Description                 | Type | Returned              | Sample                                                                                                                                                                                                                                       |
|---------|-----------------------------|------|-----------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| changed | Whether any changes were made | bool | always                | true                                                                                                                                                                                                                                        |
| service | Details about the service object | dict | when state is present | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Test-TCP-Service", "description": "Test TCP service with ports 80 and 443", "protocol": {"tcp": {"port": "80,443", "override": {"timeout": 60, "halfclose_timeout": 30, "timewait_timeout": 10}}}, "folder": "Texas", "tag": ["dev-ansible", "dev-test"]} |

## Error Handling

Common errors you might encounter when using this module:

| Error | Description | Resolution |
|-------|-------------|------------|
| Invalid service data | Protocol parameters are invalid or missing | Verify protocol configuration is correct and matches the requirements |
| Service name already exists | Attempting to create a service with a name that already exists | Use a unique name or update the existing service |
| Missing container | None of folder, snippet, or device is specified | Provide exactly one of folder, snippet, or device |
| Multiple protocol types | Both TCP and UDP protocols are specified | Specify only one protocol type (TCP or UDP) |
| Protocol not specified | Protocol is missing for state=present | Provide a protocol configuration |
| Service not found | Attempt to update or delete a service that doesn't exist | Verify the service name and container location |

<div class="termy">

<!-- termynal -->

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to create service
      cdot65.scm.service:
        provider: "{{ provider }}"
        name: "web-service"
        # Missing protocol specification
        folder: "Texas"
        state: "present"
      register: result
  rescue:
    - name: Handle validation error
      debug:
        msg: "Failed to create service. Protocol configuration is required."
    - name: Continue with other tasks
      # Additional recovery tasks
```

</div>

## Best Practices

1. **Service Naming**
   - Use descriptive names that indicate the service purpose
   - Include protocol and port information when relevant
   - Follow a consistent naming convention across services
   - Keep names concise but meaningful

2. **Port Configuration**
   - Use comma-separated lists for related ports (e.g., "80,443")
   - Document non-standard ports in the description field
   - Keep port lists focused on functionally related services
   - Consider service groups for complex port arrangements

3. **Timeout Settings**
   - Only modify timeout values when required by specific application needs
   - Document the reason for custom timeout values in the description
   - Test thoroughly when modifying default timeout values
   - Be aware of the impact on established connections when changing timeouts

4. **Organization**
   - Group related services in the same folder
   - Use tags to categorize services by application, environment, or purpose
   - Document service dependencies to aid in change management
   - Maintain a consistent organization scheme across your infrastructure

5. **Module Usage**
   - Use check mode to validate changes before applying them
   - Leverage idempotent operations to safely run playbooks multiple times
   - Implement error handling with block/rescue for production playbooks
   - Consider using variables to manage service port lists for better maintenance

## Related Modules

- [service_info](service_info.md) - Retrieve information about service objects
- [service_group](service_group.md) - Manage service group objects
- [service_group_info](service_group_info.md) - Retrieve information about service groups
- [security_rule](security_rule.md) - Configure security policies that reference services

## Author

- Calvin Remsburg (@cdot65)