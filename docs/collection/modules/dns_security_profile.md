# Dns Security Profile Configuration Object

Manage DNS security profile objects in Strata Cloud Manager (SCM).

## Synopsis

- Manage DNS security profile objects within Strata Cloud Manager (SCM).
- Create, update, and delete DNS security profile objects.
- Configure botnet domains, DNS security categories, and sinkhole settings.
- Ensures that exactly one container type (folder, snippet, device) is provided.

## Parameters

| Parameter                                             | Choices/Defaults                                                                                                      | Comments                                                     |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| name                                                  |                                                                                                                       | The name of the DNS security profile (max 63 chars).         |
| description                                           |                                                                                                                       | Description of the DNS security profile.                     |
| botnet_domains                                        |                                                                                                                       | Botnet domains configuration.                                |
| botnet_domains.dns_security_categories                |                                                                                                                       | List of DNS security categories configuration.               |
| botnet_domains.dns_security_categories.name           |                                                                                                                       | DNS security category name.                                  |
| botnet_domains.dns_security_categories.action         | <ul><li>default</li><li>allow</li><li>block</li><li>sinkhole</li></ul>                                                | Action to take for the category.                             |
| botnet_domains.dns_security_categories.log_level      | <ul><li>default</li><li>none</li><li>low</li><li>informational</li><li>medium</li><li>high</li><li>critical</li></ul> | Log level for the category.                                  |
| botnet_domains.dns_security_categories.packet_capture | <ul><li>disable</li><li>single-packet</li><li>extended-capture</li></ul>                                              | Packet capture option.                                       |
| botnet_domains.sinkhole                               |                                                                                                                       | Sinkhole configuration for DNS security.                     |
| botnet_domains.sinkhole.ipv4_address                  | <ul><li>pan-sinkhole-default-ip</li><li>127.0.0.1</li></ul>                                                           | IPv4 address for the sinkhole.                               |
| botnet_domains.sinkhole.ipv6_address                  | <ul><li>::1</li></ul>                                                                                                 | IPv6 address for the sinkhole.                               |
| botnet_domains.whitelist                              |                                                                                                                       | List of whitelisted domains.                                 |
| botnet_domains.whitelist.name                         |                                                                                                                       | Name of the whitelisted domain.                              |
| botnet_domains.whitelist.description                  |                                                                                                                       | Description of the whitelisted domain.                       |
| folder                                                |                                                                                                                       | The folder in which the resource is defined (max 64 chars).  |
| snippet                                               |                                                                                                                       | The snippet in which the resource is defined (max 64 chars). |
| device                                                |                                                                                                                       | The device in which the resource is defined (max 64 chars).  |
| provider                                              |                                                                                                                       | Authentication credentials.                                  |
| provider.client_id                                    |                                                                                                                       | Client ID for authentication.                                |
| provider.client_secret                                |                                                                                                                       | Client secret for authentication.                            |
| provider.tsg_id                                       |                                                                                                                       | Tenant Service Group ID.                                     |
| provider.log_level                                    | Default: "INFO"                                                                                                       | Log level for the SDK.                                       |
| state                                                 | <ul><li>present</li><li>absent</li></ul>                                                                              | Desired state of the DNS security profile object.            |

## Examples

```yaml
---
- name: Manage DNS Security Profiles in Strata Cloud Manager
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

    - name: Create a basic DNS security profile
      cdot65.scm.dns_security_profile:
        provider: "{{ provider }}"
        name: "test-dns-security"
        description: "Test DNS security profile"
        folder: "Texas"
        state: "present"

    - name: Create a DNS security profile with botnet domain settings
      cdot65.scm.dns_security_profile:
        provider: "{{ provider }}"
        name: "botnet-protection"
        description: "DNS profile with botnet protection"
        botnet_domains:
          dns_security_categories:
            - name: "command-and-control"
              action: "block"
              log_level: "high"
              packet_capture: "single-packet"
            - name: "malware"
              action: "sinkhole"
              log_level: "critical"
            - name: "phishing"
              action: "block"
          sinkhole:
            ipv4_address: "pan-sinkhole-default-ip"
            ipv6_address: "::1"
          whitelist:
            - name: "trusted-domain.com"
              description: "Trusted internal domain"
        folder: "Texas"
        state: "present"

    - name: Update an existing DNS security profile
      cdot65.scm.dns_security_profile:
        provider: "{{ provider }}"
        name: "botnet-protection"
        description: "Updated DNS security profile"
        botnet_domains:
          dns_security_categories:
            - name: "command-and-control"
              action: "sinkhole"
              log_level: "critical"
            - name: "malware"
              action: "block"
            - name: "spyware"
              action: "block"
              log_level: "high"
          sinkhole:
            ipv4_address: "127.0.0.1"
            ipv6_address: "::1"
        folder: "Texas"
        state: "present"

    - name: Delete a DNS security profile
      cdot65.scm.dns_security_profile:
        provider: "{{ provider }}"
        name: "botnet-protection"
        folder: "Texas"
        state: "absent"
```

## Return Values

| Key                  | Returned              | Description                             |
| -------------------- | --------------------- | --------------------------------------- |
| changed              | always                | Whether any changes were made.          |
| dns_security_profile | when state is present | Details about the DNS security profile. |

## Notes

- This module requires the pan-scm-sdk Python package to interact with the SCM API.
- Authentication is handled via the provider parameter which must include client_id, client_secret,
  and tsg_id.
- Exactly one container (folder, snippet, or device) must be specified.
- When creating a DNS security profile, the name parameter is required.
- For botnet domains configuration, various DNS security categories can be configured with different
  actions and log levels.

## Authors

- Calvin Remsburg (@cdot65)
