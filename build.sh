#!/bin/bash

echo "Building Case Generator Executable..."
echo ""

# Install PyInstaller if not already installed
pip install pyinstaller

# Clean previous builds
rm -rf build dist

# Build executable (with real-time output)
python -m PyInstaller build_executable.spec --clean --log-level=INFO

echo ""
echo "Build complete! Executable is in the 'dist' folder."
echo ""

