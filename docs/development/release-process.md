# Release Process

This document outlines the process for releasing new versions of the Palo Alto Networks Strata Cloud
Manager Ansible Collection.

## Version Numbering

The collection follows [Semantic Versioning](https://semver.org/) (SemVer):

- **MAJOR** version: Incompatible API changes
- **MINOR** version: Added functionality in a backward compatible manner
- **PATCH** version: Backward compatible bug fixes

## Release Preparation

### 1. Update Documentation

- Update CHANGELOG.md with all notable changes
- Verify all module documentation is current
- Update version numbers in:
  - galaxy.yml
  - pyproject.toml
  - README.md

### 2. Quality Assurance

- Run all linting checks:

  ```bash
  make lint
  ```

- Run all tests:

  ```bash
  make test
  ```

- Build and check documentation:

  ```bash
  make docs
  ```

### 3. Create a Release Branch

```bash
git checkout -b release/v0.1.0
git push origin release/v0.1.0
```

## Release Process

### 1. Build the Collection

```bash
ansible-galaxy collection build
```

This creates a `.tar.gz` file in the project root.

### 2. Test the Built Collection

Install the built collection in a clean environment and verify its functionality:

```bash
ansible-galaxy collection install cdot65-scm-0.1.0.tar.gz -f
```

### 3. Create a GitHub Release

1. Create a pull request from the release branch to main
2. After approval and merge, tag the release:

```bash
git checkout main
git pull
git tag v0.1.0
git push origin v0.1.0
```

3. On GitHub, create a new release:
   - Use the tag you created
   - Title: "v0.1.0"
   - Description: Copy the relevant section from CHANGELOG.md
   - Attach the built collection .tar.gz file

### 4. Publish to Ansible Galaxy

```bash
ansible-galaxy collection publish cdot65-scm-0.1.0.tar.gz
```

## Post-Release

### 1. Update Version for Development

Update version numbers to the next development version:

- galaxy.yml: increase version and add ".dev0" suffix
- pyproject.toml: increase version

### 2. Announce the Release

- Announce on appropriate channels
- Update documentation site

## Hotfix Process

For critical bugs that need immediate fixing:

1. Create a hotfix branch from the release tag:

   ```bash
   git checkout -b hotfix/v0.1.1 v0.1.0
   ```

2. Fix the bug, test, and update documentation

3. Update version numbers to the hotfix version (e.g., 0.1.1)

4. Follow the normal release process from step 2 onwards

## Release Checklist

- [ ] Update documentation
- [ ] Update version numbers
- [ ] Run all quality checks
- [ ] Create release branch
- [ ] Build and test collection
- [ ] Create GitHub release and tag
- [ ] Publish to Ansible Galaxy
- [ ] Update development version
- [ ] Make release announcement

## Troubleshooting

### Common Issues

- **Version conflict**: Ensure all version numbers are consistent
- **Galaxy upload failure**: Verify your API key and collection namespace
- **Documentation issues**: Rebuild docs and verify they're accurate

For help with the release process, contact the project maintainers.
