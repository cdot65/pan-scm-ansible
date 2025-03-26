# Syslog Server Profiles Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Syslog Server Profile Model Attributes](#syslog-server-profile-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating Syslog Server Profiles](#creating-syslog-server-profiles)
    - [Basic Syslog Server Profile](#basic-syslog-server-profile)
    - [Advanced Syslog Server Profile](#advanced-syslog-server-profile)
    - [Updating Syslog Server Profiles](#updating-syslog-server-profiles)
    - [Deleting Syslog Server Profiles](#deleting-syslog-server-profiles)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `syslog_server_profiles` module provides functionality to manage syslog server profile objects in Palo Alto Networks' Strata Cloud Manager (SCM). This module allows you to create, update, and delete syslog server profiles with specific configurations for transport protocol, port, format, and facility settings. Syslog server profiles are essential for forwarding logs from the firewall to external syslog collectors for analysis, retention, and compliance purposes.

## Core Methods

| Method     | Description                            | Parameters                               | Return Type                          |
| ---------- | -------------------------------------- | ---------------------------------------- | ------------------------------------ |
| `create()` | Creates a new syslog server profile    | `data: Dict[str, Any]`                   | `SyslogServerProfileResponseModel`   |
| `update()` | Updates an existing profile            | `profile: SyslogServerProfileUpdateModel`| `SyslogServerProfileResponseModel`   |
| `delete()` | Removes a profile                      | `object_id: str`                         | `None`                               |
| `fetch()`  | Gets a profile by name                 | `name: str`, `container: str`            | `SyslogServerProfileResponseModel`   |
| `list()`   | Lists profiles with filtering          | `folder: str`, `**filters`               | `List[SyslogServerProfileResponseModel]` |

## Syslog Server Profile Model Attributes

| Attribute              | Type   | Required      | Description                                                |
| ---------------------- | ------ | ------------- | ---------------------------------------------------------- |
| `name`                 | str    | Yes           | Profile name (max 31 chars). Must match pattern: ^[a-zA-Z0-9.\_-]+$ |
| `servers`              | dict   | Yes           | Dictionary of server configurations                         |
| `format`               | dict   | No            | Format settings for different log types                     |
| `folder`               | str    | One container* | The folder in which the profile is defined (max 64 chars)  |
| `snippet`              | str    | One container* | The snippet in which the profile is defined (max 64 chars) |
| `device`               | str    | One container* | The device in which the profile is defined (max 64 chars)  |
| `state`                | str    | Yes           | Desired state of the profile ("present" or "absent")        |

*Exactly one container parameter must be provided.

### Server Attributes

| Attribute    | Type | Required | Description                                                       |
| ------------ | ---- | -------- | ----------------------------------------------------------------- |
| `name`       | str  | Yes      | Syslog server name                                                |
| `server`     | str  | Yes      | Syslog server address                                             |
| `transport`  | str  | Yes      | Transport protocol for the syslog server (UDP, TCP)               |
| `port`       | int  | Yes      | Syslog server port (1-65535)                                      |
| `format`     | str  | Yes      | Syslog format (BSD, IETF)                                         |
| `facility`   | str  | Yes      | Syslog facility (LOG_USER, LOG_LOCAL0 through LOG_LOCAL7)         |

### Format Attributes

| Attribute | Type | Required | Description                                  |
| --------- | ---- | -------- | -------------------------------------------- |
| `config`  | str  | No       | Format string for configuration logs         |
| `system`  | str  | No       | Format string for system logs                |
| `threat`  | str  | No       | Format string for threat logs                |
| `traffic` | str  | No       | Format string for traffic logs               |
| `hip`     | str  | No       | Format string for host information logs      |
| `url`     | str  | No       | Format string for URL filtering logs         |
| `data`    | str  | No       | Format string for data filtering logs        |
| `wildfire` | str | No       | Format string for WildFire submission logs   |
| `tunnel`  | str  | No       | Format string for tunnel inspection logs     |
| `userid`  | str  | No       | Format string for user identification logs   |
| `gtp`     | str  | No       | Format string for GPRS tunneling protocol logs |
| `auth`    | str  | No       | Format string for authentication logs        |
| `sctp`    | str  | No       | Format string for SCTP logs                  |

### Provider Dictionary

| Parameter       | Type | Required | Description                            |
| --------------- | ---- | -------- | -------------------------------------- |
| `client_id`     | str  | Yes      | Client ID for SCM authentication        |
| `client_secret` | str  | Yes      | Client secret for SCM authentication    |
| `tsg_id`        | str  | Yes      | Tenant Service Group ID                 |
| `log_level`     | str  | No       | Log level for the SDK (default: "INFO") |

## Exceptions

| Exception                    | Description                      |
| ---------------------------- | -------------------------------- |
| `InvalidObjectError`         | Invalid profile data or format   |
| `NameNotUniqueError`         | Profile name already exists      |
| `ObjectNotPresentError`      | Profile not found                |
| `MissingQueryParameterError` | Missing required parameters      |
| `AuthenticationError`        | Authentication failed            |
| `ServerError`                | Internal server error            |

## Basic Configuration

The Syslog Server Profile module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Syslog Server Profile Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a basic syslog server profile exists
      cdot65.scm.syslog_server_profiles:
        provider: "{{ provider }}"
        name: "basic-syslog-profile"
        servers:
          name: "primary-syslog"
          server: "10.0.0.1"
          transport: "UDP"
          port: 514
          format: "BSD"
          facility: "LOG_LOCAL0"
        folder: "Texas"
        state: "present"
```

## Usage Examples

### Creating Syslog Server Profiles

Syslog server profiles can be configured with different transport protocols, formats, and log format templates to match the requirements of your log collection infrastructure.

### Basic Syslog Server Profile

This example creates a simple syslog server profile with UDP transport.

```yaml
- name: Create a basic syslog server profile
  cdot65.scm.syslog_server_profiles:
    provider: "{{ provider }}"
    name: "test-syslog-profile"
    servers:
      name: "primary-syslog"
      server: "10.0.0.1"
      transport: "UDP"
      port: 514
      format: "BSD"
      facility: "LOG_LOCAL0"
    folder: "Texas"
    state: "present"
```

### Advanced Syslog Server Profile

This example creates a more advanced syslog server profile with TCP transport and custom format settings for different log types.

```yaml
- name: Create a syslog server profile with custom format settings
  cdot65.scm.syslog_server_profiles:
    provider: "{{ provider }}"
    name: "detailed-syslog-profile"
    servers:
      name: "primary-syslog"
      server: "10.0.0.1"
      transport: "TCP"
      port: 514
      format: "IETF"
      facility: "LOG_LOCAL3"
    format:
      config: "{hostname} {time} {ip-address}"
      system: "{hostname} {time} {severity}"
      threat: "{hostname} {time} {source-ip} {destination-ip}"
      traffic: "{hostname} {time} {source-ip} {destination-ip} {application}"
      url: "{hostname} {time} {source-ip} {url} {category}"
      wildfire: "{hostname} {time} {sha256} {verdict}"
    folder: "Texas"
    state: "present"
```

### Updating Syslog Server Profiles

```yaml
- name: Update an existing syslog server profile
  cdot65.scm.syslog_server_profiles:
    provider: "{{ provider }}"
    name: "test-syslog-profile"
    servers:
      name: "updated-syslog"
      server: "10.0.0.2"
      transport: "TCP"
      port: 1514
      format: "IETF"
      facility: "LOG_LOCAL1"
    folder: "Texas"
    state: "present"
```

### Deleting Syslog Server Profiles

```yaml
- name: Delete a syslog server profile
  cdot65.scm.syslog_server_profiles:
    provider: "{{ provider }}"
    name: "test-syslog-profile"
    folder: "Texas"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting syslog server profiles, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated syslog server profiles"
```

### Return Values

| Name                  | Description                             | Type | Returned              | Sample                                                                                                                                                         |
| --------------------- | --------------------------------------- | ---- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| changed               | Whether any changes were made           | bool | always                | true                                                                                                                                                           |
| syslog_server_profile | Details about the syslog server profile | dict | when state is present | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "test-syslog-profile", "servers": {"name": "primary-syslog", "server": "10.0.0.1", "transport": "UDP"}} |

## Error Handling

Common errors you might encounter when using this module:

| Error                              | Description                                                 | Resolution                                                    |
| ---------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------- |
| Invalid syslog server profile data | The profile parameters don't match required formats         | Verify the format of profile values (e.g., supported formats) |
| Profile name already exists        | Attempt to create a profile with a name that already exists | Use a unique name or update the existing profile              |
| Profile not found                  | Attempt to update or delete a profile that doesn't exist    | Verify the profile name and container location                |
| Missing required parameter         | Required parameter not provided                             | Ensure all required parameters are specified                  |

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to create syslog server profile
      cdot65.scm.syslog_server_profiles:
        provider: "{{ provider }}"
        name: "test-syslog-profile"
        servers:
          name: "primary-syslog"
          server: "10.0.0.1"
          transport: "UDP"
          port: 514
          format: "BSD"
          facility: "LOG_LOCAL0"
        folder: "Texas"
        state: "present"
      register: result
  rescue:
    - name: Handle profile already exists error
      debug:
        msg: "Syslog server profile already exists or invalid input provided"
    - name: Continue with other tasks
      # Additional recovery tasks
```

## Best Practices

### Server Configuration

- Use appropriate transport protocols based on your requirements (TCP for reliability, UDP for performance)
- Choose appropriate syslog formats based on your syslog server's capabilities
- Configure suitable facility values to properly categorize logs
- Consider implementing redundant syslog servers for high availability
- For critical logs, use TCP with acknowledgment to ensure delivery

### Container Management

- Always specify exactly one container (folder, snippet, or device)
- Use consistent container names across operations
- Validate container existence before operations
- Document container hierarchy for better organization
- Implement a consistent naming convention for containers

### Format Settings

- Customize format settings based on the type of logs you want to collect
- Use variables that provide the most useful context for each log type
- Balance between verbosity and performance in your format settings
- Include timestamp and severity in all log formats
- For security investigations, include source and destination information in threat logs

### Log Management

- Configure different formats for different log types based on their use cases
- Set up retention policies on your syslog servers appropriate for each log type
- Consider performance impact of high-volume logs (traffic logs especially)
- Implement log rotation on syslog servers to manage disk space
- Document the log format variables for easier parsing and analysis

### Security Considerations

- Secure transport of logs when containing sensitive information (consider TLS or IPsec)
- Ensure syslog servers are hardened according to security best practices
- Implement access controls on your syslog servers
- Monitor syslog server health and connectivity
- Consider encryption for sensitive log data

### Module Usage

- Use idempotent operations to safely run playbooks multiple times
- Leverage check mode (`--check`) to preview changes before executing them
- Implement proper error handling with block/rescue
- Generate unique names when creating multiple similar profiles
- Test configurations in non-production environments first

## Related Modules

- [syslog_server_profiles_info](syslog_server_profiles_info.md) - Retrieve information about syslog
  server profiles
- [log_forwarding_profile](log_forwarding_profile.md) - Manage log forwarding profiles that might
  use syslog server profiles
- [log_forwarding_profile_info](log_forwarding_profile_info.md) - Retrieve information about log
  forwarding profiles
- [security_rule](security_rule.md) - Manage security rules that might reference log forwarding
  profiles

## Author

- Calvin Remsburg (@cdot65)
