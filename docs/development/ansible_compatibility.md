# Ansible Compatibility Guide

This guide outlines compatibility considerations for the cdot65.scm Ansible collection, particularly
focusing on Ansible test compatibility requirements.

## Python Version Compatibility

While the core functionality of this collection targets Python 3.11+ (as specified in
`pyproject.toml`), the Ansible Galaxy ecosystem requires compatibility with older Python versions
for testing purposes.

### Key Compatibility Requirements

1. **Ansible Test Python Versions**:

   - Ansible tests against multiple Python versions including 3.11 and 3.12
   - Our code needs to be syntax-compatible with these versions even if we don't officially support
     them

2. **Common Python Compatibility Issues**:

   - F-strings (use `"text {0}".format(var)` instead)
   - Type hints (wrap in try/except blocks)
   - Keyword-only arguments
   - Unpacking generalizations

3. **Required Boilerplate**:

   - Add `from __future__ import (absolute_import, division, print_function)` to all Python files
   - Add `__metaclass__ = type` to all Python files
   - Use GPL v3 license headers for all modules

## Import Considerations

1. **Import Order**:

   - Documentation variables (`DOCUMENTATION`, `EXAMPLES`, `RETURN`) must appear before imports in
     modules
   - Use conditional imports for external dependencies like `scm`

2. **External Dependencies**:

   - Add checks for required external dependencies:

   ```python
   try:
       import scm
       HAS_SCM = True
   except ImportError:
       HAS_SCM = False

   # Later in the code:
   if not HAS_SCM:
       module.fail_json(msg="The python pan-scm-sdk module is required for this module")
   ```

## Ansible Compatibility

The collection supports Ansible 2.17.0 and higher as specified in `meta/runtime.yml`. For module
validation testing purposes, the collection should include proper module redirects in this file.

## Manual Fixes

Some issues may require manual intervention:

1. **Import Order**: If a module has imports before documentation variables, you'll need to
   reorganize the file manually:

   - Move all imports after the `DOCUMENTATION`, `EXAMPLES`, and `RETURN` variables
   - Ensure imports are properly organized

2. **Documentation Validation**: If validation errors occur in module documentation:

   - Check for invalid keys in `no_log` parameters
   - Verify all parameter types and choices match the expected values

## Testing

After applying fixes, verify them with:

```bash
ansible-test sanity
```

For targeted tests:

```bash
ansible-test sanity --test import
ansible-test sanity --test pylint
ansible-test sanity --test validate-modules
```

## Ongoing Compatibility

When developing new modules or making changes:

1. Avoid Python 3.6+ specific features like:

   - F-strings
   - Dataclasses
   - Type annotations without fallbacks
   - Walrus operator (:=)

2. Maintain proper import structure:

   - Documentation before imports
   - Proper boilerplate

3. Check dependencies:

   - Always include conditional imports for external packages
   - Add appropriate error messages when dependencies are missing
