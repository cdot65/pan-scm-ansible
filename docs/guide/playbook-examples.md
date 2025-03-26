# Playbook Examples

This page provides real-world examples of Ansible playbooks using the Palo Alto Networks Strata
Cloud Manager Ansible Collection. These examples demonstrate common use cases and best practices for
automating SCM management.

## Basic Object Management

### Creating Address Objects and Groups

```yaml
---
- name: Manage Address Objects
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml  # Contains encrypted credentials
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
  
  tasks:
    # Create individual address objects
    - name: Create Address Objects
      cdot65.scm.address:
        provider: "{{ provider }}"
        name: "{{ item.name }}"
        folder: "Texas"
        description: "{{ item.description }}"
        ip_netmask: "{{ item.ip }}"
        state: present
      loop:
        - { name: "web-server-1", description: "Web Server 1", ip: "10.1.1.1/32" }
        - { name: "web-server-2", description: "Web Server 2", ip: "10.1.1.2/32" }
        - { name: "app-server-1", description: "App Server 1", ip: "10.1.2.1/32" }
        - { name: "app-server-2", description: "App Server 2", ip: "10.1.2.2/32" }
    
    # Create address groups
    - name: Create Address Groups
      cdot65.scm.address_group:
        provider: "{{ provider }}"
        name: "{{ item.name }}"
        folder: "Texas"
        description: "{{ item.description }}"
        static:
          - "{{ item.members[0] }}"
          - "{{ item.members[1] }}"
        state: present
      loop:
        - { name: "web-servers", description: "Web Servers", members: ["web-server-1", "web-server-2"] }
        - { name: "app-servers", description: "App Servers", members: ["app-server-1", "app-server-2"] }
    
    # Commit changes
    - name: Commit Changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        description: "Add address objects and groups"
        folders: ["Texas"]
```

### Creating Service Objects and Groups

```yaml
---
- name: Manage Service Objects
  hosts: localhost
  gather_facts: false
  vars_files:
    - vault.yaml
  vars:
    provider:
      client_id: "{{ client_id }}"
      client_secret: "{{ client_secret }}"
      tsg_id: "{{ tsg_id }}"
  
  tasks:
    # Create service objects
    - name: Create Service Objects
      cdot65.scm.service:
        provider: "{{ provider }}"
        name: "{{ item.name }}"
        folder: "Texas"
        description: "{{ item.description }}"
        protocol:
          "{{ item.protocol_type }}":
            port: "{{ item.port }}"
        state: present
      loop:
        - { name: "http", description: "HTTP", protocol_type: "tcp", port: "80" }
        - { name: "https", description: "HTTPS", protocol_type: "tcp", port: "443" }
        - { name: "ssh", description: "SSH", protocol_type: "tcp", port: "22" }
        - { name: "rdp", description: "RDP", protocol_type: "tcp", port: "3389" }
    
    # Create service group
    - name: Create Service Group
      cdot65.scm.service_group:
        provider: "{{ provider }}"
        name: "web-services"
        folder: "Texas"
        description: "Web Services"
        members: ["http", "https"]
        state: present
    
    # Commit changes
    - name: Commit Changes
      cdot65.scm.commit:
        provider: "{{ provider }}"
        description: "Add service objects and groups"
        folders: ["Texas"]
```

## Security Policy Management

### Creating Security Rules

