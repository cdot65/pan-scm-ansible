# Http Server Profiles Configuration Object

## 01. Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [HTTP Server Profile Model Attributes](#http-server-profile-model-attributes)
4. [Exceptions](#exceptions)
5. [Basic Configuration](#basic-configuration)
6. [Usage Examples](#usage-examples)
   - [Creating HTTP Server Profiles](#creating-http-server-profiles)
   - [Basic HTTP Server Profile](#basic-http-server-profile)
   - [HTTPS Server Profile](#https-server-profile)
   - [Multiple Servers Configuration](#multiple-servers-configuration)
   - [Updating HTTP Server Profiles](#updating-http-server-profiles)
   - [Deleting HTTP Server Profiles](#deleting-http-server-profiles)
7. [Managing Configuration Changes](#managing-configuration-changes)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## 02. Overview

The `http_server_profiles` Ansible module provides functionality to manage HTTP server profile objects in Palo Alto Networks' Strata Cloud Manager (SCM). HTTP server profiles define server configurations for services like log forwarding, and this module supports creating, updating, and deleting these profiles with various server configurations and protocol settings.

## 03. Core Methods

| Method     | Description                          | Parameters                            | Return Type                          |
| ---------- | ------------------------------------ | ------------------------------------- | ------------------------------------ |
| `create()` | Creates a new HTTP server profile    | `data: Dict[str, Any]`                | `HttpServerProfileResponseModel`     |
| `update()` | Updates an existing server profile   | `profile: HttpServerProfileUpdateModel` | `HttpServerProfileResponseModel`   |
| `delete()` | Removes a server profile             | `object_id: str`                      | `None`                               |
| `fetch()`  | Gets a server profile by name        | `name: str`, `container: str`         | `HttpServerProfileResponseModel`     |
| `list()`   | Lists server profiles with filtering | `folder: str`, `**filters`            | `List[HttpServerProfileResponseModel]` |

## 04. HTTP Server Profile Model Attributes

| Attribute          | Type   | Required      | Description                                                 |
| ------------------ | ------ | ------------- | ----------------------------------------------------------- |
| `name`             | str    | Yes           | Name of the HTTP server profile (max 63 chars)              |
| `description`      | str    | No            | Description of the HTTP server profile                       |
| `server`           | list   | Yes*          | List of server configurations                               |
| `tag_registration` | bool   | No            | Whether to register tags on match                           |
| `format`           | dict   | No            | Format settings for different log types                     |
| `folder`           | str    | One container | The folder in which the profile is defined (max 64 chars)   |
| `snippet`          | str    | One container | The snippet in which the profile is defined (max 64 chars)  |
| `device`           | str    | One container | The device in which the profile is defined (max 64 chars)   |

*Required when `state=present`

### Server Configuration Attributes

| Attribute             | Type    | Required | Description                                                   |
| --------------------- | ------- | -------- | ------------------------------------------------------------- |
| `name`                | str     | Yes      | Server name                                                   |
| `address`             | str     | Yes      | Server address (IP or FQDN)                                   |
| `protocol`            | str     | Yes      | Protocol: "HTTP" or "HTTPS"                                   |
| `port`                | int     | Yes      | Port number                                                   |
| `http_method`         | str     | Yes      | HTTP method: "GET", "POST", "PUT", "DELETE"                   |
| `tls_version`         | str     | No       | TLS version: "1.0", "1.1", "1.2", "1.3" (for HTTPS only)     |
| `certificate_profile` | str     | No       | Certificate profile name (for HTTPS only)                     |

### Provider Dictionary Attributes

| Attribute       | Type | Required | Default | Description                      |
| --------------- | ---- | -------- | ------- | -------------------------------- |
| `client_id`     | str  | Yes      |         | Client ID for authentication     |
| `client_secret` | str  | Yes      |         | Client secret for authentication |
| `tsg_id`        | str  | Yes      |         | Tenant Service Group ID          |
| `log_level`     | str  | No       | "INFO"  | Log level for the SDK            |

## 05. Exceptions

| Exception                    | Description                          |
| ---------------------------- | ------------------------------------ |
| `InvalidObjectError`         | Invalid profile data or format       |
| `NameNotUniqueError`         | Profile name already exists          |
| `ObjectNotPresentError`      | Profile not found                    |
| `MissingQueryParameterError` | Missing required parameters          |
| `AuthenticationError`        | Authentication failed                |
| `ServerError`                | Internal server error                |
| `InvalidServerConfigError`   | Invalid server configuration         |

## 06. Basic Configuration

The HTTP Server Profiles module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic HTTP Server Profile Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure an HTTP server profile exists
      cdot65.scm.http_server_profiles:
        provider: "{{ provider }}"
        name: "test-http-profile"
        description: "Basic HTTP server profile"
        server:
          - name: "primary-server"
            address: "10.0.0.1"
            protocol: "HTTP"
            port: 8080
            http_method: "GET"
        folder: "Texas"
        state: "present"
```

## 07. Usage Examples

### Creating HTTP Server Profiles

HTTP server profiles can be created with different server configurations and protocols to meet various logging and communication requirements.

### Basic HTTP Server Profile

This example creates a simple HTTP server profile with a single HTTP server.

```yaml
- name: Create a basic HTTP server profile
  cdot65.scm.http_server_profiles:
    provider: "{{ provider }}"
    name: "test-http-profile"
    description: "Test HTTP server profile"
    server:
      - name: "primary-server"
        address: "10.0.0.1"
        protocol: "HTTP"
        port: 8080
        http_method: "GET"
    folder: "Texas"
    state: "present"
```

### HTTPS Server Profile

This example creates an HTTPS server profile with TLS configuration for secure communication.

```yaml
- name: Create an HTTPS server profile
  cdot65.scm.http_server_profiles:
    provider: "{{ provider }}"
    name: "secure-profile"
    description: "Secure HTTPS server profile"
    server:
      - name: "secure-server"
        address: "logs.example.com"
        protocol: "HTTPS"
        port: 443
        tls_version: "1.2"
        http_method: "POST"
        certificate_profile: "default-certificate-profile"
    tag_registration: true
    folder: "Texas"
    state: "present"
```

### Multiple Servers Configuration

This example creates an HTTP server profile with multiple server configurations for redundancy.

```yaml
- name: Create an HTTP server profile with multiple servers
  cdot65.scm.http_server_profiles:
    provider: "{{ provider }}"
    name: "redundant-profile"
    description: "HTTP server profile with multiple servers"
    server:
      - name: "primary-server"
        address: "10.0.0.1"
        protocol: "HTTP"
        port: 8080
        http_method: "POST"
      - name: "backup-server"
        address: "10.0.0.2"
        protocol: "HTTP"
        port: 8080
        http_method: "POST"
    folder: "Texas"
    state: "present"
```

### Updating HTTP Server Profiles

This example updates an existing HTTP server profile with modified server configurations.

```yaml
- name: Update an existing HTTP server profile
  cdot65.scm.http_server_profiles:
    provider: "{{ provider }}"
    name: "test-http-profile"
    description: "Updated HTTP server profile"
    server:
      - name: "primary-server"
        address: "10.0.0.1"
        protocol: "HTTP"
        port: 8080
        http_method: "POST"  # Changed from GET to POST
      - name: "backup-server"
        address: "10.0.0.2"
        protocol: "HTTP"
        port: 8080
        http_method: "POST"
    folder: "Texas"
    state: "present"
```

### Deleting HTTP Server Profiles

This example removes an HTTP server profile.

```yaml
- name: Delete an HTTP server profile
  cdot65.scm.http_server_profiles:
    provider: "{{ provider }}"
    name: "test-http-profile"
    folder: "Texas"
    state: "absent"
```

## 08. Managing Configuration Changes

After creating, updating, or deleting HTTP server profiles, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Texas"]
    description: "Updated HTTP server profiles"
```

## 09. Error Handling

It's important to handle potential errors when working with HTTP server profiles.

```yaml
- name: Create or update HTTP server profile with error handling
  block:
    - name: Ensure HTTP server profile exists
      cdot65.scm.http_server_profiles:
        provider: "{{ provider }}"
        name: "test-http-profile"
        description: "Test HTTP server profile"
        server:
          - name: "primary-server"
            address: "10.0.0.1"
            protocol: "HTTP"
            port: 8080
            http_method: "GET"
        folder: "Texas"
        state: "present"
      register: profile_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Texas"]
        description: "Updated HTTP server profiles"
      when: profile_result.changed
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a server configuration error
      debug:
        msg: "Please check the server configuration parameters"
      when: "'server' in ansible_failed_result.msg"
```

## 10. Best Practices

### Server Configuration

- Use descriptive server names that reflect their purpose
- Consider using FQDNs for addresses instead of IPs for better maintainability
- Choose appropriate HTTP methods based on the server's expected interface
- Configure proper TLS versions for HTTPS servers based on security requirements
- Use certificate profiles for HTTPS servers to validate certificates

### Protocol Selection

- Use HTTP for internal, trusted networks where encryption isn't required
- Choose HTTPS with appropriate TLS versions for external or sensitive communications
- Consider network security implications when selecting protocol and port
- Validate that the selected ports are open and accessible in your network

### Profile Management

- Create separate profiles for different purposes (logging, notifications, etc.)
- Document the purpose of each profile and its server configurations
- Use consistent naming conventions across profiles
- Test server connectivity before deploying to production
- Regularly review and update server configurations

### Multiple Server Configuration

- Configure multiple servers for redundancy when possible
- Consider load balancing implications when using multiple servers
- Ensure all servers in a profile use compatible configurations
- Test failover scenarios if using profiles for critical services

### Performance Considerations

- Monitor server response times and adjust configurations as needed
- Consider the impact of high-volume logging on server performance
- Test profiles under expected load conditions
- Implement appropriate error handling and retry logic in your playbooks

## 11. Related Modules

- [http_server_profiles_info](http_server_profiles_info.md) - Retrieve information about HTTP server profiles
- [log_forwarding_profile](log_forwarding_profile.md) - Configure log forwarding profiles that use HTTP server profiles
- [log_forwarding_profile_info](log_forwarding_profile_info.md) - Retrieve information about log forwarding profiles
- [syslog_server_profiles](syslog_server_profiles.md) - Configure syslog server profiles for system logging