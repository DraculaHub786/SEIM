#!/bin/bash
# SIEM Platform - Unified Launcher (Linux/Mac)
# This script starts MongoDB and the Flask backend which serves the entire application

echo "================================================"
echo "  SIEM Platform - Unified Launcher"
echo "================================================"
echo ""

# Check if MongoDB is installed
echo "[1/3] Checking MongoDB..."
if ! command -v mongod &> /dev/null; then
    echo "      ERROR: MongoDB not found in PATH!"
    echo "      Please install MongoDB first"
    exit 1
fi
echo "      MongoDB found!"

# Check if MongoDB is running
if pgrep -x "mongod" > /dev/null; then
    echo "      MongoDB is already running"
else
    echo "      Starting MongoDB..."
    # Try to start MongoDB in background
    mongod --dbpath /data/db --fork --logpath /var/log/mongodb.log 2>/dev/null || {
        echo "      WARNING: Could not start MongoDB automatically"
        echo "      Please start MongoDB manually in another terminal:"
        echo "      mongod --dbpath /data/db"
        echo ""
        read -p "Press Enter when MongoDB is running..."
    }
fi

echo ""
echo "[2/3] Checking Python dependencies..."
cd backend || exit 1

if ! python3 -c "import flask, flask_socketio, pymongo" 2>/dev/null; then
    echo "      Installing dependencies..."
    pip3 install -r requirements.txt || {
        echo "      ERROR: Failed to install dependencies"
        exit 1
    }
fi
echo "      Dependencies OK!"

echo ""
echo "[3/3] Starting SIEM Platform..."
echo ""
echo "================================================"
echo "  Server starting..."
echo "  Access the dashboard at: http://localhost:5000"
echo "================================================"
echo ""

python3 app.py
