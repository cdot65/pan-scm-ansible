# Hip Object Information Object

## 01. Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [HIP Object Info Model Attributes](#hip-object-info-model-attributes)
4. [Exceptions](#exceptions)
5. [Basic Configuration](#basic-configuration)
6. [Usage Examples](#usage-examples)
   - [Getting Information about a Specific HIP Object](#getting-information-about-a-specific-hip-object)
   - [Listing All HIP Objects in a Folder](#listing-all-hip-objects-in-a-folder)
   - [Filtering HIP Objects by Criteria Type](#filtering-hip-objects-by-criteria-type)
   - [Using Advanced Filtering Options](#using-advanced-filtering-options)
7. [Processing Retrieved Information](#processing-retrieved-information)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)

## 02. Overview

The `hip_object_info` Ansible module provides functionality to gather information about Host Information Profile (HIP) objects in Palo Alto Networks' Strata Cloud Manager (SCM). This is an info module that allows fetching details about specific HIP objects or listing objects with various filtering options, including by criteria type (host_info, patch_management, etc.).

## 03. Core Methods

| Method    | Description                       | Parameters                    | Return Type                    |
| --------- | --------------------------------- | ----------------------------- | ------------------------------ |
| `fetch()` | Gets a specific HIP object by name | `name: str`, `container: str` | `HipObjectResponseModel`       |
| `list()`  | Lists HIP objects with filtering   | `folder: str`, `**filters`    | `List[HipObjectResponseModel]` |

## 04. HIP Object Info Model Attributes

| Parameter          | Type   | Required | Description                                                 |
| ------------------ | ------ | -------- | ----------------------------------------------------------- |
| `name`             | str    | No       | Name of a specific HIP object to retrieve                   |
| `gather_subset`    | list   | No       | Determines which information to gather (default: config)    |
| `folder`           | str    | No\*     | Filter HIP objects by folder container                      |
| `snippet`          | str    | No\*     | Filter HIP objects by snippet container                     |
| `device`           | str    | No\*     | Filter HIP objects by device container                      |
| `exact_match`      | bool   | No       | When True, only return objects defined exactly in container |
| `exclude_folders`  | list   | No       | List of folder names to exclude from results                |
| `exclude_snippets` | list   | No       | List of snippet values to exclude from results              |
| `exclude_devices`  | list   | No       | List of device values to exclude from results               |
| `criteria_type`    | list   | No       | Filter by criteria types in the HIP object                  |

\*One container parameter is required when `name` is not specified.

### Provider Dictionary Attributes

| Attribute       | Type | Required | Default | Description                      |
| --------------- | ---- | -------- | ------- | -------------------------------- |
| `client_id`     | str  | Yes      |         | Client ID for authentication     |
| `client_secret` | str  | Yes      |         | Client secret for authentication |
| `tsg_id`        | str  | Yes      |         | Tenant Service Group ID          |
| `log_level`     | str  | No       | "INFO"  | Log level for the SDK            |

## 05. Exceptions

| Exception                    | Description                    |
| ---------------------------- | ------------------------------ |
| `InvalidObjectError`         | Invalid request data or format |
| `MissingQueryParameterError` | Missing required parameters    |
| `ObjectNotPresentError`      | HIP object not found           |
| `AuthenticationError`        | Authentication failed          |
| `ServerError`                | Internal server error          |

## 06. Basic Configuration

The HIP Object Info module requires proper authentication credentials to access the
Strata Cloud Manager API.

```yaml
- name: Basic HIP Object Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get information about HIP objects
      cdot65.scm.hip_object_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: objects_result
      
    - name: Display retrieved HIP objects
      debug:
        var: objects_result
```

## 07. Usage Examples

### Getting Information about a Specific HIP Object

Retrieve details about a specific HIP object by name and container.

```yaml
- name: Get information about a specific HIP object
  cdot65.scm.hip_object_info:
    provider: "{{ provider }}"
    name: "Windows_Workstation"
    folder: "Texas"
  register: hip_info
  
- name: Display HIP object information
  debug:
    var: hip_info.hip_object
    
- name: Check criteria types
  debug:
    msg: "HIP object criteria types: {{ hip_info.hip_object | json_query('keys(@)') | list | reject('equalto', 'name') | reject('equalto', 'description') | reject('equalto', 'folder') | list }}"
```

### Listing All HIP Objects in a Folder

List all HIP objects in a specific folder.

```yaml
- name: List all HIP objects in a folder
  cdot65.scm.hip_object_info:
    provider: "{{ provider }}"
    folder: "Texas"
  register: all_objects
  
- name: Display all HIP objects
  debug:
    var: all_objects.hip_objects
    
- name: Display count of HIP objects
  debug:
    msg: "Found {{ all_objects.hip_objects | length }} HIP objects"
    
- name: List names of all HIP objects
  debug:
    msg: "{{ all_objects.hip_objects | map(attribute='name') | list }}"
```

### Filtering HIP Objects by Criteria Type

Filter HIP objects by their criteria types.

```yaml
- name: List HIP objects with host info criteria
  cdot65.scm.hip_object_info:
    provider: "{{ provider }}"
    folder: "Texas"
    criteria_type: ["host_info"]
  register: host_info_objects
  
- name: Process criteria-filtered HIP objects
  debug:
    msg: "Host info object: {{ item.name }}"
  loop: "{{ host_info_objects.hip_objects }}"

- name: List HIP objects with patch management or disk encryption criteria
  cdot65.scm.hip_object_info:
    provider: "{{ provider }}"
    folder: "Texas"
    criteria_type: ["patch_management", "disk_encryption"]
  register: security_objects
```

### Using Advanced Filtering Options

Use advanced filtering options to refine your query results.

```yaml
- name: List HIP objects with exact match parameter
  cdot65.scm.hip_object_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exact_match: true
  register: exact_match_objects

- name: List HIP objects with exclusions
  cdot65.scm.hip_object_info:
    provider: "{{ provider }}"
    folder: "Texas"
    exclude_folders: ["All"]
    exclude_snippets: ["default"]
  register: filtered_objects
```

## 08. Processing Retrieved Information

Example of processing and utilizing the retrieved HIP object information.

```yaml
- name: Analyze HIP object information
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
      log_level: "INFO"
  tasks:
    - name: Get all HIP objects
      cdot65.scm.hip_object_info:
        provider: "{{ provider }}"
        folder: "Texas"
      register: objects_info
      
    - name: Group objects by criteria type
      set_fact:
        criteria_summary: "{{ criteria_summary | default({}) | combine({item: criteria_objects[item] | map(attribute='name') | list}) }}"
      loop: "{{ criteria_objects.keys() | list }}"
      vars:
        all_objects: "{{ objects_info.hip_objects | default([]) }}"
        criteria_objects: >-
          {% set result = {'host_info': [], 'patch_management': [], 'disk_encryption': [], 'network_info': [], 'mobile_device': [], 'certificate': []} %}
          {% for obj in all_objects %}
            {% if obj.host_info is defined %}
              {% set _ = result['host_info'].append(obj) %}
            {% endif %}
            {% if obj.patch_management is defined %}
              {% set _ = result['patch_management'].append(obj) %}
            {% endif %}
            {% if obj.disk_encryption is defined %}
              {% set _ = result['disk_encryption'].append(obj) %}
            {% endif %}
            {% if obj.network_info is defined %}
              {% set _ = result['network_info'].append(obj) %}
            {% endif %}
            {% if obj.mobile_device is defined %}
              {% set _ = result['mobile_device'].append(obj) %}
            {% endif %}
            {% if obj.certificate is defined %}
              {% set _ = result['certificate'].append(obj) %}
            {% endif %}
          {% endfor %}
          {{ result }}
      
    - name: Display criteria type summary
      debug:
        var: criteria_summary
        
    - name: Find objects with multiple criteria types
      set_fact:
        multi_criteria_objects: >-
          {% set result = [] %}
          {% for obj in objects_info.hip_objects | default([]) %}
            {% set criteria_count = 0 %}
            {% if obj.host_info is defined %}{% set criteria_count = criteria_count + 1 %}{% endif %}
            {% if obj.patch_management is defined %}{% set criteria_count = criteria_count + 1 %}{% endif %}
            {% if obj.disk_encryption is defined %}{% set criteria_count = criteria_count + 1 %}{% endif %}
            {% if obj.network_info is defined %}{% set criteria_count = criteria_count + 1 %}{% endif %}
            {% if obj.mobile_device is defined %}{% set criteria_count = criteria_count + 1 %}{% endif %}
            {% if obj.certificate is defined %}{% set criteria_count = criteria_count + 1 %}{% endif %}
            {% if criteria_count > 1 %}
              {% set _ = result.append(obj) %}
            {% endif %}
          {% endfor %}
          {{ result }}
        
    - name: Display objects with multiple criteria types
      debug:
        msg: "Objects with multiple criteria types: {{ multi_criteria_objects | map(attribute='name') | list }}"
```

## 09. Error Handling

It's important to handle potential errors when retrieving information about HIP objects.

```yaml
- name: Get information about HIP objects with error handling
  block:
    - name: Try to retrieve information about a HIP object
      cdot65.scm.hip_object_info:
        provider: "{{ provider }}"
        name: "Windows_Workstation"
        folder: "Texas"
      register: info_result
      
    - name: Display HIP object information
      debug:
        var: info_result.hip_object
        
  rescue:
    - name: Handle errors
      debug:
        msg: "Failed to retrieve HIP object information: {{ ansible_failed_result.msg }}"
        
    - name: Check if it's a 'not found' error
      debug:
        msg: "The specified HIP object does not exist, creating it..."
      when: "'not found' in ansible_failed_result.msg"
```

## 10. Best Practices

### Efficient Querying

- Use specific filters to reduce API load and improve performance
- When looking for a specific HIP object, use the `name` parameter instead of filtering results
- Use container parameters consistently across queries
- Filter by criteria type when you need to find objects with specific characteristics

### Result Processing

- Always register the module output to a variable for later use
- Check if the expected data is present before processing it
- Use appropriate Ansible filters and tests when processing complex nested structures
- Create structured summaries when analyzing multiple objects

### Filter Usage

- Use `exact_match` when you only want objects defined directly in the specified container
- Use exclusion filters to refine results without overcomplicating queries
- Filter by criteria types to find specific types of HIP objects
- Combine multiple filters for precise results

### Endpoint Security Analysis

- Group HIP objects by criteria types for better organization
- Analyze criteria configurations to understand security posture
- Identify coverage gaps in your HIP object collection
- Review criteria settings for current security best practices

### Integration with Other Modules

- Use the info module to check for existing HIP objects before creating new ones
- Combine with the hip_object module for complete object management
- Use the retrieved information to make decisions in your playbooks
- Integrate with hip_profile modules to understand how objects are used in profiles

## 11. Related Modules

- [hip_object](hip_object.md) - Create, update, and delete HIP objects
- [hip_profile_info](hip_profile_info.md) - Retrieve information about HIP profiles that use HIP objects
- [hip_profile](hip_profile.md) - Create, update, and delete HIP profiles
- [security_rule_info](security_rule_info.md) - Retrieve information about security rules that may use HIP profiles