______________________________________________________________________

hide:

- navigation

______________________________________________________________________

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
    <a href="https://paloaltonetworks.com"><img src="images/logo.svg" alt="PaloAltoNetworks"></a>
</p>
<p align="center">
    <em><code>cdot65.scm</code>: Ansible Collection for Palo Alto Networks Strata Cloud Manager</em>
</p>
<p align="center">
<a href="https://github.com/cdot65/pan-scm-ansible/graphs/contributors" target="_blank">
    <img src="https://img.shields.io/github/contributors/cdot65/pan-scm-ansible.svg?style=for-the-badge" alt="Contributors">
</a>
<a href="https://github.com/cdot65/pan-scm-ansible/network/members" target="_blank">
    <img src="https://img.shields.io/github/forks/cdot65/pan-scm-ansible.svg?style=for-the-badge" alt="Forks">
</a>
<a href="https://github.com/cdot65/pan-scm-ansible/stargazers" target="_blank">
    <img src="https://img.shields.io/github/stars/cdot65/pan-scm-ansible.svg?style=for-the-badge" alt="Stars">
</a>
<a href="https://github.com/cdot65/pan-scm-ansible/issues" target="_blank">
    <img src="https://img.shields.io/github/issues/cdot65/pan-scm-ansible.svg?style=for-the-badge" alt="Issues">
</a>
<a href="https://github.com/cdot65/pan-scm-ansible/blob/main/LICENSE.md" target="_blank">
    <img src="https://img.shields.io/github/license/cdot65/pan-scm-ansible.svg?style=for-the-badge" alt="License">
</a>
</p>

______________________________________________________________________

**Documentation**:
<a href="https://cdot65.github.io/pan-scm-ansible/" target="_blank">https://cdot65.github.io/pan-scm-ansible/</a>

**Source Code**:
<a href="https://github.com/cdot65/pan-scm-ansible" target="_blank">https://github.com/cdot65/pan-scm-ansible</a>

______________________________________________________________________

This Ansible Collection provides modules, roles, and plugins for managing Palo Alto Networks Strata
Cloud Manager (SCM) configurations. It leverages the `pan-scm-sdk` Python SDK to provide reliable
and consistent interactions with the SCM API.

## Installation

**Requirements**:

- Python 3.11 or higher
- Ansible Core 2.17 or higher
- `pan-scm-sdk` version 0.3.22 or higher

<div class="termy">

```bash
$ pip install pan-scm-sdk
---> 100%
Successfully installed pan-scm-sdk-0.3.22

$ ansible-galaxy collection install cdot65.scm
---> 100%
Process completed successfully
```

</div>

## Quick Example

<div class="termy">

```yaml
# Example playbook for managing SCM address objects
---
- name: Manage SCM address objects
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
    - name: Create an address object with ip_netmask
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "Web_Server"
        description: "Web server IP address"
        ip_netmask: "192.168.1.100/32"
        folder: "Texas"
        tag: ["Web", "Production"]
        state: "present"
      register: address_result

    - name: Display the created address object
      debug:
        var: address_result

    - name: Create an address object with FQDN
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "DNS_Server"
        description: "DNS server FQDN"
        fqdn: "dns.example.com"
        folder: "Texas"
        tag: ["DNS", "Infrastructure"]
        state: "present"

    - name: Create a security rule using these addresses
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Allow_Web_to_DNS"
        description: "Allow web servers to access DNS"
        source_zone: ["trust"]
        destination_zone: ["trust"]
        source_address: ["Web_Server"]
        destination_address: ["DNS_Server"]
        application: ["dns"]
        service: ["application-default"]
        action: "allow"
        folder: "Texas"
        state: "present"
```

</div>

For more detailed usage instructions and examples, refer to the
[User Guide](guide/getting-started.md).

______________________________________________________________________

## Key Features

- **Complete Configuration Management**: Create, update, and delete SCM configuration objects
- **Idempotent Operations**: Safe to run multiple times with the same expected outcome
- **Categorized Modules**:
  - Network Objects (Address, Service, Tag)
  - Network Configuration (Zones, VPN, Routing)
  - Security Services (Rules, Profiles)
  - Deployment (Remote Networks, Service Connections)
- **Roles for Common Tasks**: Pre-built roles for bootstrapping and configuration deployment
- **Inventory Plugin**: Dynamically build inventory from SCM
- **Integration with SCM SDK**: Reliable API interactions with proper error handling

## Contributing

Contributions are welcome and greatly appreciated. Visit the
[Contributing](development/contributing.md) page for guidelines on how to contribute.

## License

This project is licensed under the MIT License - see the [License](about/license.md) page for
details.
