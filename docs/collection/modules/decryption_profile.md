# Decryption Profile Configuration Object

## Synopsis

Manage decryption profile objects within Strata Cloud Manager (SCM).

## Parameters

| Parameter                                     | Type   | Required | Default    | Choices                                                                                            | Description                                                |
| --------------------------------------------- | ------ | -------- | ---------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `name`                                        | `str`  | yes      |            |                                                                                                    | The name of the decryption profile.                        |
| `description`                                 | `str`  | no       |            |                                                                                                    | Description of the profile.                                |
| `ssl_forward_proxy`                           | `dict` | no       |            |                                                                                                    | SSL Forward Proxy settings.                                |
| `ssl_forward_proxy.enabled`                   | `bool` | no       | `false`    |                                                                                                    | Enable SSL Forward Proxy.                                  |
| `ssl_forward_proxy.block_unsupported_cipher`  | `bool` | no       | `false`    |                                                                                                    | Block sessions with unsupported ciphers.                   |
| `ssl_forward_proxy.block_unknown_cert`        | `bool` | no       | `false`    |                                                                                                    | Block sessions with unknown certificates.                  |
| `ssl_forward_proxy.block_expired_cert`        | `bool` | no       | `false`    |                                                                                                    | Block sessions with expired certificates.                  |
| `ssl_forward_proxy.block_timeoff_cert`        | `bool` | no       | `false`    |                                                                                                    | Block sessions with certificates not yet valid.            |
| `ssl_forward_proxy.block_untrusted_issuer`    | `bool` | no       | `false`    |                                                                                                    | Block sessions with untrusted issuer certificates.         |
| `ssl_forward_proxy.block_unknown_status`      | `bool` | no       | `false`    |                                                                                                    | Block sessions with certificates that have unknown status. |
| `ssl_inbound_inspection`                      | `dict` | no       |            |                                                                                                    | SSL Inbound Inspection settings.                           |
| `ssl_inbound_inspection.enabled`              | `bool` | no       | `false`    |                                                                                                    | Enable SSL Inbound Inspection.                             |
| `ssl_no_proxy`                                | `dict` | no       |            |                                                                                                    | SSL No Proxy settings.                                     |
| `ssl_no_proxy.enabled`                        | `bool` | no       | `false`    |                                                                                                    | Enable SSL No Proxy.                                       |
| `ssl_no_proxy.block_session_expired_cert`     | `bool` | no       | `false`    |                                                                                                    | Block sessions with expired certificates.                  |
| `ssl_no_proxy.block_session_untrusted_issuer` | `bool` | no       | `false`    |                                                                                                    | Block sessions with untrusted issuer certificates.         |
| `ssl_protocol_settings`                       | `dict` | no       |            |                                                                                                    | SSL Protocol settings.                                     |
| `ssl_protocol_settings.min_version`           | `str`  | no       | `"tls1-0"` | `"tls1-0"`, `"tls1-1"`, `"tls1-2"`, `"tls1-3"`                                                     | Minimum TLS version to support.                            |
| `ssl_protocol_settings.max_version`           | `str`  | no       | `"tls1-3"` | `"tls1-0"`, `"tls1-1"`, `"tls1-2"`, `"tls1-3"`                                                     | Maximum TLS version to support.                            |
| `ssl_protocol_settings.keyxchg_algorithm`     | `list` | no       |            | `"dhe"`, `"ecdhe"`                                                                                 | Key exchange algorithms to allow.                          |
| `ssl_protocol_settings.encrypt_algorithm`     | `list` | no       |            | `"rc4"`, `"rc4-md5"`, `"aes-128-cbc"`, `"aes-128-gcm"`, `"aes-256-cbc"`, `"aes-256-gcm"`, `"3des"` | Encryption algorithms to allow.                            |
| `ssl_protocol_settings.auth_algorithm`        | `list` | no       |            | `"sha1"`, `"sha256"`, `"sha384"`                                                                   | Authentication algorithms to allow.                        |
| `folder`                                      | `str`  | no       |            |                                                                                                    | The folder in which the resource is defined.               |
| `snippet`                                     | `str`  | no       |            |                                                                                                    | The snippet in which the resource is defined.              |
| `device`                                      | `str`  | no       |            |                                                                                                    | The device in which the resource is defined.               |
| `provider`                                    | `dict` | yes      |            |                                                                                                    | Authentication credentials.                                |
| `provider.client_id`                          | `str`  | yes      |            |                                                                                                    | Client ID for authentication.                              |
| `provider.client_secret`                      | `str`  | yes      |            |                                                                                                    | Client secret for authentication.                          |
| `provider.tsg_id`                             | `str`  | yes      |            |                                                                                                    | Tenant Service Group ID.                                   |
| `provider.log_level`                          | `str`  | no       | `"INFO"`   |                                                                                                    | Log level for the SDK.                                     |
| `state`                                       | `str`  | yes      |            | `"present"`, `"absent"`                                                                            | Desired state of the decryption profile.                   |

