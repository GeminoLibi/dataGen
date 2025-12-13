@echo off
echo Creating Case Data Generator Installer...
echo.

REM Check if Inno Setup is installed
where iscc >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Inno Setup Compiler (iscc.exe) not found in PATH
    echo.
    echo Please install Inno Setup from: https://jrsoftware.org/isinfo.php
    echo After installation, add it to your PATH or run this script from the Inno Setup directory
    echo.
    pause
    exit /b 1
)

REM Create installer output directory
if not exist installer mkdir installer

REM Compile installer
echo Compiling installer...
iscc create_installer.iss

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Installer created successfully!
    echo Location: installer\CaseDataGenerator-Setup.exe
    echo ========================================
) else (
    echo.
    echo ERROR: Installer compilation failed
)

echo.
pause

