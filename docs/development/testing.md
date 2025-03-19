# Testing the SCM Ansible Collection

This guide covers how to test the Palo Alto Networks Strata Cloud Manager Ansible Collection during development.

## Testing Framework

The collection uses the following testing mechanisms:

1. **Linting and Style Checking**:
   - Ruff for Python linting and formatting
   - isort for import sorting
   - ansible-lint for Ansible-specific linting

2. **Functional Testing**:
   - Ansible playbooks for module testing
   - Integration tests against SCM API

## Setting Up Test Environment

### Prerequisites

- Python 3.11 or higher
- Poetry installed
- SCM credentials for integration testing

### Initial Setup

```bash
# Install dependencies
poetry install

# Install pre-commit hooks
poetry run pre-commit install
```

## Running Tests

### Lint and Style Checks

```bash
# Run all linting checks
make lint

# Format code
make format

# Auto-fix linting issues
make fix
```

### Functional Tests

#### Testing Individual Modules

To test a specific module, run the corresponding test playbook:

```bash
# Example: Test the address module
poetry run ansible-playbook tests/test_address.yaml

# Example: Test the address_group module
poetry run ansible-playbook tests/test_address_group.yaml
```

#### Configuring Test Credentials

The test playbooks load credentials from a vault-encrypted file:

1. Create a `tests/.vault_password` file containing your vault password
2. Create a `tests/vault.yaml` file with the following content:

```yaml
client_id: "your_client_id"
client_secret: "your_client_secret"
tsg_id: "your_tsg_id"
```

3. Encrypt the file:
```bash
ansible-vault encrypt tests/vault.yaml
```

## Continuous Integration

The repository includes GitHub Actions workflows for automated testing:

- **Code Quality**: Runs linting and style checks
- **Unit Tests**: Runs unit tests with pytest
- **Integration Tests**: Runs integration tests against SCM API

## Writing Tests

### Adding a New Test Playbook

1. Create a new YAML file in the `tests/` directory
2. Include common setup tasks for required test objects
3. Test your module's functionality:
   - Create a resource
   - Update a resource
   - Verify idempotence
   - Delete a resource
4. Include cleanup tasks to remove test objects

Example test playbook structure:

```yaml
---
- name: Test Module Name
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
    # Setup tasks
    - name: Create prerequisites
      # ...

    # Test tasks
    - name: Create a resource
      cdot65.scm.module_name:
        provider: "{{ provider }}"
        name: "Test_Resource"
        # parameters...
        state: "present"
      register: create_result

    - name: Verify create result
      assert:
        that:
          - create_result.changed == true
          - create_result.resource.name == "Test_Resource"

    # Update test

    # Idempotence test

    # Delete test

    # Cleanup tasks
```

## Test Best Practices

1. **Test All Module Functions**:
   - Create, update, delete operations
   - Parameter validation
   - Error handling

2. **Verify Idempotence**:
   - Run the same task twice and ensure the second run reports no changes

3. **Clean Up After Tests**:
   - Remove all test resources after testing
   - Use `always` blocks to ensure cleanup happens even if tests fail

4. **Use Descriptive Names**:
   - Name test resources with a prefix to identify them as test objects
   - Use descriptive task names to document what's being tested

5. **Register and Verify Results**:
   - Use `register` to capture task results
   - Use `assert` tasks to verify expected behavior

## Troubleshooting

### Common Issues

- **Authentication Failures**: Verify your SCM credentials in vault.yaml
- **API Rate Limiting**: Add delays between API calls if hitting rate limits
- **Test Resource Conflicts**: Ensure unique names for test resources

### Debugging Tips

- Enable verbose output with `-v`, `-vv`, or `-vvv` flags
- Set provider log_level to "DEBUG" for detailed API logs
- Use the `debug` module to inspect variables during playbook execution

For additional help, please open an issue on the [GitHub repository](https://github.com/cdot65/pan-scm-ansible/issues).