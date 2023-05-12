#!/bin/bash

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
