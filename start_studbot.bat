@echo off
title StudBot - AI Learning Companion
color 0A

echo.
echo ================================================
echo    STUDBOT - AI Learning Companion
echo ================================================
echo.
echo Starting StudBot application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    echo.
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "app.py" (
    echo ERROR: app.py not found
    echo Please make sure you're in the correct directory
    echo.
    pause
    exit /b 1
)

if not exist "index.html" (
    echo ERROR: index.html not found
    echo Please make sure you're in the correct directory
    echo.
    pause
    exit /b 1
)

REM Install requirements if needed
if exist "requirements.txt" (
    echo Installing Python dependencies...
    pip install -r requirements.txt
    echo.
)

REM Start the application
echo Starting StudBot server...
echo The application will open in your default browser.
echo Press Ctrl+C to stop the server.
echo.
echo ================================================
echo.

python start.py

echo.
echo StudBot has been stopped.
echo Thank you for using StudBot!
echo.
pause
