# Service Connections Module

## Overview

The `service_connections` module enables management of Service Connections in Palo Alto Networks Strata Cloud Manager (SCM). Service Connections allow you to securely connect your network to various cloud services and third-party providers through the Strata Cloud Manager.

## Core Methods

| Method | Description |
|--------|-------------|
| `create` | Creates a new Service Connection in SCM |
| `update` | Modifies an existing Service Connection |
| `delete` | Removes a Service Connection from SCM |
| `get` | Retrieves information about a specific Service Connection |
| `list` | Returns a list of all configured Service Connections |

## Model Attributes

| Attribute | Type | Description | Required |
|-----------|------|-------------|----------|
| `name` | String | Name of the Service Connection | Yes |
| `description` | String | Description of the Service Connection | No |
| `service_type` | String | Type of service (aws, azure, gcp, o365, etc.) | Yes |
| `service_details` | Dict | Service-specific configuration details | Yes |
| `network_locations` | List | List of Network Locations that can use this connection | No |
| `tags` | List | List of tags to apply to the Service Connection | No |

## Configuration Examples

### Creating a Service Connection for Office 365

```yaml
- name: Create Office 365 Service Connection
  cdot65.pan_scm.service_connections:
    provider: "{{ scm_provider }}"
    state: present
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
```

### Creating a Service Connection for AWS

```yaml
- name: Create AWS Service Connection
  cdot65.pan_scm.service_connections:
    provider: "{{ scm_provider }}"
    state: present
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
```

### Deleting a Service Connection

```yaml
- name: Delete Service Connection
  cdot65.pan_scm.service_connections:
    provider: "{{ scm_provider }}"
    state: absent
    name: "AWS-Connection"
```

## Usage Examples

### Complete Example

```yaml
---
- name: Service Connections Management
  hosts: localhost
  gather_facts: false
  connection: local
  
  vars:
    scm_provider:
      client_id: "{{ lookup('env', 'SCM_CLIENT_ID') }}"
      client_secret: "{{ lookup('env', 'SCM_CLIENT_SECRET') }}"
      scope: "profile tsg_id:9876"
      token_url: "{{ lookup('env', 'SCM_TOKEN_URL') }}"
  
  tasks:
    - name: Create Azure Service Connection
      cdot65.pan_scm.service_connections:
        provider: "{{ scm_provider }}"
        state: present
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
      register: connection_result
    
    - name: Display Connection Result
      debug:
        var: connection_result
    
    - name: Create Google Cloud Service Connection
      cdot65.pan_scm.service_connections:
        provider: "{{ scm_provider }}"
        state: present
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
```

## Error Handling

The module will fail with proper error messages if:

- Authentication with SCM fails
- The Service Connection already exists when trying to create it
- The Service Connection doesn't exist when trying to update or delete it
- Required parameters are missing
- Invalid service type or service-specific details are provided
- Referenced Network Locations don't exist
- Action fails due to API errors or permission issues

## Best Practices

- Use descriptive names for Service Connections that indicate the service and purpose
- Apply least privilege principles for authentication credentials
- Regularly rotate authentication credentials for security
- Use tags to categorize and organize Service Connections
- Associate Service Connections only with Network Locations that need them
- Limit services to only those needed to minimize attack surface
- Document the purpose and usage of each Service Connection
- Review Service Connections periodically to ensure they're still needed

## Related Models

- [Network Locations](network_locations.md) - Referenced by Service Connections to determine which locations can use them
- [Security Rules](security_rule.md) - Can reference Service Connections as destinations
