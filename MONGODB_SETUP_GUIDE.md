# 🗄️ MongoDB Setup Guide for SIEM Platform

## ✅ Quick Setup Checklist

### 1. **Start MongoDB Service**

**Option A: Windows Service (Recommended)**
```cmd
# Start MongoDB service
net start MongoDB

# Check if running
sc query MongoDB
```

**Option B: Manual Start**
```cmd
# Create data directory if it doesn't exist
mkdir C:\data\db

# Start MongoDB manually
mongod --dbpath C:\data\db
```

---

### 2. **Connect with MongoDB Compass**

#### Connection Details:
- **Connection String:** `mongodb://localhost:27017/`
- **Database Name:** `siem_db`

#### Step-by-Step in Compass:
1. Open **MongoDB Compass**
2. You should see a connection form
3. In the **URI** field, paste:
   ```
   mongodb://localhost:27017/
   ```
4. Click **Connect**
5. After connecting, you'll see the database list
6. Look for **siem_db** (it will be created automatically when you run the app)

---

### 3. **Verify MongoDB Installation**

Open Command Prompt or PowerShell and run:

```cmd
# Test MongoDB connection with mongosh
mongosh

# You should see:
# Current Mongosh Log ID: ...
# Connecting to: mongodb://127.0.0.1:27017/
# Connected successfully
```

If `mongosh` is not found, download it from: https://www.mongodb.com/try/download/shell

---

### 4. **Install Python Dependencies**

```cmd
cd c:\Users\afjal\Documents\Mini-Projects\SEIM\backend
pip install -r requirements.txt
```

**Required packages:**
- pymongo==4.6.1 (MongoDB driver)
- flask==3.0.0
- flask-socketio==5.3.5
- flask-cors==4.0.0
- python-dotenv==1.0.0
- bcrypt==4.1.2
- apscheduler==3.10.4
- eventlet==0.35.1

---

### 5. **Run the Application**

```cmd
cd c:\Users\afjal\Documents\Mini-Projects\SEIM\backend
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
✓ Created 'users' collection
✓ Created indexes for 'users'
✓ Created default admin user (username: admin, password: admin123)
✓ Database initialized
============================================================
🚀 Server ready on 0.0.0.0:5000
============================================================
```

---

## 📊 MongoDB Compass - Exploring Collections

Once your app is running and has created the database, you can explore it in Compass:

### Collections Created:

1. **logs** - Stores all security event logs
   - Indexed fields: `timestamp`, `event_type`, `ip_address`, `source`
   - TTL Index: Auto-deletes logs after 90 days
   
2. **alerts** - Stores security alerts
   - Indexed fields: `timestamp`, `ip_address`, `status`, `severity`
   
3. **users** - Stores user accounts
   - Unique indexes: `username`, `email`
   - Default admin user created automatically

### How to View Collections in Compass:

1. In Compass, click on **siem_db** database
2. You'll see three collections: `logs`, `alerts`, `users`
3. Click on any collection to browse documents
4. Use the **Filter** bar to query: `{ "event_type": "failed_login" }`
5. View **Indexes** tab to see all optimizations

---

## 🧪 Test MongoDB Connection

### Test 1: Check MongoDB Status
```cmd
# In Command Prompt
mongosh --eval "db.adminCommand('ping')"

# Expected output:
# { ok: 1 }
```

### Test 2: View Databases
```cmd
mongosh --eval "show dbs"

# After running the app, you should see:
# siem_db
```

### Test 3: Query Collections
```javascript
// Connect to MongoDB shell
mongosh

// Switch to siem_db
use siem_db

// Show collections
show collections

// Count users
db.users.countDocuments()

// View admin user
db.users.findOne({ username: "admin" })

// Check indexes
db.logs.getIndexes()
```

---

## 🔧 Troubleshooting

### Issue: "MongoDB connection failed"

**Solutions:**

1. **Check if MongoDB is running:**
   ```cmd
   sc query MongoDB
   ```
   
2. **Start MongoDB service:**
   ```cmd
   net start MongoDB
   ```

