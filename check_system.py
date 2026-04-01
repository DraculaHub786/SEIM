#!/usr/bin/env python3
"""
SIEM Platform - Startup Script
Quick start script to verify system setup
"""

import sys
import subprocess
import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python():
    """Check Python version"""
    print("✓ Checking Python version...")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠️  Warning: Python 3.8+ recommended")
        return False
    return True

def check_mongodb():
    """Check if MongoDB is installed"""
    print("\n✓ Checking MongoDB...")
    try:
        result = subprocess.run(['mongod', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  {version_line}")
            return True
        else:
            print("  ⚠️  MongoDB not found")
            return False
    except FileNotFoundError:
        print("  ⚠️  MongoDB not found in PATH")
        return False
    except Exception as e:
        print(f"  ⚠️  Error checking MongoDB: {e}")
        return False

def check_dependencies():
    """Check if Python dependencies are installed"""
    print("\n✓ Checking Python dependencies...")
    required = ['flask', 'flask_socketio', 'flask_cors', 'pymongo', 
                'python-dotenv', 'apscheduler', 'bcrypt']
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} (missing)")
            missing.append(package)
    
    if missing:
        print(f"\n  To install missing packages:")
        print(f"  cd backend && pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Check if .env file exists"""
    print("\n✓ Checking environment configuration...")
    env_path = Path('backend/.env')
    env_example_path = Path('backend/.env.example')
    
    if env_path.exists():
        print("  ✓ .env file found")
        return True
    elif env_example_path.exists():
        print("  ⚠️  .env not found, but .env.example exists")
        print("  Copy .env.example to .env to customize settings")
        print("  Default settings will be used")
        return True
    else:
        print("  ⚠️  No environment configuration found")
        return False

def check_file_structure():
    """Verify all critical files exist"""
    print("\n✓ Checking file structure...")
    
    critical_files = [
        'backend/app.py',
        'backend/requirements.txt',
        'frontend/index.html',
        'frontend/logs.html',
        'frontend/alerts.html',
        'frontend/live.html',
        'frontend/css/styles.css',
        'frontend/js/dashboard.js',
        'database/sample_data_generator.py'
    ]
    
    all_exist = True
    for file_path in critical_files:
        path = Path(file_path)
        if path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (missing)")
            all_exist = False
    
    return all_exist

def print_startup_instructions():
    """Print startup instructions"""
    print_header("🚀 STARTUP INSTRUCTIONS")
    
    print("To start the SIEM platform:\n")
    
    print("1. Start MongoDB (in a separate terminal):")
    print("   mongod --dbpath /data/db")
    print("   (or start MongoDB service if installed as service)\n")
    
    print("2. Start Flask Backend (in a separate terminal):")
    print("   cd backend")
    print("   python app.py\n")
    
    print("3. Open Frontend:")
    print("   Option A: Open directly in browser")
    print("   file:///path/to/SEIM/frontend/index.html\n")
    print("   Option B: Use Python HTTP server")
    print("   cd frontend")
    print("   python -m http.server 8080")
    print("   Then open: http://localhost:8080\n")
    
    print("4. Generate Test Data:")
    print("   cd database")
    print("   python sample_data_generator.py\n")

def print_quick_test():
    """Print quick test command"""
    print_header("🧪 QUICK TEST")
    
    print("Test the API is working:")
    print("curl http://localhost:5000/api/health\n")
    
    print("Send a test log:")
    print('curl -X POST http://localhost:5000/api/logs \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"timestamp":"2024-01-15T10:30:00Z","source":"test",')
    print('      "event_type":"test_event","ip_address":"192.168.1.1"}\'')
    print()

def print_documentation():
    """Print documentation references"""
    print_header("📚 DOCUMENTATION")
    
    docs = [
        ('README.md', 'Comprehensive project overview'),
        ('QUICKSTART.md', '5-minute quick start guide'),
        ('TESTING_GUIDE.md', 'Complete testing instructions'),
        ('FINAL_INSTRUCTIONS.md', 'Setup and deployment guide'),
        ('PROJECT_FINAL_SUMMARY.md', 'Project completion summary')
    ]
    
    for doc, description in docs:
        if Path(doc).exists():
            print(f"✓ {doc:30s} - {description}")
        else:
            print(f"  {doc:30s} - {description}")
    print()

def main():
    """Main function"""
    print_header("🔐 SIEM PLATFORM - SYSTEM CHECK")
    
    # Run checks
    checks = []
    checks.append(("Python Version", check_python()))
    checks.append(("MongoDB", check_mongodb()))
    checks.append(("File Structure", check_file_structure()))
    checks.append(("Environment Config", check_env_file()))
    checks.append(("Python Dependencies", check_dependencies()))
    
    # Summary
    print_header("📊 CHECK SUMMARY")
    
    for name, passed in checks:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:25s} {status}")
    
    all_passed = all(result for _, result in checks)
    
    print()
    if all_passed:
        print("🎉 All checks passed! System is ready to start.")
        print_startup_instructions()
        print_quick_test()
    else:
        print("⚠️  Some checks failed. Please review the issues above.")
        print("\nFor help, see:")
        print("- QUICKSTART.md")
        print("- TESTING_GUIDE.md")
        print()
    
    print_documentation()
    
    print_header("✨ SYSTEM CHECK COMPLETE")

if __name__ == "__main__":
    main()
