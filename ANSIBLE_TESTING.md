# Ansible Testing in pan-scm-ansible Collection

This document outlines the testing approach and compatibility requirements for the `cdot65.scm` Ansible collection.

## Version Requirements

This collection is designed for:
- **Python 3.11+**
- **Ansible 2.17+**

These requirements are specified in:
- `galaxy.yml`: Collection metadata
- `meta/runtime.yml`: Runtime requirements for Ansible
- `.github/workflows/ansible-test.yml`: CI pipeline configuration

## Testing Approach

### Sanity Tests

The collection uses sanity tests to verify code quality and adherence to Ansible standards. We use ignore files for specific issues that either:
1. Cannot be resolved due to runtime dependencies
2. Will be addressed in future updates

The ignore files are:
- `tests/sanity/ignore-2.17.txt`: For Ansible 2.17 compatibility
- `tests/sanity/ignore-2.18.txt`: For Ansible 2.18+ compatibility

### Categories of Ignored Issues

The following issue types are present in the ignore files:

#### Import Errors for External Dependencies
These are runtime requirements that cannot be satisfied in the test environment:
- `pan-scm-sdk`: The primary SDK for interacting with Strata Cloud Manager
- `pydantic`: Used for validation

#### Documentation Format Issues
Issues like:
- Invalid `no_log` values (fixed for most but not all modules)
- Documentation structure

#### Import Order Issues
All modules currently have imports before documentation, which will be fixed in a future update.

#### License Headers
All modules need GPL v3 license headers, which will be added in a future update.

#### Style Issues
Various PEP8 and pylint issues:
- Trailing whitespace
- Missing final newlines
- Unused imports

### Running Tests Locally

To test the collection locally:

```bash
# Install dependencies
poetry install

# Run linting
poetry run ruff check plugins tests

# Format code
poetry run ruff format plugins tests

# Run Ansible tests
ansible-test sanity --docker default --python 3.11 --ansible 2.17 --use-ignore-file
```

## Future Work

The following improvements are planned:

1. **Import Order Fix**: Move documentation variables before imports
2. **GPL v3 License Headers**: Add to all module files
3. **Style Formatting**: Fix whitespace, newlines, and PEP8 issues
4. **Documentation Format**: Fix all documentation validation issues
5. **Smart Quotes**: Replace Unicode smart quotes with ASCII quotes
6. **Shebang Issues**: Fix incorrect shebangs in shell scripts
7. **Unused Imports**: Clean up unused imports

## Contributing

When contributing to this collection, please ensure your changes:
1. Are compatible with Python 3.11+ and Ansible 2.17+
2. Pass the sanity tests with the ignore files
3. Follow the established code style