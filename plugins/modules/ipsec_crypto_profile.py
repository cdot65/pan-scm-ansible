# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is Apache2.0 licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# Copyright (c) 2024 Calvin Remsburg (@cdot65)
# All rights reserved.

"""
Ansible module for managing IPsec crypto profiles in SCM.

This module provides functionality to create, update, and delete IPsec crypto profiles
in the SCM (Strata Cloud Manager) system.
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import uuid
from datetime import datetime
import json

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_text

from ansible_collections.cdot65.scm.plugins.module_utils.api_spec.ipsec_crypto_profile import IPsecCryptoProfileSpec
from ansible_collections.cdot65.scm.plugins.module_utils.authenticate import get_scm_client
from ansible_collections.cdot65.scm.plugins.module_utils.serialize_response import (
    serialize_response,
)
from scm.exceptions import InvalidObjectError, MissingQueryParameterError, ObjectNotPresentError
from scm.models.network import IPsecCryptoProfileUpdateModel

DOCUMENTATION = r"""
---
module: ipsec_crypto_profile

short_description: Manage IPsec crypto profiles in SCM.

version_added: "0.1.0"

description:
    - Manage IPsec crypto profiles within Strata Cloud Manager (SCM).
    - Create, update, and delete IPsec crypto profile objects.
    - Configure ESP encryption, ESP authentication, AH authentication, and PFS settings.
    - Set lifetime and lifesize parameters.

options:
    name:
        description: The name of the IPsec crypto profile.
        required: true
        type: str
    description:
        description: Description of the IPsec crypto profile.
        required: false
        type: str
    esp:
        description: ESP configuration.
        required: false
        type: dict
        contains:
            encryption:
                description: List of ESP encryption algorithms to use.
                required: false
                type: list
                elements: str
                choices: ["des", "3des", "aes-128-cbc", "aes-192-cbc", "aes-256-cbc", "aes-128-gcm", "aes-256-gcm", "null"]
            authentication:
                description: List of ESP authentication algorithms to use.
                required: false
                type: list
                elements: str
                choices: ["md5", "sha1", "sha256", "sha384", "sha512", "none"]
    ah:
        description: AH configuration.
        required: false
        type: dict
        contains:
            authentication:
                description: List of AH authentication algorithms to use.
                required: false
                type: list
                elements: str
                choices: ["md5", "sha1", "sha256", "sha384", "sha512"]
    dh_group:
        description: Diffie-Hellman group to use for PFS.
        required: false
        type: str
        choices: ["no-pfs", "group1", "group2", "group5", "group14", "group19", "group20"]
    lifetime:
        description: SA lifetime configuration.
        required: false
        type: dict
        contains:
            seconds:
                description: Lifetime in seconds (180-65535).
                required: false
                type: int
            minutes:
                description: Lifetime in minutes (3-65535).
                required: false
                type: int
            hours:
                description: Lifetime in hours (1-65535).
                required: false
                type: int
            days:
                description: Lifetime in days (1-365).
                required: false
                type: int
    lifesize:
        description: SA lifesize configuration.
        required: false
        type: dict
        contains:
            kb:
                description: Lifesize limit in kilobytes.
                required: false
                type: int
            mb:
                description: Lifesize limit in megabytes.
                required: false
                type: int
            gb:
                description: Lifesize limit in gigabytes.
                required: false
                type: int
            tb:
                description: Lifesize limit in terabytes.
                required: false
                type: int
    folder:
        description: The folder in which the resource is defined.
        required: false
        type: str
    snippet:
        description: The snippet in which the resource is defined.
        required: false
        type: str
    device:
        description: The device in which the resource is defined.
        required: false
        type: str
    provider:
        description: Authentication credentials.
        required: true
        type: dict
        suboptions:
            client_id:
                description: Client ID for authentication.
                required: true
                type: str
            client_secret:
                description: Client secret for authentication.
                required: true
                type: str
            tsg_id:
                description: Tenant Service Group ID.
                required: true
                type: str
            log_level:
                description: Log level for the SDK.
                required: false
                type: str
                default: "INFO"
    state:
        description: Desired state of the IPsec crypto profile.
        required: true
        type: str
        choices:
          - present
          - absent

author:
    - Calvin Remsburg (@cdot65)