```yaml
---
- name: Manage Security Rules
  hosts: localhost
  connection: local
  gather_facts: false
  
  tasks:
    # Create security zones
    - name: Create Security Zones
      cdot65.scm.security_zone:
        name: "{{ item.name }}"
        folder: "SharedFolder"
        description: "{{ item.description }}"
      loop:
        - { name: "Internet", description: "Internet Zone" }
        - { name: "DMZ", description: "DMZ Zone" }
        - { name: "Internal", description: "Internal Zone" }
    
    # Create inbound web access rule
    - name: Create Inbound Web Access Rule
      cdot65.scm.security_rule:
        name: "Allow-Inbound-Web"
        folder: "SharedFolder"
        description: "Allow inbound web traffic"
        source_zones: ["Internet"]
        destination_zones: ["DMZ"]
        source_addresses: ["any"]
        destination_addresses: ["web-servers"]
        applications: ["web-browsing", "ssl"]
        services: ["application-default"]
        action: "allow"
        log_end: true
    
    # Create outbound access rule
    - name: Create Outbound Access Rule
      cdot65.scm.security_rule:
        name: "Allow-Outbound-Web"
        folder: "SharedFolder"
        description: "Allow outbound web traffic"
        source_zones: ["Internal"]
        destination_zones: ["Internet"]
        source_addresses: ["internal-clients"]
        destination_addresses: ["any"]
        applications: ["web-browsing", "ssl"]
        services: ["application-default"]
        action: "allow"
        log_end: true
    
    # Create rule with security profiles
    - name: Create Rule with Security Profiles
      cdot65.scm.security_rule:
        name: "Allow-Inspected-Web"
        folder: "SharedFolder"
        description: "Allow web traffic with security inspection"
        source_zones: ["Internal"]
        destination_zones: ["Internet"]
        source_addresses: ["internal-clients"]
        destination_addresses: ["any"]
        applications: ["web-browsing", "ssl"]
        services: ["application-default"]
        action: "allow"
        log_end: true
        profile_type: "profiles"
        antivirus_profile: "default-antivirus"
        anti_spyware_profile: "default-anti-spyware"
        vulnerability_profile: "default-vulnerability"
        url_filtering_profile: "default-url-filtering"
    
    # Commit changes
    - name: Commit Changes
      cdot65.scm.commit:
        description: "Add security rules"
```

## Network Configuration

### Remote Network Configuration

```yaml
---
- name: Configure Remote Networks
  hosts: localhost
  connection: local
  gather_facts: false
  
  tasks:
    # Create IKE Crypto Profile
    - name: Create IKE Crypto Profile
      cdot65.scm.ike_crypto_profile:
        name: "Standard-IKE-Crypto"
        folder: "SharedFolder"
        description: "Standard IKE crypto profile"
        dh_groups: ["group14"]
        encryptions: ["aes-256-cbc"]
        authentications: ["sha256"]
    
    # Create IPsec Crypto Profile
    - name: Create IPsec Crypto Profile
      cdot65.scm.ipsec_crypto_profile:
        name: "Standard-IPsec-Crypto"
        folder: "SharedFolder"
        description: "Standard IPsec crypto profile"
        esp_encryptions: ["aes-256-cbc"]
        esp_authentications: ["sha256"]
        dh_group: "group14"
        lifetime_seconds: 3600
    
    # Create IKE Gateway
    - name: Create IKE Gateway
      cdot65.scm.ike_gateway:
        name: "Branch-Office-Gateway"
        folder: "SharedFolder"
        description: "Branch Office VPN Gateway"
        version: "ikev2"
        peer_address: "198.51.100.1"
        interface: "ethernet1/1"
        pre_shared_key: "{{ ike_psk }}"  # Should be in vault
        local_id_type: "ipaddr"
        local_id_value: "203.0.113.1"
        peer_id_type: "ipaddr"
        peer_id_value: "198.51.100.1"
        crypto_profile: "Standard-IKE-Crypto"
    
    # Create Remote Network
    - name: Create Remote Network
      cdot65.scm.remote_network:
        name: "Branch-Office-VPN"
        folder: "SharedFolder"
        description: "Branch Office VPN Connection"
        ike_gateway: "Branch-Office-Gateway"
        ipsec_crypto_profile: "Standard-IPsec-Crypto"
        tunnel_interface: "tunnel.1"
        region: "us-east"
    
    # Commit changes
    - name: Commit Changes
      cdot65.scm.commit:
        description: "Add remote network configuration"
```

## Configuration Deployment

### Deploy Configuration to Firewalls

```yaml
---
- name: Deploy Configurations
  hosts: localhost
  connection: local
  gather_facts: false
  
  tasks:
    # Commit any pending changes
    - name: Commit Changes
      cdot65.scm.commit:
        description: "Pre-deployment commit"
      register: commit_result
    
    # Push configuration to device group
    - name: Push Configuration to Device Group
      cdot65.scm.push_config:
        device_groups:
          - "Branch-Offices"
        description: "Weekly security policy update"
      register: push_result
      when: commit_result.changed
    
    # Monitor push job
    - name: Monitor Push Job
      cdot65.scm.job_info:
        job_id: "{{ push_result.job_id }}"
      register: job_status
      until: job_status.status == "COMPLETED" or job_status.status == "FAILED"
      retries: 30
      delay: 10
      when: push_result is defined and push_result.job_id is defined
    
    # Report deployment status
    - name: Report Deployment Status
      debug:
        msg: "Deployment status: {{ job_status.status }}"
      when: job_status is defined
```