3. **Check MongoDB port:**
   ```cmd
   netstat -an | findstr :27017
   ```
   - Should show `LISTENING` on port 27017

4. **Try manual start:**
   ```cmd
   mongod --dbpath C:\data\db
   ```

### Issue: "mongosh command not found"

**Solution:**
Download MongoDB Shell from: https://www.mongodb.com/try/download/shell

Or use legacy `mongo` command if you have MongoDB < 5.0

### Issue: "Access denied to data directory"

**Solution:**
Run as Administrator or create the directory manually:
```cmd
mkdir C:\data\db
icacls C:\data\db /grant Everyone:(OI)(CI)F
```

### Issue: MongoDB Compass won't connect

**Checklist:**
- [ ] MongoDB service is running (`net start MongoDB`)
- [ ] Port 27017 is not blocked by firewall
- [ ] Connection string is: `mongodb://localhost:27017/`
- [ ] No authentication required (default local setup)

---

## 📈 MongoDB Performance Tips

### 1. **Monitor Performance in Compass:**
- Click **Performance** tab in Compass
- View slow queries, operations, and network activity

### 2. **Index Usage:**
All critical indexes are auto-created:
```javascript
// Check index usage
db.logs.aggregate([
    { $indexStats: {} }
])
```

### 3. **TTL Index (Auto-Cleanup):**
Logs older than 90 days are automatically deleted:
```javascript
// Verify TTL index
db.logs.getIndexes().filter(idx => idx.expireAfterSeconds)
```

---

## 🎯 Next Steps

1. ✅ Start MongoDB service
2. ✅ Connect with MongoDB Compass (`mongodb://localhost:27017/`)
3. ✅ Run the SIEM application (`python app.py`)
4. ✅ Verify collections are created in Compass
5. ✅ Send test logs (see README.md for examples)
6. ✅ Monitor data in real-time using Compass

---

## 📝 MongoDB Compass Connection String

```
mongodb://localhost:27017/
```

**For advanced connection options:**
```
mongodb://localhost:27017/?readPreference=primary&appname=SIEM-Platform&ssl=false
```

---

## 🔐 Security Notes

**Current Setup (Development):**
- No authentication required
- Localhost only
- Default admin user: `admin` / `admin123`

**Production Recommendations:**
- Enable MongoDB authentication
- Use environment variables for credentials
- Update MONGO_URI: `mongodb://username:password@localhost:27017/`
- Change default admin password
- Enable SSL/TLS
- Restrict network access

---

## 📚 Useful MongoDB Commands

```javascript
// Connect to database
mongosh
use siem_db

// View all logs
db.logs.find().limit(10)

// Count alerts
db.alerts.countDocuments()

// Find failed logins
db.logs.find({ event_type: "failed_login" }).limit(5)

// Recent alerts
db.alerts.find().sort({ timestamp: -1 }).limit(10)

// Aggregation - Top IPs by log count
db.logs.aggregate([
    { $group: { _id: "$ip_address", count: { $sum: 1 } } },
    { $sort: { count: -1 } },
    { $limit: 10 }
])

// Delete all logs (CAUTION!)
db.logs.deleteMany({})

// Drop database (CAUTION!)
db.dropDatabase()
```

---

## 🎨 MongoDB Compass Features

1. **Documents View:** Browse, edit, and delete documents
2. **Schema Analysis:** Analyze data structure and types
3. **Explain Plans:** See query performance
4. **Indexes:** View and manage indexes
5. **Validation:** Collection validation rules
6. **Aggregation Builder:** Visual pipeline builder
7. **Export/Import:** Export data as JSON, CSV

---

## ✅ Connection Checklist

- [x] MongoDB installed and running
- [x] MongoDB Compass installed
- [x] Connected to `mongodb://localhost:27017/`
- [x] Python dependencies installed
- [x] `.env` file configured
- [x] Application running successfully
- [x] Collections visible in Compass

---

**🎉 You're all set! Your SIEM platform is now connected to MongoDB.**

For questions, check:
- MongoDB logs: `C:\Program Files\MongoDB\Server\{version}\log\`
- Application logs: Terminal output when running `python app.py`
