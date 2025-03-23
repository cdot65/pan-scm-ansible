#!/bin/bash

# Script to help diagnose collection installation issues

# Get collection paths
collection_paths=$(ansible-config dump | grep COLLECTIONS_PATHS | cut -d'=' -f2 | tr -d '[] ' | tr ',' '\n')

# Check each path
for path in $collection_paths; do
    echo "Checking collection path: $path"
    
    # Remove leading and trailing quotes if present
    path=$(echo $path | sed 's/^"\(.*\)"$/\1/')
    
    # Check if cdot65.scm collection exists
    if [ -d "$path/ansible_collections/cdot65/scm" ]; then
        echo "✅ Found cdot65.scm collection at: $path/ansible_collections/cdot65/scm"
        
        # Check modules
        if [ -d "$path/ansible_collections/cdot65/scm/plugins/modules" ]; then
            echo "📂 Modules directory exists"
            
            # List all modules
            echo "📝 Available modules:"
            ls -la "$path/ansible_collections/cdot65/scm/plugins/modules/" | grep -v "__pycache__" | grep "\.py$"
            
            # Check for address.py and address_info.py
            if [ -f "$path/ansible_collections/cdot65/scm/plugins/modules/address.py" ]; then
                echo "✅ address.py module found"
            else
                echo "❌ address.py module NOT found"
            fi
            
            if [ -f "$path/ansible_collections/cdot65/scm/plugins/modules/address_info.py" ]; then
                echo "✅ address_info.py module found"
            else
                echo "❌ address_info.py module NOT found"
            fi
        else
            echo "❌ Modules directory NOT found"
        fi
    else
        echo "❌ cdot65.scm collection NOT found at this path"
    fi
    
    echo ""
done

# Try to get address_info module documentation
echo "Trying to get address_info module documentation:"
ansible-doc -t module cdot65.scm.address_info 2>/dev/null

if [ $? -ne 0 ]; then
    echo "❌ Could not retrieve documentation for cdot65.scm.address_info"
else
    echo "✅ Successfully retrieved documentation for cdot65.scm.address_info"
fi

echo ""
echo "Collection version from galaxy.yml:"
grep "version:" galaxy.yml

echo ""
echo "Available collection tarballs:"
ls -la cdot65-scm-*.tar.gz
