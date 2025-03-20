[![MIT License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/cdot65/pan-scm-ansible-collection/blob/main/LICENSE.md)

<img src="https://raw.githubusercontent.com/cdot65/pan-scm-sdk/main/docs/images/logo.svg" width=720 alt="Strata Cloud Manager" />

# Strata Cloud Manager Ansible Collection

This Ansible Collection allows you to manage Palo Alto Networks Strata Cloud Manager (SCM) using the `pan-scm-sdk`
Python SDK.

## Table of Contents

- [Installation](#installation)
- [Getting Started](#getting-started)
    - [Python Virtual Environments](#python-virtual-environments)
    - [Configuring Ansible](#configuring-ansible)
- [Example Usage](#example-usage)
- [Collection Structure](#collection-structure)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Reporting Issues](#reporting-issues)

## Installation

1. Clone the repository and install the required Python packages:

   ```sh
   git clone https://github.com/cdot65/pan-scm-ansible-collection.git
   cd pan-scm-ansible-collection
   pip install -r requirements.txt
   ```

2. Install the collection:

   ```sh
   ansible-galaxy collection build .
   ansible-galaxy collection install cdot65-scm-x.y.z.tar.gz
   ```

## Getting Started

### Python Virtual Environments

It's recommended to use a virtual environment to isolate Ansible and its dependencies:

```sh
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Linux/macOS
source .venv/bin/activate
# On Windows
.venv\Scripts\activate

# Install Ansible and this collection's dependencies
pip install ansible
pip install -r requirements.txt
```

### Configuring Ansible

1. Create an `ansible.cfg` file in your project directory:

```ini
[defaults]
inventory = inventory.yml
collections_paths = ./collections
host_key_checking = False
retry_files_enabled = False
deprecation_warnings = False
interpreter_python = auto_silent

[persistent_connection]
connect_timeout = 60
command_timeout = 60
```

2. Create an inventory file (`inventory.yml`):

```yaml
---
all:
  children:
    scm:
      hosts:
        strata_cloud_manager:
          ansible_connection: local
      vars:
        ansible_python_interpreter: "{{ ansible_playbook_python }}"
```

3. Create a vars file for SCM credentials:

```yaml
---
# vars/scm_credentials.yml
scm_username: your_username
scm_password: your_password
```

4. Run a playbook with credentials:

```sh
ansible-playbook playbooks/example.yml -e @vars/scm_credentials.yml
```

## Example Usage

```yaml
---
- name: SCM Address Object Example
  hosts: scm
  gather_facts: false

  tasks:
    - name: Create an address object
      cdot65.scm.address:
        name: "test123"
        folder: "Texas"
        description: "My new address"
        fqdn: "example.test123.com"
```

## Collection Structure

```
collection/
├── docs/                    # Documentation for the collection
├── plugins/                 # All plugins in the collection
│   ├── modules/             # Ansible modules
│   ├── module_utils/        # Utility code for modules
│   └── inventory/           # Inventory plugins
├── roles/                   # Ansible roles
├── playbooks/               # Sample playbooks
├── tests/                   # Tests for the collection
├── galaxy.yml               # Collection metadata
└── README.md                # This file
```

## Documentation

For detailed usage, please refer to
the [Documentation](https://github.com/cdot65/pan-scm-ansible-collection/blob/main/pan_scm_ansible_collection/README.md).

## Contributing

- Refer to the [Contributing guide](https://github.com/cdot65/pan-scm-ansible-collection/blob/main/CONTRIBUTING.md) to
  get started developing, testing, and building this collection.
- All code submissions are made through pull requests against the `main` branch.
- Take care to make sure no merge commits are in the submission, and use `git rebase` vs. `git merge` for this reason.

## Reporting Issues

If you're experiencing a problem that you feel is a bug in the SCM Ansible Collection or have ideas for improvement, we
encourage you to open an issue and share your feedback. Please take a look at
our [Issues guide](https://github.com/cdot65/pan-scm-ansible-collection/blob/main/ISSUES.md) before opening a new issue.
