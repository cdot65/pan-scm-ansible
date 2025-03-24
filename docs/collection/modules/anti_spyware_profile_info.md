# Anti-Spyware Profile Information Module

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Requirements](#requirements)
4. [Usage Examples](#usage-examples)
    - [Retrieving Specific Profile Information](#retrieving-specific-profile-information)
    - [Listing All Profiles](#listing-all-profiles)
    - [Filtering by Cloud Inline Analysis](#filtering-by-cloud-inline-analysis)
    - [Filtering by Rules](#filtering-by-rules)
5. [Return Values](#return-values)
6. [Error Handling](#error-handling)
7. [Best Practices](#best-practices)
8. [Related Modules](#related-modules)

## Overview

The `anti_spyware_profile_info` module provides functionality to gather information about anti-spyware profile objects
in Palo Alto Networks' Strata Cloud Manager. This is an information-gathering module that doesn't make any changes to
the system. It supports retrieving a specific anti-spyware profile by name or listing all profiles with various filter
options including cloud inline analysis, rules, and container filters.

## Module Parameters

| Parameter              | Required | Type | Choices     | Default    | Comments                                                        |
|------------------------|----------|------|-------------|------------|-----------------------------------------------------------------|
| name                   | no       | str  |             |            | The name of a specific anti-spyware profile to retrieve.        |
| gather_subset          | no       | list | all, config | ['config'] | Determines which information to gather about profiles.          |
| folder                 | no*      | str  |             |            | Filter profiles by folder container.                            |
| snippet                | no*      | str  |             |            | Filter profiles by snippet container.                           |
| device                 | no*      | str  |             |            | Filter profiles by device container.                            |
| exact_match            | no       | bool |             | false      | Only return objects defined exactly in the specified container. |
| exclude_folders        | no       | list |             |            | List of folder names to exclude from results.                   |
| exclude_snippets       | no       | list |             |            | List of snippet values to exclude from results.                 |
| exclude_devices        | no       | list |             |            | List of device values to exclude from results.                  |
| cloud_inline_analysis  | no       | bool |             |            | Filter by cloud inline analysis setting.                        |
| rules                  | no       | list |             |            | Filter by rule names.                                           |
| provider               | yes      | dict |             |            | Authentication credentials.                                     |
| provider.client_id     | yes      | str  |             |            | Client ID for authentication.                                   |
| provider.client_secret | yes      | str  |             |            | Client secret for authentication.                               |
| provider.tsg_id        | yes      | str  |             |            | Tenant Service Group ID.                                        |
| provider.log_level     | no       | str  |             | INFO       | Log level for the SDK.                                          |

!!! note
- If `name` is not specified, one container type (`folder`, `snippet`, or `device`) must be provided.
- Container parameters (`folder`, `snippet`, `device`) are mutually exclusive.

## Requirements

- SCM Python SDK (`pan-scm-sdk`)
- Python 3.8 or higher
- Ansible 2.13 or higher

## Usage Examples

### Retrieving Specific Profile Information

<div class="termy">

<!-- termynal -->

```yaml
- name: Get information about a specific anti-spyware profile
  cdot65.scm.anti_spyware_profile_info:
    provider: "{{ provider }}"
    name: "Custom-Spyware-Profile"
    folder: "Production"
  register: profile_info
```

</div>

### Listing All Profiles

<div class="termy">

<!-- termynal -->

```yaml
- name: List all anti-spyware profiles in a folder
  cdot65.scm.anti_spyware_profile_info:
    provider: "{{ provider }}"
    folder: "Production"
  register: all_profiles
```

</div>

### Filtering by Cloud Inline Analysis

<div class="termy">

<!-- termynal -->

```yaml
- name: List profiles with cloud inline analysis enabled
  cdot65.scm.anti_spyware_profile_info:
    provider: "{{ provider }}"
    folder: "Production"
    cloud_inline_analysis: true
  register: cloud_enabled_profiles
```

</div>

### Filtering by Rules

<div class="termy">

<!-- termynal -->

```yaml
- name: List profiles with specific rules
  cdot65.scm.anti_spyware_profile_info:
    provider: "{{ provider }}"
    folder: "Production"
    rules: ["Block-Critical-Threats"]
  register: rule_profiles
```

</div>

## Return Values

| Name                  | Description                                                        | Type | Returned                   | Sample                                                                                                                                                                                                                                                                                                                            |
|-----------------------|--------------------------------------------------------------------|------|----------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| anti_spyware_profiles | List of anti-spyware profile objects matching the filter criteria. | list | when name is not specified | [{"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Custom-Spyware-Profile", "description": "Custom anti-spyware profile", "cloud_inline_analysis": true, "rules": [{"name": "Block-Critical-Threats", "severity": ["critical"], "category": "spyware", "packet_capture": "single-packet"}], "folder": "Production"}, {...}] |
| anti_spyware_profile  | Information about the requested anti-spyware profile.              | dict | when name is specified     | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Custom-Spyware-Profile", "description": "Custom anti-spyware profile", "cloud_inline_analysis": true, "rules": [{"name": "Block-Critical-Threats", "severity": ["critical"], "category": "spyware", "packet_capture": "single-packet"}], "folder": "Production"}          |

## Error Handling

Common errors you might encounter when using this module:

| Error                     | Description                                             | Resolution                                     |
|---------------------------|---------------------------------------------------------|------------------------------------------------|
| Profile not found         | Specified profile does not exist in the given container | Verify the profile name and container location |
| Missing query parameter   | Required parameter not provided                         | Ensure all required parameters are specified   |
| Invalid filter parameters | Filter parameters in incorrect format                   | Check parameter format requirements            |

<div class="termy">

<!-- termynal -->

```yaml
- name: Handle potential errors with block/rescue
  block:
    - name: Attempt to retrieve anti-spyware profile information
      cdot65.scm.anti_spyware_profile_info:
        provider: "{{ provider }}"
        name: "NonExistentProfile"
        folder: "Production"
      register: profile_info_result
  rescue:
    - name: Handle profile not found error
      debug:
        msg: "Anti-spyware profile could not be found, continuing with other tasks"
    - name: Continue with other tasks
      # Additional recovery tasks
```

</div>

## Best Practices

1. **Querying Strategies**
    - Use name parameter for querying specific profiles
    - Use container filters (folder, snippet, device) for listing profiles
    - Combine with JMESPath filters in Ansible for advanced filtering

2. **Performance Optimization**
    - Include specific container parameters to narrow search scope
    - Use exact_match parameter when possible to improve performance
    - Use exclusion filters to narrow down results when querying large systems

3. **Filtering Techniques**
    - Use cloud_inline_analysis filter to find profiles with specific cloud analysis settings
    - Use rules filter to find profiles that include specific rule names
    - Combine multiple filters for more precise results

4. **Integration with Other Modules**
    - Use anti_spyware_profile_info module output as input for anti_spyware_profile module operations
    - Chain info queries with security policy modules to see where profiles are used
    - Leverage the registered variables for conditional tasks and reporting

5. **Error Management**
    - Implement proper error handling with block/rescue pattern
    - Handle non-existent profiles gracefully in playbooks
    - Use ignore_errors where appropriate for non-critical profile queries

## Related Modules

- [anti_spyware_profile](anti_spyware_profile.md) - Manage anti-spyware profile objects
- [security_rule](security_rule.md) - Manage security rules that use anti-spyware profiles
- [security_profiles_group](security_profiles_group.md) - Manage security profile groups that include anti-spyware profiles

## Author

- Calvin Remsburg (@cdot65)