# Strata Cloud Manager Ansible Collection

![Banner Image](https://raw.githubusercontent.com/cdot65/pan-scm-sdk/main/docs/images/logo.svg)
[![MIT License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/cdot65/pan-scm-ansible/blob/main/LICENSE.md)
[![Python versions](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Ansible versions](https://img.shields.io/badge/ansible-2.17%2B-black.svg)](https://www.ansible.com/)

Ansible Collection for managing Palo Alto Networks Strata Cloud Manager (SCM) configurations.

> **NOTE**: Please refer to the [official documentation site](https://cdot65.github.io/pan-scm-ansible/) for comprehensive examples and module documentation.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Available Modules](#available-modules)
- [Example Usage](#example-usage)
- [Authentication](#authentication)
- [Documentation](#documentation)
- [Testing](#testing)
- [Contributing](#contributing)
- [Reporting Issues](#reporting-issues)
- [License](#license)

## Features

- **Configuration Management**: Create, read, update, and delete SCM configuration objects such as addresses, address groups, applications, security rules, and more.
- **Comprehensive Module Set**: Collection includes modules for network objects, security policies, VPN configurations, and more.
- **Idempotent Operations**: All modules are designed to be idempotent, ensuring consistent and predictable results.
- **Detailed Information Modules**: Companion "info" modules for retrieving detailed information about resources.
- **OAuth2 Authentication**: Securely authenticate with the Strata Cloud Manager API using OAuth2 client credentials.
- **Role-Based Automation**: Ready-to-use roles for common operational tasks.

## Requirements

- Python 3.11 or higher
- Ansible Core 2.17 or higher
- pan-scm-sdk 0.3.22 or higher

## Installation

1. Install the collection from Ansible Galaxy:

   ```bash
   ansible-galaxy collection install cdot65.scm
   ```

2. Or clone the repository and build manually:

   ```bash
   git clone https://github.com/cdot65/pan-scm-ansible.git
   cd pan-scm-ansible
   pip install -r requirements.txt
   ansible-galaxy collection build
   ansible-galaxy collection install cdot65-scm-*.tar.gz
   ```

## Available Modules

### Network Objects

- **Address Objects**: [address](https://cdot65.github.io/pan-scm-ansible/collection/modules/address/), [address_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/address_info/)
- **Address Groups**: [address_group](https://cdot65.github.io/pan-scm-ansible/collection/modules/address_group/), [address_group_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/address_group_info/)
- **Applications**: [application](https://cdot65.github.io/pan-scm-ansible/collection/modules/application/), [application_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/application_info/)
- **Application Groups**: [application_group](https://cdot65.github.io/pan-scm-ansible/collection/modules/application_group/), [application_group_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/application_group_info/)
- **Dynamic User Groups**: [dynamic_user_group](https://cdot65.github.io/pan-scm-ansible/collection/modules/dynamic_user_group/)
- **External Dynamic Lists**: [external_dynamic_lists](https://cdot65.github.io/pan-scm-ansible/collection/modules/external_dynamic_lists/), [external_dynamic_lists_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/external_dynamic_lists_info/)
- **Services**: [service](https://cdot65.github.io/pan-scm-ansible/collection/modules/service/), [service_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/service_info/)
- **Service Groups**: [service_group](https://cdot65.github.io/pan-scm-ansible/collection/modules/service_group/), [service_group_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/service_group_info/)
- **Tags**: [tag](https://cdot65.github.io/pan-scm-ansible/collection/modules/tag/), [tag_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/tag_info/)

### Network Configuration

- **Security Zones**: [security_zone](https://cdot65.github.io/pan-scm-ansible/collection/modules/security_zone/)
- **VPN Configuration**: [ike_crypto_profile](https://cdot65.github.io/pan-scm-ansible/collection/modules/ike_crypto_profile/), [ike_gateway](https://cdot65.github.io/pan-scm-ansible/collection/modules/ike_gateway/), [ipsec_crypto_profile](https://cdot65.github.io/pan-scm-ansible/collection/modules/ipsec_crypto_profile/), [ipsec_tunnel](https://cdot65.github.io/pan-scm-ansible/collection/modules/ipsec_tunnel/)
- **Routing**: [bgp_routing](https://cdot65.github.io/pan-scm-ansible/collection/modules/bgp_routing/)

### Deployment

- **Remote Networks**: [remote_networks](https://cdot65.github.io/pan-scm-ansible/collection/modules/remote_networks/)
- **Network Locations**: [network_locations](https://cdot65.github.io/pan-scm-ansible/collection/modules/network_locations/)
- **Service Connections**: [service_connections](https://cdot65.github.io/pan-scm-ansible/collection/modules/service_connections/)

### Security Services

- **Security Rules**: [security_rule](https://cdot65.github.io/pan-scm-ansible/collection/modules/security_rule/), [security_rule_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/security_rule_info/)
- **Security Profiles**: [anti_spyware_profile](https://cdot65.github.io/pan-scm-ansible/collection/modules/anti_spyware_profile/), [anti_spyware_profile_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/anti_spyware_profile_info/)
- **Security Profile Groups**: [security_profiles_group](https://cdot65.github.io/pan-scm-ansible/collection/modules/security_profiles_group/)

## Example Usage

### Create an Address Object

```yaml
- name: Create an IP-based address object
  cdot65.scm.address:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    name: "web-server"
    folder: "Texas"
    description: "Web server IP address"
    ip_netmask: "10.1.1.10/32"
    state: present
```

### Create an External Dynamic List

```yaml
- name: Create URL-based external dynamic list
  cdot65.scm.external_dynamic_lists:
    provider: "{{ provider }}"
    name: "malicious-urls"
    description: "Malicious URLs list"
    folder: "Texas"
    url_list:
      url: "https://threatfeeds.example.com/urls.txt"
      exception_list:
        - "example.com/allowed"
        - "example.org/allowed"
    weekly:
      day_of_week: "monday"
      at: "12"
    state: "present"
```

### Get Information About Objects

```yaml
- name: Get address information
  cdot65.scm.address_info:
    provider: "{{ provider }}"
    name: "web-server"
    folder: "Texas"
  register: address_info

- name: List all security rules in a folder
  cdot65.scm.security_rule_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: security_rules
```

## Authentication

All modules require authentication credentials provided via the `provider` parameter:

```yaml
provider:
  client_id: "your_client_id"
  client_secret: "your_client_secret"
  tsg_id: "your_tsg_id"
  log_level: "INFO"  # Optional, defaults to INFO
```

It's recommended to store these credentials securely using Ansible Vault:

```yaml
# group_vars/all/vault.yml (encrypted with ansible-vault)
client_id: "your-client-id"
client_secret: "your-client-secret"
tsg_id: "your-tsg-id"

# In your playbook:
vars:
  provider:
    client_id: "{{ client_id }}"
    client_secret: "{{ client_secret }}"
    tsg_id: "{{ tsg_id }}"
```

## Documentation

For comprehensive documentation, visit our [Official Documentation Site](https://cdot65.github.io/pan-scm-ansible/).

The documentation includes:
- Detailed module reference
- Usage examples
- Best practices
- Troubleshooting guides

## Testing

This collection includes testing utilities to ensure compatibility:

```bash
# Make the script executable
chmod +x fix_ansible_tests.sh

# Run the script to fix common testing issues
./fix_ansible_tests.sh
```

For more information on compatibility and testing, see [ANSIBLE_TESTING.md](ANSIBLE_TESTING.md).

## Contributing

- Refer to the [Contributing guide](CONTRIBUTING.md) for development, testing, and building information.
- All code submissions should be made through pull requests against the `main` branch.
- Use `git rebase` instead of `git merge` to avoid merge commits in your submission.

## Reporting Issues

If you encounter bugs or have ideas for improvements, please check our [Issues guide](ISSUES.md) before opening a new issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

---

*For comprehensive documentation and examples, visit our [Official Documentation Site](https://cdot65.github.io/pan-scm-ansible/).*