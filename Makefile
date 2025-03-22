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
	@echo "  make build              Build the collection"
	@echo "  make clean              Clean up build artifacts"
	@echo "  make install            Install the collection"
	@echo "  make reinstall          Reinstall the collection (remove + build + install)"
	@echo "  make test               Run tests for the collection"
	@echo "  make test-address       Run address module tests"
	@echo "  make test-address-info  Run address_info module tests"
	@echo "  make version VERSION=x.y.z  Update the version in galaxy.yml"
	@echo "  make check              Run diagnostic checks on the installation"
	@echo "  make fix-dependencies   Ensure all required module dependencies are in place"
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
	ansible-galaxy collection build --force

# Install
.PHONY: install
install:
	@echo "Installing collection $(COLLECTION_NAME) version $(VERSION)..."
	ansible-galaxy collection install $(TARBALL) --force --collections-path ./collections

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
	@echo "Running tests for collection $(COLLECTION_NAME)..."
	cd tests && ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_PATH) ANSIBLE_MODULE_UTILS=$(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/module_utils ansible-playbook test_address.yaml --vault-password-file=.vault_password -vv

# Test address module
.PHONY: test-address
test-address:
	@echo "Running tests for address module..."
	cd tests && ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_PATH) ANSIBLE_MODULE_UTILS=$(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/module_utils ansible-playbook test_address.yaml --vault-password-file=.vault_password -vv

# Test address_info module
.PHONY: test-address-info
test-address-info:
	@echo "Running tests for address_info module..."
	cd tests && ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_PATH) ANSIBLE_MODULE_UTILS=$(COLLECTION_PATH)/$(COLLECTION_NAMESPACE)/$(COLLECTION_NAME_ONLY)/plugins/module_utils ansible-playbook test_address_info.yaml --vault-password-file=.vault_password -vv

# Update version
.PHONY: version
version:
	@echo "Updating version to $(VERSION)..."
	sed -i '' "s/^version: .*/version: $(VERSION)/" galaxy.yml

# Diagnostic check
.PHONY: check
check:
	@echo "Running diagnostic checks..."
	chmod +x check_installation.sh
	ANSIBLE_COLLECTIONS_PATH=$(COLLECTION_PATH) ./check_installation.sh
