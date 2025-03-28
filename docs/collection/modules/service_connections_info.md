# Service Connections Information Object

## Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [Module Parameters](#module-parameters) 
4. [Requirements](#requirements)
5. [Usage Examples](#usage-examples)
6. [Return Values](#return-values)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)
9. [Related Modules](#related-modules)


Gather information about service connection objects in SCM.

## Synopsis

- Gather information about service connection objects within Strata Cloud Manager (SCM).
- Supports retrieving a specific service connection by name or listing connections with various filters.
- Provides additional client-side filtering capabilities for exact matches and exclusions.
- Returns detailed information about each service connection object.
- This is an info module that only retrieves information and does not modify anything.

## Parameters

| Parameter | Choices/Defaults | Comments |
| --------- | ---------------- | -------- |
| name | | The name of a specific service connection object to retrieve. |
| gather_subset | Choices:<br>- all<br>- config<br>Default: config | Determines which information to gather about service connections.<br>- all: gathers everything<br>- config: retrieves basic configuration |
| folder | | Filter service connections by folder container. |
| snippet | | Filter service connections by snippet container. |
| device | | Filter service connections by device container. |
| exact_match | Default: false | When True, only return objects defined exactly in the specified container. |
| exclude_folders | | List of folder names to exclude from results. |
| exclude_snippets | | List of snippet values to exclude from results. |
| exclude_devices | | List of device values to exclude from results. |
| connection_types | Choices:<br>- sase<br>- prisma<br>- panorama | Filter by connection types. |
| status | Choices:<br>- enabled<br>- disabled | Filter by connection status. |
| tags | | Filter by tags. |
| provider | | Authentication credentials.<br>Options:<br>- client_id: Client ID for authentication<br>- client_secret: Client secret for authentication<br>- tsg_id: Tenant Service Group ID<br>- log_level: Log level for the SDK (default: "INFO") |

## Examples

```yaml
- name: Gather Service Connection Information in Strata Cloud Manager
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:

    - name: Get information about a specific service connection
      cdot65.scm.service_connections_info:
        provider: "{{ provider }}"
        name: "Primary-SASE-Connection"
        folder: "Global"
      register: connection_info

    - name: List all service connection objects in a folder
      cdot65.scm.service_connections_info:
        provider: "{{ provider }}"
        folder: "Global"
      register: all_connections

    - name: List only SASE connection types
      cdot65.scm.service_connections_info:
        provider: "{{ provider }}"
        folder: "Global"
        connection_types: ["sase"]
      register: sase_connections

    - name: List connections with specific tags
      cdot65.scm.service_connections_info:
        provider: "{{ provider }}"
        folder: "Global"
        tags: ["Production", "Primary"]
      register: tagged_connections

    - name: List connections with exact match and exclusions
      cdot65.scm.service_connections_info:
        provider: "{{ provider }}"
        folder: "Global"
        exact_match: true
        exclude_folders: ["Test"]
        exclude_snippets: ["default"]
      register: filtered_connections
```

## Return Values

| Key | Returned | Description |
| --- | -------- | ----------- |
| service_connections | When name is not specified | List of service connection objects matching the filter criteria.<br>Contains: list of dictionaries with id, name, description, connection_type, status, etc. |
| service_connection | When name is specified | Information about the requested service connection.<br>Contains: id, name, description, connection_type, status, etc. |

## Authors

- Calvin Remsburg (@cdot65)
## Overview


## Core Methods


## Error Handling


## Best Practices


## Related Modules

