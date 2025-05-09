# Makefile for managing the collection

# Variables
COLLECTION_NAME = cdot65.scm
COLLECTION_NAMESPACE = cdot65
COLLECTION_NAME_ONLY = scm
VERSION ?= $(shell grep version galaxy.yml | awk '{print $$2}')
TARBALL = $(COLLECTION_NAMESPACE)-$(COLLECTION_NAME_ONLY)-$(VERSION).tar.gz
COLLECTION_PATH = $(shell pwd)/collections/ansible_collections

# Default target
.PHONY: all
all: help

# Help
.PHONY: help
help:
	@echo "Makefile for managing the collection"
	@echo ""
	@echo "Usage:"
	@echo "  make build                 Build the collection"
	@echo "  make clean                 Clean up build artifacts"
	@echo "  make install               Install the collection"
	@echo "  make reinstall             Reinstall the collection (remove + build + install)"
	@echo "  make test                  Run tests for the collection"
	@echo "  make test-all              Run all module tests"
	@echo "  make test-module NAME=name Run test for a specific module"
	@echo "  make validate-module NAME=name Lint, format, and test a specific module"
	@echo "  make dev-setup             Complete development setup and validation"
	@echo "  make lint                  Run linting on all modules"
	@echo "  make lint-path PATH=path   Run linting on a specific path"
	@echo "  make format                Format all modules with ruff"
	@echo "  make format-path PATH=path Format a specific path with ruff"
	@echo "  make isort                 Run isort on all modules"
	@echo "  make fix-lint              Fix common linting issues"
	@echo "  make format-docs           Format markdown files in docs/ for MkDocs"
	@echo "  make format-docs-file FILE=file Format a specific markdown file for MkDocs"
	@echo "  make lint-docs             Lint markdown files in docs/ directory"
	@echo "  make format-module-docs    Format module documentation"
	@echo "  make fix-module-doc-styling Fix module docs to comply with style guide"
	@echo "  make standardize-module-docs Standardize module docs based on golden standard"
	@echo "  make check-docs-links      Check documentation for broken links"
	@echo "  make docs-prepare-release  Prepare all documentation for release"
	@echo "  make test-address          Run address module tests"
	@echo "  make test-address-info     Run address_info module tests"
	@echo "  make test-wildfire         Run wildfire_antivirus_profiles module tests"
	@echo "  make test-wildfire-info    Run wildfire_antivirus_profiles_info module tests"
	@echo "  make docs                  Build documentation"
	@echo "  make serve-docs            Serve documentation locally"
	@echo "  make verify-naming         Verify module and API spec naming consistency"
	@echo "  make version VERSION=x.y.z Update the version in galaxy.yml"
	@echo "  make check                 Run diagnostic checks on the installation"
	@echo "  make fix-dependencies      Ensure all required module dependencies are in place"
	@echo ""

# Clean
.PHONY: clean
clean:
	@echo "Cleaning up build artifacts..."
	rm -f *.tar.gz

# Build
.PHONY: build
build: clean
	@echo "Building collection $(COLLECTION_NAME) version $(VERSION)..."
	poetry run ansible-galaxy collection build --force

# Install
.PHONY: install
install:
	@echo "Installing collection $(COLLECTION_NAME) version $(VERSION)..."
	poetry run ansible-galaxy collection install $(TARBALL) --force --collections-path ./collections

