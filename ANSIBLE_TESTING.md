# Ansible Testing Compatibility Guide

## Overview

This guide explains how to make the Palo Alto Networks Strata Cloud Manager Ansible Collection (`cdot65.scm`) compatible with Ansible's sanity tests while preserving its Python 3.11+ functionality.

## Issues and Solutions

### 1. Python Compatibility Issues

The collection is designed for Python 3.11+, but Ansible's test framework requires compatibility with older Python versions (2.7, 3.5-3.11).

**Issues:**
- F-strings (not supported in Python 2.7 or 3.5)
- Type annotations (not supported in Python 2.7)
- Python 3.6+ specific imports

**Solutions:**
- Replace f-strings with `.format()` method
- Make type annotations conditional with try/except blocks
- Add fallback definitions for older Python versions

### 2. Missing Boilerplate

Ansible modules require specific imports and declarations.

**Issues:**
- Missing `from __future__ import (absolute_import, division, print_function)`
- Missing `__metaclass__ = type`
- Missing GPL v3 license headers

**Solutions:**
- Add the required boilerplate to all Python files
- Add GPL v3 license headers to all modules

### 3. External Dependencies

The test environment doesn't have access to required external packages.

**Issues:**
- Missing `scm` package (Palo Alto Networks SCM SDK)
- Missing `pydantic` package
- Import errors in test environment

**Solutions:**
- Add conditional imports with try/except
- Add dependency checks in modules
- Use clear error messages for missing dependencies

### 4. Documentation Structure

Ansible requires specific documentation structure.

**Issues:**
- Imports before documentation in modules
- Invalid documentation format in some modules

**Solutions:**
- Ensure documentation variables come before imports
- Validate and fix documentation structure

### 5. Code Style Issues

Various style and formatting issues flagged by linters.

**Issues:**
- Trailing whitespace
- Missing final newlines
- Smart quotes in LICENSE.md

**Solutions:**
- Automatically fix whitespace and newline issues
- Replace smart quotes with ASCII quotes

## Using the Fix Script

We've provided a script to address these issues automatically:

```bash
# Run the fix script
./fix_ansible_tests.sh
```

This script:
1. Adds necessary imports and boilerplate
2. Fixes f-strings and type annotations
3. Adds conditional imports for dependencies
4. Fixes license headers and formatting issues
5. Updates runtime.yml for older Ansible versions
6. Fixes shebang and quote issues

## Remaining Manual Steps

Some issues may require manual intervention:

1. **Import Order**:
   If imports appear before documentation variables, you'll need to manually reorder the file structure.

2. **Documentation Validation**:
   Some documentation format issues may require manual fixes:
   - Fix `DOCUMENTATION.options.provider.suboptions.client_secret.no_log` issues

## Development Guidelines

When developing new modules:

1. **Python Version Independence**:
   - Avoid f-strings and use `.format()` instead
   - Handle type annotations with try/except blocks
   - Don't rely on Python 3.6+ only features

2. **Documentation First**:
   - Always put documentation variables (`DOCUMENTATION`, `EXAMPLES`, `RETURN`) before imports

3. **Dependency Handling**:
   - Always wrap external imports in try/except blocks
   - Add appropriate dependency checks

4. **Testing Before Submitting**:
   - Run `ansible-test sanity` to verify changes

## Library Requirements

The collection requires:
- pan-scm-sdk (Palo Alto Networks Strata Cloud Manager SDK)
- pydantic (for validation in some modules)

These are runtime dependencies and not required for passing tests, as we've added appropriate checks.