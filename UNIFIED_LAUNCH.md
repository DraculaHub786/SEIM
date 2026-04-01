# 🚀 SIEM Platform - Unified Launch Guide

## ✨ **What's New: One-Command Launch!**

The SIEM platform now runs as a **unified application**. Simply start the backend, and it will serve both the API and the frontend dashboard!

---

## 🎯 Quick Start (2 Steps!)

### Step 1: Ensure MongoDB is Running

**Windows:**
```bash
# Start MongoDB service
net start MongoDB

# OR start manually:
mongod --dbpath C:\data\db
```

**Linux/Mac:**
```bash
# Start MongoDB
sudo systemctl start mongod

# OR start manually:
mongod --dbpath /data/db
```

### Step 2: Start the Application

**Option A - Using the Launcher Script (Recommended):**

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Option B - Manual Start:**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Step 3: Access the Dashboard

Open your browser and go to:
```
http://localhost:5000
```

**That's it! 🎉**

---

## 📊 What You Get

When you run the backend (`python app.py`), you get:

### ✅ Backend API (Flask + Socket.IO)
- RESTful API endpoints at `/api/*`
- Real-time WebSocket connections
- Background threat detection engine
- MongoDB integration

### ✅ Frontend Dashboard (Served by Flask)
- **/** - Overview Dashboard
- **/logs** - Logs Viewer
- **/alerts** - Alerts Panel  
- **/live** - Live Monitoring