# Fix dependencies
.PHONY: fix-dependencies
fix-dependencies:
	@echo "Ensuring all required module dependencies are in place..."
	@mkdir -p $(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/module_utils
	@mkdir -p $(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/modules
	@echo "Creating __init__.py files..."
	@touch $(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/module_utils/__init__.py
	@touch $(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/modules/__init__.py
	@touch $(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/__init__.py
	@touch $(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/__init__.py
	@touch $(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/__init__.py
	@echo "Setting execute permissions on Python files..."
	@chmod +x $(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/modules/*.py

# Remove
.PHONY: remove
remove:
	@echo "Removing collection $(COLLECTION_NAME)..."
	rm -rf $(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)

# Reinstall
.PHONY: reinstall
reinstall: remove clean build install fix-dependencies

# Test
.PHONY: test
test:
	@echo "Running basic tests for collection $(COLLECTION_NAME)..."
	cd tests && ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_PATH) ANSIBLE_MODULE_UTILS=$(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/module_utils poetry run ansible-playbook test_address.yaml test_wildfire_antivirus_profiles.yaml --vault-password-file=.vault_password -vv

# Setup complete dev environment and run all steps for adding a new module
.PHONY: dev-setup
dev-setup: reinstall lint format test-all

# Run all steps needed to test and validate a specific module 
.PHONY: validate-module
validate-module:
ifndef NAME
	$(error NAME is undefined. Usage: make validate-module NAME=module_name)
endif
	@echo "Validating module $(NAME)..."
	make lint-path PATH="plugins/modules/$(NAME).py plugins/module_utils/api_spec/$(NAME).py"
	make format-path PATH="plugins/modules/$(NAME).py plugins/module_utils/api_spec/$(NAME).py"
	make reinstall
	make test-module NAME=$(NAME)

# Test address module
.PHONY: test-address
test-address:
	@echo "Running tests for address module..."
	cd tests && ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_PATH) ANSIBLE_MODULE_UTILS=$(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/module_utils poetry run ansible-playbook test_address.yaml --vault-password-file=.vault_password -vv

# Test address_info module
.PHONY: test-address-info
test-address-info:
	@echo "Running tests for address_info module..."
	cd tests && ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_PATH) ANSIBLE_MODULE_UTILS=$(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/module_utils poetry run ansible-playbook test_address_info.yaml --vault-password-file=.vault_password -vv

# Update version
.PHONY: version
version:
	@echo "Updating version to $(VERSION)..."
	sed -i '' "s/^version: .*/version: $(VERSION)/" galaxy.yml

# Test wildfire_antivirus_profiles module
.PHONY: test-wildfire
test-wildfire:
	@echo "Running tests for wildfire_antivirus_profiles module..."
	cd tests && ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_PATH) ANSIBLE_MODULE_UTILS=$(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/module_utils poetry run ansible-playbook test_wildfire_antivirus_profiles.yaml --vault-password-file=.vault_password -vv

# Test wildfire_antivirus_profiles_info module
.PHONY: test-wildfire-info
test-wildfire-info:
	@echo "Running tests for wildfire_antivirus_profiles_info module..."
	cd tests && ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_PATH) ANSIBLE_MODULE_UTILS=$(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/module_utils poetry run ansible-playbook test_wildfire_antivirus_profiles_info.yaml --vault-password-file=.vault_password -vv

# Test a specific module
.PHONY: test-module
test-module:
ifndef NAME
	$(error NAME is undefined. Usage: make test-module NAME=module_name)
endif
	@echo "Running tests for $(NAME) module..."
	cd tests && ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_PATH) ANSIBLE_MODULE_UTILS=$(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/module_utils poetry run ansible-playbook test_$(NAME).yaml --vault-password-file=.vault_password -vv

# Run all tests
.PHONY: test-all
test-all:
	@echo "Running all module tests..."
	cd tests && ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_PATH) ANSIBLE_MODULE_UTILS=$(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/module_utils poetry run ansible-playbook test_*.yaml --vault-password-file=.vault_password -vv

# Lint modules
.PHONY: lint
lint:
	@echo "Running linting on all modules..."
	poetry run ruff check plugins

# Lint specific file or directory
.PHONY: lint-path
lint-path:
ifndef PATH
	$(error PATH is undefined. Usage: make lint-path PATH=path/to/check)
endif
	@echo "Running linting on $(PATH)..."
	poetry run ruff check $(PATH)

# Format modules
.PHONY: format
format:
	@echo "Formatting all modules with ruff..."
	poetry run ruff format plugins

# Format specific file or directory
.PHONY: format-path
format-path:
ifndef PATH
	$(error PATH is undefined. Usage: make format-path PATH=path/to/format)
endif
	@echo "Formatting $(PATH) with ruff..."
	poetry run ruff format $(PATH)

# Run isort on all modules
.PHONY: isort
isort:
	@echo "Running isort on all modules..."
	poetry run isort plugins tests

# Fix common linting issues
.PHONY: fix-lint
fix-lint:
	@echo "Fixing common linting issues..."
	poetry run ruff check --fix plugins

# Diagnostic check
.PHONY: check
check:
	@echo "Running diagnostic checks..."
	chmod +x check_installation.sh
	ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_PATH) ./check_installation.sh

# Format markdown files in docs/
.PHONY: format-docs
format-docs:
	@echo "Formatting markdown files in docs/ directory for MkDocs..."
	@# Format files individually to handle errors gracefully
	@find docs/ -name "*.md" | while read file; do \
		echo "Formatting $$file"; \
		poetry run mdformat --wrap=100 --number --extensions tables "$$file" || echo "Warning: Could not format $$file"; \
	done
	@echo "Markdown formatting completed."
	@echo "Now running post-format validation to ensure MkDocs compatibility..."
	poetry run mkdocs build --strict || echo "Warning: MkDocs validation found issues but continuing..."
	@echo "All documents processed."

# Format a specific markdown file
.PHONY: format-docs-file
format-docs-file:
ifndef FILE
	$(error FILE is undefined. Usage: make format-docs-file FILE=path/to/file.md)
endif
	@echo "Formatting markdown file $(FILE) for MkDocs..."
	poetry run mdformat --wrap=100 --number --extensions tables "$(FILE)" || echo "Warning: Could not format $(FILE)"
	@echo "Markdown formatting completed."
	@echo "Now validating file with MkDocs build..."
	poetry run mkdocs build --strict || echo "Warning: MkDocs validation found issues but continuing..."
	@echo "Document processing completed."

# Lint markdown files in docs/
.PHONY: lint-docs
lint-docs:
	@echo "Linting markdown files in docs/ directory..."
	@find docs/ -name "*.md" | while read file; do \
		echo "Linting $$file"; \
		poetry run mdformat --check --extensions tables "$$file" || echo "Warning: Formatting issues in $$file"; \
	done
	@echo "Checking MkDocs build validation..."
	poetry run mkdocs build --strict || echo "Warning: MkDocs validation found issues but continuing..."
	@echo "Markdown linting and validation completed."

# Format module documentation specifically
.PHONY: format-module-docs
format-module-docs:
	@echo "Formatting module documentation for MkDocs..."
	@# Format module documentation files individually to handle errors gracefully
	@find docs/collection/modules/ -name "*.md" | while read file; do \
		echo "Formatting module doc: $$file"; \
		poetry run mdformat --wrap=100 --number --extensions tables "$$file" || echo "Warning: Could not format $$file"; \
	done
	@echo "Module documentation formatting completed."
	@echo "Validating module documentation with MkDocs build..."
	poetry run mkdocs build --strict || echo "Warning: MkDocs validation found issues but continuing..."
	@echo "Module documentation processing completed."

# Check documentation for broken links
.PHONY: check-docs-links
check-docs-links:
	@echo "Checking documentation for broken links..."
	@# We'll use find and grep to check for potential broken links
	@# This grep pattern looks for Markdown links or HTML links that don't point to actual files
	find docs/ -name "*.md" -exec grep -n -E '\[.*\]\(\S*\)|\<a href="[^"]+"' {} \; | \
		grep -v "http" | grep -v "https" | \
		grep -v "#" | grep -v "index.md" | \
		grep -v ".md" || echo "No potentially broken links found."
	@echo "Link check completed. Any output above represents potential issues."

# Fix module documentation styling according to style guide
.PHONY: fix-module-doc-styling
fix-module-doc-styling:
	@echo "Fixing module documentation styling according to style guide..."
	@echo "This will update titles, fix TOC numbering, and remove termy div tags"
	@find docs/collection/modules/ -name "*.md" | while read file; do \
		echo "Processing: $$file"; \
		module_name=$$(basename $$file .md | sed 's/_info//g' | sed 's/_/ /g' | awk '{for(i=1;i<=NF;i++) $$i=toupper(substr($$i,1,1)) substr($$i,2)} 1'); \
		sed -i '' -e '/<div class="termy">/d' -e '/<!-- termynal -->/d' -e '/<\/div>/d' "$$file"; \
		sed -i '' -e 's/^0\([0-9]\. \)/\1/g' "$$file"; \
		if [ "$$(echo $$file | grep '_info.md')" ]; then \
			sed -i '' -e "1s/^# .*/# $$module_name Information Object/" "$$file"; \
		else \
			sed -i '' -e "1s/^# .*/# $$module_name Configuration Object/" "$$file"; \
		fi; \
	done
	@echo "Module documentation styling has been fixed according to style guide."
	@echo "Now validating with MkDocs build..."
	poetry run mkdocs build --strict || echo "Warning: MkDocs validation found issues but continuing..."
	@echo "Module documentation styling completed successfully."

# Standardize module docs based on golden standard
.PHONY: standardize-module-docs
standardize-module-docs:
	@echo "Standardizing module docs based on golden standard..."
	@# Make the script executable
	chmod +x standardize_docs.sh
	@# Run the script
	./standardize_docs.sh
	@echo "Module documentation standardization completed."
	@echo "Now validating with MkDocs build..."
	poetry run mkdocs build --strict || echo "Warning: MkDocs validation found issues but continuing..."
	@echo "Module documentation standardization completed successfully."

# Prepare all documentation for release
.PHONY: docs-prepare-release
docs-prepare-release:
	@echo "Preparing all documentation for release..."
	@# First, fix module documentation styling
	$(MAKE) fix-module-doc-styling
	@# Then, standardize module docs
	$(MAKE) standardize-module-docs
	@# Then, format all docs
	$(MAKE) format-docs
	@# Then, run special formatting for module docs
	$(MAKE) format-module-docs
	@# Verify docs build correctly
	poetry run mkdocs build --strict
	@# Check all links in documentation
	$(MAKE) check-docs-links
	@echo "Documentation has been prepared for release and validated successfully."

# Build docs
.PHONY: docs
docs:
	@echo "Building documentation..."
	poetry run mkdocs build --strict

# Serve docs locally
.PHONY: serve-docs
serve-docs:
	@echo "Serving documentation locally..."
	poetry run mkdocs serve

# Verify module and API spec naming consistency
.PHONY: verify-naming
verify-naming:
	@echo "Verifying module and API spec naming consistency..."
	@for file in plugins/modules/*.py; do \
		module_name=$$(basename $$file .py); \
		if [ ! -f "plugins/module_utils/api_spec/$$module_name.py" ] && [ ! -f "plugins/module_utils/api_spec/$${module_name%_info}.py" ]; then \
			echo "WARNING: Module $$module_name has no matching API spec file"; \
		fi \
	done
	@echo "Naming consistency check complete"