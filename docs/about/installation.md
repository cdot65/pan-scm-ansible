# Installation

This guide covers the installation of the Palo Alto Networks SCM Ansible Collection and its
dependencies.

## Prerequisites

Before installing the collection, ensure you have the following prerequisites:

- Python 3.8 or higher
- Ansible 2.13 or higher
- pip (Python package manager)

## Installing from Ansible Galaxy

The recommended way to install the collection is from Ansible Galaxy:

```bash
ansible-galaxy collection install cdot65.scm
```

This command installs the latest version of the collection. To install a specific version:

```bash
ansible-galaxy collection install cdot65.scm:1.0.0
```

## Installing the Python SDK Dependency

This collection depends on the `pan-scm-sdk` Python package. Install it using pip:

```bash
pip install pan-scm-sdk
```

## Installing from Source

To install the collection from source:

1. Clone the GitHub repository:

   ```bash
   git clone https://github.com/cdot65/pan-scm-ansible.git
   cd pan-scm-ansible
   ```

2. Build and install the collection:

   ```bash
   ansible-galaxy collection build
   ansible-galaxy collection install cdot65-scm-*.tar.gz
   ```

## Development Installation

For development purposes, you can install the collection in development mode:

1. Clone the repository:

   ```bash
   git clone https://github.com/cdot65/pan-scm-ansible.git
   cd pan-scm-ansible
   ```

2. Install the Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a symbolic link to your Ansible collections directory:

   ```bash
   mkdir -p ~/.ansible/collections/ansible_collections/cdot65
   ln -s $(pwd) ~/.ansible/collections/ansible_collections/cdot65/scm
   ```

## Verifying Installation

To verify the installation, run:

```bash
ansible-galaxy collection list | grep cdot65.scm
```

You should see the collection listed with its installed version.

## Next Steps

After installation, proceed to the [Getting Started](getting-started.md) guide to configure
authentication and run your first SCM Ansible playbook.