### ✅ Static Assets
- CSS, JavaScript, Images
- All served from the same port (5000)

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         http://localhost:5000               │
├─────────────────────────────────────────────┤
│                                             │
│  Frontend Routes (HTML Pages)               │
│  ├─ GET /          → Dashboard (index.html)│
│  ├─ GET /logs      → Logs Viewer           │
│  ├─ GET /alerts    → Alerts Panel          │
│  └─ GET /live      → Live Monitor          │
│                                             │
│  API Routes (JSON)                          │
│  ├─ POST /api/logs → Ingest logs           │
│  ├─ GET  /api/logs → Retrieve logs         │
│  ├─ GET  /api/alerts → Retrieve alerts     │
│  └─ GET  /api/health → Health check        │
│                                             │
│  Static Assets                              │
│  ├─ /css/*   → Stylesheets                 │
│  ├─ /js/*    → JavaScript files            │
│  └─ /assets/* → Images, fonts, etc.        │
│                                             │
│  WebSocket (Socket.IO)                      │
│  └─ Real-time updates (logs, alerts)       │
│                                             │
└─────────────────────────────────────────────┘
                    ↓
         ┌──────────────────┐
         │     MongoDB      │
         │   localhost:27017│
         └──────────────────┘
```

---

## 🧪 Testing the System

### 1. Verify Server is Running

```bash
# Check API health
curl http://localhost:5000/api/health

# Expected response:
# {"status":"healthy","database":"connected","timestamp":"..."}
```

### 2. Access the Dashboard

Open in browser:
- Main Dashboard: http://localhost:5000/
- Logs Page: http://localhost:5000/logs
- Alerts Page: http://localhost:5000/alerts
- Live Monitor: http://localhost:5000/live

### 3. Generate Test Data

In a new terminal:

```bash
cd database
python sample_data_generator.py
```

Choose option:
- **1** - Normal logs (100 logs)
- **2** - Brute force attack (triggers alert)
- **3** - Mixed traffic
- **4** - All scenarios

### 4. Watch Real-Time Updates

1. Open the **Live Monitor** page (http://localhost:5000/live)
2. Run the sample data generator
3. Watch logs appear in real-time!
4. After 30 seconds, check the **Alerts** page for detected threats

---

## 🔧 Configuration

All settings are in `backend/.env` (optional):

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017/
DB_NAME=siem_db

# Flask
FLASK_ENV=development
FLASK_PORT=5000
FLASK_HOST=0.0.0.0

# Detection
DETECTION_INTERVAL=30
```

If no `.env` file exists, sensible defaults are used.

---

## 🎨 Features

### ✅ Unified Launch
- One command to start everything
- No need for separate frontend server
- Simplified deployment

### ✅ Real-Time Communication
- Socket.IO for live updates
- Automatic reconnection
- No manual refresh needed

### ✅ Professional UI
- Dark cybersecurity theme
- Smooth animations
- Responsive design
- 4 complete pages

### ✅ Powerful Backend
- RESTful API
- MongoDB aggregation pipelines
- Background threat detection
- Automatic alert generation

---

## 📱 Page Overview

### 1. Dashboard (/)
- Total logs and alerts count
- Active threats overview
- Charts: Logs over time, Events by type
- Recent alerts list
- Real-time updates

### 2. Logs Viewer (/logs)
- Searchable and filterable log table
- Pagination (100 logs per page)
- Filters: IP, Event Type, Source, Time Range
- Export to CSV
- JSON detail view

### 3. Alerts Panel (/alerts)
- Alert cards with severity badges
- Status management (Open, Investigating, Resolved, False Positive)
- Filter by status and severity
- Real-time alert notifications
- Alert statistics

### 4. Live Monitor (/live)
- Real-time log stream
- Live statistics (logs/min)
- Active sessions count
- Pause/Resume monitoring
- Auto-scroll toggle

---

## 🐛 Troubleshooting

### Issue: "Connection refused" in browser

**Solution:**
1. Check backend is running: `netstat -an | find "5000"`
2. Check MongoDB is running: `mongod --version`
3. Check backend console for errors

### Issue: "Module not found" error

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Issue: No logs appearing

**Solution:**
1. Verify MongoDB is running
2. Run the sample data generator
3. Check browser console for errors (F12)
4. Verify Socket.IO connection (should show "Connected")

### Issue: Alerts not generating

**Solution:**
1. Generate brute force attack (option 2 in sample_data_generator.py)
2. Wait 30 seconds for detection engine
3. Check alerts page or MongoDB: `db.alerts.find().pretty()`

---

## 🚀 Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -k eventlet -b 0.0.0.0:5000 app:app
```

Or use the provided launcher scripts with proper environment variables.

---

## 📊 API Endpoints

### Frontend Pages
- `GET /` - Dashboard
- `GET /logs` - Logs viewer
- `GET /alerts` - Alerts panel
- `GET /live` - Live monitor

### API Endpoints
- `POST /api/logs` - Ingest log
- `GET /api/logs` - Get logs (with filters)
- `GET /api/logs/stats` - Dashboard stats
- `GET /api/alerts` - Get alerts
- `GET /api/alerts/stats` - Alert stats
- `PATCH /api/alerts/<id>/status` - Update alert
- `GET /api/health` - Health check

### WebSocket Events
- `new_log` - New log received
- `new_alert` - New alert generated

---

## 🎯 Benefits of Unified Launch

### Before (2 servers):
```bash
# Terminal 1: Frontend
cd frontend
python -m http.server 8080

# Terminal 2: Backend
cd backend
python app.py

# Access: http://localhost:8080
```

### Now (1 server):
```bash
# Terminal 1: Backend (serves everything)
cd backend
python app.py

# Access: http://localhost:5000
```

### Advantages:
- ✅ **Simpler** - One command to rule them all
- ✅ **No CORS issues** - Same origin for frontend and backend
- ✅ **Easier deployment** - Single port, single process
- ✅ **Production-ready** - Standard Flask architecture
- ✅ **Less confusion** - One URL for everything

---

## 🎉 Summary

**To run the entire SIEM platform:**

```bash
# 1. Start MongoDB (if not already running)
mongod --dbpath /data/db

# 2. Run the backend (serves everything!)
cd backend
python app.py

# 3. Open browser
http://localhost:5000
```

**That's all you need! 🚀**

---

## 📚 Additional Documentation

- `TESTING_GUIDE.md` - Complete testing instructions
- `PROJECT_FINAL_SUMMARY.md` - Full project overview
- `README.md` - Original comprehensive documentation
- `QUICKSTART.md` - Legacy quick start guide

---

**Your SIEM platform is now easier than ever to launch! 🔐**
