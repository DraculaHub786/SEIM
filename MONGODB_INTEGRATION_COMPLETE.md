# ✅ MongoDB Integration Complete - SIEM Platform

## 🎉 What Has Been Set Up

Your SEIM project is now **fully configured** for MongoDB! Here's what's ready:

### ✅ Files Created/Updated

1. **`.env` file** - Environment configuration with MongoDB settings
2. **`MONGODB_SETUP_GUIDE.md`** - Complete setup and troubleshooting guide
3. **`MONGODB_COMPASS_REFERENCE.md`** - Quick reference for using MongoDB Compass
4. **`mongodb_helper.bat`** - Windows helper script for managing MongoDB

### ✅ Existing Database Structure (Already Built-In)

Your project already has a complete MongoDB implementation:

- **Database Connection** (`backend/database/db_connection.py`) ✅
- **Configuration** (`backend/config/config.py`) ✅  
- **Collections:** `logs`, `alerts`, `users` ✅
- **Indexes:** Optimized for performance ✅
- **TTL Index:** Auto-deletes logs after 90 days ✅
- **Schema Validation:** Enforces data integrity ✅

---

## 🚀 Quick Start (3 Steps)

### Step 1: Start MongoDB

**Option A - Windows Service:**
```cmd
net start MongoDB
```

**Option B - Manual Start:**
```cmd
mkdir C:\data\db
mongod --dbpath C:\data\db
```

### Step 2: Connect MongoDB Compass

1. Open **MongoDB Compass**
2. Paste this connection string:
   ```
   mongodb://localhost:27017/
   ```
3. Click **Connect**

### Step 3: Run SIEM Application

```cmd
cd c:\Users\afjal\Documents\Mini-Projects\SEIM\backend
pip install -r requirements.txt
python app.py
```

**That's it!** 🎉

---

## 📋 MongoDB Compass Connection Details

| Setting | Value |
|---------|-------|
| **Connection String** | `mongodb://localhost:27017/` |
| **Database Name** | `siem_db` |
| **Port** | 27017 |
| **Authentication** | None (localhost) |

### Collections Created Automatically:

1. **logs** - Security event logs (with TTL: 90 days)
2. **alerts** - Security alerts  
3. **users** - User accounts (default admin created)

---

## 🎯 What You Can Do Now

### In MongoDB Compass:
✅ View all collections (logs, alerts, users)  
✅ Run queries and aggregations  
✅ Monitor database performance  
✅ Export data to JSON/CSV  
✅ View indexes and schema  

### Common Queries:

**View recent logs:**
```javascript
{ "timestamp": { "$gte": new Date(Date.now() - 3600000) } }
```

**Find failed logins:**
```javascript
{ "event_type": "failed_login" }
```

**View open alerts:**
```javascript
{ "status": "open" }
```

---

## 🛠️ Helper Tools

### MongoDB Helper Script
Run this for an interactive menu:
```cmd
mongodb_helper.bat
```

Features:
- Check MongoDB status
- Start/Stop MongoDB service
- Test connection
- Install dependencies
- Run SIEM application
- View connection string

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `MONGODB_SETUP_GUIDE.md` | Detailed setup, troubleshooting, and MongoDB commands |
| `MONGODB_COMPASS_REFERENCE.md` | Quick reference for queries, aggregations, and tips |
| `mongodb_helper.bat` | Interactive helper script |
| `README.md` | Main project documentation |

---

## 🔍 Verify Everything Works

### Test MongoDB Connection:
```cmd
mongosh --eval "db.adminCommand('ping')"
```
Expected: `{ ok: 1 }`

### Test Application:
```cmd
cd backend
python app.py
```
Expected output should show:
```
✓ Connected to MongoDB: siem_db
✓ Created 'logs' collection
✓ Created indexes for 'logs' (TTL: 90 days)
...
🚀 Server ready on 0.0.0.0:5000
```

