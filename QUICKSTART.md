# 🚀 SIEM Platform - Quick Start Guide

## Get Up and Running in 5 Minutes!

### Step 1: Check Prerequisites ✅

```bash
# Check Python version (need 3.8+)
python --version

# Check MongoDB is installed
mongosh --version
```

### Step 2: Start MongoDB 🗄️

**Windows:**
```bash
net start MongoDB
```

**Linux/Mac:**
```bash
sudo systemctl start mongod
```

### Step 3: Install Python Dependencies 📦

```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Configure Environment ⚙️

```bash
cd backend
copy .env.example .env
# Edit .env if needed (defaults should work)
```

### Step 5: Start the Backend Server 🖥️

```bash
cd backend
python app.py
```

You should see:
```
🔐 SIEM Platform - Starting Server
✓ Connected to MongoDB: siem_db
✓ Database initialized
✓ Routes registered
✓ Detection engine initialized
✓ Scheduler started (interval: 30s)
🚀 Server ready on 0.0.0.0:5000
```

### Step 6: Open the Dashboard 🎨

Open your browser and go to:
```
http://localhost:5000/index.html
```

You should see:
- Dark-themed cybersecurity dashboard
- 4 stat cards (Total Logs, Alerts, Open Alerts, Critical Threats)
- 2 charts (Logs Over Time, Events by Type)
- Recent Alerts panel
- ✅ **Connected** status in top right

### Step 7: Generate Test Data 🧪

Open a new terminal:

```bash
cd database
python sample_data_generator.py
```

Select option **1** (Generate normal traffic) or **4** (Generate all).

After 30 seconds, you should see:
- Logs appearing in the dashboard
- If you generated the brute force attack, an alert will appear!

---

## Common Issues & Fixes 🔧

### ❌ "MongoDB connection failed"
**Fix:** Start MongoDB service
```bash
net start MongoDB  # Windows
sudo systemctl start mongod  # Linux
```

### ❌ "Module not found"
**Fix:** Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### ❌ "Port 5000 already in use"
**Fix:** Change port in `.env` file
```env
PORT=5001
```

### ❌ "Socket.IO not connecting"
**Fix:** Check backend is running and browser console for errors

---

## Next Steps 🎯

1. **Explore the Dashboard**: Check all 4 pages (Overview, Logs, Alerts, Live Monitor)
2. **Test Detection**: Run the brute force attack simulation
3. **Read API Docs**: See `README.md` for complete API documentation
4. **Customize**: Add your own detection rules in `backend/services/detection_engine.py`

---

## Default Login 🔑

- **Username:** `admin`
- **Password:** `admin123`

(User authentication not yet implemented in frontend)

---

## File Locations 📁

- **Backend:** `c:\Users\afjal\Documents\Mini-Projects\SEIM\backend\`
- **Frontend:** `c:\Users\afjal\Documents\Mini-Projects\SEIM\frontend\`
- **Database Scripts:** `c:\Users\afjal\Documents\Mini-Projects\SEIM\database\`
- **Logs:** Check MongoDB `siem_db` database

---

## Testing the Detection Engine 🚨

**Trigger a Brute Force Alert:**

```bash
cd database
python sample_data_generator.py
# Choose option 2 (Generate brute force attack)
```

This will:
1. Send 15 failed login attempts from same IP
2. Wait 30 seconds for detection engine
3. Alert appears in dashboard with:
   - 🔴 High severity badge
   - IP address: 192.168.1.105
   - Event count: 15
   - Threat score: 85/100

---

## Architecture at a Glance 🏗️

```
User Browser (Frontend)
         ↓
    Flask Server (Backend)
         ↓
    MongoDB Database
         ↓
Detection Engine (Every 30s)
         ↓
    Socket.IO → Frontend (Real-time alerts)
```

---

## Key Features ⭐

✅ Real-time log ingestion  
✅ MongoDB aggregation-based threat detection  
✅ Socket.IO real-time updates  
✅ Professional dark-themed UI  
✅ TTL-based auto log cleanup (90 days)  
✅ Brute force attack detection  
✅ Extensible detection framework  

---

## Getting Help 💬

1. Check `README.md` for detailed docs
2. Review MongoDB indexes: `db.logs.getIndexes()`
3. Check Flask console for errors
4. Verify MongoDB is running: `mongosh`

---

**🔐 Happy SIEM-ing!**

Built for cybersecurity professionals and enthusiasts.
