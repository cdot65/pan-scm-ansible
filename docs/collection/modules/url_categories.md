# Url Categories Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Module Parameters](#module-parameters)
3. [Examples](#examples)
4. [Return Values](#return-values)
5. [Usage Notes](#usage-notes)

## Overview

The `url_categories` module manages URL categories within Palo Alto Networks' Strata Cloud Manager
(SCM). It provides functionality to create, update, and delete URL category objects used for URL
filtering and security policies.

URL categories can be of two types:

- URL List: Contains a list of specific URLs to match
- Category Match: Matches predefined URL categories

## Module Parameters

| Parameter   | Type | Required | Choices                  | Default  | Description                            |
| ----------- | ---- | -------- | ------------------------ | -------- | -------------------------------------- |
| name        | str  | yes      |                          |          | Name of the URL category object        |
| description | str  | no       |                          |          | Description of the URL category object |
| list        | list | yes†     |                          |          | List of URLs or categories             |
| type        | str  | no       | URL List, Category Match | URL List | Type of URL category                   |
| folder      | str  | yes‡     |                          |          | Folder where this resource is stored   |
| snippet     | str  | yes‡     |                          |          | Snippet where this resource is defined |
| device      | str  | yes‡     |                          |          | Device where this resource is defined  |
| provider    | dict | yes      |                          |          | SCM authentication credentials         |
| state       | str  | yes      | present, absent          |          | Whether the resource should exist      |

† Required when `state=present`\
‡ One of these parameters is required

### Provider Dictionary

| Parameter     | Type | Required | Default | Description             |
| ------------- | ---- | -------- | ------- | ----------------------- |
| client_id     | str  | yes      |         | OAuth2 client ID        |
| client_secret | str  | yes      |         | OAuth2 client secret    |
| tsg_id        | str  | yes      |         | Tenant Service Group ID |
| log_level     | str  | no       | INFO    | Log level for the SDK   |

## Examples



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




```yaml
- name: Delete URL category
  cdot65.scm.url_categories:
    provider: "{{ provider }}"
    name: "Social_Media"
    folder: "Security"
    state: "absent"
```


## Return Values



```yaml
changed:
    description: Whether any changes were made
    returned: always
    type: bool
    sample: true

url_category:
    description: Details about the URL category object
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "Malicious_URLs"
        description: "List of known malicious URLs"
        type: "URL List"
        list: ["malware.example.com", "phishing.example.net"]
        folder: "Security"
```


## Usage Notes

### URL List Type

- Use the `URL List` type to specify a list of specific URLs to match
- URLs can include domains, subdomains, or paths
- Example: `["example.com", "malicious.example.net", "subdomain.example.org/path"]`

### Category Match Type

- Use the `Category Match` type to match against predefined URL categories
- Example: `["social-networking", "gambling", "adult"]`

### Name Restrictions

- URL category names are limited to 31 characters
- Use short, descriptive names to avoid this limitation

### Location Parameters

- Exactly one of `folder`, `snippet`, or `device` must be provided
- Most commonly, URL categories are defined within a folder
