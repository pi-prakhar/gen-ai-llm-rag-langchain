SHELL := /bin/bash
VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
ACTIVATE := source $(VENV_DIR)/bin/activate

# Check if inside virtual environment
define CHECK_VENV
	@if [ -z "$$VIRTUAL_ENV" ]; then \
		echo "❌ Not inside virtual environment!"; \
		exit 1; \
	else \
		echo "✅ Inside virtual environment"; \
	fi
endef

.PHONY: all venv enter exit check setup run install test

# Create virtual environment if not exists
venv:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment..."; \
		python3 -m venv $(VENV_DIR); \
	fi

# Enter virtual environment (Run this manually as Makefile can't keep shell state)
enter:
	@echo "Run the following command to enter the virtual environment:"
	@echo "source $(VENV_DIR)/bin/activate"

# Exit virtual environment (Run this manually as well)
exit:
	@echo "Run the following command to exit the virtual environment:"
	@echo "deactivate"

# Check if inside virtual environment
check:
	$(call CHECK_VENV)

# Setup command to run necessary scripts
setup: venv
	$(call CHECK_VENV)
	$(PYTHON) create_db.py
	$(PYTHON) rag_pipeline.py

# Run the main script
run: venv
	$(call CHECK_VENV)
	$(PYTHON) main.py

# Install requirements (only if inside venv)
install: venv
	$(call CHECK_VENV)
	$(PIP) install -r requirements.txt

