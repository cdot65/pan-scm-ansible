# External Dynamic Lists Configuration Object

## Table of Contents

1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [EDL Model Attributes](#edl-model-attributes)
4. [Exceptions](#exceptions)
5. [Basic Configuration](#basic-configuration)
6. [Usage Examples](#usage-examples)
    - [Creating EDL Objects](#creating-edl-objects)
    - [Retrieving EDLs](#retrieving-edls)
    - [Updating EDLs](#updating-edls)
    - [Listing EDLs](#listing-edls)
    - [Deleting EDLs](#deleting-edls)
7. [Managing Configuration Changes](#managing-configuration-changes)
    - [Performing Commits](#performing-commits)
    - [Monitoring Jobs](#monitoring-jobs)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Full Script Examples](#full-script-examples)
11. [Related Models](#related-models)

## Overview

The External Dynamic Lists (EDL) module provides functionality to manage external dynamic lists in Palo Alto Networks' Strata Cloud Manager. EDLs are used to dynamically fetch updated lists of IPs, domains, URLs, IMSIs, or IMEIs from external sources to use in security policies. The module offers comprehensive support for creating, updating, retrieving, and deleting various types of external dynamic lists with configurable update intervals.

## Core Methods

| Method     | Description                   | Parameters                         | Return Type               |
|------------|-------------------------------|------------------------------------|--------------------|
| `create()` | Creates a new EDL object      | `data: Dict[str, Any]`             | `ExternalDynamicListResponseModel` |
| `get()`    | Retrieves an EDL by ID        | `object_id: str`                   | `ExternalDynamicListResponseModel` |
| `update()` | Updates an existing EDL       | `edl: ExternalDynamicListUpdateModel` | `ExternalDynamicListResponseModel` |
| `delete()` | Deletes an EDL                | `object_id: str`                   | `None`                    |
| `list()`   | Lists EDLs with filtering     | `folder: str`, `**filters`         | `List[ExternalDynamicListResponseModel]` |
| `fetch()`  | Gets EDL by name and container| `name: str`, `folder: str`         | `ExternalDynamicListResponseModel` |

## EDL Model Attributes

| Attribute        | Type      | Required     | Description                                 |
|------------------|-----------|--------------|---------------------------------------------|
| `name`           | str       | Yes          | Name of EDL object (max 63 chars)           |
| `id`             | UUID      | Yes*         | Unique identifier (*response only)          |
| `description`    | str       | No           | Object description (max 255 chars)          |
| `ip_list`        | dict      | One Required | Configuration for IP-based EDL              |
| `domain_list`    | dict      | One Required | Configuration for domain-based EDL          |
| `url_list`       | dict      | One Required | Configuration for URL-based EDL             |
| `imsi_list`      | dict      | One Required | Configuration for IMSI-based EDL            |
| `imei_list`      | dict      | One Required | Configuration for IMEI-based EDL            |
| `five_minute`    | bool      | One Required | Update every 5 minutes                      |
| `hourly`         | bool      | One Required | Update hourly                               |
| `daily`          | dict      | One Required | Update daily at specified hour              |
| `weekly`         | dict      | One Required | Update weekly on specified day and time     |
| `monthly`        | dict      | One Required | Update monthly on specified day and time    |
| `folder`         | str       | Yes**        | Folder location (**one container required)  |
| `snippet`        | str       | Yes**        | Snippet location (**one container required) |
| `device`         | str       | Yes**        | Device location (**one container required)  |

### List Type Details

Each list type (`ip_list`, `domain_list`, `url_list`, `imsi_list`, `imei_list`) supports the following parameters:

| Attribute            | Type      | Required | Description                                    |
|----------------------|-----------|----------|------------------------------------------------|
| `url`                | str       | Yes      | URL to fetch the list content                  |
| `exception_list`     | List[str] | No       | List of entries to exclude                     |
| `certificate_profile`| str       | No       | Certificate profile for HTTPS connections      |
| `auth`               | dict      | No       | Authentication for the URL                     |
| `expand_domain`      | bool      | No       | Domain expansion (domain_list only)            |

## Exceptions

| Exception                    | HTTP Code | Description                    |
|------------------------------|-----------|--------------------------------|
| `InvalidObjectError`         | 400       | Invalid EDL data or format     |
| `MissingQueryParameterError` | 400       | Missing required parameters    |
| `NameNotUniqueError`         | 409       | EDL name already exists        |
| `ObjectNotPresentError`      | 404       | EDL not found                  |
| `ReferenceNotZeroError`      | 409       | EDL still referenced           |
| `AuthenticationError`        | 401       | Authentication failed          |
| `ServerError`                | 500       | Internal server error          |

## Basic Configuration

The External Dynamic Lists service can be accessed using either the unified client interface (recommended) or the traditional service instantiation.

### Unified Client Interface (Recommended)

<div class="termy">

<!-- termynal -->

```python
from scm.client import ScmClient

# Initialize client
client = ScmClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    tsg_id="your_tsg_id"
)

# Access the EDL service directly through the client
# No need to create a separate ExternalDynamicList instance
edls = client.external_dynamic_list
```

</div>

### Traditional Service Instantiation (Legacy)

<div class="termy">

<!-- termynal -->

```python
from scm.client import Scm
from scm.config.objects import ExternalDynamicList

# Initialize client
client = Scm(
    client_id="your_client_id",
    client_secret="your_client_secret",
    tsg_id="your_tsg_id"
)

# Initialize EDL object explicitly
edls = ExternalDynamicList(client)
```

</div>

!!! note
While both approaches work, the unified client interface is recommended for new development as it provides a more
streamlined developer experience and ensures proper token refresh handling across all services.

## Usage Examples

### Creating EDL Objects

<div class="termy">

<!-- termynal -->

```python
from scm.client import ScmClient

# Initialize client
client = ScmClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    tsg_id="your_tsg_id"
)

# Prepare IP-based EDL configuration with hourly updates
ip_edl_config = {
    "name": "malicious-ips",
    "ip_list": {
        "url": "https://threatfeeds.example.com/ips.txt",
        "exception_list": ["192.168.1.100", "10.0.0.1"],
        "auth": {
            "username": "testuser",
            "password": "testpass"
        },
        "recurring": {
            "hourly": {}
        },
        "description": "Known malicious IPs"
    },
    "folder": "Texas"
}

# Create the IP-based EDL object
ip_edl = client.external_dynamic_list.create(ip_edl_config)

# Prepare domain-based EDL configuration with daily updates
domain_edl_config = {
    "name": "blocked-domains",
    "domain_list": {
        "url": "https://threatfeeds.example.com/domains.txt",
        "expand_domain": True,
        "recurring": {
            "daily": {
                "at": "03"
            }
        },
        "description": "Blocked domains list"
    },
    "folder": "Texas"
}

# Create the domain-based EDL object
domain_edl = client.external_dynamic_list.create(domain_edl_config)

# Prepare URL-based EDL configuration with weekly updates
url_edl_config = {
    "name": "malicious-urls",
    "url_list": {
        "url": "https://threatfeeds.example.com/urls.txt",
        "exception_list": ["example.com/allowed", "example.org/allowed"],
        "certificate_profile": "default-certificate-profile",
        "recurring": {
            "weekly": {
                "day_of_week": "monday",
                "at": "12"
            }
        },
        "description": "Malicious URLs list"
    },
    "folder": "Texas"
}

# Create the URL-based EDL object
url_edl = client.external_dynamic_list.create(url_edl_config)
```

</div>

### Retrieving EDLs

<div class="termy">

<!-- termynal -->

```python
# Fetch by name and folder
edl = client.external_dynamic_list.fetch(name="malicious-ips", folder="Texas")
print(f"Found EDL: {edl.name}")

# Get by ID
edl_by_id = client.external_dynamic_list.get(edl.id)
print(f"Retrieved EDL: {edl_by_id.name}")
```

</div>

### Updating EDLs

<div class="termy">

<!-- termynal -->

```python
# Fetch existing EDL
existing_edl = client.external_dynamic_list.fetch(name="malicious-ips", folder="Texas")

# Update EDL configuration (convert from hourly to 5-minute updates)
update_data = {
    "id": str(existing_edl.id),
    "name": existing_edl.name,
    "folder": existing_edl.folder,
    "type": {
        "ip": {
            "url": "https://threatfeeds.example.com/new-ips.txt",
            "description": "Updated malicious IPs list",
            "recurring": {
                "five_minute": {}
            }
        }
    }
}

# Convert to update model
from scm.models.objects import ExternalDynamicListsUpdateModel
update_model = ExternalDynamicListsUpdateModel(**update_data)

# Perform update
updated_edl = client.external_dynamic_list.update(update_model)
```

</div>

### Listing EDLs

<div class="termy">

<!-- termynal -->

```python
# List all EDLs in a folder
edl_list = client.external_dynamic_list.list(folder="Texas")

# Process results
for edl in edl_list:
    edl_type = next(iter(edl.type.__dict__.keys()))
    print(f"Name: {edl.name}, Type: {edl_type}")
    
    # Access properties of specific EDL types
    if edl_type == "ip":
        print(f"URL: {edl.type.ip.url}")
    elif edl_type == "domain":
        print(f"URL: {edl.type.domain.url}")
    elif edl_type == "url":
        print(f"URL: {edl.type.url.url}")
```

</div>

### Deleting EDLs

<div class="termy">

<!-- termynal -->

```python
# Delete by ID
edl_id = "123e4567-e89b-12d3-a456-426655440000"
client.external_dynamic_list.delete(edl_id)

# Or delete by fetching first
edl = client.external_dynamic_list.fetch(name="malicious-ips", folder="Texas")
client.external_dynamic_list.delete(str(edl.id))
```

</div>

## Managing Configuration Changes

### Performing Commits

<div class="termy">

<!-- termynal -->

```python
# Prepare commit parameters
commit_params = {
    "folders": ["Texas"],
    "description": "Added new external dynamic lists",
    "sync": True,
    "timeout": 300  # 5 minute timeout
}

# Commit the changes
result = client.commit(**commit_params)

print(f"Commit job ID: {result.job_id}")
```

</div>

### Monitoring Jobs

<div class="termy">

<!-- termynal -->

```python
# Get status of specific job directly from the client
job_status = client.get_job_status(result.job_id)
print(f"Job status: {job_status.data[0].status_str}")

# List recent jobs directly from the client
recent_jobs = client.list_jobs(limit=10)
for job in recent_jobs.data:
    print(f"Job {job.id}: {job.type_str} - {job.status_str}")
```

</div>

## Error Handling

<div class="termy">

<!-- termynal -->

```python
from scm.client import ScmClient
from scm.exceptions import (
    InvalidObjectError,
    MissingQueryParameterError,
    NameNotUniqueError,
    ObjectNotPresentError
)

# Initialize client
client = ScmClient(
    client_id="your_client_id",
    client_secret="your_client_secret",
    tsg_id="your_tsg_id"
)

try:
    # Create EDL configuration
    edl_config = {
        "name": "test-edl",
        "url_list": {
            "url": "https://threatfeeds.example.com/urls.txt",
            "exception_list": ["example.com/exception"],
            "certificate_profile": "default-certificate-profile",
            "auth": {
                "username": "testuser",
                "password": "testpass"
            },
            "recurring": {
                "five_minute": {}
            },
            "description": "Test URL list"
        },
        "folder": "Texas"
    }

    # Create the EDL using the unified client interface
    new_edl = client.external_dynamic_list.create(edl_config)

    # Commit changes directly from the client
    result = client.commit(
        folders=["Texas"],
        description="Added test EDL",
        sync=True
    )

    # Check job status directly from the client
    status = client.get_job_status(result.job_id)

except InvalidObjectError as e:
    print(f"Invalid EDL data: {e.message}")
except NameNotUniqueError as e:
    print(f"EDL name already exists: {e.message}")
except ObjectNotPresentError as e:
    print(f"EDL not found: {e.message}")
except MissingQueryParameterError as e:
    print(f"Missing parameter: {e.message}")
```

</div>

## Best Practices

1. **Client Usage**
    - Use the unified client interface (`client.external_dynamic_list`) for streamlined code
    - Create a single client instance and reuse it across your application
    - Perform commit operations directly on the client object (`client.commit()`)

2. **Container Management**
    - Always specify exactly one container (folder, snippet, or device)
    - Use consistent container names across operations
    - Validate container existence before operations

3. **EDL Types and Update Schedules**
    - Specify exactly one EDL type per object (IP, Domain, URL, IMSI, or IMEI)
    - Choose the appropriate update schedule based on the criticality of the list
    - Consider system load when using frequent update intervals (five_minute)
    - For less critical lists, use daily or weekly updates to reduce system load

4. **Error Handling**
    - Implement comprehensive error handling for all operations
    - Check for empty or null certificate_profile values
    - Format exception_list properly (must be a list of strings)
    - Handle specific exceptions before generic ones
    - Log error details for troubleshooting

5. **Performance**
    - Consider list size and update frequency impact on firewall performance
    - For large lists, prefer less frequent updates
    - Cache frequently accessed objects
    - Implement proper retry mechanisms with exponential backoff

6. **Security**
    - Use certificate profiles for HTTPS sources to validate server authenticity
    - Implement proper authentication handling for secured EDL sources
    - Validate input data for security vulnerabilities
    - Use secure connection settings

## Full Script Examples

Refer to the [external_dynamic_lists.py example](https://github.com/cdot65/pan-scm-sdk/blob/main/examples/scm/config/objects/external_dynamic_lists.py).

## Related Models

- External Dynamic Lists Info module
- Security Rule module for utilizing EDLs in security policies