# BGP Routing Configuration Object

## Table of Contents

- [BGP Routing Configuration Object](#bgp-routing-configuration-object)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Core Methods](#core-methods)
  - [BGP Routing Model Attributes](#bgp-routing-model-attributes)
    - [Routing Preference Options](#routing-preference-options)
      - [Cold Potato Routing Attributes](#cold-potato-routing-attributes)
    - [Backbone Routing Options](#backbone-routing-options)
  - [Exceptions](#exceptions)
  - [Basic Configuration](#basic-configuration)
  - [Usage Examples](#usage-examples)
    - [Configuring BGP Routing](#configuring-bgp-routing)
    - [Basic BGP Configuration](#basic-bgp-configuration)
    - [Comprehensive BGP Configuration](#comprehensive-bgp-configuration)
    - [Updating BGP Configuration](#updating-bgp-configuration)
    - [Retrieving BGP Configuration](#retrieving-bgp-configuration)
  - [Managing Configuration Changes](#managing-configuration-changes)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
    - [Routing Model Selection](#routing-model-selection)
    - [Backbone Routing Strategy](#backbone-routing-strategy)
    - [Route Advertisement](#route-advertisement)
    - [Change Management](#change-management)
    - [Performance Considerations](#performance-considerations)
  - [Related Modules](#related-modules)

## Overview

The `bgp_routing` Ansible module provides functionality to manage BGP (Border Gateway Protocol)
routing configuration in Palo Alto Networks' Strata Cloud Manager (SCM). This module allows you to
configure BGP routing preferences, backbone routing options, outbound routes for services, and other
key BGP parameters to control traffic flow across your network.

## Core Methods

| Method     | Description                 | Parameters             | Return Type               |
| ---------- | --------------------------- | ---------------------- | ------------------------- |
| `get()`    | Retrieves BGP configuration | No parameters required | `BgpRoutingResponseModel` |
| `update()` | Updates BGP configuration   | `data: Dict[str, Any]` | `BgpRoutingResponseModel` |

## BGP Routing Model Attributes

| Attribute                      | Type           | Required | Description                                             |
| ------------------------------ | -------------- | -------- | ------------------------------------------------------- |
| `routing_preference`           | Dict[str, Any] | No       | BGP routing preferences configuration (hot/cold potato) |
| `backbone_routing`             | str            | No       | Backbone routing mode selection                         |
| `accept_route_over_SC`         | bool           | No       | Whether to accept routes over service connections       |
| `outbound_routes_for_services` | List[str]      | No       | List of outbound routes to be advertised for services   |
| `onboarding_status`            | str            | No       | Current BGP onboarding status (read-only)               |

### Routing Preference Options

| Option                | Type | Description                             |
| --------------------- | ---- | --------------------------------------- |
| `hot_potato_routing`  | Dict | Exit traffic at closest point to source |
| `cold_potato_routing` | Dict | Exit traffic at designated regions      |

#### Cold Potato Routing Attributes

| Attribute          | Type | Required | Description                     |
| ------------------ | ---- | -------- | ------------------------------- |
| `primary_region`   | str  | Yes      | Primary exit region for traffic |
| `secondary_region` | str  | No       | Backup exit region for traffic  |

### Backbone Routing Options

| Value                                | Description                                        |
| ------------------------------------ | -------------------------------------------------- |
| `symmetric-routing`                  | Traffic flows through same path in both directions |
| `asymmetric-routing`                 | Traffic may flow through different paths           |
| `asymmetric-routing-with-load-share` | Traffic distributed across multiple paths          |

## Exceptions

| Exception                   | Description                      |
| --------------------------- | -------------------------------- |
| `InvalidConfigurationError` | Invalid BGP configuration format |
| `ValidationError`           | Configuration validation failed  |
| `MissingRequiredFieldError` | Required parameter not provided  |
| `InvalidRouteError`         | Invalid route format specified   |
| `AuthenticationError`       | Authentication failed            |
| `ServerError`               | Internal server error            |

## Basic Configuration

The BGP Routing module requires proper authentication credentials to access the Strata Cloud Manager
API.

```yaml
- name: Basic BGP Routing Configuration
  hosts: localhost
  gather_facts: false
  vars:
    provider:
      client_id: "your_client_id"
      client_secret: "your_client_secret"
      tsg_id: "your_tsg_id"
      log_level: "INFO"
  tasks:
    - name: Configure BGP routing
      cdot65.scm.bgp_routing:
        provider: "{{ provider }}"
        backbone_routing: "asymmetric-routing-with-load-share"
        routing_preference:
          hot_potato_routing: {}
        accept_route_over_SC: true
        outbound_routes_for_services:
          - "10.0.0.0/8"
        state: "present"
```

## Usage Examples

### Configuring BGP Routing

BGP routing configuration enables you to control how traffic flows between your network and external
networks.

### Basic BGP Configuration

This example creates a simple BGP configuration with hot potato routing.

```yaml
- name: Configure basic BGP routing
  cdot65.scm.bgp_routing:
    provider: "{{ provider }}"
    routing_preference:
      hot_potato_routing: {}
    backbone_routing: "asymmetric-routing"
    accept_route_over_SC: true
    state: "present"
```

### Comprehensive BGP Configuration

This example creates a more comprehensive BGP configuration with cold potato routing, specific
backbone mode, and defined outbound routes.

```yaml
- name: Configure comprehensive BGP routing
  cdot65.scm.bgp_routing:
    provider: "{{ provider }}"
    routing_preference:
      cold_potato_routing:
        primary_region: "us-east-1"
        secondary_region: "us-west-1"
    backbone_routing: "symmetric-routing"
    accept_route_over_SC: true
    outbound_routes_for_services:
      - "10.0.0.0/8"
      - "172.16.0.0/12"
      - "192.168.0.0/16"
    state: "present"
```

### Updating BGP Configuration

This example updates an existing BGP configuration by changing the routing preference and backbone
routing options.

```yaml
- name: Update BGP routing configuration
  cdot65.scm.bgp_routing:
    provider: "{{ provider }}"
    routing_preference:
      hot_potato_routing: {}  # Switching from cold potato to hot potato
    backbone_routing: "asymmetric-routing-with-load-share"
    accept_route_over_SC: true
    outbound_routes_for_services:
      - "10.0.0.0/8"
      - "172.16.0.0/12"
    state: "present"
```

### Retrieving BGP Configuration

This example retrieves the current BGP configuration without making any changes.

```yaml
- name: Get current BGP routing configuration
  cdot65.scm.bgp_routing:
    provider: "{{ provider }}"
    state: "present"
  register: bgp_config

- name: Display current BGP configuration
  debug:
    var: bgp_config
```

## Managing Configuration Changes

After configuring or updating BGP routing, you may need to commit your changes to apply them across
the network.

```yaml
- name: Commit BGP configuration changes
  cdot65.scm.commit:
    provider: "{{ provider }}"
    description: "Updated BGP routing configuration"
```

## Error Handling

It's important to handle potential errors when working with BGP routing configuration.

```yaml
- name: Configure BGP routing with error handling
  block:
    - name: Update BGP routing configuration
      cdot65.scm.bgp_routing:
        provider: "{{ provider }}"
        routing_preference:
          cold_potato_routing:
            primary_region: "us-east-1"
            secondary_region: "us-west-1"
        backbone_routing: "symmetric-routing"
        accept_route_over_SC: true
        outbound_routes_for_services:
          - "10.0.0.0/8"
        state: "present"
      register: bgp_result
      
    - name: Commit changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        description: "Updated BGP routing configuration"
      
  rescue:
    - name: Handle errors
      debug:
        msg: "An error occurred with BGP configuration: {{ ansible_failed_result.msg }}"
        
    - name: Get current BGP configuration for troubleshooting
      cdot65.scm.bgp_routing:
        provider: "{{ provider }}"
        state: "present"
      register: current_bgp
      ignore_errors: yes
      
    - name: Display current configuration for debugging
      debug:
        var: current_bgp
      when: current_bgp is defined
```

## Best Practices

### Routing Model Selection

- Choose hot potato routing when you want traffic to exit at the closest point to the source
- Use cold potato routing to direct all traffic through specific regional exit points
- Align routing model with your application requirements and network topology
- Consider regulatory requirements that may impact traffic routing decisions
- Document your routing preference and the reasoning behind the choice

### Backbone Routing Strategy

- Use symmetric routing when consistent path selection is required for traffic flow
- Consider asymmetric routing for greater flexibility in traffic handling
- Implement asymmetric routing with load sharing for improved bandwidth utilization
- Understand the impact of each mode on troubleshooting and monitoring
- Test backbone routing changes in a controlled environment before deployment

### Route Advertisement

- Be selective about which networks to advertise over service connections
- Avoid advertising overlapping routes which can lead to routing issues
- Only advertise routes that need to be accessible through service connections
- Use CIDR notation properly to define precise network boundaries
- Regularly audit advertised routes to ensure they remain necessary

### Change Management

- Document your BGP routing design and configuration choices
- Implement changes during maintenance windows to minimize disruption
- Test BGP routing changes in non-production environments first
- Develop a rollback plan for each BGP configuration change
- Monitor routing convergence and stability after making changes

### Performance Considerations

- Balance routing efficiency with security requirements
- Consider the impact of routing decisions on latency-sensitive applications
- Monitor BGP session health and routing stability
- Implement alerts for unexpected routing changes
- Plan for redundancy in critical routing paths

## Related Modules

- [network_locations](network_locations.md) - Configure network locations that affect routing
- [remote_networks](remote_networks.md) - Configure remote networks using BGP
- [service_connections](service_connections.md) - Manage service connections used with BGP routing
- [ike_gateway](ike_gateway.md) - Configure VPN tunnels that may use BGP routing
- [ipsec_tunnel](ipsec_tunnel.md) - Manage IPsec tunnels that can work with BGP routing
