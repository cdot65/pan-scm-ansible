# Security Rule Information Module

## Table of Contents

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Future Development](#future-development)

## Overview

The `security_rule_info` module will provide functionality to gather information about security rule objects in Palo Alto Networks' Strata Cloud Manager. This module is currently in development and will be available in a future release.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Future Development

This module is planned for a future release and will include the following features:

- Retrieving information about specific security rules by name
- Listing all security rules with various filter options
- Filtering by source, destination, application, service, and other criteria
- Support for container-based filtering (folder, snippet, device)

Until this module is implemented, you can use the `security_rule` module to manage security rules in SCM.

## Related Modules

- [security_rule](security_rule.md) - Manage security rule objects
- [service](service.md) - Manage individual service objects
- [service_group](service_group.md) - Manage service group objects
- [address](address.md) - Manage address objects
- [address_group](address_group.md) - Manage address group objects

## Author

- Calvin Remsburg (@cdot65)