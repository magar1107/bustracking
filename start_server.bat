@echo off
title Bus Tracking System - Local Server

echo.
echo ========================================
echo    Bus Tracking System - Web Server
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6 or later from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "index.html" (
    echo ERROR: index.html not found
    echo Please run this script from the web_app directory
    echo.
    pause
    exit /b 1
)

echo Starting local web server...
echo.
echo Available at: http://localhost:8080
echo.
echo Instructions:
echo 1. The browser should open automatically
echo 2. Use test_data_generator.html to simulate bus data
echo 3. View real-time tracking on index.html
echo 4. Press Ctrl+C to stop the server
echo.

REM Start the Python server
python start_server.py

echo.
echo Server stopped.
pause
