#!/bin/bash

INIT_FILE="src/cli_scheduler/__init__.py"

# Extract the version from the first line of __init__.py
version=$(grep -m 1 "__version__" "$INIT_FILE" | awk -F'"' '{print $2}')

# Check if version exists on PyPI
PACKAGE_NAME="python-cli-scheduler"

version_exists=$(curl -s "https://pypi.org/pypi/${PACKAGE_NAME}/json" | grep "\"${version}\"")

if [[ -n "$version_exists" ]]; then
    echo "Error: Version ${version} of ${PACKAGE_NAME} already exists on PyPI."
    exit 1
fi

echo "Version: $version"

# Setup
python3 -m pip install build twine

# Clear dist
rm -rf dist/
echo "Clear dist"

# Build package
python3 -m build

# Confirm package build
twine check dist/*

# Upload package
twine upload dist/*

# Remove built package
rm -rf dist/
