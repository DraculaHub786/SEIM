@echo off
REM SIEM Platform - Unified Launcher (Windows)
REM This script starts MongoDB and the Flask backend which serves the entire application

echo ================================================
echo   SIEM Platform - Unified Launcher
echo ================================================
echo.

REM Check if MongoDB is running
echo [1/3] Checking MongoDB...
mongod --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: MongoDB not found in PATH!
    echo Please install MongoDB or add it to PATH
    echo.
    pause
    exit /b 1
)
echo       MongoDB found!

REM Check if MongoDB is already running
netstat -an | find "27017" | find "LISTENING" >nul
if %errorlevel% equ 0 (
    echo       MongoDB is already running
) else (
    echo       Starting MongoDB service...
    net start MongoDB >nul 2>&1
    if %errorlevel% neq 0 (
        echo       WARNING: Could not start MongoDB service
        echo       Please start MongoDB manually: mongod --dbpath C:\data\db
        echo.
        pause
        exit /b 1
    )
)

echo.
echo [2/3] Checking Python dependencies...
cd backend
python -c "import flask, flask_socketio, pymongo" >nul 2>&1
if %errorlevel% neq 0 (
    echo       Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo       ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)
echo       Dependencies OK!

echo.
echo [3/3] Starting SIEM Platform...
echo.
echo ================================================
echo   Server starting...
echo   Access the dashboard at: http://localhost:5000
echo ================================================
echo.

python app.py

pause