"""

EXAMPLES = r"""
---
- name: Manage IPsec Crypto Profiles in Strata Cloud Manager
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

    - name: Create an IPsec crypto profile with AES-256 and SHA-256
      cdot65.scm.ipsec_crypto_profile:
        provider: "{{ provider }}"
        name: "ipsec-esp-aes256-sha256"
        description: "IPsec ESP AES-256 SHA-256 profile"
        esp:
          encryption:
            - "aes-256-cbc"
          authentication:
            - "sha256"
        dh_group: "group14"
        lifetime:
          hours: 8
        lifesize:
          gb: 20
        folder: "Shared"
        state: "present"

    - name: Create an IPsec crypto profile with AES-128-GCM
      cdot65.scm.ipsec_crypto_profile:
        provider: "{{ provider }}"
        name: "ipsec-esp-aes128-gcm"
        description: "IPsec ESP AES-128-GCM profile"
        esp:
          encryption:
            - "aes-128-gcm"
          authentication:
            - "none"
        dh_group: "group19"
        lifetime:
          days: 1
        folder: "Shared"
        state: "present"

    - name: Create an IPsec crypto profile with AH
      cdot65.scm.ipsec_crypto_profile:
        provider: "{{ provider }}"
        name: "ipsec-ah-sha512"
        description: "IPsec AH SHA-512 profile"
        ah:
          authentication:
            - "sha512"
        dh_group: "group14"
        lifetime:
          hours: 24
        folder: "Shared"
        state: "present"
        
    - name: Update an existing IPsec crypto profile
      cdot65.scm.ipsec_crypto_profile:
        provider: "{{ provider }}"
        name: "ipsec-esp-aes256-sha256"
        description: "Updated IPsec ESP AES-256 SHA-256 profile"
        esp:
          encryption:
            - "aes-256-cbc"
          authentication:
            - "sha256"
        dh_group: "group19"  # Updated from group14
        lifetime:
          hours: 12  # Updated from 8
        lifesize:
          gb: 30  # Updated from 20
        folder: "Shared"
        state: "present"

    - name: Delete an IPsec crypto profile
      cdot65.scm.ipsec_crypto_profile:
        provider: "{{ provider }}"
        name: "ipsec-esp-aes128-gcm"
        folder: "Shared"
        state: "absent"
"""

RETURN = r"""
ipsec_crypto_profile:
  description: Information about the IPsec crypto profile
  returned: always
  type: complex
  contains:
    id:
      description: Unique ID of the IPsec crypto profile
      returned: always
      type: str
      sample: "01234567-89ab-cdef-0123-456789abcdef"
    name:
      description: Name of the IPsec crypto profile
      returned: always
      type: str
      sample: "ipsec-esp-aes256-sha256"
    description:
      description: Description of the IPsec crypto profile
      returned: when configured
      type: str
      sample: "IPsec ESP AES-256 SHA-256 profile"
    esp:
      description: ESP configuration
      returned: when configured
      type: dict
      contains:
        encryption:
          description: List of ESP encryption algorithms
          returned: when configured
          type: list
          sample: ["aes-256-cbc"]
        authentication:
          description: List of ESP authentication algorithms
          returned: when configured
          type: list
          sample: ["sha256"]
    ah:
      description: AH configuration
      returned: when configured
      type: dict
      contains:
        authentication:
          description: List of AH authentication algorithms
          returned: when configured
          type: list
          sample: ["sha512"]
    dh_group:
      description: Diffie-Hellman group used for PFS
      returned: when configured
      type: str
      sample: "group14"
    lifetime:
      description: SA lifetime configuration
      returned: when configured
      type: dict
      sample: {"hours": 8}
    lifesize:
      description: SA lifesize configuration
      returned: when configured
      type: dict
      sample: {"gb": 20}
    folder:
      description: Folder containing the profile
      returned: when applicable
      type: str
      sample: "Shared"
    snippet:
      description: Snippet containing the profile
      returned: when applicable
      type: str
    device:
      description: Device containing the profile
      returned: when applicable
      type: str
    created_on:
      description: Profile creation timestamp
      returned: always
      type: str
      sample: "2024-03-25T12:00:00Z"
    created_by:
      description: Creator of the profile
      returned: always
      type: str
      sample: "admin"
    modified_on:
      description: Profile last modification timestamp
      returned: always
      type: str
      sample: "2024-03-25T13:30:00Z"
    modified_by:
      description: Last modifier of the profile
      returned: always
      type: str
      sample: "admin"
