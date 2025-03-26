# Contributing

We welcome contributions to the Palo Alto Networks SCM Ansible Collection! This guide outlines the
process for contributing and developing the collection.

## Code of Conduct

All contributors are expected to adhere to our project's code of conduct. Please be respectful and
constructive in your communications and contributions.

## Getting Started

1. **Fork the Repository**: Create a fork of the
   [repository](https://github.com/cdot65/pan-scm-ansible) on GitHub.

2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/YOUR-USERNAME/pan-scm-ansible.git
   cd pan-scm-ansible
   ```

3. **Set Up Development Environment**:

   ```bash
   pip install -r requirements-dev.txt
   pre-commit install
   ```

4. **Create a Branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

This project follows standard Ansible development practices:

- Use YAML for module definitions
- Follow
  [Ansible module guidelines](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)
- PEP 8 for Python code
- Use meaningful variable names and include docstrings

### Pre-commit Hooks

We use pre-commit hooks to ensure code quality:

```bash
pre-commit run --all-files
```

### Testing

All contributions should include appropriate tests:

1. **Sanity Tests**:

   ```bash
   ansible-test sanity --docker
   ```

2. **Unit Tests**:

   ```bash
   ansible-test units --docker
   ```

3. **Integration Tests** (requires SCM credentials):

   ```bash
   ansible-test integration --docker
   ```

### Documentation

Update documentation to reflect your changes:

- Update module documentation in the `docs/` directory
- Add examples to showcase new functionality
- Update CHANGELOG.md with your changes

## Submitting Changes

1. **Commit Your Changes**:

   ```bash
   git add .
   git commit -m "feat: add support for X"
   ```

   We follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

2. **Push to Your Fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**: Open a pull request from your fork to the main repository.

4. **Code Review**: Maintainers will review your code and may request changes.

5. **Merge**: Once approved, your changes will be merged into the main branch.

## Adding New Modules

When adding a new module:

1. Use the module template:

   ```bash
   ./scripts/create_module.py --name your_module_name
   ```

2. Implement the module functionality in `plugins/modules/your_module_name.py`

3. Add documentation in `docs/collection/modules/your_module_name.md`

4. Add examples in `examples/your_module_name.yml`

5. Add tests in `tests/unit/plugins/modules/test_your_module_name.py`

## Reporting Bugs

If you find a bug, please [open an issue](https://github.com/cdot65/pan-scm-ansible/issues/new)
with:

- A clear description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Version information

## Feature Requests

For feature requests, [open an issue](https://github.com/cdot65/pan-scm-ansible/issues/new)
describing:

- The feature you'd like to see
- Use cases for the feature
- How it would integrate with existing functionality

## Questions?

If you have questions about contributing, please open a discussion on GitHub or contact the
maintainers.

Thank you for contributing to the SCM Ansible Collection!