### Test in MongoDB Compass:
1. Connect to `mongodb://localhost:27017/`
2. Look for `siem_db` database
3. Click on `logs`, `alerts`, or `users` collection
4. Verify indexes in the **Indexes** tab

---

## 🧪 Send Test Logs

Send a test log via PowerShell:

```powershell
$body = @{
    source = "test-server"
    event_type = "failed_login"
    ip_address = "192.168.1.100"
    username = "admin"
    severity = "medium"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/logs" -Method Post -Body $body -ContentType "application/json"
```

Then check MongoDB Compass - you should see the log in the `logs` collection!

---

## 🎨 MongoDB Compass Views

### Logs Collection View:
```
_id         | timestamp           | event_type    | ip_address    | source
------------------------------------------------------------------------
ObjectId()  | 2026-04-01 15:30   | failed_login  | 192.168.1.100 | test-server
```

### Alerts Collection View:
```
_id         | alert_type          | severity | status | ip_address
-----------------------------------------------------------------------
ObjectId()  | brute_force_attack  | high     | open   | 192.168.1.100
```

### Users Collection View:
```
_id         | username | role  | is_active | last_login
-----------------------------------------------------------
ObjectId()  | admin    | admin | true      | 2026-04-01
```

---

## 🔐 Default Credentials

**Admin Account (Auto-created):**
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Change this in production!**

---

## 📊 Database Statistics

Once running, check stats in MongoDB Compass or via shell:

```javascript
// In mongosh
use siem_db

// Collection stats
db.logs.countDocuments()
db.alerts.countDocuments()
db.users.countDocuments()

// Database info
db.stats()

// Index info
db.logs.getIndexes()
```

---

## 🎯 Next Steps

1. ✅ Start MongoDB service
2. ✅ Connect MongoDB Compass
3. ✅ Run SIEM application
4. ✅ View collections in Compass
5. ✅ Send test logs
6. ✅ Monitor real-time data

**Optional:**
- Install `mongosh` for CLI access
- Set up MongoDB as Windows service (auto-start)
- Configure MongoDB Compass saved connections
- Create additional users with different roles

---

## 🆘 Troubleshooting

### MongoDB Won't Start?
```cmd
# Check if already running
sc query MongoDB

# Try starting manually
mongod --dbpath C:\data\db
```

### Can't Connect in Compass?
- Verify MongoDB is running
- Check port 27017 is listening: `netstat -an | findstr :27017`
- Try connection string: `mongodb://127.0.0.1:27017/`

### Application Errors?
```cmd
# Reinstall dependencies
cd backend
pip install -r requirements.txt

# Check .env file exists
dir .env
```

**Need more help?** Check `MONGODB_SETUP_GUIDE.md` for detailed troubleshooting!

---

## 📞 Quick Commands Reference

| Task | Command |
|------|---------|
| Start MongoDB | `net start MongoDB` |
| Stop MongoDB | `net stop MongoDB` |
| Check Status | `sc query MongoDB` |
| Test Connection | `mongosh --eval "db.adminCommand('ping')"` |
| Run SIEM App | `cd backend && python app.py` |
| Install Deps | `cd backend && pip install -r requirements.txt` |
| MongoDB Shell | `mongosh` |

---

## ✨ Features Already Implemented

Your SEIM platform has a **production-ready** MongoDB integration:

✅ **Connection Pooling** - Efficient database connections  
✅ **Auto-Indexing** - Performance-optimized queries  
✅ **TTL Cleanup** - Automatic old log deletion  
✅ **Schema Validation** - Data integrity enforcement  
✅ **Error Handling** - Graceful connection failures  
✅ **Default Admin** - Auto-created admin account  
✅ **Collections** - Pre-configured logs, alerts, users  

---

## 🎉 Success!

Your SIEM platform is now **fully integrated with MongoDB**!

**MongoDB Compass Connection String:**
```
mongodb://localhost:27017/
```

**Database Name:**
```
siem_db
```

**Ready to use!** 🚀

---

**Questions?** Check the documentation files or run `mongodb_helper.bat` for interactive help.
