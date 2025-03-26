# External Dynamic Lists Configuration Object

## Overview

The External Dynamic Lists module (`cdot65.scm.external_dynamic_lists`) manages external dynamic
lists (EDLs) in Palo Alto Networks' Strata Cloud Manager. EDLs are used to dynamically fetch updated
lists of IPs, domains, URLs, IMSIs, or IMEIs from external sources to use in security policies. This
module enables you to create, update, and delete various types of external dynamic lists with
configurable update intervals.

## Module Parameters

| Parameter     | Type    | Required         | Default | Choices         | Description                                                 |
| ------------- | ------- | ---------------- | ------- | --------------- | ----------------------------------------------------------- |
| `name`        | string  | Yes              |         |                 | Name of the external dynamic list (max 63 chars)            |
| `description` | string  | No               |         |                 | Description of the external dynamic list (max 255 chars)    |
| `ip_list`     | dict    | One Required     |         |                 | Configuration for an IP-based external dynamic list         |
| `domain_list` | dict    | One Required     |         |                 | Configuration for a domain-based external dynamic list      |
| `url_list`    | dict    | One Required     |         |                 | Configuration for a URL-based external dynamic list         |
| `imsi_list`   | dict    | One Required     |         |                 | Configuration for an IMSI-based external dynamic list       |
| `imei_list`   | dict    | One Required     |         |                 | Configuration for an IMEI-based external dynamic list       |
| `five_minute` | boolean | One Required\*   |         |                 | Configure list to update every five minutes                 |
| `hourly`      | boolean | One Required\*   |         |                 | Configure list to update hourly                             |
| `daily`       | dict    | One Required\*   |         |                 | Configure list to update daily at specified hour            |
| `weekly`      | dict    | One Required\*   |         |                 | Configure list to update weekly on specified day and time   |
| `monthly`     | dict    | One Required\*   |         |                 | Configure list to update monthly on specified day and time  |
| `folder`      | string  | One Required\*\* |         |                 | The folder in which the resource is defined (max 64 chars)  |
| `snippet`     | string  | One Required\*\* |         |                 | The snippet in which the resource is defined (max 64 chars) |
| `device`      | string  | One Required\*\* |         |                 | The device in which the resource is defined (max 64 chars)  |
| `provider`    | dict    | Yes              |         |                 | Authentication credentials                                  |
| `state`       | string  | Yes              |         | present, absent | Desired state of the external dynamic list                  |

\*Note: Exactly one update interval (five_minute, hourly, daily, weekly, or monthly) must be
specified.\
\*\*Note: Exactly one container parameter (folder, snippet, or device) must be specified.

### List Type Details

Each list type (`ip_list`, `domain_list`, `url_list`, `imsi_list`, `imei_list`) supports the
following parameters:

| Parameter             | Type    | Required | Description                                               |
| --------------------- | ------- | -------- | --------------------------------------------------------- |
| `url`                 | string  | Yes      | URL to fetch the list content                             |
| `exception_list`      | list    | No       | List of entries to exclude from the external dynamic list |
| `certificate_profile` | string  | No       | Client certificate profile for secure connections         |
| `auth`                | dict    | No       | Authentication credentials for the list URL               |
| `expand_domain`       | boolean | No       | Domain expansion (domain_list only)                       |

### Update Interval Details

| Parameter     | Sub-parameters                           | Description                                   |
| ------------- | ---------------------------------------- | --------------------------------------------- |
| `five_minute` | None (boolean flag)                      | Update every 5 minutes                        |
| `hourly`      | None (boolean flag)                      | Update every hour                             |
| `daily`       | `at`: Hour of day (00-23)                | Update once a day at the specified hour       |
| `weekly`      | `day_of_week`: Day of week<br>`at`: Hour | Update once a week on specified day and time  |
| `monthly`     | `day_of_month`: Day (1-31)<br>`at`: Hour | Update once a month on specified day and time |

### Provider Dictionary

