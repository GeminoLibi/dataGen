# Releases

This folder contains compiled executables for distribution.

## Current Release

- **CaseGenerator-v1.0.0.exe** - Initial release
  - Standalone executable (no Python required)
  - Includes all dependencies
  - Console window enabled for debugging
  - Auto-opens browser to web interface

## Installation

Simply download and run the `.exe` file. No installation required.

## System Requirements

- Windows 10 or later
- No additional dependencies needed

## Usage

1. Double-click `CaseGenerator-v1.0.0.exe`
2. A console window will open showing server status
3. Browser should automatically open to `http://localhost:5000`
4. If browser doesn't open, manually navigate to `http://localhost:5000`

## Troubleshooting

- If Windows shows a security warning, click "More info" then "Run anyway" (executable is unsigned)
- If antivirus flags it, add an exception (false positive with PyInstaller executables)
- Check the console window for error messages

