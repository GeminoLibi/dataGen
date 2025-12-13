@echo off
echo Building Case Generator Executable...
echo This may take a few minutes - output will stream below...
echo.

REM Install PyInstaller if not already installed
pip install pyinstaller

REM Clean previous builds (safely)
if exist build\build_executable rmdir /s /q build\build_executable
if exist dist\CaseGenerator.exe del /q dist\CaseGenerator.exe
if exist dist\CaseGenerator rmdir /s /q dist\CaseGenerator

REM Build executable (with real-time output)
python -m PyInstaller build_executable.spec --clean --log-level=INFO

echo.
echo Build complete! Executable is in the 'dist' folder.
echo.
pause

