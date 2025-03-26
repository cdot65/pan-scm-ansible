# Url Categories Information Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [URL Category Info Parameters](#url-category-info-parameters)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Retrieving a Specific URL Category](#retrieving-a-specific-url-category)
    - [Listing All URL Categories](#listing-all-url-categories)
    - [Filtering URL Categories by List Members](#filtering-url-categories-by-list-members)
    - [Advanced Filtering](#advanced-filtering)
    - [Filtering with Ansible](#filtering-with-ansible)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `url_categories_info` module retrieves information about URL categories in Palo Alto Networks' Strata Cloud Manager (SCM). It allows you to fetch details about specific URL categories or list multiple URL categories with various filtering options. This information-gathering module is essential for auditing URL filtering configurations, preparing for policy updates, and understanding the current URL category landscape in your security environment.

## Core Methods

| Method    | Description                      | Parameters                    | Return Type                    |
| --------- | -------------------------------- | ----------------------------- | ------------------------------ |
| `fetch()` | Gets a specific URL category     | `name: str`, `container: str` | `UrlCategoryResponseModel`     |
| `list()`  | Lists URL categories with filters| `folder: str`, `**filters`    | `List[UrlCategoryResponseModel]` |

## URL Category Info Parameters

| Parameter          | Type   | Required      | Description                                                    |
| ------------------ | ------ | ------------- | -------------------------------------------------------------- |
| `name`             | str    | No            | Name of a specific URL category to retrieve                    |
| `gather_subset`    | list   | No            | Information to gather (default: ['config'])                    |
| `folder`           | str    | One container* | Filter URL categories by folder container                      |
| `snippet`          | str    | One container* | Filter URL categories by snippet container                     |
| `device`           | str    | One container* | Filter URL categories by device container                      |
| `exact_match`      | bool   | No            | Only return objects defined exactly in the specified container |
| `exclude_folders`  | list   | No            | List of folder names to exclude from results                   |
| `exclude_snippets` | list   | No            | List of snippet values to exclude                              |
| `exclude_devices`  | list   | No            | List of device values to exclude                               |
| `members`          | list   | No            | Filter by URLs or categories in the list                       |

*One container parameter is required when `name` is not specified.

### Provider Dictionary

| Parameter       | Type | Required | Description                            |
| --------------- | ---- | -------- | -------------------------------------- |
| `client_id`     | str  | Yes      | Client ID for SCM authentication        |
| `client_secret` | str  | Yes      | Client secret for SCM authentication    |
| `tsg_id`        | str  | Yes      | Tenant Service Group ID                 |
| `log_level`     | str  | No       | Log level for the SDK (default: "INFO") |

## Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid request data or format |
| `MissingQueryParameterError` | Missing required parameters    |
| `ObjectNotPresentError`      | URL category not found         |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## Basic Configuration

The URL Categories Info module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic URL Categories Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about URL categories
      cdot65.scm.url_categories_info:
        provider: "{{ provider }}"
        folder: "Security"
      register: categories_result
    
    - name: Display categories
      debug:
        var: categories_result.url_categories
```

## Usage Examples

### Retrieving a Specific URL Category

This example retrieves detailed information about a specific URL category by name.

```yaml
- name: Get information about a specific URL category
  cdot65.scm.url_categories_info:
    provider: "{{ provider }}"
    name: "Malicious_URLs"
    folder: "Security"
  register: url_category_info

- name: Display the URL category information
  debug:
    var: url_category_info.url_category
    
- name: Check URL category type
  debug:
    msg: "Category type is {{ url_category_info.url_category.type }}"
  when: url_category_info.url_category is defined
```

### Listing All URL Categories

This example lists all URL categories in a specific folder.

```yaml
- name: List all URL categories in a folder
  cdot65.scm.url_categories_info:
    provider: "{{ provider }}"
    folder: "Security"
  register: all_url_categories

- name: Display all URL categories
  debug:
    var: all_url_categories.url_categories
    
- name: Count URL categories
  debug:
    msg: "Found {{ all_url_categories.url_categories | length }} URL categories"
```

### Filtering URL Categories by List Members

This example demonstrates filtering URL categories by specific entries in their lists.

```yaml
- name: List URL categories containing specific URLs
  cdot65.scm.url_categories_info:
    provider: "{{ provider }}"
    folder: "Security"
    members: ["malware.example.com"]
  register: filtered_url_categories

- name: Display filtered URL categories
  debug:
    var: filtered_url_categories.url_categories
    
- name: Use filtered results in security policy
  debug:
    msg: "URL categories containing malware.example.com: {{ filtered_url_categories.url_categories | map(attribute='name') | join(', ') }}"
```

### Advanced Filtering

This example shows how to use exact matches and exclusion filters for more precise results.

```yaml
- name: List URL categories with exact match and exclusions
  cdot65.scm.url_categories_info:
    provider: "{{ provider }}"
    folder: "Security"
    exact_match: true
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_url_categories

- name: Display filtered URL categories
  debug:
    var: filtered_url_categories.url_categories
```

### Filtering with Ansible

This example demonstrates how to use Ansible's built-in filters to process the results.

```yaml
- name: Get all URL categories for further filtering
  cdot65.scm.url_categories_info:
    provider: "{{ provider }}"
    folder: "Security"
  register: all_categories
  
# Filter in memory for URL categories with "malicious" in the name
- name: Filter for malicious URL categories
  set_fact:
    malicious_categories: 
      url_categories: "{{ all_categories.url_categories | selectattr('name', 'search', 'malicious') | list }}"

# Work with the filtered results
- name: Display malicious categories
  debug:
    var: malicious_categories
```

## Managing Configuration Changes

As an info module, `url_categories_info` does not make any configuration changes. However, you can use the information it retrieves to make decisions about other configuration operations.

```yaml
- name: Use URL category information for security policy configuration
  block:
    - name: Get malicious URL categories
      cdot65.scm.url_categories_info:
        provider: "{{ provider }}"
        folder: "Security"
        members: ["malware"]
      register: malicious_categories
      
    - name: Create security rule to block malicious URLs
      cdot65.scm.security_rule:
        provider: "{{ provider }}"
        name: "Block-Malicious-URLs"
        folder: "Security"
        source_zones: ["Trust"]
        destination_zones: ["Untrust"]
        source_addresses: ["any"]
        destination_addresses: ["any"]
        url_categories: "{{ malicious_categories.url_categories | map(attribute='name') | list }}"
        action: "deny"
        description: "Block access to known malicious URLs"
        state: "present"
      when: malicious_categories.url_categories | length > 0
      
    - name: Commit changes if rule was created
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Security"]
        description: "Created security rule to block malicious URLs"
      when: malicious_categories.url_categories | length > 0
```

### Return Values

When retrieving a specific URL category:

| Name         | Description                            | Type | Returned                      | Sample                                                                                                                                        |
| ------------ | -------------------------------------- | ---- | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| url_category | Information about the requested category | dict | success, when name is specified | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Malicious_URLs", "description": "List of known malicious URLs", "type": "URL List", "list": ["malware.example.com", "phishing.example.net"], "folder": "Security"} |

When listing URL categories:

| Name          | Description                                        | Type | Returned                          | Sample                                                                                                                                         |
| ------------- | -------------------------------------------------- | ---- | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| url_categories | List of URL categories matching the filter criteria | list | success, when name is not specified | [{"id": "123...", "name": "Malicious_URLs", ...}, {"id": "234...", "name": "Social_Media", ...}] |

## Error Handling

It's important to handle potential errors when retrieving URL category information.

```yaml
- name: Get URL category information with error handling
  block:
    - name: Attempt to get URL category info
      cdot65.scm.url_categories_info:
        provider: "{{ provider }}"
        name: "NonExistentCategory"
        folder: "Security"
      register: result
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a 'not found' error
      debug:
        msg: "URL category does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

## Best Practices

### Filtering Strategies

- Use specific filters to narrow down results and improve performance
- Combine container filters with member and exclusion filters for precision
- Use exact_match=true when you only want objects defined directly in the container
- Document filtering patterns used in playbooks for team understanding
- Create reusable tasks for common filtering operations

### Container Management

- Use consistent container types across operations
- Filter at the API level whenever possible rather than post-processing
- Document container hierarchies and relationships
- Consider performance implications when working with large containers
- Use exclusion filters to refine results in complex environments

### Member Filtering

- Use member filtering to find categories containing specific URLs
- Create playbooks to audit URL category memberships
- Document which URL categories contain critical URLs
- Use member filtering to identify overlap between categories
- Consider case sensitivity when filtering by URL members

### Performance Optimization

- Include specific container parameters to narrow search scope
- Use exact_match for faster, more specific queries
- Combine multiple filters to minimize result sets
- Request only the gather_subset data needed
- Process large result sets in batches

### Integration with Security Policies

- Map URL categories to security policies before making changes
- Use URL category information to identify potential policy gaps
- Create documentation linking URL categories to security policies
- Implement version control for URL category changes
- Test URL filtering policies in a safe environment before deployment

### Automation and Reporting

- Create regular reports on URL category usage
- Build automated auditing of URL category memberships
- Develop playbooks to synchronize URL categories across environments
- Create dashboards of URL filtering effectiveness
- Schedule regular reviews of URL category configurations

## Related Modules

- [url_categories](url_categories.md) - Manage URL categories (create, update, delete)
- [security_rule](security_rule.md) - Configure security policies that use URL categories
- [security_rule_info](security_rule_info.md) - Get information about security rules
- [security_profiles_group](security_profiles_group.md) - Configure security profile groups
- [log_forwarding_profile](log_forwarding_profile.md) - Configure log forwarding for URL filtering events
