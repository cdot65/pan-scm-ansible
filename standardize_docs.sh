#!/bin/bash
# Script to standardize module documentation based on the golden standard

GOLDEN_STANDARD="docs/collection/modules/wildfire_antivirus_profiles.md"
GOLDEN_STANDARD_INFO="docs/collection/modules/wildfire_antivirus_profiles_info.md"

# Create TOC template from the golden standard
extract_toc() {
  sed -n '/^## Table of Contents/,/^## /p' "$1" | grep -v "^## " > toc_template.txt
}

# Extract TOC from golden standard files
extract_toc "$GOLDEN_STANDARD"

# Process each module doc file
find docs/collection/modules/ -name "*.md" | grep -v "wildfire_antivirus_profiles" | grep -v "index.md" | while read file; do
  echo "Processing: $file"
  is_info_module=false
  
  # Determine if this is an info module
  if [[ "$file" == *"_info.md" ]]; then
    is_info_module=true
    reference_file="$GOLDEN_STANDARD_INFO"
  else
    reference_file="$GOLDEN_STANDARD"
  fi
  
  # Get basic module information
  module_name=$(basename "$file" .md)
  friendly_name=$(echo "$module_name" | sed 's/_info//g' | sed 's/_/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1')
  
  # Create a temporary file
  temp_file="${file}.tmp"
  
  # Format the document title
  if $is_info_module; then
    echo "# $friendly_name Information Object" > "$temp_file"
  else
    echo "# $friendly_name Configuration Object" > "$temp_file"
  fi
  echo "" >> "$temp_file"
  
  # Add standardized TOC if it doesn't exist
  if ! grep -q "^## Table of Contents" "$file"; then
    echo "## Table of Contents" >> "$temp_file"
    echo "" >> "$temp_file"
    
    # Add standard TOC sections based on module type
    if $is_info_module; then
      cat << EOF >> "$temp_file"
1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [Module Parameters](#module-parameters) 
4. [Requirements](#requirements)
5. [Usage Examples](#usage-examples)
6. [Return Values](#return-values)
7. [Error Handling](#error-handling)
8. [Best Practices](#best-practices)
9. [Related Modules](#related-modules)
EOF
    else
      cat << EOF >> "$temp_file"
1. [Overview](#overview)
2. [Core Methods](#core-methods)
3. [Module Parameters](#module-parameters)
4. [Requirements](#requirements)
5. [Usage Examples](#usage-examples)
   - [Creating ${friendly_name}s](#creating-${module_name}s)
   - [Updating ${friendly_name}s](#updating-${module_name}s)
   - [Deleting ${friendly_name}s](#deleting-${module_name}s)
6. [Managing Configuration Changes](#managing-configuration-changes)
7. [Return Values](#return-values)
8. [Error Handling](#error-handling)
9. [Best Practices](#best-practices)
10. [Related Modules](#related-modules)
EOF
    fi
    echo "" >> "$temp_file"
  else
    # Copy existing TOC
    sed -n '/^## Table of Contents/,/^## /p' "$file" | grep -v "^## " >> "$temp_file"
  fi
  
  # Copy content excluding the title and TOC
  if grep -q "^## Table of Contents" "$file"; then
    sed -n '/^## Table of Contents/,$p' "$file" | sed '1,/^## Table of Contents/d' >> "$temp_file"
  else
    # Skip the first line (title) and copy the rest
    sed '1d' "$file" >> "$temp_file"
  fi
  
  # Replace the original file with the temp file
  mv "$temp_file" "$file"
  
  # Ensure all required sections exist
  sections=("Overview" "Core Methods" "Error Handling" "Best Practices" "Related Modules")
  
  # Add more sections for non-info modules
  if ! $is_info_module; then
    sections+=("Managing Configuration Changes")
  fi
  
  # Check and add missing sections
  for section in "${sections[@]}"; do
    if ! grep -q "^## $section" "$file"; then
      echo -e "\n## $section\n" >> "$file"
      echo "Added missing section: $section to $file"
    fi
  done
  
  # Ensure Core Methods table has return types if not present
  if grep -q "^## Core Methods" "$file" && ! grep -q "Return Type" "$file"; then
    # Find Core Methods section and replace the table with a standardized one
    sed -i '' '/^## Core Methods/,/^## /s/| Method.*|/| Method | Description | Parameters | Return Type |/g' "$file"
    # Fix table formatting
    sed -i '' '/^## Core Methods/,/^## /s/|.*|/| ----- | ----------- | ---------- | ---------- |/g' "$file"
  fi
  
  # Fix any remaining style issues
  sed -i '' -e 's/<div class="termy">//g' -e 's/<!-- termynal -->//g' -e 's/<\/div>//g' "$file"
  
  echo "Standardized: $file"
done

# Clean up
rm -f toc_template.txt