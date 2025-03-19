# Palo Alto Networks Strata Cloud Manager Ansible Collection

<div class="grid cards" markdown>

-   :material-ansible:{ .lg .middle } __Ansible Collection__

    ---

    Ansible Collection for managing Palo Alto Networks Strata Cloud Manager configurations.

    [:octicons-arrow-right-24: Getting started](about/getting-started.md)

-   :material-code-json:{ .lg .middle } __Based on SCM SDK__

    ---

    Built on top of the `pan-scm-sdk` Python SDK for reliable API interactions.
    
    [:octicons-arrow-right-24: SDK Integration](guide/authentication.md)

-   :material-book-open-page-variant:{ .lg .middle } __Rich Documentation__

    ---

    Comprehensive documentation for modules, roles, and implementation examples.

    [:octicons-arrow-right-24: Collection Reference](collection/index.md)

-   :material-github:{ .lg .middle } __Open Source__

    ---

    MIT-licensed open source project with community contributions welcome.

    [:octicons-arrow-right-24: Contributing](development/contributing.md)

</div>

## Overview

This Ansible Collection provides modules, roles, and plugins for managing Palo Alto Networks Strata Cloud Manager (SCM) configurations. It leverages the `pan-scm-sdk` Python SDK to provide reliable and consistent interactions with the SCM API.

```yaml
- name: Create an address object
  cdot65.scm.address:
    name: "test123"
    folder: "Texas"
    description: "My new address"
    fqdn: "example.test123.com"
```

## Key Features

- **Complete Configuration Management**: Create, update, and delete SCM configuration objects
- **Idempotent Operations**: Safe to run multiple times with the same expected outcome
- **Roles for Common Tasks**: Pre-built roles for bootstrapping and configuration deployment
- **Inventory Plugin**: Dynamically build inventory from SCM
- **Integration with SCM SDK**: Reliable API interactions with proper error handling

## Installation

```terminal
pip install pan-scm-sdk
ansible-galaxy collection install cdot65.scm
```

## Requirements

- Python 3.8 or higher
- Ansible 2.13 or higher
- `pan-scm-sdk` Python package
