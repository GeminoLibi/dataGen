#!/bin/bash

echo "Building Case Generator Executable..."
echo ""

# Install PyInstaller if not already installed
pip install pyinstaller

# Clean previous builds
rm -rf build dist

# Build executable
pyinstaller build_executable.spec

echo ""
echo "Build complete! Executable is in the 'dist' folder."
echo ""

