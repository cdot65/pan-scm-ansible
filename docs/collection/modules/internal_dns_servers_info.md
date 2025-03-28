# Internal DNS Servers Information Object

## Table of Contents

- [Internal DNS Servers Information Object](#internal-dns-servers-information-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [Internal DNS Server Info Parameters](#internal-dns-server-info-parameters)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Getting Information about a Specific Internal DNS Server](#getting-information-about-a-specific-internal-dns-server)
    - [Listing All Internal DNS Servers](#listing-all-internal-dns-servers)
    - [Processing DNS Server Results](#processing-dns-server-results)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Efficient Querying](#efficient-querying)
    - [Result Processing](#result-processing)
    - [Error Handling](#error-handling-1)
    - [Integration with Other Modules](#integration-with-other-modules)
    - [Performance Considerations](#performance-considerations)
  - [Related Modules](#related-modules)

## Overview

The `internal_dns_servers_info` Ansible module provides functionality to gather information about internal DNS server configurations in Palo Alto Networks' Strata Cloud Manager (SCM). This is an info module that allows fetching details about specific DNS server configurations or listing all DNS servers without making any changes to the system.

## Core Methods

| Method    | Description                          | Parameters             | Return Type                            |
| --------- | ------------------------------------ | ---------------------- | -------------------------------------- |
| `fetch()` | Gets a specific DNS server by name   | `name: str`            | `InternalDnsServersResponseModel`      |
| `list()`  | Lists DNS servers with filtering     | `**filters`            | `List[InternalDnsServersResponseModel]` |

## Internal DNS Server Info Parameters

| Parameter        | Type | Required | Description                                                |
| ---------------- | ---- | -------- | ---------------------------------------------------------- |
| `name`           | str  | No       | Name of a specific internal DNS server to retrieve          |
| `gather_subset`  | list | No       | Determines which information to gather (default: config)    |

## Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid request data or format |
| `MissingQueryParameterError` | Missing required parameters    |
| `ObjectNotPresentError`      | DNS server not found           |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The Internal DNS Servers Info module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic Internal DNS Server Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about internal DNS servers
      cdot65.scm.internal_dns_servers_info:
        provider: "{{ provider }}"
      register: dns_servers_result
      
    - name: Display retrieved internal DNS servers
      debug:
        var: dns_servers_result
```

## Usage Examples

### Getting Information about a Specific Internal DNS Server

Retrieve details about a specific internal DNS server by name.

```yaml
- name: Get information about a specific internal DNS server
  cdot65.scm.internal_dns_servers_info:
    provider: "{{ provider }}"
    name: "main-dns-server"
  register: dns_server_info
  
- name: Display internal DNS server information
  debug:
    var: dns_server_info.internal_dns_server
    
- name: Check if DNS server has multiple domains
  debug:
    msg: "DNS server has {{ dns_server_info.internal_dns_server.domain_name | length }} domains configured"
  when: dns_server_info.internal_dns_server is defined
```

### Listing All Internal DNS Servers

List all internal DNS server configurations.

```yaml
- name: List all internal DNS servers
  cdot65.scm.internal_dns_servers_info:
    provider: "{{ provider }}"
  register: all_dns_servers
  
- name: Display all internal DNS servers
  debug:
    var: all_dns_servers.internal_dns_servers
    
- name: Display count of internal DNS servers
  debug:
    msg: "Found {{ all_dns_servers.internal_dns_servers | length }} internal DNS servers"
    
- name: List names of all internal DNS servers
  debug:
    msg: "{{ all_dns_servers.internal_dns_servers | map(attribute='name') | list }}"
```

### Processing DNS Server Results

Filter and process the retrieved DNS server information.

```yaml
- name: List all internal DNS servers
  cdot65.scm.internal_dns_servers_info:
    provider: "{{ provider }}"
  register: all_dns_servers

- name: Find DNS servers with secondary DNS configured
  set_fact:
    dns_servers_with_secondary: "{{ all_dns_servers.internal_dns_servers | selectattr('secondary', 'defined') | list }}"

- name: Display DNS servers with secondary DNS
  debug:
    var: dns_servers_with_secondary

- name: Find DNS servers handling a specific domain
  set_fact:
    specific_domain_servers: "{{ all_dns_servers.internal_dns_servers | 
                              selectattr('domain_name', 'defined') | 
                              selectattr('domain_name', 'contains', 'example.com') | 
                              list }}"
  
- name: Display servers handling the specific domain
  debug:
    var: specific_domain_servers
```

## Error Handling

It's important to handle potential errors when retrieving information about internal DNS servers.

```yaml
- name: Get information about internal DNS servers with error handling
  block:
    - name: Try to retrieve information about an internal DNS server
      cdot65.scm.internal_dns_servers_info:
        provider: "{{ provider }}"
        name: "main-dns-server"
      register: info_result
      
    - name: Display internal DNS server information
      debug:
        var: info_result.internal_dns_server
        
  rescue:
    - name: Handle errors
      debug:
        msg: "Failed to retrieve internal DNS server information: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a 'not found' error
      debug:
        msg: "The specified internal DNS server does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

## Best Practices

### Efficient Querying

- When looking for a specific DNS server, use the `name` parameter for direct retrieval
- Process results in Ansible rather than making multiple API calls for filtering
- Cache results when making multiple queries for the same information

### Result Processing

- Always register the module output to a variable for later use
- Check if the expected data is present before processing it
- Use appropriate Ansible filters and tests when processing nested structures

### Error Handling

- Implement try/except blocks to handle potential errors
- Verify that DNS servers exist before attempting operations on them
- Provide meaningful error messages for troubleshooting

### Integration with Other Modules

- Use the info module to check for existing DNS servers before creating new ones
- Combine with the internal_dns_servers module for complete DNS server management
- Use the retrieved information to make decisions in your playbooks

### Performance Considerations

- Limit the data retrieved to only what's needed for your task
- Consider batching operations when processing multiple DNS servers
- Use conditional logic to minimize API calls

## Related Modules

- [internal_dns_servers](internal_dns_servers.md) - Create, update, and delete internal DNS server configurations
- [http_server_profiles_info](http_server_profiles_info.md) - Retrieve information about HTTP server profiles
- [syslog_server_profiles_info](syslog_server_profiles_info.md) - Retrieve information about syslog server profiles