| Parameter       | Type   | Required | Default | Choices                               | Description                      |
| --------------- | ------ | -------- | ------- | ------------------------------------- | -------------------------------- |
| `client_id`     | string | Yes      |         |                                       | Client ID for authentication     |
| `client_secret` | string | Yes      |         |                                       | Client secret for authentication |
| `tsg_id`        | string | Yes      |         |                                       | Tenant Service Group ID          |
| `log_level`     | string | No       | "INFO"  | DEBUG, INFO, WARNING, ERROR, CRITICAL | Log level for the SDK            |

## Examples



```yaml
- name: Create IP-based external dynamic list with hourly updates
  cdot65.scm.external_dynamic_lists:
    provider: "{{ provider }}"
    name: "malicious-ips"
    description: "Known malicious IPs"
    folder: "Texas"
    ip_list:
      url: "https://threatfeeds.example.com/ips.txt"
      auth:
        username: "user123"
        password: "pass123"
    hourly: true
    state: "present"

- name: Create domain-based external dynamic list with daily updates at 3 AM
  cdot65.scm.external_dynamic_lists:
    provider: "{{ provider }}"
    name: "blocked-domains"
    description: "Blocked domains list"
    folder: "Texas"
    domain_list:
      url: "https://threatfeeds.example.com/domains.txt"
      expand_domain: true
    daily:
      at: "03"
    state: "present"

- name: Create URL-based external dynamic list with weekly updates
  cdot65.scm.external_dynamic_lists:
    provider: "{{ provider }}"
    name: "malicious-urls"
    description: "Malicious URLs list"
    folder: "Texas"
    url_list:
      url: "https://threatfeeds.example.com/urls.txt"
      exception_list:
        - "example.com/allowed"
        - "example.org/allowed"
    weekly:
      day_of_week: "monday"
      at: "12"
    state: "present"

- name: Update external dynamic list with new description and auth
  cdot65.scm.external_dynamic_lists:
    provider: "{{ provider }}"
    name: "malicious-ips"
    description: "Updated malicious IPs list"
    folder: "Texas"
    ip_list:
      url: "https://threatfeeds.example.com/ips.txt"
      auth:
        username: "newuser"
        password: "newpass"
    five_minute: true
    state: "present"

- name: Delete external dynamic list
  cdot65.scm.external_dynamic_lists:
    provider: "{{ provider }}"
    name: "blocked-domains"
    folder: "Texas"
    state: "absent"
```


## Return Values



```yaml
changed:
    description: Whether any changes were made.
    returned: always
    type: bool
    sample: true
external_dynamic_list:
    description: Details about the external dynamic list.
    returned: when state is present
    type: dict
    sample:
        id: "123e4567-e89b-12d3-a456-426655440000"
        name: "malicious-ips"
        description: "Known malicious IPs"
        type:
          ip:
            url: "https://threatfeeds.example.com/ips.txt"
            description: "Known malicious IPs"
            recurring:
              hourly: {}
        folder: "Texas"
```


## Complete Playbook Example

This example demonstrates a complete workflow for managing external dynamic lists, including
creation, retrieval, updating, and deletion.



