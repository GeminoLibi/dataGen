@echo off
echo Building Case Generator Executable...
echo This will show real-time progress...
echo.

REM Install PyInstaller if not already installed
pip install pyinstaller

REM Clean previous builds (safely)
if exist build\build_executable rmdir /s /q build\build_executable
if exist dist\CaseGenerator.exe del /q dist\CaseGenerator.exe
if exist dist\CaseGenerator rmdir /s /q dist\CaseGenerator

echo.
echo ========================================
echo Starting build process...
echo ========================================
echo.

REM Build executable with verbose output
python -m PyInstaller build_executable.spec --clean --log-level=DEBUG 2>&1 | findstr /V /C:"INFO: " /C:"DEBUG: " /C:"WARNING: " | findstr /C:"ERROR" /C:"Building" /C:"completed" /C:"Writing" /C:"Copying"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Build complete! Executable is in the 'dist' folder.
    echo ========================================
) else (
    echo.
    echo ========================================
    echo Build completed (check for errors above)
    echo ========================================
)

echo.
pause

