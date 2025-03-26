# Authentication

This guide explains the authentication methods available when using the Palo Alto Networks Strata
Cloud Manager Ansible Collection.

## Authentication Overview

The collection uses OAuth2 client credentials to authenticate with the Strata Cloud Manager API. All
modules and roles require these credentials to interact with SCM.

## Provider Dictionary

The recommended way to authenticate is using the `provider` dictionary parameter that's consistent
across all modules:

```yaml
- name: Create address object
  cdot65.scm.address:
    provider:
      client_id: "your-client-id"
      client_secret: "your-client-secret"
      tsg_id: "your-tsg-id"
      log_level: "INFO"  # Optional, default is INFO
    name: "web-server"
    folder: "Texas"
    ip_netmask: "10.1.1.1/32"
    state: "present"
```

The provider dictionary contains:

| Parameter       | Description             | Required | Default  |
| --------------- | ----------------------- | -------- | -------- |
| `client_id`     | OAuth2 client ID        | Yes      | -        |
| `client_secret` | OAuth2 client secret    | Yes      | -        |
| `tsg_id`        | Tenant Service Group ID | Yes      | -        |
| `log_level`     | SDK log level           | No       | `"INFO"` |

## Using Ansible Vault

For better security, store credentials in an encrypted Ansible Vault file:

1. Create an encrypted vault file:

```bash
ansible-vault create vault.yaml
```

2. Add your credentials to the file:

```yaml
---
client_id: "your-client-id"
client_secret: "your-client-secret"
tsg_id: "your-tsg-id"
```

3. Include the vault file in your playbook and reference the credentials in a provider dictionary:

```yaml
- name: SCM Configuration
  hosts: localhost
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
  
  tasks:
    - name: Create address object
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "web-server"
        folder: "Texas"
        ip_netmask: "10.1.1.1/32"
        state: "present"
```

4. Run the playbook with vault password:

```bash
ansible-playbook your_playbook.yml --ask-vault-pass
```

## Authentication with Roles

When using collection roles, provide authentication in the role variables:

```yaml
- name: SCM Bootstrap
  hosts: localhost
  vars_files:
    - vault.yaml
  roles:
    - role: cdot65.scm.bootstrap
      vars:
        scm_client_id: "{{ client_id }}"
        scm_client_secret: "{{ client_secret }}"
        scm_tsg_id: "{{ tsg_id }}"
        bootstrap_folder: "Production"
```

## Using Environment Variables (Not Recommended)

While not the preferred method, you can set environment variables for testing purposes:

```bash
export SCM_CLIENT_ID="your-client-id"
export SCM_CLIENT_SECRET="your-client-secret"
export SCM_TSG_ID="your-tsg-id"
```

With special configuration, the collection can read these variables. However, the `provider`
dictionary approach is more explicit and reliable.

## Token Management

The `pan-scm-sdk` underlying this collection automatically handles token management:

- Obtains OAuth2 tokens when requests are made
- Caches tokens for their lifetime (typically 1 hour)
- Refreshes tokens automatically when they expire
- Handles token revocation on session end

## Obtaining API Credentials

To obtain API credentials for SCM:

1. Log in to the SCM portal as an administrator
2. Navigate to **Settings** > **API Access**
3. Create a new API client
4. Record the client ID, client secret, and TSG ID
5. Assign appropriate API permissions to the client

## Best Practices

1. **Use Ansible Vault**: Always store credentials in encrypted vault files
2. **Define Provider Once**: Define the provider dictionary in variables and reference it
3. **Avoid Hardcoding**: Never hardcode credentials in playbooks
4. **Set Restricted File Permissions**: Restrict access to vault files
5. **Use Least Privilege**: Create API clients with only the permissions needed
6. **Regularly Rotate**: Rotate client secrets periodically
7. **CI/CD Integration**: Use secure credential storage in CI/CD pipelines

## Troubleshooting Authentication

Common authentication issues:

- **Invalid Credentials**: Verify client ID and secret are correct
- **TSG ID Mismatch**: Ensure TSG ID matches your tenant
- **Permission Issues**: API client may lack required permissions
- **Network Problems**: Check connectivity to SCM API endpoints
- **Rate Limiting**: API requests may be rate limited
- **Clock Sync**: Ensure your system clock is synchronized

For detailed error messages, run playbooks with increased verbosity:

```bash
ansible-playbook your_playbook.yml -vvv
```

## Next Steps

Now that you understand authentication, proceed to:

- [Using Modules](using-modules.md)
- [Playbook Examples](playbook-examples.md)
