@echo off
echo ========================================
echo Case Data Generator - Build and Installer
echo ========================================
echo.

REM Step 1: Build the executable
echo [1/2] Building executable...
call build.bat
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

REM Step 2: Create installer
echo.
echo [2/2] Creating installer...
call create_installer.bat
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Installer creation failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Complete!
echo ========================================
echo.
echo Files created:
echo   - dist\CaseGenerator.exe (standalone executable)
echo   - installer\CaseDataGenerator-Setup.exe (installer package)
echo.
pause

