# Internal DNS Servers Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Internal DNS Server Model Attributes](#internal-dns-server-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating Internal DNS Servers](#creating-internal-dns-servers)
    - [Basic Internal DNS Server](#basic-internal-dns-server)
    - [Multiple Domain Internal DNS Server](#multiple-domain-internal-dns-server)
    - [Updating Internal DNS Servers](#updating-internal-dns-servers)
    - [Deleting Internal DNS Servers](#deleting-internal-dns-servers)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `internal_dns_servers` Ansible module provides functionality to manage internal DNS server configurations in Palo Alto Networks' Strata Cloud Manager (SCM). These configurations define DNS servers that resolve specific domain names for your network, allowing you to control and manage DNS resolution for internal and external domains.

## Core Methods

| Method     | Description                         | Parameters                        | Return Type                       |
| ---------- | ----------------------------------- | --------------------------------- | --------------------------------- |
| `create()` | Creates a new internal DNS server   | `data: Dict[str, Any]`            | `InternalDnsServersResponseModel` |
| `update()` | Updates an existing DNS server      | `dns_server: InternalDnsServersUpdateModel` | `InternalDnsServersResponseModel` |
| `delete()` | Removes a DNS server configuration  | `object_id: str`                  | `None`                            |
| `fetch()`  | Gets a DNS server by name           | `name: str`                       | `InternalDnsServersResponseModel` |
| `list()`   | Lists DNS servers with filtering    | `**filters`                       | `List[InternalDnsServersResponseModel]` |

## Internal DNS Server Model Attributes

| Attribute     | Type      | Required | Description                                            |
| ------------- | --------- | -------- | ------------------------------------------------------ |
| `name`        | str       | Yes      | Name of the internal DNS server (max 31 chars)         |
| `domain_name` | list[str] | Yes      | List of domain names to be resolved by these DNS servers |
| `primary`     | str       | Yes      | IP address of the primary DNS server                    |
| `secondary`   | str       | No       | IP address of the secondary DNS server                  |

## Exceptions

| Exception                    | Description                       |
| ---------------------------- | --------------------------------- |
| `InvalidObjectError`         | Invalid DNS server data or format |
| `NameNotUniqueError`         | DNS server name already exists    |
| `ObjectNotPresentError`      | DNS server not found              |
| `MissingQueryParameterError` | Missing required parameters       |
| `AuthenticationError`        | Authentication failed             |
| `ServerError`                | Internal server error             |

## Basic Configuration

The Internal DNS Servers module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Internal DNS Server Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure an internal DNS server exists
      cdot65.scm.internal_dns_servers:
        provider: "{{ provider }}"
        name: "main-dns-server"
        domain_name: ["example.com", "internal.example.com"]
        primary: "192.168.1.10"
        secondary: "192.168.1.11"
        state: "present"
```

## Usage Examples

### Creating Internal DNS Servers

Internal DNS servers can be configured to resolve specific domain names using primary and optional secondary DNS servers.

### Basic Internal DNS Server

This example creates a simple internal DNS server with a primary DNS server for a single domain.

```yaml
- name: Create a basic internal DNS server
  cdot65.scm.internal_dns_servers:
    provider: "{{ provider }}"
    name: "corp-dns-server"
    domain_name: ["company.local"]
    primary: "10.10.10.10"
    state: "present"
```

### Multiple Domain Internal DNS Server

This example creates an internal DNS server configuration that handles multiple domains with both primary and secondary servers.

```yaml
- name: Create an internal DNS server with multiple domains
  cdot65.scm.internal_dns_servers:
    provider: "{{ provider }}"
    name: "multi-domain-dns"
    domain_name: 
      - "example.com"
      - "internal.example.com"
      - "test.example.com"
    primary: "192.168.1.10"
    secondary: "192.168.1.11"
    state: "present"
```

### Updating Internal DNS Servers

This example updates an existing internal DNS server with an additional domain and a different secondary server.

```yaml
- name: Update an internal DNS server
  cdot65.scm.internal_dns_servers:
    provider: "{{ provider }}"
    name: "corp-dns-server"
    domain_name: 
      - "company.local"
      - "new-domain.company.local"
    primary: "10.10.10.10"
    secondary: "10.10.10.11"
    state: "present"
```

### Deleting Internal DNS Servers

This example removes an internal DNS server configuration.

```yaml
- name: Delete an internal DNS server
  cdot65.scm.internal_dns_servers:
    provider: "{{ provider }}"
    name: "corp-dns-server"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting internal DNS server configurations, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    description: "Updated internal DNS server configurations"
```

## Error Handling

It's important to handle potential errors when working with internal DNS server configurations.

```yaml
- name: Create or update internal DNS server with error handling
  block:
    - name: Ensure internal DNS server exists
      cdot65.scm.internal_dns_servers:
        provider: "{{ provider }}"
        name: "main-dns-server"
        domain_name: ["example.com", "internal.example.com"]
        primary: "192.168.1.10"
        secondary: "192.168.1.11"
        state: "present"
      register: dns_server_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        description: "Updated internal DNS server configurations"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```

## Best Practices

### DNS Server Configuration

- Provide both primary and secondary DNS servers for redundancy
- Use reliable and stable internal DNS servers with good performance
- Consider geographic proximity to minimize latency
- Regularly verify DNS server health and performance

### Domain Name Management

- Group related domains under a single DNS server configuration
- Document the purpose of each domain in your configuration
- Include all required domains to avoid resolution failures
- Use consistent naming patterns for related domains

### IP Address Management

- Use static IP addresses for DNS servers
- Document DNS server information in your inventory
- Ensure DNS servers are properly secured
- Implement monitoring for DNS server availability

### Configuration Management

- Develop a consistent naming convention for DNS server configurations
- Document the purpose of each DNS server configuration
- Test DNS resolution before implementing in production
- Implement proper change management for DNS server modifications

## Related Modules

- [internal_dns_servers_info](internal_dns_servers_info.md) - Retrieve information about internal DNS servers
- [http_server_profiles](http_server_profiles.md) - Manage HTTP server profiles for additional service configuration
- [syslog_server_profiles](syslog_server_profiles.md) - Manage syslog server profiles for logging configuration