"""


def build_profile_data(module_params):
    """
    Build the profile data dictionary from the module parameters.

    Args:
        module_params (dict): Module parameters

    Returns:
        dict: Profile data dictionary formatted for the SCM API
    """
    profile_data = {}

    # Name is required
    if module_params.get("name"):
        profile_data["name"] = module_params["name"]
    
    # Description is optional
    if module_params.get("description"):
        profile_data["description"] = module_params["description"]
    
    # Container types (one of folder, snippet, or device must be set)
    if module_params.get("folder"):
        profile_data["folder"] = module_params["folder"]
    
    if module_params.get("snippet"):
        profile_data["snippet"] = module_params["snippet"]
    
    if module_params.get("device"):
        profile_data["device"] = module_params["device"]

    # DH Group
    if module_params.get("dh_group"):
        profile_data["dh_group"] = module_params["dh_group"]
    
    # Process ESP parameters
    if module_params.get("esp"):
        profile_data["esp"] = {}
        
        if module_params["esp"].get("encryption"):
            profile_data["esp"]["encryption"] = module_params["esp"]["encryption"]
        
        if module_params["esp"].get("authentication"):
            profile_data["esp"]["authentication"] = module_params["esp"]["authentication"]
    
    # Process AH parameters
    if module_params.get("ah"):
        profile_data["ah"] = {}
        
        if module_params["ah"].get("authentication"):
            profile_data["ah"]["authentication"] = module_params["ah"]["authentication"]
    
    # Process lifetime
    if module_params.get("lifetime"):
        lifetime = {}
        for unit in ["seconds", "minutes", "hours", "days"]:
            if unit in module_params["lifetime"] and module_params["lifetime"][unit] is not None:
                # Convert to integer to ensure correct typing
                lifetime[unit] = int(module_params["lifetime"][unit])
        
        if lifetime:
            profile_data["lifetime"] = lifetime
    
    # Process lifesize - ensure only one unit is used
    if module_params.get("lifesize"):
        lifesize = {}
        # Check all units and find the first non-null value
        units = ["kb", "mb", "gb", "tb"]
        for unit in units:
            if unit in module_params["lifesize"] and module_params["lifesize"][unit] is not None:
                # Convert to integer to ensure correct typing
                lifesize[unit] = int(module_params["lifesize"][unit])
                # Only use the first non-null unit we find
                break
        
        if lifesize:
            profile_data["lifesize"] = lifesize
    
    return profile_data


def is_container_specified(data):
    """
    Check if exactly one container type (folder, snippet, device) is specified.

    Args:
        data (dict): Profile parameters

    Returns:
        bool: True if exactly one container is specified, False otherwise
    """
    container_count = sum(1 for c in ["folder", "snippet", "device"] if data.get(c))
    return container_count == 1


def get_existing_profile(client, profile_data):
    """
    Attempt to fetch an existing IPsec crypto profile.

    Args:
        client: SCM client instance
        profile_data (dict): Profile parameters to search for

    Returns:
        tuple: (bool, object) indicating if profile exists and the profile object if found
    """
    name = profile_data.get("name")
    folder = profile_data.get("folder")
    snippet = profile_data.get("snippet")
    device = profile_data.get("device")

    try:
        # Fetch the profile by name and container
        # Validate client has ipsec_crypto_profile attribute
        if not hasattr(client, 'ipsec_crypto_profile'):
            return False, "SCM client does not have ipsec_crypto_profile service initialized"
        
        profile = client.ipsec_crypto_profile.fetch(
            name=name,
            folder=folder,
            snippet=snippet,
            device=device,
        )
        return True, profile
    except ObjectNotPresentError:
        # Profile doesn't exist
        return False, None
    except Exception as e:
        return False, str(e)


def needs_update(existing, params):
    """
    Determine if the IPsec crypto profile needs to be updated.

    Args:
        existing: Existing IPsec crypto profile object from the SCM API
        params (dict): Profile parameters with desired state from Ansible module

    Returns:
        (bool, dict): Tuple containing:
            - bool: Whether an update is needed
            - dict: Complete object data for update including all fields from the existing
                   object with any modifications from the params
    """
    # Convert the existing profile to a dict
    existing_dict = existing.model_dump()
    
    # Create a dictionary for the update model, starting with the ID
    update_data = {"id": existing.id}
    
    # Check if each field needs to be updated
    update_needed = False
    
    # Check name
    if params.get("name") and params["name"] != existing.name:
        update_data["name"] = params["name"]
        update_needed = True
    else:
        update_data["name"] = existing.name
    
    # Safely check description - it might not be in the API response model
    if params.get("description"):
        if hasattr(existing, "description") and params["description"] != existing.description:
            update_data["description"] = params["description"]
            update_needed = True
        elif not hasattr(existing, "description"):
            # Description not in API response, but we're setting it
            update_data["description"] = params["description"]
            update_needed = True
    elif hasattr(existing, "description") and existing.description:
        update_data["description"] = existing.description
    
    # Check DH Group
    if params.get("dh_group") and params["dh_group"] != existing_dict.get("dh_group"):
        update_data["dh_group"] = params["dh_group"]
        update_needed = True
    else:
        update_data["dh_group"] = existing_dict.get("dh_group")
    
    # Check ESP configuration
    if params.get("esp"):
        if not existing_dict.get("esp"):
            update_data["esp"] = params["esp"]
            update_needed = True
        else:
            update_data["esp"] = {}
            
            # Check encryption
            if "encryption" in params["esp"]:
                existing_enc = existing_dict.get("esp", {}).get("encryption", [])
                requested_enc = params["esp"]["encryption"]
                
                # Compare lists without regard to order
                if sorted(existing_enc) != sorted(requested_enc):
                    update_data["esp"]["encryption"] = requested_enc
                    update_needed = True
                else:
                    update_data["esp"]["encryption"] = existing_enc
            elif "encryption" in existing_dict.get("esp", {}):
                update_data["esp"]["encryption"] = existing_dict["esp"]["encryption"]
            
            # Check authentication
            if "authentication" in params["esp"]:
                existing_auth = existing_dict.get("esp", {}).get("authentication", [])
                requested_auth = params["esp"]["authentication"]
                
                # Compare lists without regard to order
                if sorted(existing_auth) != sorted(requested_auth):
                    update_data["esp"]["authentication"] = requested_auth
                    update_needed = True
                else:
                    update_data["esp"]["authentication"] = existing_auth
            elif "authentication" in existing_dict.get("esp", {}):
                update_data["esp"]["authentication"] = existing_dict["esp"]["authentication"]
    else:
        if existing_dict.get("esp"):
            update_data["esp"] = existing_dict["esp"]
    
    # Check AH configuration
    if params.get("ah"):
        if not existing_dict.get("ah"):
            update_data["ah"] = params["ah"]
            update_needed = True
        else:
            update_data["ah"] = {}
            
            # Check authentication
            if "authentication" in params["ah"]:
                existing_auth = existing_dict.get("ah", {}).get("authentication", [])
                requested_auth = params["ah"]["authentication"]
                
                # Compare lists without regard to order
                if sorted(existing_auth) != sorted(requested_auth):
                    update_data["ah"]["authentication"] = requested_auth
                    update_needed = True
                else:
                    update_data["ah"]["authentication"] = existing_auth
            elif "authentication" in existing_dict.get("ah", {}):
                update_data["ah"]["authentication"] = existing_dict["ah"]["authentication"]
    else:
        if existing_dict.get("ah"):
            update_data["ah"] = existing_dict["ah"]
    
    # Check lifetime configuration
    if params.get("lifetime"):
        if not existing_dict.get("lifetime"):
            update_data["lifetime"] = params["lifetime"]
            update_needed = True
        else:
            # Compare lifetime dictionaries
            update_data["lifetime"] = {}
            for unit in ["seconds", "minutes", "hours", "days"]:
                if unit in params["lifetime"]:
                    if unit not in existing_dict["lifetime"] or params["lifetime"][unit] != existing_dict["lifetime"][unit]:
                        update_data["lifetime"][unit] = params["lifetime"][unit]
                        update_needed = True
                    else:
                        update_data["lifetime"][unit] = existing_dict["lifetime"][unit]
                elif unit in existing_dict["lifetime"]:
                    update_data["lifetime"][unit] = existing_dict["lifetime"][unit]
    else:
        if existing_dict.get("lifetime"):
            update_data["lifetime"] = existing_dict["lifetime"]
    
    # Check lifesize configuration
    if params.get("lifesize"):
        if not existing_dict.get("lifesize"):
            update_data["lifesize"] = params["lifesize"]
            update_needed = True
        else:
            # Compare lifesize dictionaries
            update_data["lifesize"] = {}
            for unit in ["kb", "mb", "gb", "tb"]:
                if unit in params["lifesize"]:
                    if unit not in existing_dict["lifesize"] or params["lifesize"][unit] != existing_dict["lifesize"][unit]:
                        update_data["lifesize"][unit] = params["lifesize"][unit]
                        update_needed = True
                    else:
                        update_data["lifesize"][unit] = existing_dict["lifesize"][unit]
                elif unit in existing_dict["lifesize"]:
                    update_data["lifesize"][unit] = existing_dict["lifesize"][unit]
    else:
        if existing_dict.get("lifesize"):
            update_data["lifesize"] = existing_dict["lifesize"]
    
    # Check container fields
    for container in ["folder", "snippet", "device"]:
        if params.get(container) and params[container] != existing_dict.get(container):
            update_data[container] = params[container]
            update_needed = True
        elif existing_dict.get(container):
            update_data[container] = existing_dict[container]
    
    return update_needed, update_data


def main():
    """
    Main execution path for the ipsec_crypto_profile module.

    This module provides functionality to create, update, and delete IPsec crypto profiles
    in the SCM (Strata Cloud Manager) system.

    :return: Ansible module exit data
    :rtype: dict
    """
    module = AnsibleModule(
        argument_spec=IPsecCryptoProfileSpec.spec(),
        supports_check_mode=True,
        mutually_exclusive=[
            ["folder", "snippet", "device"],
        ],
        required_one_of=[
            ["folder", "snippet", "device"],
        ],
    )

    # Get parameters
    state = module.params.get("state")
    check_mode = module.check_mode
    
    # Build profile data from module parameters
    try:
        profile_data = build_profile_data(module.params)
    except ValueError as e:
        module.fail_json(msg=str(e))
    
    # Validate that exactly one container type is specified
    if not is_container_specified(profile_data):
        module.fail_json(
            msg="Exactly one container type (folder, snippet, or device) must be specified"
        )
    
    # Validate ESP and AH combinations
    has_esp = "esp" in profile_data
    has_ah = "ah" in profile_data
    
    if state == "present" and not (has_esp or has_ah):
        module.fail_json(
            msg="At least one security protocol (ESP or AH) must be configured when state=present"
        )
        
    if has_esp and has_ah and state == "present":
        # Both are allowed, but warn the user as this is uncommon
        module.warn("Both ESP and AH protocols are configured. This is an uncommon configuration.")
    
    # Get the SCM client
    try:
        client = get_scm_client(module)
    except Exception as e:
        module.fail_json(msg=f"Failed to initialize SCM client: {str(e)}")
    
    # Determine which container parameter was provided
    container = None
    container_value = None
    
    if module.params.get("folder"):
        container = "folder"
        container_value = module.params["folder"]
    elif module.params.get("snippet"):
        container = "snippet"
        container_value = module.params["snippet"]
    elif module.params.get("device"):
        container = "device"
        container_value = module.params["device"]
    
    if not container or not container_value:
        module.fail_json(msg="One of 'folder', 'snippet', or 'device' must be provided")
    
    # Check if profile exists
    exists = False
    existing_profile = None
    
    try:
        # Fetch the profile by name and container
        # Validate client has ipsec_crypto_profile attribute
        if not hasattr(client, 'ipsec_crypto_profile'):
            module.fail_json(msg="SCM client does not have ipsec_crypto_profile service initialized")
        
        profile = client.ipsec_crypto_profile.fetch(
            name=profile_data.get("name"),
            folder=profile_data.get("folder"),
            snippet=profile_data.get("snippet"),
            device=profile_data.get("device"),
        )
        
        if profile:
            exists = True
            existing_profile = profile
    except ObjectNotPresentError:
        # Profile doesn't exist, this is not an error
        exists = False
    except Exception as e:
        module.fail_json(msg=f"Error checking if profile exists: {str(e)}")
    
    result = {
        "changed": False,
        "ipsec_crypto_profile": None,
    }
    
    if state == "present":
        if exists:
            # Check if update is needed
            try:
                update_needed, update_data = needs_update(existing_profile, profile_data)
                
                # Enhanced debugging for idempotence issues
                if existing_profile and hasattr(existing_profile, 'model_dump'):
                    existing_data = existing_profile.model_dump()
                    class UUIDEncoder(json.JSONEncoder):
                        def default(self, obj):
                            if isinstance(obj, uuid.UUID):
                                # Return a string representation of the UUID
                                return str(obj)
                            # Let the base class handle anything else
                            return json.JSONEncoder.default(self, obj)
                    
                    module.debug(f"Existing profile (API): {json.dumps(existing_data, indent=2, sort_keys=True, cls=UUIDEncoder)}")
                    module.debug(f"Requested profile (Module): {json.dumps(profile_data, indent=2, sort_keys=True, cls=UUIDEncoder)}")
                    module.debug(f"Update needed: {update_needed}")
                    
                    # Add specific debugging for known troublesome fields
                    if "esp" in profile_data and "esp" in existing_data:
                        module.debug(f"ESP check: {profile_data['esp']} vs {existing_data['esp']}")
                        if "authentication" in profile_data.get("esp", {}) and "authentication" in existing_data.get("esp", {}):
                            module.debug(f"ESP auth check: {sorted(profile_data['esp']['authentication'])} vs {sorted(existing_data['esp']['authentication'])}")
                        if "encryption" in profile_data.get("esp", {}) and "encryption" in existing_data.get("esp", {}):
                            module.debug(f"ESP enc check: {sorted(profile_data['esp']['encryption'])} vs {sorted(existing_data['esp']['encryption'])}")
                    
                    if "lifetime" in profile_data and "lifetime" in existing_data:
                        module.debug(f"Lifetime check: {profile_data['lifetime']} vs {existing_data['lifetime']}")
                    
                    if "lifesize" in profile_data and "lifesize" in existing_data:
                        module.debug(f"Lifesize check: {profile_data['lifesize']} vs {existing_data['lifesize']}")
                    
                    if "description" in profile_data:
                        module.debug(f"Description in module params: {profile_data['description']}")
                        if "description" in existing_data:
                            module.debug(f"Description in API: {existing_data['description']}")
                        else:
                            module.debug("Description not in API response")
                
                if update_needed:
                    if not check_mode:
                        try:
                            # Create an update model
                            update_model = IPsecCryptoProfileUpdateModel(**update_data)
                            
                            # Validate client has ipsec_crypto_profile attribute
                            if not hasattr(client, 'ipsec_crypto_profile'):
                                module.fail_json(msg="SCM client does not have ipsec_crypto_profile service initialized")
                            
                            # Update the profile
                            updated_profile = client.ipsec_crypto_profile.update(update_model)
                            
                            # Update result
                            result["changed"] = True
                            result["ipsec_crypto_profile"] = serialize_response(updated_profile)
                        except InvalidObjectError as e:
                            module.fail_json(msg=f"Failed to update IPsec crypto profile, invalid data: {str(e)}")
                        except Exception as e:
                            module.fail_json(msg=f"Failed to update IPsec crypto profile: {str(e)}")
                    else:
                        result["changed"] = True
                        result["ipsec_crypto_profile"] = serialize_response(existing_profile)
                else:
                    # No update needed
                    result["ipsec_crypto_profile"] = serialize_response(existing_profile)
            except Exception as e:
                module.fail_json(msg=f"Error determining if update is needed: {str(e)}")
        else:
            # Create new profile
            if not check_mode:
                try:
                    # Validate client has ipsec_crypto_profile attribute
                    if not hasattr(client, 'ipsec_crypto_profile'):
                        module.fail_json(msg="SCM client does not have ipsec_crypto_profile service initialized")
                    
                    # Create the profile
                    created_profile = client.ipsec_crypto_profile.create(profile_data)
                    
                    # Update result
                    result["changed"] = True
                    result["ipsec_crypto_profile"] = serialize_response(created_profile)
                except InvalidObjectError as e:
                    module.fail_json(msg=f"Failed to create IPsec crypto profile, invalid data: {str(e)}")
                except Exception as e:
                    module.fail_json(msg=f"Failed to create IPsec crypto profile: {str(e)}")
            else:
                result["changed"] = True
    
    elif state == "absent":
        if exists:
            if not check_mode:
                try:
                    # Check if client and profile exist
                    if client and existing_profile and hasattr(existing_profile, 'id'):
                        # Validate client has ipsec_crypto_profile attribute
                        if not hasattr(client, 'ipsec_crypto_profile'):
                            module.fail_json(msg="SCM client does not have ipsec_crypto_profile service initialized")
                        
                        # Ensure existing_profile has an id attribute
                        if not hasattr(existing_profile, 'id'):
                            module.fail_json(msg="Profile object does not have an ID attribute")
                        
                        # Delete the profile
                        client.ipsec_crypto_profile.delete(object_id=str(existing_profile.id))
                        
                        # Update result
                        result["changed"] = True
                    else:
                        module.fail_json(msg="Failed to delete IPsec crypto profile: Client or profile is not properly initialized")
                except ObjectNotPresentError:
                    # Object was already deleted, this is not an error
                    result["changed"] = False
                except Exception as e:
                    module.fail_json(msg=f"Failed to delete IPsec crypto profile: {str(e)}")
            else:
                result["changed"] = True
    
    module.exit_json(**result)


if __name__ == "__main__":
    main()