@echo off
REM MongoDB Setup and Connection Helper for SIEM Platform
echo ============================================================
echo    MongoDB Setup Helper - SIEM Platform
echo ============================================================
echo.

:MENU
echo Please choose an option:
echo.
echo [1] Check MongoDB Status
echo [2] Start MongoDB Service
echo [3] Stop MongoDB Service
echo [4] Test MongoDB Connection
echo [5] Open MongoDB Compass (Connection String)
echo [6] Install Python Dependencies
echo [7] Run SIEM Application
echo [8] View MongoDB Connection String
echo [9] Exit
echo.
set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto CHECK_STATUS
if "%choice%"=="2" goto START_SERVICE
if "%choice%"=="3" goto STOP_SERVICE
if "%choice%"=="4" goto TEST_CONNECTION
if "%choice%"=="5" goto COMPASS_STRING
if "%choice%"=="6" goto INSTALL_DEPS
if "%choice%"=="7" goto RUN_APP
if "%choice%"=="8" goto SHOW_STRING
if "%choice%"=="9" goto EXIT
goto MENU

:CHECK_STATUS
echo.
echo Checking MongoDB service status...
sc query MongoDB
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ MongoDB service found!
) else (
    echo.
    echo ✗ MongoDB service not found. Is MongoDB installed?
)
echo.
pause
goto MENU

:START_SERVICE
echo.
echo Starting MongoDB service...
net start MongoDB
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ MongoDB service started successfully!
) else (
    echo.
    echo ✗ Failed to start MongoDB service.
    echo   Try running this script as Administrator.
)
echo.
pause
goto MENU

:STOP_SERVICE
echo.
echo Stopping MongoDB service...
net stop MongoDB
echo.
pause
goto MENU

:TEST_CONNECTION
echo.
echo Testing MongoDB connection...
echo.
mongosh --eval "db.adminCommand('ping')" 2>NUL
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ MongoDB is running and accepting connections!
) else (
    echo.
    echo ✗ Cannot connect to MongoDB.
    echo   Make sure MongoDB service is running.
)
echo.
pause
goto MENU

:COMPASS_STRING
echo.
echo ============================================================
echo   MongoDB Compass Connection String
echo ============================================================
echo.
echo   mongodb://localhost:27017/
echo.
echo ============================================================
echo.
echo Copy the above connection string and paste it into
echo MongoDB Compass to connect to your SIEM database.
echo.
echo Database Name: siem_db
echo.
pause
goto MENU

:INSTALL_DEPS
echo.
echo Installing Python dependencies...
cd backend
pip install -r requirements.txt
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✓ Dependencies installed successfully!
) else (
    echo.
    echo ✗ Failed to install dependencies.
)
cd ..
echo.
pause
goto MENU

:RUN_APP
echo.
echo ============================================================
echo   Starting SIEM Application
echo ============================================================
echo.
cd backend
python app.py
cd ..
pause
goto MENU

:SHOW_STRING
echo.
echo ============================================================
echo   MongoDB Configuration for SIEM
echo ============================================================
echo.
echo   Connection String: mongodb://localhost:27017/
echo   Database Name:     siem_db
echo   Port:              27017
echo.
echo   Collections:
echo     - logs    (Security event logs with TTL)
echo     - alerts  (Security alerts)
echo     - users   (User accounts)
echo.
echo   Default Admin Account:
echo     Username: admin
echo     Password: admin123
echo.
echo ============================================================
echo.
pause
goto MENU

:EXIT
echo.
echo Goodbye!
exit /b 0