## Requirements

- Exactly one of `folder`, `snippet`, or `device` must be provided.

## Examples

### Create a decryption profile with SSL Forward Proxy enabled

```yaml
- name: Create decryption profile with SSL Forward Proxy enabled
  cdot65.scm.decryption_profile:
    provider: "{{ provider }}"
    name: "Custom-Decryption-Profile"
    description: "Custom decryption profile for forward proxy"
    ssl_forward_proxy:
      enabled: true
      block_expired_cert: true
      block_untrusted_issuer: true
    ssl_protocol_settings:
      min_version: "tls1-2"
      max_version: "tls1-3"
      keyxchg_algorithm: ["ecdhe"]
      encrypt_algorithm: ["aes-128-gcm", "aes-256-gcm"]
      auth_algorithm: ["sha256", "sha384"]
    folder: "Production"
    state: "present"
```

### Update a decryption profile with additional settings

```yaml
- name: Update decryption profile with additional settings
  cdot65.scm.decryption_profile:
    provider: "{{ provider }}"
    name: "Custom-Decryption-Profile"
    description: "Updated decryption profile with additional settings"
    ssl_forward_proxy:
      enabled: true
      block_expired_cert: true
      block_untrusted_issuer: true
      block_unknown_cert: true
    ssl_no_proxy:
      enabled: true
      block_session_expired_cert: true
    ssl_protocol_settings:
      min_version: "tls1-2"
      max_version: "tls1-3"
      keyxchg_algorithm: ["ecdhe"]
      encrypt_algorithm: ["aes-128-gcm", "aes-256-gcm"]
      auth_algorithm: ["sha256", "sha384"]
    folder: "Production"
    state: "present"
```

### Remove a decryption profile

```yaml
- name: Remove decryption profile
  cdot65.scm.decryption_profile:
    provider: "{{ provider }}"
    name: "Custom-Decryption-Profile"
    folder: "Production"
    state: "absent"
```

## Return Values

### When state is present

Returns a dictionary with details about the decryption profile object.

```json
{
    "decryption_profile": {
        "id": "123e4567-e89b-12d3-a456-426655440000",
        "name": "Custom-Decryption-Profile",
        "description": "Custom decryption profile for forward proxy",
        "ssl_forward_proxy": {
            "enabled": true,
            "block_expired_cert": true,
            "block_untrusted_issuer": true
        },
        "ssl_protocol_settings": {
            "min_version": "tls1-2",
            "max_version": "tls1-3",
            "keyxchg_algorithm": ["ecdhe"],
            "encrypt_algorithm": ["aes-128-gcm", "aes-256-gcm"],
            "auth_algorithm": ["sha256", "sha384"]
        },
        "folder": "Production"
    },
    "changed": true
}
```

## Notes

- At least one of `ssl_forward_proxy`, `ssl_inbound_inspection`, or `ssl_no_proxy` should be enabled
  in a production environment.
- SSL Protocol settings are globally applied to all enabled proxy types.
- The module supports check mode for previewing changes without modifying the system.
