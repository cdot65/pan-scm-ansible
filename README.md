[![MIT License](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/cdot65/pan-scm-ansible/blob/main/LICENSE.md)

<img src="https://raw.githubusercontent.com/cdot65/pan-scm-sdk/main/docs/images/logo.svg" width=720 alt="Strata Cloud Manager" />

# Strata Cloud Manager Ansible Collection

This Ansible Collection allows you to manage Palo Alto Networks Strata Cloud Manager (SCM) using the `pan-scm-sdk`
Python SDK.

## Requirements

- Python 3.11 or higher
- Ansible Core 2.17 or higher
- pan-scm-sdk 0.3.22 or higher

## Installation

1. Clone the repository and install the required Python packages:

   ```sh
   git clone https://github.com/cdot65/pan-scm-ansible.git
   cd pan-scm-ansible
   pip install -r requirements.txt
   ```

2. Install the collection:

   ```sh
   ansible-galaxy collection build .
   ansible-galaxy collection install cdot65-scm-x.y.z.tar.gz
   ```

## Example Usage

```yaml
- name: Create an address object
  cdot65.scm.address:
    name: "test123"
    folder: "Texas"
    description: "My new address"
    fqdn: "example.test123.com"
```

## Documentation

For detailed usage, please refer to
the [Documentation](https://github.com/cdot65/pan-scm-ansible/blob/main/pan_scm_ansible_collection/README.md).

## Testing

This collection comes with an Ansible testing automation script to handle common compatibility issues:

```bash
# Make the script executable
chmod +x fix_ansible_tests.sh

# Run the script to fix common testing issues
./fix_ansible_tests.sh
```

For more information on compatibility and testing, see [ANSIBLE_TESTING.md](ANSIBLE_TESTING.md).

## Contributing

- Refer to the [Contributing guide](https://github.com/cdot65/pan-scm-ansible/blob/main/CONTRIBUTING.md) to get started
  developing, testing, and building this collection.
- All code submissions are made through pull requests against the `main` branch.
- Take care to make sure no merge commits are in the submission, and use `git rebase` vs. `git merge` for this reason.

## Reporting Issues

If you're experiencing a problem that you feel is a bug in the SCM Ansible Collection or have ideas for improvement, we
encourage you to open an issue and share your feedback. Please take a look at
our [Issues guide](https://github.com/cdot65/pan-scm-ansible/blob/main/ISSUES.md) before opening a new issue.