```yaml
---
# Playbook for managing External Dynamic Lists in Strata Cloud Manager
- name: Manage External Dynamic Lists in SCM
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
    test_timestamp: "{{ lookup('pipe', 'date +%Y%m%d%H%M%S') }}"
    test_folder: "Texas"
  tasks:
    # First clean up any existing test objects if they exist
    - name: Remove test external dynamic lists if they exist
      cdot65.scm.external_dynamic_lists:
        provider: "{{ provider }}"
        name: "{{ item }}"
        folder: "{{ test_folder }}"
        state: "absent"
      ignore_errors: true
      loop:
        - "Test_EDL_URL_{{ test_timestamp }}"
        - "Test_EDL_Domain_{{ test_timestamp }}"

    # Create a URL-based external dynamic list
    - name: Create a URL-based external dynamic list
      cdot65.scm.external_dynamic_lists:
        provider: "{{ provider }}"
        name: "Test_EDL_URL_{{ test_timestamp }}"
        description: "Test URL list for Ansible module"
        folder: "{{ test_folder }}"
        url_list:
          url: "https://example.com/urls.txt"
          certificate_profile: "default-certificate-profile"
          exception_list: 
            - "example.com/exception"
          auth:
            username: "testuser"
            password: "testpass"
        five_minute: true
        state: "present"
      register: create_url_result

    # Display the created EDL for verification
    - name: Debug URL EDL creation result
      debug:
        var: create_url_result
        verbosity: 0

    # Create a domain-based external dynamic list
    - name: Create a domain-based external dynamic list
      cdot65.scm.external_dynamic_lists:
        provider: "{{ provider }}"
        name: "Test_EDL_Domain_{{ test_timestamp }}"
        description: "Test domain list for Ansible module"
        folder: "{{ test_folder }}"
        domain_list:
          url: "https://threatfeeds.example.com/domains.txt"
          certificate_profile: "default-certificate-profile"
          exception_list: 
            - "example.com"
          auth:
            username: "testuser"
            password: "testpass"
          expand_domain: true
        daily:
          at: "03"
        state: "present"
      register: create_domain_result

    # Get information about the created URL-based EDL using info module
    - name: Get information about the URL-based external dynamic list
      cdot65.scm.external_dynamic_lists_info:
        provider: "{{ provider }}"
        name: "{{ create_url_result.external_dynamic_list.name }}"
        folder: "{{ test_folder }}"
      register: url_info_result

    # Update the URL-based external dynamic list
    - name: Update the URL-based external dynamic list
      cdot65.scm.external_dynamic_lists:
        provider: "{{ provider }}"
        name: "{{ create_url_result.external_dynamic_list.name }}"
        description: "Updated URL list for Ansible module"
        folder: "{{ test_folder }}"
        url_list:
          url: "https://threatfeeds.example.com/urls.txt"
          certificate_profile: "default-certificate-profile"
          exception_list: 
            - "example.com/exception"
          auth:
            username: "testuser"
            password: "testpass"
        daily:
          at: "03"
        state: "present"
      register: update_result

    # Clean up by deleting the test EDLs
    - name: Delete the external dynamic lists
      cdot65.scm.external_dynamic_lists:
        provider: "{{ provider }}"
        name: "{{ item }}"
        folder: "{{ test_folder }}"
        state: "absent"
      loop:
        - "{{ create_url_result.external_dynamic_list.name }}"
        - "{{ create_domain_result.external_dynamic_list.name }}"
```


## Notes and Limitations

### Certificate Profile Handling

When working with certificate profiles in any EDL type, be aware of the following:

- If `certificate_profile` is provided as an empty string or `null`, the module will remove it from
  the request to avoid API validation issues
- To specify a certificate profile, provide a valid profile name such as
  "default-certificate-profile"
- Certificate profiles must already exist in SCM before they can be referenced

### Exception List Handling

Exception lists have these behaviors:

- If the exception list is empty, it will be removed from the request
- Exception list entries must be formatted according to the EDL type (IP addresses for IP lists,
  domain names for domain lists, etc.)

### Update Interval Requirements

- Exactly one update interval must be specified (`five_minute`, `hourly`, `daily`, `weekly`, or
  `monthly`)
- For `daily`, `weekly`, and `monthly` intervals, additional parameters are required:
  - `daily` requires `at` parameter specifying the hour (00-23)
  - `weekly` requires `day_of_week` parameter and optionally `at`
  - `monthly` requires `day_of_month` parameter and optionally `at`

### Container Requirements

- Exactly one container parameter must be specified: `folder`, `snippet`, or `device`

## Idempotency

The module attempts to handle idempotency, but there are known issues:

- An EDL is considered unchanged if all parameters match exactly
- Any difference in parameters will trigger an update
- There are some known limitations with idempotency that may cause unnecessary updates in some cases

## Related Information

- [External Dynamic Lists Info module](external_dynamic_lists_info.md) - Module for retrieving
  information about external dynamic lists
- [Security Rule module](security_rule.md) - For configuring security rules that utilize external
  dynamic lists
