# Contributing to the Strata Cloud Manager Ansible Collection

Thank you for your interest in contributing to the Palo Alto Networks Strata Cloud Manager Ansible Collection. This guide provides information on how to contribute to this project effectively.

## Getting Started

### Setting Up Your Development Environment

1. **Fork and Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/pan-scm-ansible.git
   cd pan-scm-ansible
   ```

2. **Install Development Dependencies**:
   ```bash
   poetry install
   poetry run pre-commit install
   ```

3. **Create a Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Building and Testing

We provide a comprehensive Makefile with various commands to help you develop, test, and validate your contributions:

```bash
# Install dependencies
make setup

# Run linting
make lint

# Format code
make format

# Run tests
make test

# Build documentation
make docs
```

### Code Style and Guidelines

The codebase follows these conventions:

- **Python**: Follow PEP 8 guidelines with a maximum line length of 100 characters
- **Imports**: Sort using isort with black profile
- **Formatting**: Use double quotes for strings and 4 spaces for indentation
- **Documentation**: Include docstrings with Args and Returns sections for functions
- **Error Handling**: Use try/except blocks with specific exceptions

### Creating New Modules

When adding a new module:

1. **Create Module File**:
   - Create a new file in `pan_scm_ansible/plugins/modules/`
   - Follow the structure of existing modules

2. **Documentation**:
   - Add DOCUMENTATION, EXAMPLES, and RETURN variables
   - Create a corresponding Markdown file in `docs/collection/modules/`

3. **Tests**:
   - Create test playbooks in the `tests/` directory

## Pull Request Process

1. **Ensure Code Quality**:
   - Run `make lint-format` to ensure your code passes all linting checks
   - Run `make test` to validate functionality

2. **Update Documentation**:
   - Ensure module documentation is complete
   - Update README.md if necessary
   - If adding new features, update relevant docs

3. **Submit Pull Request**:
   - Create a PR against the `main` branch
   - Follow the PR template
   - Provide a clear description of your changes

4. **Code Review**:
   - Respond to reviewer feedback
   - Make requested changes and push updates

## Commit Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) standard:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions or modifications
- `refactor:` for code refactoring
- `chore:` for routine tasks, maintenance, etc.

Example:
```
feat: add support for address groups

Implement address_group module for managing static and dynamic address groups
in Strata Cloud Manager. Add corresponding documentation and tests.
```

## Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the [GitHub Issues](https://github.com/cdot65/pan-scm-ansible/issues)
2. If not, create a new issue with:
   - Clear description
   - Steps to reproduce (for bugs)
   - Expected behavior
   - Actual behavior
   - Version information

## Development Best Practices

1. **Keep Changes Focused**:
   - Each PR should address a single concern
   - Avoid combining unrelated changes

2. **Test Coverage**:
   - Write tests for new functionality
   - Ensure existing tests pass

3. **Documentation**:
   - Update documentation to reflect changes
   - Include examples for new features

4. **Backward Compatibility**:
   - Maintain backward compatibility when possible
   - Document breaking changes clearly

Thank you for contributing to the Strata Cloud Manager Ansible Collection!