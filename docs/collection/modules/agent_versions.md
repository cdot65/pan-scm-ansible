# Agent Versions Configuration Object

## Table of Contents

- [Agent Versions Configuration Object](#agent-versions-configuration-object)
  - [Table of Contents](#table-of-contents)
  - [Synopsis](#synopsis)
  - [Requirements (on host that executes module)](#requirements-on-host-that-executes-module)
  - [Parameters](#parameters)
  - [Examples](#examples)
  - [Return Values](#return-values)
  - [Authors](#authors)


Manage agent versions in Strata Cloud Manager (SCM).

## Synopsis

- This module enables users to manage agent versions within Palo Alto Networks Strata Cloud Manager (SCM).
- It provides functionality for creating, updating, and retrieving agent version information.
- It supports various filter options to find specific agent versions.
- The module handles GlobalProtect, NGFW, SD-WAN, and CPE agent versions.

## Requirements (on host that executes module)

- Python >= 3.9
- pan-scm-sdk

## Parameters

| Parameter | Type | Required | Default | Choices | Comments |
|-----------|------|----------|---------|---------|----------|
| name | str | no | | | The name of a specific agent to filter by. |
| version | str | no | | | The specific version to filter by. |
| type | str | no | | prisma_access, ngfw, sdwan, cpe | The type of agent to filter by. |
| status | str | no | | recommended, current, deprecated, obsolete | The status of agent versions to filter by. |
| platform | str | no | | | The platform to filter by (e.g., 'linux_x86_64'). |
| features_enabled | list | no | | | List of features that must be enabled in the agent versions. |
| release_date | str | no | | | Filter by release date (format: YYYY-MM-DD). |
| end_of_support_date | str | no | | | Filter by end of support date (format: YYYY-MM-DD). |
| release_notes_url | str | no | | | Release notes URL for the agent version. |
| gather_subset | list | no | config | all, config | Determines which information to gather about agent versions. |
| exact_match | bool | no | false | | When True, require exact matches on filter criteria. |
| exact_version | bool | no | false | | When True, require exact version match rather than prefix match. |
| provider | dict | yes | | | Authentication credentials for SCM. |
| provider.client_id | str | yes | | | Client ID for authentication to SCM. |
| provider.client_secret | str | yes | | | Client secret for authentication to SCM. |
| provider.tsg_id | str | yes | | | Tenant Service Group ID for SCM. |
| provider.log_level | str | no | INFO | | Log level for the SDK. |
| state | str | yes | | present, absent | Desired state of the agent version configuration. |
| testmode | bool | no | false | | Enable test mode for CI/CD environments (no API calls). |

## Examples

```yaml
- name: Manage Agent Versions in Strata Cloud Manager
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
    # Information retrieval examples
    - name: Get information about all agent versions
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        state: present
      register: all_versions

    - name: Get information about a specific version
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        version: "1.2.3"
        state: present
      register: specific_version

    - name: List all recommended versions
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        status: "recommended"
        state: present
      register: recommended_versions

    - name: List Prisma Access agent versions
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        type: "prisma_access"
        state: present
      register: prisma_versions

    # Configuration examples
    - name: Set version to recommended status
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        name: "GlobalProtect Agent"
        version: "5.3.0"
        status: "recommended"
        state: present
      register: update_result

    - name: Update agent version metadata
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        name: "GlobalProtect Agent"
        version: "5.3.0"
        release_date: "2023-06-15"
        end_of_support_date: "2024-06-15"
        release_notes_url: "https://example.com/release-notes/5.3.0"
        features_enabled:
          - ipsec
          - ssl_vpn
          - globalprotect
        state: present
      register: metadata_result

    - name: Remove agent version
      cdot65.scm.agent_versions:
        provider: "{{ provider }}"
        name: "GlobalProtect Agent"
        version: "5.2.7"
        state: absent
      register: remove_result
```

## Return Values

| Name | Description | Returned | Type | Sample |
|------|-------------|----------|------|--------|
| agent_versions | List of agent versions matching the filter criteria. | when state is present and no specific name/version is specified | list | See below |
| agent_version | Information about the specific agent version. | when state is present and a specific name/version is specified | dict | See below |
| changed | Whether any changes were made. | always | bool | true |

Example return value:

```json
{
    "agent_versions": [
        {
            "id": "123e4567-e89b-12d3-a456-426655440000",
            "name": "Prisma Access Agent",
            "version": "1.2.3",
            "type": "prisma_access",
            "status": "recommended",
            "platform": "linux_x86_64",
            "features_enabled": ["ipsec", "ssl_vpn", "globalprotect"],
            "release_date": "2023-01-15",
            "end_of_support_date": "2024-01-15",
            "release_notes_url": "https://example.com/release-notes/1.2.3"
        },
        {
            "id": "234e5678-e89b-12d3-a456-426655440001",
            "name": "SD-WAN Agent",
            "version": "2.1.0",
            "type": "sdwan",
            "status": "current",
            "platform": "linux_arm64",
            "features_enabled": ["qos", "traffic_shaping"],
            "release_date": "2023-02-20",
            "end_of_support_date": "2024-02-20",
            "release_notes_url": "https://example.com/release-notes/2.1.0"
        }
    ],
    "changed": false
}
```

## Authors

- Calvin Remsburg (@cdot65)
