# Remote Networks Information Object

## Table of Contents

- [Remote Networks Information Object](#remote-networks-information-object)
  - [Table of Contents](#table-of-contents)
  - [Synopsis](#synopsis)
  - [Parameters](#parameters)
    - [Parameter: provider](#parameter-provider)
  - [Examples](#examples)
  - [Return Values](#return-values)
    - [Return Value: remote\_networks](#return-value-remote_networks)
    - [Return Value: remote\_network](#return-value-remote_network)


Gather information about remote networks in SCM.

## Synopsis

- Gather information about remote networks within Strata Cloud Manager (SCM).
- Supports retrieving a specific remote network by name or listing networks with various filters.
- Provides additional client-side filtering capabilities by regions, license types, and subnets.
- Returns detailed information about each remote network.
- This is an info module that only retrieves information and does not modify anything.

## Parameters

| Parameter | Choices/Defaults | Comments |
| --- | --- | --- |
| name |  | The name of a specific remote network to retrieve. |
| gather_subset | <ul><li>all</li><li>config *default*</li></ul> | Determines which information to gather about remote networks.<br>C(all) gathers everything.<br>C(config) is the default which retrieves basic configuration. |
| folder |  | Filter remote networks by folder. |
| regions |  | Filter remote networks by regions. |
| license_types | <ul><li>FWAAS-AGGREGATE</li><li>FWAAS-BYOL</li><li>CN-SERIES</li><li>FWAAS-PAYG</li></ul> | Filter remote networks by license types. |
| subnets |  | Filter remote networks by subnets. |
| provider |  | Authentication credentials.<br>*Required*<br>See [sub-options](#parameter-provider). |

### Parameter: provider

| Parameter | Comments |
| --- | --- |
| client_id | Client ID for authentication.<br>*Required* |
| client_secret | Client secret for authentication.<br>*Required* |
| tsg_id | Tenant Service Group ID.<br>*Required* |
| log_level | Log level for the SDK.<br>Default: "INFO" |

## Examples



```yaml
- name: Gather Remote Network Information in Strata Cloud Manager
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
  tasks:

    - name: Get information about a specific remote network
      cdot65.scm.remote_networks_info:
        provider: "{{ provider }}"
        name: "Branch-Office-1"
        folder: "Remote Networks"
      register: network_info

    - name: List all remote networks in a folder
      cdot65.scm.remote_networks_info:
        provider: "{{ provider }}"
        folder: "Remote Networks"
      register: all_networks

    - name: List remote networks in a specific region
      cdot65.scm.remote_networks_info:
        provider: "{{ provider }}"
        folder: "Remote Networks"
        regions: ["us-east-1"]
      register: region_networks

    - name: List remote networks with specific license types
      cdot65.scm.remote_networks_info:
        provider: "{{ provider }}"
        folder: "Remote Networks"
        license_types: ["FWAAS-AGGREGATE"]
      register: license_networks

    - name: List remote networks with specific subnets
      cdot65.scm.remote_networks_info:
        provider: "{{ provider }}"
        folder: "Remote Networks"
        subnets: ["10.1.0.0/16"]
      register: subnet_networks
```



## Return Values

| Key | Returned | Description |
| --- | --- | --- |
| remote_networks | Success, when name is not specified | List of remote network objects matching the filter criteria. |
| remote_network | Success, when name is specified | Information about the requested remote network. |

### Return Value: remote_networks



```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426655440000",
    "name": "Branch-Office-1",
    "description": "Remote network for Branch Office 1",
    "region": "us-east-1",
    "license_type": "FWAAS-AGGREGATE",
    "spn_name": "main-spn",
    "folder": "Remote Networks",
    "ecmp_load_balancing": "disable",
    "ipsec_tunnel": "tunnel-to-branch1",
    "subnets": ["10.1.0.0/16", "10.2.0.0/16"]
  },
  {
    "id": "234e5678-e89b-12d3-a456-426655440001",
    "name": "Branch-Office-2",
    "description": "Remote network for Branch Office 2",
    "region": "us-west-1",
    "license_type": "FWAAS-AGGREGATE",
    "spn_name": "west-spn",
    "folder": "Remote Networks",
    "ecmp_load_balancing": "enable",
    "subnets": ["10.3.0.0/16", "10.4.0.0/16"]
  }
]
```



### Return Value: remote_network



```json
{
  "id": "123e4567-e89b-12d3-a456-426655440000",
  "name": "Branch-Office-1",
  "description": "Remote network for Branch Office 1",
  "region": "us-east-1",
  "license_type": "FWAAS-AGGREGATE",
  "spn_name": "main-spn",
  "folder": "Remote Networks",
  "ecmp_load_balancing": "disable",
  "ipsec_tunnel": "tunnel-to-branch1",
  "subnets": ["10.1.0.0/16", "10.2.0.0/16"]
}
```
