# Http Server Profiles Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Parameters](#parameters)
3. [Server Configuration](#server-configuration)
4. [Examples](#examples)
   - [Creating HTTP Server Profiles](#creating-http-server-profiles)
   - [Creating HTTPS Server Profiles](#creating-https-server-profiles)
   - [Updating Server Profiles](#updating-server-profiles)
   - [Deleting Server Profiles](#deleting-server-profiles)
5. [Return Values](#return-values)
6. [Status Codes](#status-codes)

## Overview

The `http_server_profiles` module manages HTTP server profile objects within Palo Alto Networks'
Strata Cloud Manager (SCM). HTTP server profiles define server configurations for services like log
forwarding. The module supports operations for creating, updating, and deleting HTTP server profiles
with various server configurations.

## Parameters

| Parameter          | Type         | Required | Description                                                               |
| ------------------ | ------------ | -------- | ------------------------------------------------------------------------- |
| `name`             | string       | Yes      | Name of the HTTP server profile (max 63 chars)                            |
| `server`           | list of dict | Yes\*    | List of server configurations (\*required when state=present)             |
| `tag_registration` | boolean      | No       | Whether to register tags on match                                         |
| `description`      | string       | No       | Description of the HTTP server profile                                    |
| `format`           | dict         | No       | Format settings for different log types                                   |
| `folder`           | string       | Yes\*\*  | The folder in which the resource is defined (\*\*one container required)  |
| `snippet`          | string       | Yes\*\*  | The snippet in which the resource is defined (\*\*one container required) |
| `device`           | string       | Yes\*\*  | The device in which the resource is defined (\*\*one container required)  |
| `provider`         | dict         | Yes      | Authentication credentials (see [Provider](#provider))                    |
| `state`            | string       | Yes      | Desired state: 'present' or 'absent'                                      |

### Provider

| Parameter       | Type   | Required | Description                      |
| --------------- | ------ | -------- | -------------------------------- |
| `client_id`     | string | Yes      | Client ID for authentication     |
| `client_secret` | string | Yes      | Client secret for authentication |
| `tsg_id`        | string | Yes      | Tenant Service Group ID          |
| `log_level`     | string | No       | SDK log level (default: "INFO")  |

## Server Configuration

The `server` parameter takes a list of server configurations with the following attributes:

| Parameter             | Type    | Required | Description                                                                   |
| --------------------- | ------- | -------- | ----------------------------------------------------------------------------- |
| `name`                | string  | Yes      | Server name                                                                   |
| `address`             | string  | Yes      | Server address (IP or FQDN)                                                   |
| `protocol`            | string  | Yes      | Protocol: "HTTP" or "HTTPS"                                                   |
| `port`                | integer | Yes      | Port number                                                                   |
| `http_method`         | string  | Yes      | HTTP method: "GET", "POST", "PUT", "DELETE"                                   |
| `tls_version`         | string  | No       | TLS version: "1.0", "1.1", "1.2", "1.3" (only applies when protocol is HTTPS) |
| `certificate_profile` | string  | No       | Certificate profile name (only applies when protocol is HTTPS)                |

## Examples

### Creating HTTP Server Profiles



```yaml
- name: Create an HTTP server profile with a single HTTP server
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


### Creating HTTPS Server Profiles



```yaml
- name: Create an HTTPS server profile with TLS configuration
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
    tag_registration: true
    folder: "Texas"
    state: "present"
```


### Updating Server Profiles



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
        http_method: "GET"
      - name: "backup-server"
        address: "10.0.0.2"
        protocol: "HTTP"
        port: 8080
        http_method: "GET"
    folder: "Texas"
    state: "present"
```


### Deleting Server Profiles



```yaml
- name: Delete an HTTP server profile
  cdot65.scm.http_server_profiles:
    provider: "{{ provider }}"
    name: "test-http-profile"
    folder: "Texas"
    state: "absent"
```


## Return Values

| Name                  | Type    | Description                        | Sample                                                                             |
| --------------------- | ------- | ---------------------------------- | ---------------------------------------------------------------------------------- |
| `changed`             | boolean | Whether changes were made          | `true`                                                                             |
| `http_server_profile` | dict    | Details of the HTTP server profile | `{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "test-http-profile", ...}` |

## Status Codes

| Code | Description                  |
| ---- | ---------------------------- |
| 200  | Success                      |
| 400  | Invalid input data or format |
| 401  | Authentication error         |
| 404  | Resource not found           |
| 409  | Resource name already exists |
| 500  | Server error                 |
