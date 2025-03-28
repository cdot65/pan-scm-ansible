# Service Connections Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [Module Parameters](#module-parameters)
4. [Requirements](#requirements)
5. [Usage Examples](#usage-examples)
   - [Creating Service Connectionss](#creating-service_connectionss)
   - [Updating Service Connectionss](#updating-service_connectionss)
   - [Deleting Service Connectionss](#deleting-service_connectionss)
6. [Managing Configuration Changes](#managing-configuration-changes)
7. [Return Values](#return-values)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)


Manage service connection objects in SCM.

## Synopsis

- Manage service connection objects within Strata Cloud Manager (SCM).
- Create, update, and delete service connection objects with various configuration options.
- Ensures that exactly one container type (folder, snippet, device) is provided.

## Parameters

| Parameter | Choices/Defaults | Comments |
| --------- | ---------------- | -------- |
| name | | The name of the service connection object (max 63 chars). |
| description | | Description of the service connection object (max 1023 chars). |
| connection_type | Choices:<br>- sase<br>- prisma<br>- panorama | Type of service connection. |
| status | Choices:<br>- enabled<br>- disabled | Status of the service connection. |
| auto_key_rotation | | Whether automatic key rotation is enabled. |
| tag | | List of tags associated with the service connection (max 64 chars each). |
| qos | | Quality of Service settings for the connection.<br>Options:<br>- enabled: Whether QoS is enabled for this connection<br>- profile: The QoS profile to use |
| backup_connection | | Backup connection configuration.<br>Options:<br>- connection_name: Name of the backup connection (max 63 chars)<br>- folder: Folder containing the backup connection (max 64 chars)<br>- snippet: Snippet containing the backup connection (max 64 chars)<br>- device: Device containing the backup connection (max 64 chars) |
| folder | | The folder in which the resource is defined (max 64 chars). |
| snippet | | The snippet in which the resource is defined (max 64 chars). |
| device | | The device in which the resource is defined (max 64 chars). |
| provider | | Authentication credentials.<br>Options:<br>- client_id: Client ID for authentication<br>- client_secret: Client secret for authentication<br>- tsg_id: Tenant Service Group ID<br>- log_level: Log level for the SDK (default: "INFO") |
| state | Choices:<br>- present<br>- absent | Desired state of the service connection object. |

## Examples

```yaml
- name: Manage Service Connection Objects in Strata Cloud Manager
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

    - name: Create a basic service connection
      cdot65.scm.service_connections:
        provider: "{{ provider }}"
        name: "Test_Service_Connection"
        description: "A test service connection"
        connection_type: "sase"
        status: "enabled"
        folder: "Global"
        tag: ["Network", "Primary"]
        state: "present"

    - name: Create a service connection with QoS settings
      cdot65.scm.service_connections:
        provider: "{{ provider }}"
        name: "QoS_Service_Connection"
        description: "Service connection with QoS"
        connection_type: "sase"
        status: "enabled"
        folder: "Global"
        qos:
          enabled: true
          profile: "default"
        state: "present"

    - name: Create a service connection with backup connection
      cdot65.scm.service_connections:
        provider: "{{ provider }}"
        name: "Backup_Service_Connection"
        description: "Service connection with backup"
        connection_type: "prisma"
        status: "enabled"
        folder: "Global"
        auto_key_rotation: true
        backup_connection:
          connection_name: "Backup Connection"
          folder: "Global"
        state: "present"

    - name: Update a service connection
      cdot65.scm.service_connections:
        provider: "{{ provider }}"
        name: "Test_Service_Connection"
        description: "Updated description for test connection"
        connection_type: "sase"
        status: "disabled"
        folder: "Global"
        tag: ["Network", "Primary", "Updated"]
        state: "present"

    - name: Delete service connection
      cdot65.scm.service_connections:
        provider: "{{ provider }}"
        name: "Test_Service_Connection"
        folder: "Global"
        state: "absent"
```

## Return Values

| Key | Returned | Description |
| --- | -------- | ----------- |
| changed | Always | Whether any changes were made. |
| service_connection | When state is present | Details about the service connection object.<br>Contains: id, name, description, connection_type, status, folder, tag, auto_key_rotation, etc. |

## Authors

- Calvin Remsburg (@cdot65)
## Overview


## Core Methods


## Error Handling


## Best Practices


## Related Modules


## Managing Configuration Changes

