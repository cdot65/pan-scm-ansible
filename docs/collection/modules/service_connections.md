# Service Connections Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [Service Connections Model Attributes](#service-connections-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating Service Connections](#creating-service-connections)
    - [Office 365 Service Connection](#office-365-service-connection)
    - [AWS Service Connection](#aws-service-connection)
    - [Azure Service Connection](#azure-service-connection)
    - [GCP Service Connection](#gcp-service-connection)
    - [Updating Service Connections](#updating-service-connections)
    - [Deleting Service Connections](#deleting-service-connections)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `service_connections` Ansible module provides functionality to manage Service Connections in
Palo Alto Networks' Strata Cloud Manager (SCM). Service Connections allow you to securely connect
your network to various cloud services and third-party providers, enabling direct access to SaaS
applications, cloud resources, and other internet-based services with appropriate security controls.

## Core Methods

| Method     | Description                      | Parameters                                 | Return Type                            |
| ---------- | -------------------------------- | ------------------------------------------ | -------------------------------------- |
| `create()` | Creates a new Service Connection | `data: Dict[str, Any]`                     | `ServiceConnectionResponseModel`       |
| `update()` | Updates an existing connection   | `connection: ServiceConnectionUpdateModel` | `ServiceConnectionResponseModel`       |
| `delete()` | Removes a connection             | `object_id: str`                           | `None`                                 |
| `fetch()`  | Gets a connection by name        | `name: str`, `container: str`              | `ServiceConnectionResponseModel`       |
| `list()`   | Lists connections with filtering | `folder: str`, `**filters`                 | `List[ServiceConnectionResponseModel]` |

## Service Connections Model Attributes

| Attribute           | Type | Required | Description                                            |
| ------------------- | ---- | -------- | ------------------------------------------------------ |
| `name`              | str  | Yes      | Name of the Service Connection                         |
| `description`       | str  | No       | Description of the Service Connection                  |
| `service_type`      | str  | Yes      | Type of service (aws, azure, gcp, o365, etc.)          |
| `service_details`   | dict | Yes      | Service-specific configuration details                 |
| `network_locations` | list | No       | List of Network Locations that can use this connection |
| `tags`              | list | No       | List of tags to apply to the Service Connection        |

### Service Details Attributes (O365)

| Attribute  | Type | Required | Description                                                 |
| ---------- | ---- | -------- | ----------------------------------------------------------- |
| `region`   | str  | Yes      | Region for O365 (worldwide, china, etc.)                    |
| `services` | list | Yes      | O365 services to enable (exchange, sharepoint, skype, etc.) |

### Service Details Attributes (AWS)

| Attribute        | Type | Required | Description                                 |
| ---------------- | ---- | -------- | ------------------------------------------- |
| `region`         | str  | Yes      | AWS region (us-east-1, eu-west-1, etc.)     |
| `services`       | list | Yes      | AWS services to enable (s3, dynamodb, etc.) |
| `authentication` | dict | Yes      | Authentication details for AWS              |

## Exceptions

| Exception                    | Description                       |
| ---------------------------- | --------------------------------- |
| `InvalidObjectError`         | Invalid connection data or format |
| `NameNotUniqueError`         | Connection name already exists    |
| `ObjectNotPresentError`      | Connection not found              |
| `MissingQueryParameterError` | Missing required parameters       |
| `AuthenticationError`        | Authentication failed             |
| `ServerError`                | Internal server error             |
| `ReferenceNotFoundError`     | Referenced location doesn't exist |

## Basic Configuration

The Service Connections module requires proper authentication credentials to access the Strata Cloud
Manager API.

```yaml
- name: Basic Service Connection Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure Office 365 service connection exists
      cdot65.scm.service_connections:
        provider: "{{ provider }}"
        name: "O365-Connection"
        description: "Service connection for Office 365 direct access"
        service_type: "o365"
        service_details:
          region: "worldwide"
          services:
            - "exchange"
            - "sharepoint"
        network_locations:
          - "primary-branch"
        state: "present"
```

## Usage Examples

### Creating Service Connections

Service Connections allow your network to securely access various cloud services and SaaS
applications.

### Office 365 Service Connection

This example creates a service connection for Office 365 to enable direct access to Exchange,
SharePoint, and Skype.

```yaml
- name: Create Office 365 Service Connection
  cdot65.scm.service_connections:
    provider: "{{ provider }}"
    name: "O365-Connection"
    description: "Service connection for Office 365 direct access"
    service_type: "o365"
    service_details:
      region: "worldwide"
      services:
        - "exchange"
        - "sharepoint"
        - "skype"
    network_locations:
      - "primary-branch"
      - "secondary-branch"
    tags: 
      - "cloud-services"
      - "productivity"
    state: "present"
```

### AWS Service Connection

This example creates a service connection for AWS services using role-based authentication.

```yaml
- name: Create AWS Service Connection
  cdot65.scm.service_connections:
    provider: "{{ provider }}"
    name: "AWS-Connection"
    description: "Service connection for AWS services"
    service_type: "aws"
    service_details:
      region: "us-east-1"
      services:
        - "s3"
        - "dynamodb"
      authentication:
        type: "role"
        role_arn: "arn:aws:iam::123456789012:role/PaloAltoAccess"
    network_locations:
      - "datacenter-1"
    tags:
      - "cloud-services"
      - "aws"
    state: "present"
```

### Azure Service Connection

This example creates a service connection for Azure services using service principal authentication.

```yaml
- name: Create Azure Service Connection
  cdot65.scm.service_connections:
    provider: "{{ provider }}"
    name: "Azure-Services"
    description: "Connection to Azure cloud services"
    service_type: "azure"
    service_details:
      region: "eastus"
      services:
        - "storage"
        - "sql"
      authentication:
        type: "service_principal"
        tenant_id: "{{ azure_tenant_id }}"
        client_id: "{{ azure_client_id }}"
        client_secret: "{{ azure_client_secret }}"
    network_locations:
      - "branch-office-1"
      - "branch-office-2"
    tags:
      - "cloud-services"
      - "azure"
    state: "present"
```

### GCP Service Connection

This example creates a service connection for Google Cloud Platform services using service account
authentication.

```yaml
- name: Create Google Cloud Service Connection
  cdot65.scm.service_connections:
    provider: "{{ provider }}"
    name: "GCP-Services"
    description: "Connection to Google Cloud Platform services"
    service_type: "gcp"
    service_details:
      region: "us-central1"
      services:
        - "storage"
        - "bigquery"
      authentication:
        type: "service_account"
        key_file: "{{ gcp_key_json | from_json }}"
    network_locations:
      - "branch-office-3"
    tags:
      - "cloud-services"
      - "gcp"
    state: "present"
```

### Updating Service Connections

This example updates an existing service connection with new settings.

```yaml
- name: Update Office 365 Service Connection
  cdot65.scm.service_connections:
    provider: "{{ provider }}"
    name: "O365-Connection"
    description: "Updated service connection for Office 365"
    service_type: "o365"
    service_details:
      region: "worldwide"
      services:
        - "exchange"
        - "sharepoint"
        - "teams"  # Updated to include Teams instead of Skype
    network_locations:
      - "primary-branch"
      - "secondary-branch"
      - "new-branch"  # Added a new location
    tags: 
      - "cloud-services"
      - "productivity"
      - "updated"  # Added a new tag
    state: "present"
```

### Deleting Service Connections

This example removes a service connection that is no longer needed.

```yaml
- name: Delete Service Connection
  cdot65.scm.service_connections:
    provider: "{{ provider }}"
    name: "AWS-Connection"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting service connections, you need to commit your changes to apply
them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    description: "Updated service connection configurations"
```

## Error Handling

It's important to handle potential errors when working with service connections.

```yaml
- name: Create or update service connection with error handling
  block:
    - name: Ensure service connection exists
      cdot65.scm.service_connections:
        provider: "{{ provider }}"
        name: "O365-Connection"
        description: "Service connection for Office 365 direct access"
        service_type: "o365"
        service_details:
          region: "worldwide"
          services:
            - "exchange"
            - "sharepoint"
        network_locations:
          - "primary-branch"
        state: "present"
      register: connection_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        description: "Updated service connection configurations"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Check if referenced location doesn't exist
      debug:
        msg: "Check if the referenced network locations exist."
      when: "'referenced object does not exist' in ansible_failed_result.msg"
```

## Best Practices

### Connection Design

- Use descriptive names for Service Connections that indicate the service and purpose
- Include specific details in descriptions for easier administration
- Configure only the services that are needed to minimize attack surface
- Document purpose and requirements for each connection
- Follow a consistent naming convention for easier management

### Authentication Security

- Apply least privilege principles for authentication credentials
- Use role-based authentication when possible instead of static credentials
- Regularly rotate authentication credentials for security
- Store sensitive authentication information in secure vaults
- Use service principals with minimum required permissions

### Network Location Management

- Associate Service Connections only with Network Locations that need them
- Use logical groupings of locations for similar access requirements
- Document which locations use which service connections
- Regularly review location associations to ensure they're still needed
- Test connectivity from each location after configuration changes

### Service Selection

- Limit services to only those needed to minimize attack surface
- Document the business purpose for each service
- Group related services into common connections
- Monitor service usage to identify unused services
- Regularly audit service configurations against security policies

### Management and Maintenance

- Review Service Connections periodically to ensure they're still needed
- Document dependencies between services and applications
- Implement change management procedures for connection modifications
- Test changes in pre-production environments before applying to production
- Create automated testing to validate connectivity after changes

## Related Modules

- [network_locations](network_locations.md) - Manage network locations that can use service
  connections
- [security_rule](security_rule.md) - Configure security policies that reference service connections
- [remote_networks](remote_networks.md) - Configure remote networks that may use service connections
- [tag](tag.md) - Manage tags that can be applied to service connections
- [security_zone](security_zone.md) - Configure security zones for network traffic control
