# Decryption Profile Info Module

## Synopsis

Gather information about decryption profile objects within Strata Cloud Manager (SCM).

## Parameters

| Parameter | Type | Required | Default | Choices | Description |
|-----------|------|----------|---------|---------|-------------|
| `name` | `str` | no | | | The name of a specific decryption profile to retrieve. |
| `gather_subset` | `list` | no | `["config"]` | `"all"`, `"config"` | Determines which information to gather about decryption profiles. `all` gathers everything. `config` is the default which retrieves basic configuration. |
| `folder` | `str` | no | | | Filter decryption profiles by folder container. |
| `snippet` | `str` | no | | | Filter decryption profiles by snippet container. |
| `device` | `str` | no | | | Filter decryption profiles by device container. |
| `exact_match` | `bool` | no | `false` | | When True, only return objects defined exactly in the specified container. |
| `exclude_folders` | `list` | no | | | List of folder names to exclude from results. |
| `exclude_snippets` | `list` | no | | | List of snippet values to exclude from results. |
| `exclude_devices` | `list` | no | | | List of device values to exclude from results. |
| `provider` | `dict` | yes | | | Authentication credentials. |
| `provider.client_id` | `str` | yes | | | Client ID for authentication. |
| `provider.client_secret` | `str` | yes | | | Client secret for authentication. |
| `provider.tsg_id` | `str` | yes | | | Tenant Service Group ID. |
| `provider.log_level` | `str` | no | `"INFO"` | | Log level for the SDK. |

## Requirements

- If `name` is specified, exactly one of `folder`, `snippet`, or `device` must be provided.
- If `name` is not specified, exactly one of `folder`, `snippet`, or `device` must be provided.

## Examples

### Get information about a specific decryption profile

```yaml
- name: Get information about a specific decryption profile
  cdot65.scm.decryption_profile_info:
    provider: "{{ provider }}"
    name: "Custom-Decryption-Profile"
    folder: "Production"
  register: profile_info
```

### List all decryption profiles in a folder

```yaml
- name: List all decryption profiles in a folder
  cdot65.scm.decryption_profile_info:
    provider: "{{ provider }}"
    folder: "Production"
  register: all_profiles
```

### List profiles with exact match and exclusions

```yaml
- name: List profiles with exact match and exclusions
  cdot65.scm.decryption_profile_info:
    provider: "{{ provider }}"
    folder: "Production"
    exact_match: true
    exclude_folders: ["Shared"]
  register: filtered_profiles
```

## Return Values

### When name is specified

Returns information about the specific decryption profile.

```json
{
    "profile": {
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
    }
}
```

### When name is not specified

Returns a list of decryption profiles that match the specified filters.

```json
{
    "profiles": [
        {
            "id": "123e4567-e89b-12d3-a456-426655440000",
            "name": "Custom-Decryption-Profile",
            "description": "Custom decryption profile for forward proxy",
            "ssl_forward_proxy": {
                "enabled": true,
                "block_expired_cert": true,
                "block_untrusted_issuer": true
            },
            "folder": "Production"
        },
        {
            "id": "234e5678-e89b-12d3-a456-426655440001",
            "name": "Inbound-Inspection-Profile",
            "description": "Decryption profile for inbound inspection",
            "ssl_inbound_inspection": {
                "enabled": true
            },
            "folder": "Production"
        }
    ]
}
```

## Notes

- This is an info module that only retrieves information and does not modify anything.
- The module supports check mode, though it has no effect as the module does not modify the system.