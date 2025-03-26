# URL Categories Info Module

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Examples](#examples)
4. [Return Values](#return-values)
5. [Usage Notes](#usage-notes)

## Overview

The `url_categories_info` module retrieves information about URL categories in Palo Alto Networks' Strata Cloud Manager (SCM). It allows you to fetch details about specific URL categories or list multiple URL categories with various filtering options.

## Module Parameters

| Parameter       | Type    | Required | Choices       | Default | Description                                    |
|-----------------|---------|----------|---------------|---------|------------------------------------------------|
| name            | str     | no       |               |         | Name of a specific URL category to retrieve    |
| gather_subset   | list    | no       | all, config   | config  | Information to gather about URL categories     |
| folder          | str     | yes*     |               |         | Filter URL categories by folder container      |
| snippet         | str     | yes*     |               |         | Filter URL categories by snippet container     |
| device          | str     | yes*     |               |         | Filter URL categories by device container      |
| exact_match     | bool    | no       |               | false   | Only return objects in the specified container |
| exclude_folders | list    | no       |               |         | List of folder names to exclude from results   |
| exclude_snippets| list    | no       |               |         | List of snippet values to exclude              |
| exclude_devices | list    | no       |               |         | List of device values to exclude               |
| members         | list    | no       |               |         | Filter by URLs or categories in the list       |
| provider        | dict    | yes      |               |         | SCM authentication credentials                 |

*One of these parameters is required if `name` is not specified

### Provider Dictionary

| Parameter     | Type | Required | Default | Description                           |
|---------------|------|----------|---------|---------------------------------------|
| client_id     | str  | yes      |         | OAuth2 client ID                      |
| client_secret | str  | yes      |         | OAuth2 client secret                  |
| tsg_id        | str  | yes      |         | Tenant Service Group ID               |
| log_level     | str  | no       | INFO    | Log level for the SDK                 |

## Examples

### Retrieve a Specific URL Category

<div class="termy">

<!-- termynal -->

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
```

</div>

### List All URL Categories in a Folder

<div class="termy">

<!-- termynal -->

```yaml
- name: List all URL categories in a folder
  cdot65.scm.url_categories_info:
    provider: "{{ provider }}"
    folder: "Security"
  register: all_url_categories

- name: Display all URL categories
  debug:
    var: all_url_categories.url_categories
```

</div>

### Filter URL Categories by List Members

<div class="termy">

<!-- termynal -->

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
```

</div>

### Advanced Filtering

<div class="termy">

<!-- termynal -->

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

</div>

## Return Values

### When Retrieving a Specific URL Category

<div class="termy">

<!-- termynal -->

```yaml
url_category:
    description: Information about the requested URL category
    returned: success, when name is specified
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Malicious_URLs"
        description: "List of known malicious URLs"
        type: "URL List"
        list: ["malware.example.com", "phishing.example.net"]
        folder: "Security"
```

</div>

### When Listing URL Categories

<div class="termy">

<!-- termynal -->

```yaml
url_categories:
    description: List of URL category objects matching the filter criteria
    returned: success, when name is not specified
    type: list
    elements: dict
    sample:
      - id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Malicious_URLs"
        description: "List of known malicious URLs"
        type: "URL List"
        list: ["malware.example.com", "phishing.example.net"]
        folder: "Security"
      - id: "234e5678-e89b-12d3-a456-426655440001"
        name: "Social_Media"
        description: "Category for social media sites"
        type: "Category Match"
        list: ["social-networking"]
        folder: "Security"
```

</div>

## Usage Notes

### Filtering Options

The `url_categories_info` module supports these filtering mechanisms:

1. **Container Filtering**:
   - `folder`, `snippet`, or `device` - Only one can be specified
   - This is the primary filter that determines the scope of your query

2. **Member Filtering**:
   - `members` - Filter by specific URLs or categories in the list
   - Useful for finding URL categories containing specific entries

3. **Exact Match**:
   - `exact_match` - When set to `true`, only returns objects defined exactly in the specified container
   - Excludes inherited or shared objects

4. **Exclusion Filters**:
   - `exclude_folders` - Exclude URL categories from specific folders
   - `exclude_snippets` - Exclude URL categories from specific snippets
   - `exclude_devices` - Exclude URL categories from specific devices

### Container Selection

- When retrieving a specific URL category by name, you must specify which container to search in
- For listing operations, one container parameter is required

### Performance Considerations

- List operations might return a large number of objects
- Use appropriate filters to narrow down results
- Combining filters (e.g., using both `exact_match` and `members`) can significantly reduce result size