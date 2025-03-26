# Security Rule Information Object

Gather information about security rule objects in Strata Cloud Manager (SCM).

## Description

Gather information about security rule objects within Strata Cloud Manager (SCM). Supports
retrieving a specific security rule by name or listing security rules with various filters. Provides
additional client-side filtering capabilities for exact matches and exclusions. Returns detailed
information about each security rule object. This is an info module that only retrieves information
and does not modify anything.

## Requirements

- Python >= 3.11
- pan-scm-sdk

## Parameters

| Parameter        | Choices/Defaults                                                                 | Comments                                                                   |
| ---------------- | -------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| name             |                                                                                  | The name of a specific security rule object to retrieve.                   |
| gather_subset    | Choices: ["all", "config"] <br> Default: ["config"]                              | Determines which information to gather about security rules.               |
| folder           |                                                                                  | Filter security rules by folder container.                                 |
| snippet          |                                                                                  | Filter security rules by snippet container.                                |
| device           |                                                                                  | Filter security rules by device container.                                 |
| rulebase         | Choices: ["pre", "post"] <br> Default: "pre"                                     | Which rulebase to query.                                                   |
| exact_match      | Default: false                                                                   | When True, only return objects defined exactly in the specified container. |
| exclude_folders  |                                                                                  | List of folder names to exclude from results.                              |
| exclude_snippets |                                                                                  | List of snippet values to exclude from results.                            |
| exclude_devices  |                                                                                  | List of device values to exclude from results.                             |
| action           | Choices: ["allow", "deny", "drop", "reset-client", "reset-server", "reset-both"] | Filter by action.                                                          |
| category         |                                                                                  | Filter by URL categories.                                                  |
| service          |                                                                                  | Filter by services.                                                        |
| application      |                                                                                  | Filter by applications.                                                    |
| destination      |                                                                                  | Filter by destinations.                                                    |
| to\_             |                                                                                  | Filter by to zones.                                                        |
| source           |                                                                                  | Filter by sources.                                                         |
| from\_           |                                                                                  | Filter by from zones.                                                      |
| tag              |                                                                                  | Filter by tags.                                                            |
| disabled         |                                                                                  | Filter by disabled status.                                                 |
| profile_setting  |                                                                                  | Filter by profile setting groups.                                          |
| log_setting      |                                                                                  | Filter by log setting.                                                     |
| provider         |                                                                                  | Authentication credentials.                                                |

## Examples

```yaml
- name: Gather Security Rule Information in Strata Cloud Manager
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

    - name: Get information about a specific security rule
      cdot65.scm.security_rule_info:
        provider: "{{ provider }}"
        name: "Allow_Web_Traffic"
        folder: "Texas"
        rulebase: "pre"
      register: rule_info

    - name: List all security rules in a folder
      cdot65.scm.security_rule_info:
        provider: "{{ provider }}"
        folder: "Texas"
        rulebase: "pre"
      register: all_rules

    - name: List only allow action security rules
      cdot65.scm.security_rule_info:
        provider: "{{ provider }}"
        folder: "Texas"
        rulebase: "pre"
        action: ["allow"]
      register: allow_rules

    - name: List security rules with specific tags
      cdot65.scm.security_rule_info:
        provider: "{{ provider }}"
        folder: "Texas"
        rulebase: "pre"
        tag: ["web", "internet"]
      register: tagged_rules

    - name: List security rules with exact match and exclusions
      cdot65.scm.security_rule_info:
        provider: "{{ provider }}"
        folder: "Texas"
        rulebase: "post"
        exact_match: true
        exclude_folders: ["All"]
        exclude_snippets: ["default"]
      register: filtered_rules

    - name: List security rules with specific source/destination
      cdot65.scm.security_rule_info:
        provider: "{{ provider }}"
        folder: "Texas"
        rulebase: "pre"
        source: ["any"]
        destination: ["Web-Servers"]
      register: web_server_rules
```

## Return Values

| Key            | Returned                   | Description                                                 |
| -------------- | -------------------------- | ----------------------------------------------------------- |
| security_rules | When name is not specified | List of security rule objects matching the filter criteria. |
| security_rule  | When name is specified     | Information about the requested security rule.              |

## Notes

- Security rules require exactly one container (folder, snippet, or device) to be specified.
- When using rulebase="post", the module will query the post-rulebase rather than the default
  pre-rulebase.
- The module supports check mode for all operations.

## Authors

- Calvin Remsburg (@cdot65)
