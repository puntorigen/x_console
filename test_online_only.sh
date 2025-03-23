#!/bin/bash
# This script creates a virtual environment, installs only online translation dependencies,
# and runs the test script to verify it works

echo "Creating test environment for online-only translation..."
python -m venv test_env_online
source test_env_online/bin/activate

echo "Installing x_console with online-only dependencies..."
pip install -e ".[online]"

echo "Running test script..."
python test_dependencies.py

echo "Deactivating virtual environment..."
deactivate
