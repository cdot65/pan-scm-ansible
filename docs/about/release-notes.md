# Release Notes

## Version 1.0.0 (2025-03-15)

Initial release of the Palo Alto Networks SCM Ansible Collection.

### Added
- Core modules for SCM object management:
  - Address and Address Group modules
  - Application and Application Group modules
  - Security Rule module
  - Tag module
  - Service and Service Group modules
  - Security Zone module
  - IKE Gateway module
  - Remote Networks module
- Bootstrap role for initial SCM setup
- Deploy Configuration role for managing configuration deployment
- Inventory plugin for dynamic SCM inventory
- Lookup plugins for SCM data

### Known Issues
- Integration with Terraform HCP SCM provider not yet implemented
- Limited support for advanced security policy features
- BGP routing module supports basic configurations only

## Version 0.9.0 (2025-02-28)

Beta release for testing and feedback.

### Added
- Initial implementation of core modules
- Basic documentation
- Test framework

### Known Issues
- Role documentation incomplete
- Some error handling needs improvement
- Performance optimizations pending for large deployments

## Version 0.5.0 (2025-01-15)

Alpha release for initial testing.

### Added
- Prototype modules for basic SCM objects
- Framework for authentication and API interaction
- Initial CI/CD pipeline
