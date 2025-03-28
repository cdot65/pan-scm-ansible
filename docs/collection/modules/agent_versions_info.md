# agent_versions_info

Gather information about agent versions in Strata Cloud Manager (SCM).

## Synopsis

- This module enables users to gather information about agent versions within Palo Alto Networks Strata Cloud Manager (SCM).
- It provides various filtering options to find specific agent versions.
- It supports retrieving detailed information about GlobalProtect, NGFW, SD-WAN, and CPE agent versions.
- This is an info module that only retrieves information and does not modify anything.

## Requirements (on host that executes module)

- Python >= 3.9
- pan-scm-sdk

## Parameters

| Parameter | Type | Required | Default | Choices | Comments |
|-----------|------|----------|---------|---------|----------|
| name | str | no | | | The name of a specific agent to retrieve information about. |
| version | str | no | | | The specific version to retrieve information about. |
| type | list | no | | prisma_access, ngfw, sdwan, cpe | Filter agent versions by their type. |
| status | list | no | | recommended, current, deprecated, obsolete | Filter agent versions by their status. |
| platform | list | no | | | Filter agent versions by platform compatibility. |
| features | list | no | | | Filter agent versions by supported features. |
| gather_subset | list | no | config | all, config | Determines which information to gather about agent versions. |
| exact_match | bool | no | false | | When True, only return objects with exact matching criteria. |
| exact_version | bool | no | false | | When True, require exact version match rather than prefix match. |
| provider | dict | yes | | | Authentication credentials for SCM. |
| provider.client_id | str | yes | | | Client ID for authentication to SCM. |
| provider.client_secret | str | yes | | | Client secret for authentication to SCM. |
| provider.tsg_id | str | yes | | | Tenant Service Group ID for SCM. |
| provider.log_level | str | no | INFO | | Log level for the SDK. |
| testmode | bool | no | false | | Enable test mode for CI/CD environments (no API calls). |
| test_timestamp | str | no | | | Timestamp to use for test mode data generation. |

## Examples

```yaml
- name: Gather Agent Version Information in Strata Cloud Manager
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
    - name: Get information about all agent versions
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
      register: all_versions

    - name: Get information about a specific version
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
        version: "5.3.0"
      register: specific_version

    - name: List all recommended versions
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
        status: ["recommended"]
      register: recommended_versions

    - name: List Prisma Access agent versions
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
        type: ["prisma_access"]
      register: prisma_versions

    - name: List versions with exact matching
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
        version: "5.3.0"
        exact_match: true
        exact_version: true
      register: exact_versions

    - name: List versions by platform
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
        platform: ["linux_x86_64"]
      register: platform_versions

    - name: List versions supporting specific features
      cdot65.scm.agent_versions_info:
        provider: "{{ provider }}"
        features: ["ipsec", "ssl_vpn"]
      register: feature_versions
```

## Return Values

| Name | Description | Returned | Type | Sample |
|------|-------------|----------|------|--------|
| agent_versions | List of agent versions matching the filter criteria. | when version is not specified | list | See below |
| agent_version | Information about the requested agent version. | when version is specified | dict | See below |

Example return value:

```json
{
    "agent_versions": [
        {
            "id": "123e4567-e89b-12d3-a456-426655440000",
            "name": "Prisma Access Agent",
            "version": "5.3.0",
            "type": "prisma_access",
            "status": "recommended",
            "platform": "linux_x86_64",
            "features_enabled": ["ipsec", "ssl_vpn", "globalprotect"],
            "release_date": "2023-06-15",
            "end_of_support_date": "2024-06-15",
            "release_notes_url": "https://example.com/release-notes/5.3.0"
        },
        {
            "id": "234e5678-e89b-12d3-a456-426655440001",
            "name": "SD-WAN Agent",
            "version": "2.1.0",
            "type": "sdwan",
            "status": "current",
            "platform": "linux_arm64",
            "features_enabled": ["qos", "traffic_shaping"],
            "release_date": "2023-05-20",
            "end_of_support_date": "2024-05-20",
            "release_notes_url": "https://example.com/release-notes/2.1.0"
        }
    ]
}
```

## Authors

- Calvin Remsburg (@cdot65)