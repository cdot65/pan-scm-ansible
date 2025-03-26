# BGP Routing Configuration Object

## 1. Overview

The BGP Routing module allows you to manage BGP (Border Gateway Protocol) routing configuration within Strata Cloud
Manager (SCM). This module provides capabilities to configure BGP routing preferences, backbone routing options,
outbound routes for services, and other key BGP parameters.

## 2. Core Methods

| Method     | Description                 | Parameters             | Return Type     |
|------------|-----------------------------|------------------------|-----------------|
| `get()`    | Retrieves BGP configuration | -                      | `ResponseModel` |
| `update()` | Updates BGP configuration   | `data: Dict[str, Any]` | `ResponseModel` |

## 3. Model Attributes

| Attribute                      | Type           | Required | Description                             |
|--------------------------------|----------------|----------|-----------------------------------------|
| `routing_preference`           | Dict[str, Any] | No       | BGP routing preferences configuration   |
| `backbone_routing`             | str            | No       | Backbone routing mode                   |
| `accept_route_over_SC`         | bool           | No       | Accept routes over service connections  |
| `outbound_routes_for_services` | List[str]      | No       | Outbound routes advertised for services |
| `onboarding_status`            | str            | No       | BGP onboarding status (read-only)       |

### Routing Preference Options

- `hot_potato_routing` - Hot Potato routing
- `cold_potato_routing` - Cold Potato routing (with options)

### Backbone Routing Options

- `symmetric-routing` - Symmetric routing
- `asymmetric-routing` - Asymmetric routing
- `asymmetric-routing-with-load-share` - Asymmetric routing with load sharing

## 4. Basic Configuration

<div class="termy">

<!-- termynal -->

```yaml
- name: Update BGP routing configuration
  cdot65.scm.bgp_routing:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    backbone_routing: "asymmetric-routing-with-load-share"
    routing_preference:
      hot_potato_routing: {}
    accept_route_over_SC: true
    outbound_routes_for_services:
      - "10.0.0.0/8"
```

</div>

## 5. Usage Examples

### Retrieving Current BGP Configuration

<div class="termy">

<!-- termynal -->

```yaml
- name: Get current BGP routing configuration
  cdot65.scm.bgp_routing:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    state: "present"
  register: bgp_config

- name: Display current BGP configuration
  debug:
    var: bgp_config
```

</div>

### Configuring Hot Potato Routing

<div class="termy">

<!-- termynal -->

```yaml
- name: Configure hot potato routing
  cdot65.scm.bgp_routing:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    routing_preference:
      hot_potato_routing: {}
    backbone_routing: "asymmetric-routing-with-load-share"
    accept_route_over_SC: true
    state: "present"
```

</div>

### Configuring Cold Potato Routing

<div class="termy">

<!-- termynal -->

```yaml
- name: Configure cold potato routing
  cdot65.scm.bgp_routing:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    routing_preference:
      cold_potato_routing:
        primary_region: "us-east-1"
        secondary_region: "us-west-1"
    backbone_routing: "symmetric-routing"
    accept_route_over_SC: true
    state: "present"
```

</div>

### Configuring Service Routes

<div class="termy">

<!-- termynal -->

```yaml
- name: Configure outbound routes for services
  cdot65.scm.bgp_routing:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
    outbound_routes_for_services:
      - "10.0.0.0/8"
      - "172.16.0.0/12"
      - "192.168.0.0/16"
    state: "present"
```

</div>

## 6. Error Handling

<div class="termy">

<!-- termynal -->

```yaml
- name: Update BGP routing with error handling
  block:
    - name: Attempt to update BGP routing
      cdot65.scm.bgp_routing:
        provider: "{{ provider }}"
        routing_preference:
          invalid_option: {}  # Invalid option
        state: "present"
  rescue:
    - name: Handle error
      debug:
        msg: "Failed to update BGP routing. Check configuration parameters."
```

</div>

## 7. Best Practices

1. **Understand Routing Models**
    - Hot Potato Routing: Traffic exits the network at the closest point to the source
    - Cold Potato Routing: Traffic exits at specific designated regions
    - Choose the routing model based on your application requirements and network topology

2. **Backbone Routing Configuration**
    - Symmetric Routing: Ensures traffic flows through the same path in both directions
    - Asymmetric Routing: Allows different paths for inbound and outbound traffic
    - Asymmetric Routing with Load Share: Distributes traffic across multiple paths

3. **Service Connection Routes**
    - Carefully plan which networks should be advertised over service connections
    - Avoid advertising overlapping routes
    - Only advertise routes that need to be accessible through service connections

4. **Testing and Validation**
    - Test BGP routing changes during maintenance windows
    - Validate routing behavior after making changes
    - Monitor routing stability and convergence times

5. **Documentation**
    - Document your BGP routing design and configuration choices
    - Maintain records of any BGP-related changes
    - Document peering relationships and advertised routes

## 8. Related Models

- [Network Locations](network_locations.md) - Configure network locations that affect routing
- [Remote Networks](remote_networks.md) - Configure remote networks using BGP
- [IKE Gateway](ike_gateway.md) - Configure VPN tunnels that may use BGP routing