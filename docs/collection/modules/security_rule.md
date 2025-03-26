# Security Rule Configuration Object

Manage security rule objects in Strata Cloud Manager (SCM).

## Description

Manage security rule objects within Strata Cloud Manager (SCM). Create, update, and delete security
rule objects with various parameters. Ensures that exactly one container type (folder, snippet,
device) is provided. Supports both pre-rulebase and post-rulebase configurations.

## Requirements

- Python >= 3.11
- pan-scm-sdk

## Parameters

| Parameter          | Choices/Defaults                                                                                       | Comments                                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| name               |                                                                                                        | The name of the security rule object.                                                                   |
| disabled           | Default: false                                                                                         | Whether the security rule is disabled.                                                                  |
| description        |                                                                                                        | Description of the security rule object.                                                                |
| tag                |                                                                                                        | List of tags associated with the security rule object.                                                  |
| from\_             | Default: ["any"]                                                                                       | List of source security zones.                                                                          |
| source             | Default: ["any"]                                                                                       | List of source addresses.                                                                               |
| negate_source      | Default: false                                                                                         | Whether to negate the source addresses.                                                                 |
| source_user        | Default: ["any"]                                                                                       | List of source users and/or groups.                                                                     |
| source_hip         | Default: ["any"]                                                                                       | List of source Host Integrity Profiles.                                                                 |
| to\_               | Default: ["any"]                                                                                       | List of destination security zones.                                                                     |
| destination        | Default: ["any"]                                                                                       | List of destination addresses.                                                                          |
| negate_destination | Default: false                                                                                         | Whether to negate the destination addresses.                                                            |
| destination_hip    | Default: ["any"]                                                                                       | List of destination Host Integrity Profiles.                                                            |
| application        | Default: ["any"]                                                                                       | List of applications being accessed.                                                                    |
| service            | Default: ["any"]                                                                                       | List of services being accessed.                                                                        |
| category           | Default: ["any"]                                                                                       | List of URL categories being accessed.                                                                  |
| action             | Choices: ["allow", "deny", "drop", "reset-client", "reset-server", "reset-both"] <br> Default: "allow" | Action to be taken when the rule is matched.                                                            |
| profile_setting    |                                                                                                        | Security profile settings for the rule. Contains 'group' list parameter with default ["best-practice"]. |
| log_setting        |                                                                                                        | Log forwarding profile for the rule.                                                                    |
| schedule           |                                                                                                        | Schedule for the rule.                                                                                  |
| log_start          |                                                                                                        | Whether to log at the start of the session.                                                             |
| log_end            |                                                                                                        | Whether to log at the end of the session.                                                               |
| folder             |                                                                                                        | The folder in which the resource is defined.                                                            |
| snippet            |                                                                                                        | The snippet in which the resource is defined.                                                           |
| device             |                                                                                                        | The device in which the resource is defined.                                                            |
| rulebase           | Choices: ["pre", "post"] <br> Default: "pre"                                                           | Which rulebase to use.                                                                                  |
| provider           |                                                                                                        | Authentication credentials.                                                                             |
| state              | Choices: ["present", "absent"]                                                                         | Desired state of the security rule object.                                                              |

## Examples

```yaml
- name: Manage Security Rules in Strata Cloud Manager
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

    - name: Create a security rule
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Allow_Web_Traffic"
        description: "Allow web traffic to the web server"
        from_: ["Internet"]
        source: ["any"]
        to_: ["DMZ"]
        destination: ["Web-Servers"]
        application: ["web-browsing", "ssl"]
        service: ["application-default"]
        action: "allow"
        folder: "Texas"
        rulebase: "pre"
        profile_setting:
          group: ["best-practice"]
        tag: ["web", "internet"]
        state: "present"

    - name: Update a security rule
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Allow_Web_Traffic"
        description: "Allow web traffic to the web server (updated)"
        from_: ["Internet"]
        source: ["any"]
        to_: ["DMZ"]
        destination: ["Web-Servers"]
        application: ["web-browsing", "ssl", "http2"]
        service: ["application-default"]
        action: "allow"
        folder: "Texas"
        rulebase: "pre"
        profile_setting:
          group: ["strict-security"]
        tag: ["web", "internet", "updated"]
        state: "present"

    - name: Create a security rule in post-rulebase
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Block_Malicious_Traffic"
        description: "Block traffic to known malicious sites"
        from_: ["any"]
        source: ["any"]
        to_: ["any"]
        destination: ["any"]
        application: ["any"]
        service: ["any"]
        category: ["malware", "command-and-control"]
        action: "deny"
        folder: "Texas"
        rulebase: "post"
        log_setting: "default-log-profile"
        log_end: true
        state: "present"

    - name: Delete security rule
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Allow_Web_Traffic"
        folder: "Texas"
        rulebase: "pre"
        state: "absent"
```

## Return Values

| Key           | Returned              | Description                             |
| ------------- | --------------------- | --------------------------------------- |
| changed       | Always                | Whether any changes were made.          |
| security_rule | When state is present | Details about the security rule object. |

## Notes

- Security rules require exactly one container (folder, snippet, or device) to be specified.
- When using rulebase="post", the rule will be added to the post-rulebase rather than the default
  pre-rulebase.
- The module supports check mode for all operations.

## Authors

- Calvin Remsburg (@cdot65)
