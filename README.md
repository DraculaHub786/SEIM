# 🔐 SIEM Platform - Security Log & Incident Response System

A complete, production-ready Security Information and Event Management (SIEM) platform built with Flask (Python), MongoDB, and vanilla JavaScript. This system collects, analyzes, and visualizes security logs in real-time.

![SIEM Platform](https://img.shields.io/badge/SIEM-Platform-cyan)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-6.0+-green)
![Flask](https://img.shields.io/badge/Flask-3.0-orange)

---

## 🚀 **Quick Start (Unified Launch)**

**New!** The entire platform now launches with a single command:

```bash
# 1. Start MongoDB (if not already running)
mongod --dbpath /data/db

# 2. Run the application
cd backend
pip install -r requirements.txt
python app.py

# 3. Open browser
# http://localhost:5000
```

**Or use the automated launcher:**

**Windows:** `start.bat`  
**Linux/Mac:** `./start.sh`

That's it! The backend now serves both the API and the frontend dashboard.

📖 **See [UNIFIED_LAUNCH.md](UNIFIED_LAUNCH.md) for complete details**

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Testing](#-testing)
- [API Documentation](#-api-documentation)
- [Frontend Usage](#-frontend-usage)
- [MongoDB Aggregation Pipelines](#-mongodb-aggregation-pipelines)
- [Future Improvements](#-future-improvements)

---

## ✨ Features

### Core Functionality
- **Log Ingestion System**: Flexible API endpoint accepting logs from Windows, Linux, and network devices
- **MongoDB-Centric Storage**: Schema-less design with strategic indexing and TTL (90-day auto-deletion)
- **Detection Engine**: MongoDB aggregation pipelines for real-time threat detection
- **Real-Time Alerts**: Socket.IO integration for instant security notifications
- **Professional Dashboard**: Dark-themed cybersecurity UI with charts and visualizations

### Detection Rules
- **Brute Force Detection**: Identifies 10+ failed login attempts within 2 minutes
- **Extensible Framework**: Easy to add custom detection rules

### Dashboard Features
- **Overview Dashboard**: Total logs, alerts, active threats, charts
- **Logs Viewer**: Filterable table with IP, event type, time range filters
- **Alerts Panel**: Severity-based alert display with status management
- **Live Monitoring**: Real-time log stream with Socket.IO

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Log Sources (Any System)        │
└────────────────┬────────────────────────┘
                 │ HTTP POST /api/logs
                 ▼
┌─────────────────────────────────────────┐
│          Flask Backend (Python)         │
│  ┌────────────────────────────────┐     │
│  │  Detection Engine              │     │
│  │  (MongoDB Aggregation)         │     │
│  └────────────────────────────────┘     │
│  ┌────────────────────────────────┐     │
│  │  Socket.IO Server              │     │
│  └────────────────────────────────┘     │
└────────────┬────────────────────────────┘
             │
             ▼
┌────────────────────────────────────────┐
│          MongoDB Database              │
│  • logs (with TTL index)               │
│  • alerts                              │
│  • users                               │
└────────────────────────────────────────┘
```

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **MongoDB 6.0+**: [Download MongoDB](https://www.mongodb.com/try/download/community)
- **Git**: [Download Git](https://git-scm.com/downloads)

---

## 🚀 Installation

### Step 1: Clone or Navigate to Project

```bash
cd c:\Users\afjal\Documents\Mini-Projects\SEIM
```

### Step 2: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Required packages:**
- Flask 3.0.0
- Flask-SocketIO 5.3.5
- Flask-CORS 4.0.0
- PyMongo 4.6.1
- python-socketio 5.10.0
- python-dotenv 1.0.0
- bcrypt 4.1.2
- APScheduler 3.10.4
- eventlet 0.35.1

### Step 3: Start MongoDB

**Windows:**
```bash
# Start MongoDB service
net start MongoDB

# Or run mongod directly
mongod --dbpath C:\data\db
```

**Linux/Mac:**
```bash
sudo systemctl start mongod
# Or
mongod --dbpath /data/db
```

Verify MongoDB is running:
```bash
mongosh
# Should connect successfully
```

---

## ⚙️ Configuration

### Step 1: Environment Variables

Copy the example environment file:

```bash
cd backend
copy .env.example .env
```

### Step 2: Edit `.env` File

```env
# Flask Settings
SECRET_KEY=your-random-secret-key-here
DEBUG=True
HOST=0.0.0.0
PORT=5000

# MongoDB Settings
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=siem_db

# Detection Engine Settings
DETECTION_INTERVAL=30
FAILED_LOGIN_THRESHOLD=10
FAILED_LOGIN_TIME_WINDOW=120

# Data Retention
LOG_TTL_DAYS=90
```

---

## 🎮 Running the Application

### Start the Backend Server

```bash
cd backend
python app.py
```

Expected output:
```
============================================================
🔐 SIEM Platform - Starting Server
============================================================
✓ Connected to MongoDB: siem_db
✓ Created 'logs' collection
✓ Created indexes for 'logs' (TTL: 90 days)
✓ Created 'alerts' collection
✓ Created indexes for 'alerts'
✓ Created default admin user (username: admin, password: admin123)
✓ Database initialized
✓ Routes registered
✓ Detection engine initialized
✓ Scheduler started (interval: 30s)
============================================================
🚀 Server ready on 0.0.0.0:5000
============================================================
```

### Open the Frontend

Open your browser and navigate to:

```
http://localhost:5000/index.html
```

Or open the HTML files directly from the `frontend/` directory.

---

## 🧪 Testing

### Test 1: Ingest Sample Logs

Use PowerShell to send test logs:

```powershell
# Failed login log
$body = @{
    source = "windows-server-01"
    event_type = "failed_login"
    ip_address = "192.168.1.100"
    username = "admin"
    severity = "medium"
    details = @{
        event_id = 4625
        logon_type = 3
    }
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/logs" -Method Post -Body $body -ContentType "application/json"
```

### Test 2: Trigger Brute Force Detection

Send 10+ failed logins to trigger an alert:

```powershell
# Send 12 failed login attempts
for ($i=1; $i -le 12; $i++) {
    $body = @{
        source = "windows-server-01"
        event_type = "failed_login"
        ip_address = "192.168.1.105"
        username = "administrator"
        severity = "medium"
    } | ConvertTo-Json
    
    Invoke-RestMethod -Uri "http://localhost:5000/api/logs" -Method Post -Body $body -ContentType "application/json"
    Start-Sleep -Seconds 2
}
```

After 30 seconds (detection interval), an alert should appear in the dashboard.

### Test 3: Sample Data Generator

Create `backend/tests/generate_logs.py`:

```python
import requests
import time
import random
from datetime import datetime

API_URL = "http://localhost:5000/api/logs"

sources = ["windows-server-01", "linux-web-01", "firewall-01"]
event_types = ["failed_login", "successful_login", "file_access", "firewall_block"]
ips = ["192.168.1.100", "192.168.1.105", "10.0.0.45", "172.16.0.20"]

for i in range(100):
    log = {
        "source": random.choice(sources),
        "event_type": random.choice(event_types),
        "ip_address": random.choice(ips),
        "username": random.choice(["admin", "user1", "root"]),
        "severity": random.choice(["low", "medium", "high"])
    }
    
    response = requests.post(API_URL, json=log)
    print(f"Log {i+1}: {response.status_code} - {log['event_type']}")
    time.sleep(0.5)
```

Run:
```bash
cd backend
python tests/generate_logs.py
```

---

## 📚 API Documentation

### Ingest Log

**POST** `/api/logs`

```json
{
  "source": "windows-server-01",
  "event_type": "failed_login",
  "ip_address": "192.168.1.100",
  "username": "admin",
  "severity": "medium",
  "details": {}
}
```

### Get Logs

**GET** `/api/logs?page=1&page_size=100&ip_address=192.168.1.100&event_type=failed_login`

### Get Log Statistics

**GET** `/api/logs/stats`

Response:
```json
{
  "success": true,
  "stats": {
    "total_logs": 1234,
    "logs_today": 56,
    "last_24_hours": 123
  }
}
```

### Get Alerts

**GET** `/api/alerts?status=open&severity=high`

### Get Alert Statistics

**GET** `/api/alerts/stats`

### Update Alert Status

**PATCH** `/api/alerts/<alert_id>/status`

```json
{
  "status": "resolved"
}
```

---

## 🎨 Frontend Usage

### Navigation

1. **Overview Dashboard** (`index.html`): Main dashboard with statistics and charts
2. **Logs Viewer** (`logs.html`): Search and filter logs
3. **Alerts Panel** (`alerts.html`): View and manage security alerts
4. **Live Monitor** (`live.html`): Real-time log stream

### Features

- **Real-Time Updates**: Dashboard updates automatically via Socket.IO
- **Filters**: Filter logs by IP, event type, source, time range
- **Export**: Export logs to CSV
- **Dark Theme**: Professional cybersecurity aesthetic

---

## 🔍 MongoDB Aggregation Pipelines

### Brute Force Detection Pipeline

```javascript
db.logs.aggregate([
    // Match failed logins in time window
    {
        $match: {
            event_type: 'failed_login',
            timestamp: { $gte: ISODate('2026-04-01T08:00:00Z') }
        }
    },
    // Group by IP and count
    {
        $group: {
            _id: { ip_address: '$ip_address', username: '$username' },
            count: { $sum: 1 },
            first_attempt: { $min: '$timestamp' },
            last_attempt: { $max: '$timestamp' }
        }
    },
    // Filter threshold
    {
        $match: { count: { $gte: 10 } }
    }
])
```

### View Indexes

```javascript
db.logs.getIndexes()
db.alerts.getIndexes()
```

---

## 🔮 Future Improvements

### Short-Term Enhancements

1. **Authentication**: Role-based access control (admin/analyst/viewer)
2. **Advanced Filters**: Date range picker, regex search
3. **Export Options**: JSON, PDF reports
4. **Email Alerts**: SMTP integration for critical alerts
5. **Geolocation**: IP address geolocation mapping

### Long-Term Features

1. **Machine Learning**: Anomaly detection using scikit-learn
2. **Correlation Rules**: Multi-stage attack detection
3. **Threat Intelligence**: Integration with threat feeds
4. **SIEM Connectors**: Syslog, SNMP, WMI integrations
5. **Compliance Reports**: PCI-DSS, HIPAA reporting templates

### Additional Detection Rules

```python
# Future detection rules
def detect_port_scan(self):
    """Detect port scanning activity"""
    pass

def detect_data_exfiltration(self):
    """Detect unusual data transfer patterns"""
    pass

def detect_privilege_escalation(self):
    """Detect unauthorized privilege changes"""
    pass
```

---

## 📁 Project Structure

```
SEIM/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config/
│   │   └── config.py          # Configuration management
│   ├── database/
│   │   └── db_connection.py   # MongoDB connection
│   ├── models/
│   │   ├── log_model.py       # Log data model
│   │   └── alert_model.py     # Alert data model
│   ├── controllers/
│   │   ├── log_controller.py  # Log business logic
│   │   └── alert_controller.py
│   ├── routes/
│   │   ├── log_routes.py      # Log API endpoints
│   │   └── alert_routes.py
│   ├── services/
│   │   └── detection_engine.py # Threat detection
│   └── requirements.txt
├── frontend/
│   ├── index.html             # Overview dashboard
│   ├── logs.html              # Logs viewer
│   ├── alerts.html            # Alerts panel
│   ├── live.html              # Live monitor
│   ├── css/
│   │   └── styles.css         # Custom styles
│   └── js/
│       ├── socket-client.js   # Socket.IO client
│       ├── dashboard.js       # Dashboard logic
│       ├── logs.js            # Logs page logic
│       ├── alerts.js          # Alerts page logic
│       └── live.js            # Live monitor logic
└── README.md
```

---

## 🐛 Troubleshooting

### Issue: MongoDB Connection Failed

**Solution:**
```bash
# Check MongoDB is running
mongosh

# Start MongoDB
net start MongoDB  # Windows
sudo systemctl start mongod  # Linux
```

### Issue: Module Not Found

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Issue: Socket.IO Not Connecting

**Solution:**
- Check CORS settings in `config.py`
- Verify backend is running on port 5000
- Check browser console for errors

### Issue: No Alerts Generated

**Solution:**
- Wait 30 seconds (detection interval)
- Check detection threshold (10 failed logins)
- Verify logs have `event_type: "failed_login"`

---

## 👨‍💻 Default Credentials

**Admin User:**
- Username: `admin`
- Password: `admin123`

⚠️ **Security Note**: Change default password in production!

---

## 📝 License

This project is for educational purposes. Use at your own risk in production environments.

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional detection rules
- UI/UX enhancements
- Performance optimizations
- Documentation improvements

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review MongoDB logs
3. Check Flask console output
4. Verify all dependencies are installed

---

**Built with ❤️ for cybersecurity professionals**

🔐 **Stay Secure!**
