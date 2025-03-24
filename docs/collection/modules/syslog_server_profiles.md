# Syslog Server Profiles Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
    - [Creating Syslog Server Profiles](#creating-syslog-server-profiles)
    - [Updating Syslog Server Profiles](#updating-syslog-server-profiles)
    - [Deleting Syslog Server Profiles](#deleting-syslog-server-profiles)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `syslog_server_profiles` module provides functionality to manage syslog server profile objects in Palo Alto Networks' Strata Cloud Manager. This module allows you to create, update, and delete syslog server profiles with specific configurations for transport protocol, port, format, and facility settings.

## Module Parameters

| Parameter                | Required | Type    | Choices                                                                                      | Default | Comments                                                             |
|--------------------------|----------|---------|----------------------------------------------------------------------------------------------|---------|----------------------------------------------------------------------|
| name                     | yes      | str     |                                                                                              |         | The name of the syslog server profile (max 31 chars).               |
| servers                  | yes*     | dict    |                                                                                              |         | Dictionary of server configurations.                                 |
| servers.name             | yes      | str     |                                                                                              |         | Syslog server name.                                                  |
| servers.server           | yes      | str     |                                                                                              |         | Syslog server address.                                               |
| servers.transport        | yes      | str     | UDP, TCP                                                                                     |         | Transport protocol for the syslog server.                            |
| servers.port             | yes      | int     |                                                                                              |         | Syslog server port (1-65535).                                        |
| servers.format           | yes      | str     | BSD, IETF                                                                                    |         | Syslog format.                                                       |
| servers.facility         | yes      | str     | LOG_USER, LOG_LOCAL0, LOG_LOCAL1, LOG_LOCAL2, LOG_LOCAL3, LOG_LOCAL4, LOG_LOCAL5, LOG_LOCAL6, LOG_LOCAL7 |       | Syslog facility.                                                    |
| format                   | no       | dict    |                                                                                              |         | Format settings for different log types.                             |
| folder                   | no       | str     |                                                                                              |         | The folder in which the resource is defined (max 64 chars).          |
| snippet                  | no       | str     |                                                                                              |         | The snippet in which the resource is defined (max 64 chars).         |
| device                   | no       | str     |                                                                                              |         | The device in which the resource is defined (max 64 chars).          |
| provider                 | yes      | dict    |                                                                                              |         | Authentication credentials.                                          |
| provider.client_id       | yes      | str     |                                                                                              |         | Client ID for authentication.                                        |
| provider.client_secret   | yes      | str     |                                                                                              |         | Client secret for authentication.                                    |
| provider.tsg_id          | yes      | str     |                                                                                              |         | Tenant Service Group ID.                                             |
| provider.log_level       | no       | str     |                                                                                              | INFO    | Log level for the SDK.                                               |
| state                    | yes      | str     | present, absent                                                                              |         | Desired state of the syslog server profile.                          |

!!! note
- The `servers` parameter is required when state is present.
- Exactly one container type (`folder`, `snippet`, or `device`) must be provided.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.11 or higher
- Ansible 2.15 or higher

## Usage Examples

### Creating Syslog Server Profiles

<div class="termy">

<!-- termynal -->

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

</div>

<div class="termy">

<!-- termynal -->

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
    folder: "Texas"
    state: "present"
```

</div>

### Updating Syslog Server Profiles

<div class="termy">

<!-- termynal -->

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

</div>

### Deleting Syslog Server Profiles

<div class="termy">

<!-- termynal -->

```yaml
- name: Delete a syslog server profile
  cdot65.scm.syslog_server_profiles:
    provider: "{{ provider }}"
    name: "test-syslog-profile"
    folder: "Texas"
    state: "absent"
```

</div>

## Return Values

| Name                 | Description                          | Type | Returned              | Sample                                                                                                                                                       |
|----------------------|-------------------------------------|------|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| changed              | Whether any changes were made        | bool | always                | true                                                                                                                                                         |
| syslog_server_profile| Details about the syslog server profile | dict | when state is present | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "test-syslog-profile", "servers": {"name": "primary-syslog", "server": "10.0.0.1", "transport": "UDP"}} |

## Error Handling

Common errors you might encounter when using this module:

| Error                               | Description                                                      | Resolution                                                        |
|-------------------------------------|------------------------------------------------------------------|-------------------------------------------------------------------|
| Invalid syslog server profile data  | The profile parameters don't match required formats              | Verify the format of profile values (e.g., supported formats)     |
| Profile name already exists         | Attempt to create a profile with a name that already exists      | Use a unique name or update the existing profile                  |
| Profile not found                   | Attempt to update or delete a profile that doesn't exist         | Verify the profile name and container location                    |
| Missing required parameter          | Required parameter not provided                                  | Ensure all required parameters are specified                      |

<div class="termy">

<!-- termynal -->

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

</div>

## Best Practices

1. **Server Configuration**
    - Use appropriate transport protocols based on your requirements (TCP for reliability, UDP for performance)
    - Choose appropriate syslog formats based on your syslog server's capabilities
    - Configure suitable facility values to properly categorize logs

2. **Container Management**
    - Always specify exactly one container (folder, snippet, or device)
    - Use consistent container names across operations
    - Validate container existence before operations

3. **Format Settings**
    - Customize format settings based on the type of logs you want to collect
    - Use variables that provide the most useful context for each log type
    - Balance between verbosity and performance in your format settings

4. **Module Usage**
    - Use idempotent operations to safely run playbooks multiple times
    - Leverage check mode (`--check`) to preview changes before executing them
    - Implement proper error handling with block/rescue
    - Generate unique names when creating multiple similar profiles

5. **Integration with Other Systems**
    - Ensure your syslog server is properly configured to receive logs
    - Test connectivity to your syslog servers before deploying configurations
    - Consider the impact of log volume on your syslog server's performance

## Related Modules

- [syslog_server_profiles_info](syslog_server_profiles_info.md) - Retrieve information about syslog server profiles
- [log_forwarding_profile](log_forwarding_profile.md) - Manage log forwarding profiles that might use syslog server profiles
- [log_forwarding_profile_info](log_forwarding_profile_info.md) - Retrieve information about log forwarding profiles
- [security_rule](security_rule.md) - Manage security rules that might reference log forwarding profiles

## Author

- Calvin Remsburg (@cdot65)