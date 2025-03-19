.PHONY: setup lint format test clean install-hooks docs docs-serve sanity-tests integration-tests ansible-lint help format-all

# Default goal
.DEFAULT_GOAL := help

# Install poetry dependencies
setup:
	@echo "Installing dependencies..."
	poetry install
	@echo "Installing pre-commit hooks..."
	poetry run pre-commit install

# Run linting with ruff
lint:
	@echo "Running linting checks..."
	poetry run ruff check pan_scm_ansible tests
	@echo "Running ansible-lint..."
	poetry run ansible-lint

# Run formatting with ruff
format:
	@echo "Running code formatter..."
	poetry run ruff format pan_scm_ansible tests
	@echo "Running isort..."
	poetry run isort pan_scm_ansible tests

# Format all files and ignore exit code (for CI)
format-all:
	@echo "Formatting all files..."
	-poetry run pre-commit run ruff-format --all-files
	-poetry run pre-commit run isort --all-files

# Check and auto-fix with ruff
fix:
	@echo "Auto-fixing linting issues..."
	poetry run ruff check --fix pan_scm_ansible tests

# Run both linting and formatting
lint-format: format lint

# Run tests
test:
	@echo "Running tests..."
	poetry run pytest

# Run tests with coverage
test-cov:
	@echo "Running tests with coverage..."
	poetry run pytest --cov=pan_scm_ansible tests/

# Clean caches
clean:
	@echo "Cleaning cache directories..."
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Install pre-commit hooks
install-hooks:
	@echo "Installing pre-commit hooks..."
	poetry run pre-commit install

# Update all hooks to the latest version
update-hooks:
	@echo "Updating pre-commit hooks..."
	poetry run pre-commit autoupdate

# Run pre-commit on all files
pre-commit-all:
	@echo "Running pre-commit on all files..."
	@echo "NOTE: Formatters may modify files and exit with non-zero, this is normal"
	@echo "Use 'make format-all && make lint-check' for CI environments"
	poetry run pre-commit run --all-files || echo "Formatters modified files, run again to verify"

# Only run lint checks (no formatters)
lint-check:
	@echo "Running only lint checks (no formatters)..."
	poetry run pre-commit run --all-files --hook-stage manual

# Build documentation
docs:
	@echo "Building documentation site..."
	poetry run mkdocs build --strict --no-directory-urls

# Serve documentation locally
docs-serve:
	@echo "Starting documentation server..."
	poetry run mkdocs serve

# Run Ansible sanity tests
sanity-tests:
	@echo "Running Ansible sanity tests..."
	poetry run ansible-test sanity

# Run Ansible integration tests
integration-tests:
	@echo "Running Ansible integration tests..."
	poetry run ansible-test integration

# Run Ansible linting
ansible-lint:
	@echo "Running ansible-lint..."
	poetry run ansible-lint

help:
	@echo "Available commands:"
	@echo "  setup               - Install dependencies and pre-commit hooks"
	@echo "  lint                - Run linting checks with ruff and ansible-lint"
	@echo "  format              - Format code with ruff and isort"
	@echo "  format-all          - Format all files (ignores errors)"
	@echo "  fix                 - Auto-fix linting issues with ruff"
	@echo "  lint-format         - Run both linting and formatting"
	@echo "  lint-check          - Run only lint checks (no formatters)"
	@echo "  test                - Run tests"
	@echo "  test-cov            - Run tests with coverage"
	@echo "  clean               - Clean cache directories"
	@echo "  docs                - Build documentation site (with strict validation)"
	@echo "  docs-serve          - Serve documentation locally for development"
	@echo "  install-hooks       - Install pre-commit hooks"
	@echo "  update-hooks        - Update pre-commit hooks to the latest versions"
	@echo "  pre-commit-all      - Run pre-commit on all files"
	@echo "  sanity-tests        - Run Ansible sanity tests"
	@echo "  integration-tests   - Run Ansible integration tests"
	@echo "  ansible-lint        - Run ansible-lint"