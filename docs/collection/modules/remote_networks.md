# Remote Networks Configuration Object

## Table of Contents

- [Remote Networks Configuration Object](#remote-networks-configuration-object)
  - [Table of Contents](#table-of-contents)
  - [Synopsis](#synopsis)
  - [Parameters](#parameters)
    - [Parameter: ecmp\_tunnels](#parameter-ecmp_tunnels)
    - [Parameter: protocol](#parameter-protocol)
      - [Parameter: protocol bgp](#parameter-protocol-bgp)
    - [Parameter: provider](#parameter-provider)
  - [Examples](#examples)
  - [Return Values](#return-values)


Manage remote networks in SCM.

## Synopsis

- Manage remote networks within Strata Cloud Manager (SCM).
- Create, update, and delete remote networks that establish site-to-site VPN connections.
- Configure remote networks with various settings including ECMP load balancing and BGP.
- Support for different license types (FWAAS-AGGREGATE, FWAAS-BYOL, CN-SERIES, FWAAS-PAYG).

## Parameters

| Parameter | Choices/Defaults | Comments |
| --- | --- | --- |
| name |  | The name of the remote network.<br>*Required* |
| description |  | Description of the remote network. |
| region |  | The AWS region where the remote network is located.<br>*Required* |
| license_type | <ul><li>FWAAS-AGGREGATE *default*</li><li>FWAAS-BYOL</li><li>CN-SERIES</li><li>FWAAS-PAYG</li></ul> | The license type for the remote network. |
| spn_name |  | The SPN name, required when license_type is FWAAS-AGGREGATE. |
| subnets |  | List of subnet CIDR ranges for the remote network. |
| folder |  | The folder in which the resource is defined. |
| ecmp_load_balancing | <ul><li>enable</li><li>disable</li></ul> | Enable or disable ECMP load balancing for the remote network.<br>*Required* |
| ecmp_tunnels |  | List of ECMP tunnels when ecmp_load_balancing is enabled.<br>See [sub-options](#parameter-ecmp_tunnels). |
| ipsec_tunnel |  | The IPsec tunnel name when ecmp_load_balancing is disabled. |
| protocol |  | Protocol configuration for the remote network.<br>See [sub-options](#parameter-protocol). |
| provider |  | Authentication credentials.<br>*Required*<br>See [sub-options](#parameter-provider). |
| state | <ul><li>present</li><li>absent</li></ul> | Desired state of the remote network.<br>*Required* |

### Parameter: ecmp_tunnels

| Parameter | Comments |
| --- | --- |
| name | Name of the ECMP tunnel.<br>*Required* |
| ipsec_tunnel | The IPsec tunnel name for this ECMP tunnel.<br>*Required* |
| local_ip_address | The local IP address for this tunnel.<br>*Required* |
| peer_ip_address | The peer IP address for this tunnel.<br>*Required* |
| peer_as | The peer AS number for BGP.<br>*Required* |

### Parameter: protocol

| Parameter | Comments |
| --- | --- |
| bgp | BGP configuration for the remote network.<br>See [sub-options](#parameter-protocol-bgp). |

#### Parameter: protocol bgp

| Parameter | Comments |
| --- | --- |
| enable | Enable or disable BGP. |
| local_ip_address | The local IP address for BGP. |
| peer_ip_address | The peer IP address for BGP. |
| peer_as | The peer AS number for BGP. |
| local_as | The local AS number for BGP. |
| secret | The BGP authentication secret. |

### Parameter: provider

| Parameter | Comments |
| --- | --- |
| client_id | Client ID for authentication.<br>*Required* |
| client_secret | Client secret for authentication.<br>*Required* |
| tsg_id | Tenant Service Group ID.<br>*Required* |
| log_level | Log level for the SDK.<br>Default: "INFO" |

## Examples



```yaml
- name: Manage Remote Networks in Strata Cloud Manager
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

    - name: Create a remote network with standard IPsec tunnel
      cdot65.scm.remote_networks:
        provider: "{{ provider }}"
        name: "Branch-Office-1"
        description: "Remote network for Branch Office 1"
        region: "us-east-1"
        license_type: "FWAAS-AGGREGATE"
        spn_name: "main-spn"
        folder: "Remote Networks"
        ecmp_load_balancing: "disable"
        ipsec_tunnel: "tunnel-to-branch1"
        subnets: ["10.1.0.0/16", "10.2.0.0/16"]
        protocol:
          bgp:
            enable: true
            local_ip_address: "10.0.0.1"
            peer_ip_address: "10.0.0.2"
            local_as: "65000"
            peer_as: "65001"
            secret: "bgp-auth-key"
        state: "present"

    - name: Create a remote network with ECMP load balancing
      cdot65.scm.remote_networks:
        provider: "{{ provider }}"
        name: "Branch-Office-2"
        description: "Remote network for Branch Office 2 with ECMP"
        region: "us-west-1"
        license_type: "FWAAS-AGGREGATE"
        spn_name: "west-spn"
        folder: "Remote Networks"
        ecmp_load_balancing: "enable"
        ecmp_tunnels:
          - name: "tunnel1"
            ipsec_tunnel: "tunnel-to-branch2-1"
            local_ip_address: "10.0.1.1"
            peer_ip_address: "10.0.1.2"
            peer_as: "65002"
          - name: "tunnel2"
            ipsec_tunnel: "tunnel-to-branch2-2"
            local_ip_address: "10.0.2.1"
            peer_ip_address: "10.0.2.2"
            peer_as: "65002"
        subnets: ["10.3.0.0/16", "10.4.0.0/16"]
        state: "present"

    - name: Update a remote network
      cdot65.scm.remote_networks:
        provider: "{{ provider }}"
        name: "Branch-Office-1"
        description: "Updated description for Branch Office 1"
        region: "us-east-1"
        folder: "Remote Networks"
        ecmp_load_balancing: "disable"
        ipsec_tunnel: "updated-tunnel-to-branch1"
        subnets: ["10.1.0.0/16", "10.2.0.0/16", "10.5.0.0/16"]
        state: "present"

    - name: Delete a remote network
      cdot65.scm.remote_networks:
        provider: "{{ provider }}"
        name: "Branch-Office-2"
        folder: "Remote Networks"
        state: "absent"
```



## Return Values

| Key | Returned | Description |
| --- | --- | --- |
| changed | Always | Whether any changes were made. |
| remote_network | When state is present | Details about the remote network. |



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
