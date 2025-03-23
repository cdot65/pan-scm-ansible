# Service Group Info Module

The `service_group_info` module allows you to retrieve information about service group objects in Strata Cloud Manager (SCM).

## Parameters

| Parameter | Type | Required | Default | Choices | Description |
|-----------|------|----------|---------|---------|-------------|
| name | string | no | | | The name of a specific service group object to retrieve. |
| gather_subset | list | no | ['config'] | ['all', 'config'] | Determines which information to gather about service groups. |
| folder | string | no | | | Filter service groups by folder container. |
| snippet | string | no | | | Filter service groups by snippet container. |
| device | string | no | | | Filter service groups by device container. |
| exact_match | boolean | no | false | | When True, only return objects defined exactly in the specified container. |
| exclude_folders | list | no | | | List of folder names to exclude from results. |
| exclude_snippets | list | no | | | List of snippet values to exclude from results. |
| exclude_devices | list | no | | | List of device values to exclude from results. |
| members | list | no | | | Filter by service members contained in the groups. |
| tags | list | no | | | Filter by tags. |
| provider | dictionary | yes | | | Authentication credentials. |

## Examples

```yaml
- name: Get information about a specific service group
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    name: "web-services"
    folder: "Texas"
  register: service_group_info

- name: List all service group objects in a folder
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_service_groups

- name: List service groups containing a specific member
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    members: ["HTTPS"]
  register: https_service_groups

- name: List service groups with specific tags
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    tags: ["Production", "Web"]
  register: tagged_service_groups

- name: List service groups with exact match and exclusions
  cdot65.scm.service_group_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_service_groups
```

## Return Values

When retrieving a specific service group (using the `name` parameter):

```json
{
  "service_group": {
    "id": "123e4567-e89b-12d3-a456-426655440000",
    "name": "web-services",
    "members": ["HTTPS", "SSH", "web-custom-service"],
    "folder": "Texas",
    "tag": ["Web", "Production"]
  }
}
```

When listing multiple service groups:

```json
{
  "service_groups": [
    {
      "id": "123e4567-e89b-12d3-a456-426655440000",
      "name": "web-services",
      "members": ["HTTPS", "SSH", "web-custom-service"],
      "folder": "Texas",
      "tag": ["Web", "Production"]
    },
    {
      "id": "234e5678-e89b-12d3-a456-426655440001",
      "name": "database-services",
      "members": ["SQL", "mysql-custom", "Oracle"],
      "folder": "Texas",
      "tag": ["Database", "Production"]
    }
  ]
}
```