## Workflow Examples

### Security Policy Update Workflow

```yaml
---
- name: Security Policy Update Workflow
  hosts: localhost
  connection: local
  gather_facts: false
  
  vars:
    policy_folder: "SecurityPolicies"
    policy_change_ticket: "CHG0012345"
    deploy_to_prod: false
  
  tasks:
    # Create new address objects
    - name: Create New Address Objects
      cdot65.scm.address:
        name: "{{ item.name }}"
        folder: "{{ policy_folder }}"
        description: "{{ item.description }} ({{ policy_change_ticket }})"
        ip_netmask: "{{ item.ip }}"
      loop: "{{ new_address_objects }}"
      
    # Create new application rule
    - name: Create Application Access Rule
      cdot65.scm.security_rule:
        name: "Allow-App-Traffic-{{ policy_change_ticket }}"
        folder: "{{ policy_folder }}"
        description: "Allow application traffic ({{ policy_change_ticket }})"
        source_zones: ["Internal"]
        destination_zones: ["DMZ"]
        source_addresses: ["internal-clients"]
        destination_addresses: "{{ new_address_objects | map(attribute='name') | list }}"
        applications: ["web-browsing", "ssl"]
        services: ["application-default"]
        action: "allow"
        log_end: true
        position: "before"
        reference_rule: "Default-Deny"
      
    # Commit changes
    - name: Commit Changes
      cdot65.scm.commit:
        description: "Security rule update for {{ policy_change_ticket }}"
      register: commit_result
      
    # Deploy to test firewalls only
    - name: Deploy to Test Environment
      cdot65.scm.push_config:
        device_groups:
          - "Test-Firewalls"
        description: "Test deployment for {{ policy_change_ticket }}"
      register: push_result
      
    # Deploy to production if flag is set
    - name: Deploy to Production
      cdot65.scm.push_config:
        device_groups:
          - "Production-Firewalls"
        description: "Production deployment for {{ policy_change_ticket }}"
      register: prod_push_result
      when: deploy_to_prod | bool
```

### Multi-Tenant Configuration

```yaml
---
- name: Multi-Tenant Configuration
  hosts: localhost
  connection: local
  gather_facts: false
  
  vars:
    tenants:
      - name: "Tenant-A"
        folder: "Tenant-A"
        prefix: "A"
        networks:
          - "10.1.0.0/16"
          - "192.168.1.0/24"
      - name: "Tenant-B"
        folder: "Tenant-B"
        prefix: "B"
        networks:
          - "10.2.0.0/16"
          - "192.168.2.0/24"
  
  tasks:
    # Loop through each tenant
    - name: Configure Each Tenant
      include_tasks: tenant_config.yml
      loop: "{{ tenants }}"
      loop_control:
        loop_var: tenant
        
    # File: tenant_config.yml
    # - name: Create Tenant Folder
    #   cdot65.scm.folder:
    #     name: "{{ tenant.folder }}"
    #     
    # - name: Create Tenant Networks
    #   cdot65.scm.address:
    #     name: "{{ tenant.prefix }}-Net-{{ index }}"
    #     folder: "{{ tenant.folder }}"
    #     ip_netmask: "{{ network }}"
    #   loop: "{{ tenant.networks }}"
    #   loop_control:
    #     index_var: index
    #
    # - name: Create Tenant Tags
    #   cdot65.scm.tag:
    #     name: "{{ tenant.name }}"
    #     folder: "{{ tenant.folder }}"
    #     color: "color{{ 5 + loop.index }}"
    #
    # - name: Create Address Group
    #   cdot65.scm.address_group:
    #     name: "{{ tenant.prefix }}-Networks"
    #     folder: "{{ tenant.folder }}"
    #     static_members: "{{ tenant.networks | map('regex_replace', '^(.*)$', tenant.prefix + '-Net-\\1') | list }}"
    #     
    # - name: Create Tenant Zone
    #   cdot65.scm.security_zone:
    #     name: "{{ tenant.prefix }}-Zone"
    #     folder: "{{ tenant.folder }}"
    #
    # - name: Create Tenant Rules
    #   cdot65.scm.security_rule:
    #     name: "{{ tenant.prefix }}-Outbound"
    #     folder: "{{ tenant.folder }}"
    #     source_zones: ["{{ tenant.prefix }}-Zone"]
    #     destination_zones: ["Internet"]
    #     source_addresses: ["{{ tenant.prefix }}-Networks"]
    #     destination_addresses: ["any"]
    #     action: "allow"
```

