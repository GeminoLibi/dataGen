@echo off
echo Testing CaseGenerator.exe...
echo.

if not exist dist\CaseGenerator.exe (
    echo ERROR: CaseGenerator.exe not found!
    echo Please run build.bat first.
    pause
    exit /b 1
)

echo Starting CaseGenerator.exe...
echo The application should open a browser window at http://localhost:5000
echo.
echo If it doesn't open automatically, navigate to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

cd dist
start CaseGenerator.exe

timeout /t 3 /nobreak >nul

echo.
echo Attempting to open browser...
start http://localhost:5000

echo.
echo Server is running. Check the console window for any errors.
echo Press any key to stop the server and exit...
pause >nul

taskkill /F /IM CaseGenerator.exe >nul 2>&1

