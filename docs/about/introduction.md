# Introduction

The Palo Alto Networks Strata Cloud Manager (SCM) Ansible Collection provides a comprehensive set of
Ansible modules, roles, and plugins designed to automate the configuration and management of Palo
Alto Networks SCM.

## What is Strata Cloud Manager?

Strata Cloud Manager (SCM) is Palo Alto Networks' cloud-delivered service for centralized management
of network security. It provides a unified management plane for Palo Alto Networks security services
and products, enabling organizations to simplify operations and improve security posture.

## About This Collection

This collection leverages the `pan-scm-sdk` Python SDK to interact with the SCM API, providing
Ansible users with reliable and consistent automation capabilities. The collection is designed with
the following goals in mind:

- **Simplify Automation**: Reduce complex SCM API interactions into easy-to-use Ansible modules
- **Ensure Idempotency**: Safe to run repeatedly with consistent results
- **Provide Comprehensive Coverage**: Support for a wide range of SCM configuration objects
- **Maintain Quality**: Rigorous testing and documentation

## Collection Contents

The collection includes:

- **Modules**: Individual modules for managing SCM configuration objects
- **Roles**: Pre-built roles for common SCM management tasks
- **Plugins**: Inventory plugins and lookups for dynamic integration with SCM

## Use Cases

The SCM Ansible Collection can be used for various network security automation scenarios:

- **Configuration Management**: Deploy and manage SCM configurations at scale
- **Security Policy Automation**: Automate security policy changes with proper approval workflows
- **Infrastructure as Code**: Manage SCM configurations using GitOps principles
- **Compliance Automation**: Ensure configurations meet compliance requirements through automation

## License

This collection is released under the MIT License, allowing for broad use in both commercial and
non-commercial applications.
