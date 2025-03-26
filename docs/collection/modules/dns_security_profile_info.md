# Dns Security Profile Information Object

Gather information about DNS security profile objects in Strata Cloud Manager (SCM).

## Synopsis

- Gather information about DNS security profile objects within Strata Cloud Manager (SCM).
- Supports retrieving a specific DNS security profile by name or listing profiles with various
  filters.
- Provides additional client-side filtering capabilities for exact matches and exclusions.
- Returns detailed information about each DNS security profile object.
- This is an info module that only retrieves information and does not modify anything.

## Parameters

| Parameter               | Choices/Defaults                                                    | Comments                                                                                                                                                               |
| ----------------------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name                    |                                                                     | The name of a specific DNS security profile to retrieve.                                                                                                               |
| gather_subset           | Default: ['config']<br>Options:<ul><li>all</li><li>config</li></ul> | Determines which information to gather about DNS security profiles.<br>- C(all) gathers everything.<br>- C(config) is the default which retrieves basic configuration. |
| folder                  |                                                                     | Filter DNS security profiles by folder container.                                                                                                                      |
| snippet                 |                                                                     | Filter DNS security profiles by snippet container.                                                                                                                     |
| device                  |                                                                     | Filter DNS security profiles by device container.                                                                                                                      |
| exact_match             | Default: false                                                      | When True, only return objects defined exactly in the specified container.                                                                                             |
| exclude_folders         |                                                                     | List of folder names to exclude from results.                                                                                                                          |
| exclude_snippets        |                                                                     | List of snippet values to exclude from results.                                                                                                                        |
| exclude_devices         |                                                                     | List of device values to exclude from results.                                                                                                                         |
| dns_security_categories |                                                                     | Filter by DNS security categories.                                                                                                                                     |
| provider                |                                                                     | Authentication credentials.                                                                                                                                            |
| provider.client_id      |                                                                     | Client ID for authentication.                                                                                                                                          |
| provider.client_secret  |                                                                     | Client secret for authentication.                                                                                                                                      |
| provider.tsg_id         |                                                                     | Tenant Service Group ID.                                                                                                                                               |
| provider.log_level      | Default: "INFO"                                                     | Log level for the SDK.                                                                                                                                                 |

## Examples

```yaml
---
- name: Gather DNS Security Profile Information in Strata Cloud Manager
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

    - name: Get information about a specific DNS security profile
      cdot65.scm.dns_security_profile_info:
        provider: "{{ provider }}"
        name: "test-dns-security"
        folder: "Texas"
      register: profile_info

    - name: List all DNS security profiles in a folder
      cdot65.scm.dns_security_profile_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: all_profiles

    - name: List DNS security profiles with specific security categories
      cdot65.scm.dns_security_profile_info:
        provider: "{{ provider }}"
        folder: "Texas"
        dns_security_categories: ["command-and-control", "malware"]
      register: category_profiles

    - name: List profiles with exact match and exclusions
      cdot65.scm.dns_security_profile_info:
        provider: "{{ provider }}"
        folder: "Texas"
        exact_match: true
        exclude_folders: ["All"]
        exclude_snippets: ["default"]
      register: filtered_profiles
```

## Return Values

| Key                   | Returned                            | Description                                                        |
| --------------------- | ----------------------------------- | ------------------------------------------------------------------ |
| dns_security_profiles | success, when name is not specified | List of DNS security profile objects matching the filter criteria. |
| dns_security_profile  | success, when name is specified     | Information about the requested DNS security profile.              |

## Notes

- This module requires the pan-scm-sdk Python package to interact with the SCM API.
- Authentication is handled via the provider parameter which must include client_id, client_secret,
  and tsg_id.
- If retrieving a specific DNS security profile by name, the container (folder, snippet, or device)
  must also be specified.
- When listing DNS security profiles, various filtering options are available including
  container-based filters and DNS security category filters.
- The return value will be either a single DNS security profile (when using the name parameter) or a
  list of profiles (when listing).

## Authors

- Calvin Remsburg (@cdot65)
