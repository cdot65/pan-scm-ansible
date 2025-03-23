# Service Info Module

The `service_info` module allows you to retrieve information about service objects in Strata Cloud Manager (SCM).

## Parameters

| Parameter | Type | Required | Default | Choices | Description |
|-----------|------|----------|---------|---------|-------------|
| name | string | no | | | The name of a specific service object to retrieve. |
| gather_subset | list | no | ['config'] | ['all', 'config'] | Determines which information to gather about services. |
| folder | string | no | | | Filter services by folder container. |
| snippet | string | no | | | Filter services by snippet container. |
| device | string | no | | | Filter services by device container. |
| exact_match | boolean | no | false | | When True, only return objects defined exactly in the specified container. |
| exclude_folders | list | no | | | List of folder names to exclude from results. |
| exclude_snippets | list | no | | | List of snippet values to exclude from results. |
| exclude_devices | list | no | | | List of device values to exclude from results. |
| protocol_types | list | no | | ['tcp', 'udp'] | Filter by protocol types. |
| tags | list | no | | | Filter by tags. |
| provider | dictionary | yes | | | Authentication credentials. |

## Examples

```yaml
- name: Get information about a specific service
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    name: "web-service"
    folder: "Texas"
  register: service_info

- name: List all service objects in a folder
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_services

- name: List only TCP service objects
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    folder: "Texas"
    protocol_types: ["tcp"]
  register: tcp_services

- name: List services with specific tags
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["Production", "Web"]
  register: tagged_services

- name: List services with exact match and exclusions
  cdot65.scm.service_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_services
```

## Return Values

When retrieving a specific service (using the `name` parameter):

```json
{
  "service": {
    "id": "123e4567-e89b-12d3-a456-426655440000",
    "name": "web-service",
    "description": "Web service ports",
    "protocol": {
      "tcp": {
        "port": "80,443",
        "override": {
          "timeout": 30,
          "halfclose_timeout": 15
        }
      }
    },
    "folder": "Texas",
    "tag": ["Web", "Production"]
  }
}
```

When listing multiple services:

```json
{
  "services": [
    {
      "id": "123e4567-e89b-12d3-a456-426655440000",
      "name": "web-service",
      "description": "Web service ports",
      "protocol": {
        "tcp": {
          "port": "80,443",
          "override": {
            "timeout": 30,
            "halfclose_timeout": 15
          }
        }
      },
      "folder": "Texas",
      "tag": ["Web", "Production"]
    },
    {
      "id": "234e5678-e89b-12d3-a456-426655440001",
      "name": "dns-service",
      "description": "DNS service",
      "protocol": {
        "udp": {
          "port": "53",
          "override": {
            "timeout": 60
          }
        }
      },
      "folder": "Texas",
      "tag": ["DNS", "Network"]
    }
  ]
}
```