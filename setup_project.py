"""
SIEM Platform - Complete Setup Script
This script creates the entire project structure and all necessary files
"""

import os
import json

# Base directory
BASE_DIR = r"c:\Users\afjal\Documents\Mini-Projects\SEIM"

# Directory structure
DIRECTORIES = [
    "backend",
    "backend/config",
    "backend/models",
    "backend/controllers",
    "backend/routes",
    "backend/services",
    "backend/database",
    "backend/utils",
    "frontend",
    "frontend/css",
    "frontend/js",
    "frontend/assets",
    "frontend/assets/images",
    "database",
    "tests",
    "logs"
]

def create_directories():
    """Create all project directories"""
    print("📁 Creating project directories...")
    for directory in DIRECTORIES:
        dir_path = os.path.join(BASE_DIR, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"   ✓ {directory}")
    print()

def create_file(filepath, content):
    """Create a file with content"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def setup_backend_files():
    """Create all backend files"""
    print("🐍 Creating backend files...")
    
    # requirements.txt
    requirements = """flask==3.0.0
flask-socketio==5.3.5
flask-cors==4.0.0
pymongo==4.6.1
python-socketio==5.10.0
python-dotenv==1.0.0
bcrypt==4.1.2
redis==5.0.1
apscheduler==3.10.4
eventlet==0.35.1
"""
    create_file(os.path.join(BASE_DIR, "backend", "requirements.txt"), requirements)
    print("   ✓ requirements.txt")
    
    # .env.example
    env_example = """# Environment Configuration
SECRET_KEY=your-secret-key-here-change-this
DEBUG=True
HOST=0.0.0.0
PORT=5000

# MongoDB Settings
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=siem_db

# Redis Settings (Optional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_ENABLED=False

# Socket.IO Settings
SOCKETIO_CORS_ALLOWED_ORIGINS=*

# Detection Engine Settings
DETECTION_INTERVAL=30
FAILED_LOGIN_THRESHOLD=10
FAILED_LOGIN_TIME_WINDOW=120

# Data Retention
LOG_TTL_DAYS=90

# Pagination
DEFAULT_PAGE_SIZE=100
MAX_PAGE_SIZE=1000
"""
    create_file(os.path.join(BASE_DIR, "backend", ".env.example"), env_example)
    print("   ✓ .env.example")
    
    # __init__.py files
    init_dirs = ["backend", "backend/config", "backend/models", "backend/controllers", 
                 "backend/routes", "backend/services", "backend/database", "backend/utils"]
    for dir_name in init_dirs:
        create_file(os.path.join(BASE_DIR, dir_name, "__init__.py"), "")
    print("   ✓ __init__.py files")
    
    print()

def create_placeholder_files():
    """Create placeholder files for directories"""
    print("📄 Creating placeholder files...")
    
    placeholders = [
        "frontend/assets/.gitkeep",
        "logs/.gitkeep",
        "tests/.gitkeep"
    ]
    
    for placeholder in placeholders:
        create_file(os.path.join(BASE_DIR, placeholder), "")
    print("   ✓ Placeholders created")
    print()

def main():
    """Main setup function"""
    print("=" * 60)
    print("🚀 SIEM Platform - Project Setup")
    print("=" * 60)
    print()
    
    create_directories()
    setup_backend_files()
    create_placeholder_files()
    
    print("=" * 60)
    print("✅ Project structure created successfully!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. cd backend")
    print("2. Copy .env.example to .env and configure")
    print("3. pip install -r requirements.txt")
    print("4. python app.py")
    print()

if __name__ == "__main__":
    main()
