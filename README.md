# Strata Cloud Manager Ansible Collection

![Banner Image](https://raw.githubusercontent.com/cdot65/pan-scm-sdk/main/docs/images/logo.svg)
[![MIT License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/cdot65/pan-scm-ansible/blob/main/LICENSE.md)
[![Python versions](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Ansible versions](https://img.shields.io/badge/ansible-2.17%2B-black.svg)](https://www.ansible.com/)

Ansible Collection for managing Palo Alto Networks Strata Cloud Manager (SCM) configurations.

> **NOTE**: Please refer to the [official documentation site](https://cdot65.github.io/pan-scm-ansible/) for
> comprehensive examples and module documentation.

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

- **Configuration Management**: Create, read, update, and delete SCM configuration objects such as addresses, address
  groups, applications, security rules, and more.
- **Comprehensive Module Set**: Collection includes modules for network objects, security policies, VPN configurations,
  and more.
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

| Module                                                                                                        | Description                              | Info Module                                                                                                             |
|---------------------------------------------------------------------------------------------------------------|------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| [address](https://cdot65.github.io/pan-scm-ansible/collection/modules/address/)                               | Manage address objects                   | [address_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/address_info/)                               |
| [address_group](https://cdot65.github.io/pan-scm-ansible/collection/modules/address_group/)                   | Manage address groups                    | [address_group_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/address_group_info/)                   |
| [application](https://cdot65.github.io/pan-scm-ansible/collection/modules/application/)                       | Manage applications                      | [application_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/application_info/)                       |
| [application_group](https://cdot65.github.io/pan-scm-ansible/collection/modules/application_group/)           | Manage application groups                | [application_group_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/application_group_info/)           |
| [dynamic_user_group](https://cdot65.github.io/pan-scm-ansible/collection/modules/dynamic_user_group/)         | Manage dynamic user groups               | [dynamic_user_group_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/dynamic_user_group_info/)         |
| [external_dynamic_lists](https://cdot65.github.io/pan-scm-ansible/collection/modules/external_dynamic_lists/) | Manage external dynamic lists            | [external_dynamic_lists_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/external_dynamic_lists_info/) |
| [hip_object](https://cdot65.github.io/pan-scm-ansible/collection/modules/hip_object/)                         | Manage Host Information Profile objects  | [hip_object_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/hip_object_info/)                         |
| [hip_profile](https://cdot65.github.io/pan-scm-ansible/collection/modules/hip_profile/)                       | Manage Host Information Profile profiles | [hip_profile_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/hip_profile_info/)                       |
| [service](https://cdot65.github.io/pan-scm-ansible/collection/modules/service/)                               | Manage service objects                   | [service_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/service_info/)                               |
| [service_group](https://cdot65.github.io/pan-scm-ansible/collection/modules/service_group/)                   | Manage service groups                    | [service_group_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/service_group_info/)                   |
| [tag](https://cdot65.github.io/pan-scm-ansible/collection/modules/tag/)                                       | Manage tag objects                       | [tag_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/tag_info/)                                       |

### Network Configuration

| Module                                                                                                    | Description                      | Info Module                                                                                                     |
|-----------------------------------------------------------------------------------------------------------|----------------------------------|----------------------------------------------------------------------------------------------------------------|
| [security_zone](https://cdot65.github.io/pan-scm-ansible/collection/modules/security_zone/)               | Manage security zones            |                                                                                                                |
| [ike_crypto_profile](https://cdot65.github.io/pan-scm-ansible/collection/modules/ike_crypto_profile/)     | Manage IKE crypto profiles       |                                                                                                                |
| [ike_gateway](https://cdot65.github.io/pan-scm-ansible/collection/modules/ike_gateway/)                   | Manage IKE gateways              |                                                                                                                |
| [ipsec_crypto_profile](https://cdot65.github.io/pan-scm-ansible/collection/modules/ipsec_crypto_profile/) | Manage IPsec crypto profiles     |                                                                                                                |
| [ipsec_tunnel](https://cdot65.github.io/pan-scm-ansible/collection/modules/ipsec_tunnel/)                 | Manage IPsec tunnels             |                                                                                                                |
| [bgp_routing](https://cdot65.github.io/pan-scm-ansible/collection/modules/bgp_routing/)                   | Manage BGP routing configuration | [bgp_routing_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/bgp_routing_info/)             |

### Deployment

| Module                                                                                                        | Description                       | Info Module                                                                                                             |
|---------------------------------------------------------------------------------------------------------------|-----------------------------------|------------------------------------------------------------------------------------------------------------------------|
| [bandwidth_allocations](https://cdot65.github.io/pan-scm-ansible/collection/modules/bandwidth_allocations/)   | Manage bandwidth allocations      | [bandwidth_allocations_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/bandwidth_allocations_info/)   |
| [internal_dns_servers](https://cdot65.github.io/pan-scm-ansible/collection/modules/internal_dns_servers/)     | Manage internal DNS servers       | [internal_dns_servers_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/internal_dns_servers_info/)     |
| [remote_networks](https://cdot65.github.io/pan-scm-ansible/collection/modules/remote_networks/)               | Manage remote networks            | [remote_networks_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/remote_networks_info/)               |
| [network_locations](https://cdot65.github.io/pan-scm-ansible/collection/modules/network_locations/)           | Manage network locations          |                                                                                                                        |
| [service_connections](https://cdot65.github.io/pan-scm-ansible/collection/modules/service_connections/)       | Manage service connections        |                                                                                                                        |

### Security Services

| Module                                                                                                          | Description                    | Info Module                                                                                                         |
|-----------------------------------------------------------------------------------------------------------------|--------------------------------|---------------------------------------------------------------------------------------------------------------------|
| [security_rule](https://cdot65.github.io/pan-scm-ansible/collection/modules/security_rule/)                     | Manage security rules          | [security_rule_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/security_rule_info/)               |
| [anti_spyware_profile](https://cdot65.github.io/pan-scm-ansible/collection/modules/anti_spyware_profile/)       | Manage anti-spyware profiles   | [anti_spyware_profile_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/anti_spyware_profile_info/) |
| [decryption_profile](https://cdot65.github.io/pan-scm-ansible/collection/modules/decryption_profile/)           | Manage decryption profiles     | [decryption_profile_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/decryption_profile_info/)     |
| [dns_server_profiles](https://cdot65.github.io/pan-scm-ansible/collection/modules/dns_server_profiles/)         | Manage DNS server profiles     | [dns_server_profiles_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/dns_server_profiles_info/)   |
| [security_profiles_group](https://cdot65.github.io/pan-scm-ansible/collection/modules/security_profiles_group/) | Manage security profile groups | -                                                                                                                   |
| [vulnerability_protection_profile](https://cdot65.github.io/pan-scm-ansible/collection/modules/vulnerability_protection_profile/) | Manage vulnerability protection profiles | [vulnerability_protection_profile_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/vulnerability_protection_profile_info/) |
| [wildfire_antivirus_profiles](https://cdot65.github.io/pan-scm-ansible/collection/modules/wildfire_antivirus_profiles/) | Manage WildFire antivirus profiles | [wildfire_antivirus_profiles_info](https://cdot65.github.io/pan-scm-ansible/collection/modules/wildfire_antivirus_profiles_info/) |

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

### Create a DNS Server Profile

```yaml
- name: Create a DNS server profile with multiple servers
  cdot65.scm.dns_server_profiles:
    provider: "{{ provider }}"
    name: "multi-dns-profile"
    description: "DNS profile with multiple servers"
    server:
      - name: "google-dns-1"
        address: "8.8.8.8"
        protocol: "UDP"
        port: 53
      - name: "google-dns-2"
        address: "8.8.4.4"
        protocol: "UDP"
        port: 53
      - name: "tcp-dns"
        address: "9.9.9.9"
        protocol: "TCP"
        port: 53
        enable_edns0: true
    default_server: "google-dns-1"
    folder: "Texas"
    state: "present"
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

If you encounter bugs or have ideas for improvements, please check our [Issues guide](ISSUES.md) before opening a new
issue.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

---

*For comprehensive documentation and examples, visit
our [Official Documentation Site](https://cdot65.github.io/pan-scm-ansible/).*