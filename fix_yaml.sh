#!/bin/bash
# Script to fix common YAML issues
# 1. Remove trailing whitespace
# 2. Ensure files end with a newline

set -e

# Navigate to the project root
cd "$(dirname "$0")"

# Find all yaml files and fix them
find ./tests -name "*.yaml" -type f | while read -r file; do
  echo "Fixing $file"
  
  # Fix trailing whitespace
  sed -i '' 's/[[:space:]]*$//' "$file"
  
  # Ensure file ends with a newline
  if [ "$(tail -c1 "$file" | wc -l)" -eq 0 ]; then
    echo "" >> "$file"
  fi
done

# Make sure the .yamllint file also ends with a newline
if [ "$(tail -c1 .yamllint | wc -l)" -eq 0 ]; then
  echo "" >> .yamllint
fi

echo "All YAML files have been fixed."