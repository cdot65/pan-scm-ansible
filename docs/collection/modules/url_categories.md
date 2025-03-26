# Url Categories Configuration Object

## Table of Contents

01. [Overview](#overview)
02. [Core Methods](#core-methods)
03. [URL Category Model Attributes](#url-category-model-attributes)
04. [Exceptions](#exceptions)
05. [Basic Configuration](#basic-configuration)
06. [Usage Examples](#usage-examples)
    - [Creating URL Categories](#creating-url-categories)
    - [URL List Category](#url-list-category)
    - [Category Match Type](#category-match-type)
    - [Updating URL Categories](#updating-url-categories)
    - [Deleting URL Categories](#deleting-url-categories)
07. [Managing Configuration Changes](#managing-configuration-changes)
08. [Error Handling](#error-handling)
09. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## Overview

The `url_categories` module manages URL categories within Palo Alto Networks' Strata Cloud Manager (SCM). It provides functionality to create, update, and delete URL category objects used for URL filtering and security policies. URL categories are essential components in web filtering solutions, allowing organizations to control access to websites based on their categorization.

URL categories can be of two types:

- **URL List**: Contains a list of specific URLs to match
- **Category Match**: Matches predefined URL categories that are maintained by Palo Alto Networks

## Core Methods

| Method     | Description                   | Parameters                       | Return Type                    |
| ---------- | ----------------------------- | -------------------------------- | ------------------------------ |
| `create()` | Creates a new URL category    | `data: Dict[str, Any]`           | `UrlCategoryResponseModel`     |
| `update()` | Updates an existing category  | `category: UrlCategoryUpdate`    | `UrlCategoryResponseModel`     |
| `delete()` | Removes a URL category        | `object_id: str`                 | `None`                         |
| `fetch()`  | Gets a category by name       | `name: str`, `container: str`    | `UrlCategoryResponseModel`     |
| `list()`   | Lists categories with filters | `folder: str`, `**filters`       | `List[UrlCategoryResponseModel]` |

## URL Category Model Attributes

| Attribute     | Type | Required      | Description                                                 |
| ------------- | ---- | ------------- | ----------------------------------------------------------- |
| `name`        | str  | Yes           | Name of the URL category (max 31 chars)                     |
| `description` | str  | No            | Description of the URL category                             |
| `list`        | list | Yes           | List of URLs or predefined categories                       |
| `type`        | str  | No            | Type of URL category: 'URL List' or 'Category Match'        |
| `folder`      | str  | One container* | The folder where this resource is stored (max 64 chars)     |
| `snippet`     | str  | One container* | The snippet where this resource is defined (max 64 chars)   |
| `device`      | str  | One container* | The device where this resource is defined (max 64 chars)    |
| `state`       | str  | Yes           | Desired state: 'present' or 'absent'                        |

*Exactly one container parameter must be provided.

### URL List Type Configuration

For URL List type categories, the list should contain specific URLs to match:

- Can include domains, subdomains, or paths
- Example: `["example.com", "malicious.example.net", "subdomain.example.org/path"]`

### Category Match Type Configuration

For Category Match type categories, the list should contain predefined URL categories:

- References Palo Alto Networks maintained categories
- Example: `["social-networking", "gambling", "adult"]`

### Provider Dictionary

| Parameter       | Type | Required | Description                            |
| --------------- | ---- | -------- | -------------------------------------- |
| `client_id`     | str  | Yes      | Client ID for SCM authentication        |
| `client_secret` | str  | Yes      | Client secret for SCM authentication    |
| `tsg_id`        | str  | Yes      | Tenant Service Group ID                 |
| `log_level`     | str  | No       | Log level for the SDK (default: "INFO") |

## Exceptions

| Exception                    | Description                      |
| ---------------------------- | -------------------------------- |
| `InvalidObjectError`         | Invalid category data or format  |
| `NameNotUniqueError`         | Category name already exists     |
| `ObjectNotPresentError`      | Category not found               |
| `MissingQueryParameterError` | Missing required parameters      |
| `AuthenticationError`        | Authentication failed            |
| `ServerError`                | Internal server error            |

## Basic Configuration

The URL Categories module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic URL Category Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Ensure a basic URL category exists
      cdot65.scm.url_categories:
        provider: "{{ provider }}"
        name: "Malicious_URLs"
        description: "List of known malicious URLs"
        type: "URL List"
        list: ["malware.example.com", "phishing.example.net"]
        folder: "Security"
        state: "present"
```

## Usage Examples

### Creating URL Categories

URL categories can be created to manage access to different types of websites, whether by specifying individual URLs or leveraging predefined categories.

### URL List Category

This example creates a URL category with specific URLs to block or allow.

```yaml
- name: Create a URL category with URL List type
  cdot65.scm.url_categories:
    provider: "{{ provider }}"
    name: "Malicious_URLs"
    description: "List of known malicious URLs"
    type: "URL List"
    list: ["malware.example.com", "phishing.example.net"]
    folder: "Security"
    state: "present"
```

### Category Match Type

This example creates a URL category that matches against predefined categories maintained by Palo Alto Networks.

```yaml
- name: Create a URL category with Category Match type
  cdot65.scm.url_categories:
    provider: "{{ provider }}"
    name: "Social_Media"
    description: "Category for social media sites"
    type: "Category Match"
    list: ["social-networking"]
    folder: "Security"
    state: "present"
```

### Updating URL Categories

This example updates an existing URL category with additional URLs.

```yaml
- name: Update a URL category with new URLs
  cdot65.scm.url_categories:
    provider: "{{ provider }}"
    name: "Malicious_URLs"
    description: "Updated list of known malicious URLs"
    type: "URL List"
    list: ["malware.example.com", "phishing.example.net", "ransomware.example.org"]
    folder: "Security"
    state: "present"
```

### Deleting URL Categories

This example removes a URL category that is no longer needed.

```yaml
- name: Delete URL category
  cdot65.scm.url_categories:
    provider: "{{ provider }}"
    name: "Social_Media"
    folder: "Security"
    state: "absent"
```

## Managing Configuration Changes

After creating, updating, or deleting URL categories, you need to commit your changes to apply them.

```yaml
- name: Commit changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    folders: ["Security"]
    description: "Updated URL categories"
```

### Return Values

| Name         | Description                             | Type | Returned              | Sample                                                                                                                                                  |
| ------------ | --------------------------------------- | ---- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| changed      | Whether any changes were made           | bool | always                | true                                                                                                                                                    |
| url_category | Details about the URL category object   | dict | when state is present | {"id": "123e4567-e89b-12d3-a456-426655440000", "name": "Malicious_URLs", "description": "List of known malicious URLs", "type": "URL List", "list": ["malware.example.com", "phishing.example.net"], "folder": "Security"} |

## Error Handling

It's important to handle potential errors when working with URL categories.

```yaml
- name: Create or update URL category with error handling
  block:
    - name: Ensure URL category exists
      cdot65.scm.url_categories:
        provider: "{{ provider }}"
        name: "Malicious_URLs"
        description: "List of known malicious URLs"
        type: "URL List"
        list: ["malware.example.com", "phishing.example.net"]
        folder: "Security"
        state: "present"
      register: category_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        folders: ["Security"]
        description: "Updated URL categories"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred: {{ ansible_failed_result.msg }}"
```

## Best Practices

### URL List Management

- Use specific, targeted URLs for better performance and accuracy
- Implement a consistent naming convention for URL categories
- Keep URL lists manageable and organized by function or purpose
- Regularly review and update URLs to maintain effectiveness
- Document the purpose of each URL list for easier maintenance

### Category Selection

- Understand the predefined categories available in your deployment
- Use the most specific predefined category that meets your needs
- Combine multiple predefined categories when necessary
- Create custom URL lists only when predefined categories are insufficient
- Regularly review category definitions as they may be updated by Palo Alto Networks

### Performance Considerations

- Keep URL lists concise for better performance
- Use wildcard domains sparingly as they can impact performance
- Break large lists into functional categories for easier management
- Consider the impact of URL filtering on overall firewall performance
- Test URL category configurations before deploying to production

### Policy Integration

- Plan how URL categories will be used in security policies
- Create categories that align with your organization's acceptable use policies
- Test URL filtering policies in a controlled environment
- Monitor logs to ensure URL categories are working as expected
- Develop a process for handling false positives/negatives

### Maintenance and Updates

- Establish a regular review cycle for custom URL lists
- Document the justification for each custom URL category
- Implement change control procedures for URL category modifications
- Use version control for tracking changes to URL lists
- Consider automation for updating URL lists from threat intelligence feeds

## Related Modules

- [url_categories_info](url_categories_info.md) - Retrieve information about URL categories
- [security_rule](security_rule.md) - Configure security policies that use URL categories
- [security_profiles_group](security_profiles_group.md) - Configure security profile groups
- [log_forwarding_profile](log_forwarding_profile.md) - Configure log forwarding for URL filtering events