## Inventory and Reporting

### Inventory-Based Configuration

```yaml
---
- name: Configure Firewalls Based on Inventory
  hosts: scm_firewalls
  connection: local
  gather_facts: false
  
  tasks:
    # Create zones based on inventory
    - name: Create Security Zones
      cdot65.scm.security_zone:
        name: "{{ item }}-Zone"
        folder: "SharedFolder"
        description: "Zone for {{ item }}"
      loop: "{{ groups | select('match', '^location_.*') | list | map('regex_replace', '^location_(.*)$', '\\1') | list }}"
      
    # Create address objects from inventory hosts
    - name: Create Address Objects for Hosts
      cdot65.scm.address:
        name: "host-{{ inventory_hostname }}"
        folder: "SharedFolder"
        description: "Host {{ inventory_hostname }}"
        ip_netmask: "{{ ansible_host }}/32"
      when: ansible_host is defined
```

### SCM Reporting

```yaml
---
- name: Generate SCM Configuration Report
  hosts: localhost
  connection: local
  gather_facts: false
  
  tasks:
    # Gather information on security rules
    - name: Get Security Rules
      cdot65.scm.security_rule_info:
        folder: "SharedFolder"
      register: security_rules
      
    # Generate report on unused rules
    - name: Find Unused Rules
      set_fact:
        unused_rules: "{{ security_rules.rules | selectattr('hit_count', 'equalto', 0) | list }}"
      when: security_rules.rules is defined
      
    # Create CSV report
    - name: Create Unused Rules Report
      copy:
        content: "Rule Name,Description,Last Modified,Hit Count\n{{ unused_rules | map(attribute='name') | zip(unused_rules | map(attribute='description'), unused_rules | map(attribute='last_modified'), unused_rules | map(attribute='hit_count')) | map('join', ',') | join('\n') }}"
        dest: "./unused_rules_report.csv"
      when: unused_rules is defined and unused_rules | length > 0
```

## Integration with Other Platforms

### ServiceNow Integration

```yaml
---
- name: SCM and ServiceNow Integration
  hosts: localhost
  connection: local
  gather_facts: false
  
  vars:
    snow_instance: "{{ lookup('env', 'SNOW_INSTANCE') }}"
    snow_username: "{{ lookup('env', 'SNOW_USERNAME') }}"
    snow_password: "{{ lookup('env', 'SNOW_PASSWORD') }}"
    change_number: "CHG0012345"
    
  tasks:
    # Get change request details
    - name: Get Change Request Details
      uri:
        url: "https://{{ snow_instance }}.service-now.com/api/now/table/change_request?number={{ change_number }}"
        method: GET
        user: "{{ snow_username }}"
        password: "{{ snow_password }}"
        force_basic_auth: yes
        return_content: yes
        headers:
          Accept: application/json
      register: change_result
      
    # Extract change details
    - name: Extract Change Details
      set_fact:
        change_details: "{{ change_result.json.result[0] }}"
        change_description: "{{ change_result.json.result[0].description }}"
      when: change_result.json.result | length > 0
      
    # Implement firewall changes
    - name: Implement Firewall Changes
      cdot65.scm.security_rule:
        name: "Rule-{{ change_number }}"
        folder: "SharedFolder"
        description: "{{ change_description | default('Rule for ' + change_number) }}"
        source_zones: ["Internal"]
        destination_zones: ["DMZ"]
        source_addresses: ["any"]
        destination_addresses: ["web-servers"]
        applications: ["web-browsing", "ssl"]
        action: "allow"
      register: rule_result
      when: change_details is defined
      
    # Update ServiceNow with implementation status
    - name: Update Change Request
      uri:
        url: "https://{{ snow_instance }}.service-now.com/api/now/table/change_request/{{ change_details.sys_id }}"
        method: PATCH
        user: "{{ snow_username }}"
        password: "{{ snow_password }}"
        force_basic_auth: yes
        body_format: json
        body:
          work_notes: "Firewall rule implemented via Ansible. Rule ID: {{ rule_result.scm_object.id }}"
          state: "3"  # Implement state
        headers:
          Content-Type: application/json
      when: rule_result is defined and rule_result.changed
```

These examples demonstrate various usage scenarios for the SCM Ansible Collection. For more specific
guidance or advanced examples, refer to the [Module Reference](../collection/modules/index.md) and
[Using Roles](using-roles.md) documentation.
