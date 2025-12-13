@echo off
echo Building Case Generator Executable...
echo.

REM Install PyInstaller if not already installed
pip install pyinstaller

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build executable
pyinstaller build_executable.spec

echo.
echo Build complete! Executable is in the 'dist' folder.
echo.
pause

