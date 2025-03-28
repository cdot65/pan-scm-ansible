# BGP Routing Information Object

## Table of Contents

- [BGP Routing Information Object](#bgp-routing-information-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [BGP Routing Info Model Attributes](#bgp-routing-info-model-attributes)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Retrieving BGP Routing Information](#retrieving-bgp-routing-information)
    - [Using Different Gather Subsets](#using-different-gather-subsets)
    - [Checking Routing Preference Type](#checking-routing-preference-type)
    - [Analyzing Outbound Routes](#analyzing-outbound-routes)
  - [Processing Retrieved Information](#processing-retrieved-information)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Information Handling](#information-handling)
    - [Performance Optimization](#performance-optimization)
    - [Integration with Other Modules](#integration-with-other-modules)
    - [Configuration Auditing](#configuration-auditing)
    - [Troubleshooting](#troubleshooting)
  - [Related Modules](#related-modules)

## Overview

The `bgp_routing_info` Ansible module provides functionality to retrieve information about BGP (Border Gateway Protocol) routing configuration in Palo Alto Networks' Strata Cloud Manager (SCM). This is a read-only module that can retrieve detailed information about the global BGP routing configuration including routing preferences, backbone routing settings, outbound routes, and other BGP-related parameters. BGP routing is a singleton object in SCM, meaning there is only one global configuration.

## Core Methods

| Method  | Description                             | Parameters                    | Return Type               |
| ------- | --------------------------------------- | ----------------------------- | ------------------------- |
| `get()` | Gets the global BGP routing configuration | No parameters required        | `BgpRoutingResponseModel` |

## BGP Routing Info Model Attributes

| Attribute                   | Type           | Required | Description                                       |
| --------------------------- | -------------- | -------- | ------------------------------------------------- |
| `gather_subset`             | list           | No       | Determines which information to gather (default: ['config']) |
| `routing_preference`        | Dict[str, Any] | No       | BGP routing preferences configuration (hot/cold potato) |
| `backbone_routing`          | str            | No       | Backbone routing mode selection                   |
| `accept_route_over_SC`      | bool           | No       | Whether routes are accepted over service connections |
| `outbound_routes_for_services` | List[str]   | No       | List of outbound routes advertised for services   |
| `add_host_route_to_ike_peer` | bool          | No       | Whether host routes are added to IKE peers        |
| `withdraw_static_route`     | bool           | No       | Whether static routes are withdrawn               |
| `onboarding_status`         | str            | No       | Current BGP onboarding status (read-only)         |

## Exceptions

| Exception                | Description                      |
| ------------------------ | -------------------------------- |
| `ObjectNotPresentError`  | BGP routing config not found     |
| `InvalidObjectError`     | Invalid BGP configuration format |
| `AuthenticationError`    | Authentication failed            |
| `ServerError`            | Internal server error            |

## Basic Configuration

The BGP Routing Info module requires proper authentication credentials to access the Strata Cloud Manager API.

```yaml
- name: Basic BGP Routing Info Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Get BGP routing information
      cdot65.scm.bgp_routing_info:
        provider: "{{ provider }}"
      register: bgp_info
      
    - name: Display retrieved information
      debug:
        var: bgp_info.bgp_routing
```

## Usage Examples

### Retrieving BGP Routing Information

The module provides ways to retrieve BGP routing information based on your specific needs.

<div class="termynal" data-termynal>
```yaml
- name: Get BGP routing information
  cdot65.scm.bgp_routing_info:
    provider: "{{ provider }}"
  register: bgp_info

- name: Display BGP routing information
  debug:
    var: bgp_info.bgp_routing
```
</div>

### Using Different Gather Subsets

You can specify different gather subsets to control what information is retrieved.

<div class="termynal" data-termynal>
```yaml
- name: Get basic BGP routing configuration
  cdot65.scm.bgp_routing_info:
    provider: "{{ provider }}"
    gather_subset: ["config"]
  register: basic_bgp_info

- name: Get all BGP routing information
  cdot65.scm.bgp_routing_info:
    provider: "{{ provider }}"
    gather_subset: ["all"]
  register: complete_bgp_info
```
</div>

### Checking Routing Preference Type

This example shows how to check which routing preference type is configured.

<div class="termynal" data-termynal>
```yaml
- name: Get BGP routing information
  cdot65.scm.bgp_routing_info:
    provider: "{{ provider }}"
  register: bgp_info

- name: Check routing preference type
  debug:
    msg: >
      Routing preference type is
      {% if bgp_info.bgp_routing.routing_preference.default is defined %}
      default routing
      {% elif bgp_info.bgp_routing.routing_preference.hot_potato_routing is defined %}
      hot potato routing
      {% else %}
      unknown
      {% endif %}
```
</div>

### Analyzing Outbound Routes

This example retrieves BGP routing information and examines the configured outbound routes.

<div class="termynal" data-termynal>
```yaml
- name: Get BGP routing information
  cdot65.scm.bgp_routing_info:
    provider: "{{ provider }}"
  register: bgp_info

- name: Display outbound routes
  debug:
    msg: "Outbound routes: {{ bgp_info.bgp_routing.outbound_routes_for_services }}"
  when: bgp_info.bgp_routing.outbound_routes_for_services | length > 0

- name: Count number of outbound routes
  debug:
    msg: "Number of outbound routes: {{ bgp_info.bgp_routing.outbound_routes_for_services | length }}"
  when: bgp_info.bgp_routing.outbound_routes_for_services is defined
```
</div>

## Processing Retrieved Information

After retrieving BGP routing information, you can process the data for various purposes such as reporting, configuration validation, or troubleshooting.

<div class="termynal" data-termynal>
```yaml
- name: Create a summary of BGP routing configuration
  block:
    - name: Get BGP routing information
      cdot65.scm.bgp_routing_info:
        provider: "{{ provider }}"
      register: bgp_info
      
    - name: Set routing facts
      set_fact:
        backbone_mode: "{{ bgp_info.bgp_routing.backbone_routing }}"
        routing_type: "{{ 'default' if bgp_info.bgp_routing.routing_preference.default is defined else 'hot_potato' if bgp_info.bgp_routing.routing_preference.hot_potato_routing is defined else 'unknown' }}"
        accepts_routes: "{{ bgp_info.bgp_routing.accept_route_over_SC }}"
        outbound_routes: "{{ bgp_info.bgp_routing.outbound_routes_for_services | default([]) }}"
        
    - name: Display BGP configuration summary
      debug:
        msg: |
          BGP Routing Summary:
          - Backbone Routing Mode: {{ backbone_mode }}
          - Routing Preference Type: {{ routing_type }}
          - Accepts Routes over Service Connections: {{ accepts_routes }}
          - Number of Outbound Routes: {{ outbound_routes | length }}
          - Outbound Routes: {{ outbound_routes | join(', ') if outbound_routes else 'None configured' }}
```
</div>

## Error Handling

It's important to handle potential errors when retrieving BGP routing information.

<div class="termynal" data-termynal>
```yaml
- name: Retrieve BGP routing info with error handling
  block:
    - name: Attempt to retrieve BGP routing information
      cdot65.scm.bgp_routing_info:
        provider: "{{ provider }}"
      register: bgp_info
      
  rescue:
    - name: Handle BGP routing info error
      debug:
        msg: "Failed to retrieve BGP routing information: {{ ansible_failed_result.msg }}"
        
    - name: Log the error and continue
      debug:
        msg: "Continuing with other tasks without BGP routing information"
```
</div>

## Best Practices

### Information Handling

- Register results to variables for further processing
- Check if bgp_routing is defined before accessing properties
- Process different routing types appropriately (default vs. hot potato)

### Performance Optimization

- Retrieve only the information you need
- Use appropriate gather_subset to minimize data transfer
- Consider caching results for repeated access within the same playbook

### Integration with Other Modules

- Use retrieved BGP routing information to inform other module operations
- Combine with remote_networks_info and service_connections_info for a complete view
- Generate reports on routing configuration and status
- Validate actual BGP routing configuration against desired state

### Configuration Auditing

- Regular auditing of BGP routing configuration is recommended
- Generate reports on routing preferences, backbone routing mode, and advertised routes
- Compare configuration across different environments for consistency
- Document changes to BGP routing configuration for compliance purposes

### Troubleshooting

- Use BGP routing info to identify potential routing issues
- Verify routing preference settings match network design
- Check outbound routes for accuracy and completeness
- Validate backbone routing mode selections against design requirements
- Monitor for unauthorized or unexpected changes to BGP routing configuration

## Related Modules

- [bgp_routing](bgp_routing.md) - Manage BGP routing configuration (create, update, reset)
- [network_locations](network_locations.md) - Configure network locations that affect routing
- [remote_networks](remote_networks.md) - Configure remote networks using BGP
- [service_connections](service_connections.md) - Manage service connections used with BGP routing
- [ike_gateway](ike_gateway.md) - Configure VPN tunnels that may use BGP routing