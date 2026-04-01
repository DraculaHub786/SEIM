# 🎯 SIEM Platform - Complete Testing & Demonstration Guide

## 📖 Table of Contents
1. [System Overview](#system-overview)
2. [How It Works](#how-it-works)
3. [Quick Start Testing](#quick-start-testing)
4. [Manual Testing Methods](#manual-testing-methods)
5. [Verifying Results](#verifying-results)
6. [Understanding the Data Flow](#understanding-the-data-flow)
7. [Advanced Testing](#advanced-testing)

---

## 🔍 System Overview

Your SIEM (Security Information and Event Management) platform:

**What it does:**
- ✅ Collects security logs from any source via REST API
- ✅ Stores logs in MongoDB with automatic 90-day retention
- ✅ Detects security threats (brute force attacks)
- ✅ Generates real-time alerts
- ✅ Provides web dashboard for monitoring

**Technology Stack:**
- Backend: Flask (Python) + Socket.IO
- Database: MongoDB
- Frontend: Vanilla JavaScript
- Real-time: WebSocket

---

## 🎬 How It Works

### Data Flow Diagram:

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Log Source (Any System)                            │
│  • Windows Server                                           │
│  • Linux Server                                             │
│  • Firewall                                                 │
│  • Application                                              │
└────────────────┬────────────────────────────────────────────┘
                 │ POST /api/logs (JSON)
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: SIEM Backend (Flask API)                           │
│  • Receives JSON log data                                    │
│  • Validates required fields                                 │
│  • Normalizes timestamp                                      │
└────────────────┬────────────────────────────────────────────┘
                 │ insert_one()
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: MongoDB Database                                    │
│  • Stores log in 'logs' collection                          │
│  • Indexed for fast queries                                  │
│  • Auto-deletes after 90 days (TTL index)                   │
└────────────────┬────────────────────────────────────────────┘
                 │ Every 30 seconds
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Detection Engine (Background Job)                   │
│  • Analyzes logs for patterns                                │
│  • Detects: Brute force attacks (10+ failed logins/2min)    │
│  • Creates alerts in 'alerts' collection                     │
└────────────────┬────────────────────────────────────────────┘
                 │ WebSocket broadcast
                 ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: Real-Time Dashboard                                 │
│  • Updates automatically via Socket.IO                       │
│  • Shows log count, alerts, charts                          │
│  • Displays active threats                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start Testing

### Method 1: Use the Testing Script (Easiest!)

**Step 1: Make sure SIEM is running**
```bash
cd backend
python app.py
```

**Step 2: Run the test script in a NEW terminal**
```bash
cd backend
python test_siem.py
```

**Step 3: Follow the interactive menu**
```
Select option (1-9): 8  # Run all tests
```

**What happens:**
1. ✅ Checks system health
2. ✅ Sends single test log
3. ✅ Sends 5 diverse logs
4. ✅ Triggers brute force alert (12 failed logins)
5. ✅ Waits 30 seconds for detection
6. ✅ Shows success message

---

## 📝 Manual Testing Methods

### Method 1: PowerShell (Windows)

**Send Single Log:**
```powershell
$body = @{
    source = "windows-server-01"
    event_type = "failed_login"
    ip_address = "192.168.1.100"
    username = "admin"
    severity = "medium"
    message = "Failed login attempt detected"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/logs" `
  -Method Post `
  -Body $body `
  -ContentType "application/json"
```

**Expected Output:**
```json
{
  "success": true,
  "message": "Log ingested successfully",
  "log_id": "507f1f77bcf86cd799439011"
}
```

**Send Multiple Logs (Loop):**
```powershell
for ($i=1; $i -le 5; $i++) {
    $body = @{
        source = "test-server"
        event_type = "test_event"
        ip_address = "192.168.1.$i"
        severity = "low"
        message = "Test log #$i"
    } | ConvertTo-Json
    
    Invoke-RestMethod -Uri "http://localhost:5000/api/logs" `
      -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "Sent log $i"
    Start-Sleep -Seconds 1
}
```

---

### Method 2: curl (Linux/Mac/Windows with curl)

**Send Single Log:**
```bash
curl -X POST http://localhost:5000/api/logs \
  -H "Content-Type: application/json" \
  -d '{
    "source": "linux-server-01",
    "event_type": "ssh_failed_login",
    "ip_address": "203.0.113.45",
    "username": "root",
    "severity": "high",
    "message": "SSH authentication failure"
  }'
```

**Send Log from File:**
```bash
# Create log.json file
cat > log.json << 'EOF'
{
  "source": "firewall-01",
  "event_type": "port_scan",
  "ip_address": "198.51.100.22",
  "severity": "medium",
  "message": "Port scanning detected"
}
EOF

# Send it
curl -X POST http://localhost:5000/api/logs \
  -H "Content-Type: application/json" \
  -d @log.json
```

---

### Method 3: Python Requests

**Quick Test:**
```python
import requests

log = {
    "source": "web-server",
    "event_type": "sql_injection",
    "ip_address": "192.0.2.50",
    "severity": "high",
    "message": "SQL injection attempt detected"
}

response = requests.post("http://localhost:5000/api/logs", json=log)
print(response.json())
```

---

### Method 4: Postman / Insomnia

**Configuration:**
- **Method:** POST
- **URL:** `http://localhost:5000/api/logs`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "source": "mail-server-01",
  "event_type": "spam_detected",
  "ip_address": "10.0.0.15",
  "severity": "low",
  "message": "Spam email blocked"
}
```

---

## 🔎 Verifying Results

### Method 1: MongoDB Compass (Visual)

**Step 1: Connect to MongoDB**
1. Open MongoDB Compass
2. Connection string: `mongodb://localhost:27017/`
3. Click "Connect"

**Step 2: View Logs**
1. Click on `siem_db` database
2. Click on `logs` collection
3. You should see all sent logs!

**Example Document:**
```json
{
  "_id": ObjectId("65abc123..."),
  "source": "windows-server-01",
  "event_type": "failed_login",
  "ip_address": "192.168.1.100",
  "username": "admin",
  "severity": "medium",
  "message": "Failed login attempt detected",
  "timestamp": ISODate("2026-04-01T17:15:30.000Z")
}
```

**Step 3: View Alerts (After Test 3)**
1. Click on `alerts` collection
2. You should see brute force alert!

**Example Alert:**
```json
{
  "_id": ObjectId("65abc456..."),
  "alert_type": "brute_force_attack",
  "severity": "high",
  "ip_address": "192.168.1.105",
  "username": "administrator",
  "status": "open",
  "description": "Brute force attack detected: 12 failed login attempts",
  "failed_login_count": 12,
  "timestamp": ISODate("2026-04-01T17:16:00.000Z")
}
```

---

### Method 2: MongoDB Shell (mongosh)

```javascript
// Connect to MongoDB
mongosh

// Switch to siem_db
use siem_db

// Count total logs
db.logs.countDocuments()
// Output: 18

// View recent logs
db.logs.find().sort({timestamp: -1}).limit(5).pretty()

// Find failed logins
db.logs.find({event_type: "failed_login"}).count()

// Find logs from specific IP
db.logs.find({ip_address: "192.168.1.100"})

// View all alerts
db.alerts.find().pretty()

// Count open alerts
db.alerts.countDocuments({status: "open"})
```

---

### Method 3: API Endpoints

**Check Health:**
```bash
curl http://localhost:5000/api/health
```

**Get Recent Logs:**
```bash
curl http://localhost:5000/api/logs?page=1&page_size=10
```

**Get Logs by IP:**
```bash
curl "http://localhost:5000/api/logs?ip_address=192.168.1.100"
```

**Get Active Alerts:**
```bash
curl "http://localhost:5000/api/alerts?status=open"
```

**Get Log Statistics:**
```bash
curl http://localhost:5000/api/logs/stats
```

---

### Method 4: Web Dashboard

1. Open browser: `http://localhost:5000/`
2. You should see:
   - Total Logs count
   - Active Alerts count
   - Recent activity chart
   - Log table with live updates

---

## 📊 Understanding the Data Flow

### Log Structure Explained:

**Required Fields:**
```json
{
  "source": "string",        // WHERE: Source system name
  "event_type": "string",    // WHAT: Type of security event
  "ip_address": "string"     // WHO: IP address involved
}
```

**Optional Fields:**
```json
{
  "username": "string",      // WHO: Username involved
  "severity": "low|medium|high",  // HOW BAD: Severity level
  "timestamp": "ISO8601",    // WHEN: Auto-generated if missing
  "message": "string",       // WHY: Human-readable description
  "details": {}              // EXTRA: Any additional JSON data
}
```

**What Happens to Each Field:**
- `source` → Indexed for fast source-based queries
- `event_type` → Indexed, used by detection engine
- `ip_address` → Indexed, used to find attack sources
- `timestamp` → Indexed with TTL (auto-delete after 90 days)
- `severity` → Used for filtering and prioritization
- `username` → Tracked in brute force detection
- `details` → Flexible JSON object for custom data

---

## 🧪 Advanced Testing

### Test 1: Trigger Brute Force Alert

**Scenario:** Simulate an attacker trying multiple password attempts

```powershell
# PowerShell - Send 12 failed logins from same IP
for ($i=1; $i -le 12; $i++) {
    $body = @{
        source = "windows-dc-01"
        event_type = "failed_login"
        ip_address = "192.168.1.200"
        username = "administrator"
        severity = "medium"
    } | ConvertTo-Json
    
    Invoke-RestMethod -Uri "http://localhost:5000/api/logs" `
      -Method Post -Body $body -ContentType "application/json"
    
    Write-Host "Attempt $i/12"
    Start-Sleep -Seconds 1
}

Write-Host "`nWait 30 seconds for detection engine..."
Start-Sleep -Seconds 30

Write-Host "Check MongoDB Compass > alerts collection!"
```

**Expected Result:**
- Alert Type: `brute_force_attack`
- Severity: `high`
- Description: "Brute force attack detected: 12 failed login attempts"

---

### Test 2: High-Severity Events

```python
import requests
import time

high_severity_events = [
    {
        "source": "web-app-01",
        "event_type": "sql_injection",
        "ip_address": "203.0.113.66",
        "severity": "high",
        "message": "SQL injection in /login endpoint"
    },
    {
        "source": "database-01",
        "event_type": "unauthorized_access",
        "ip_address": "198.51.100.88",
        "username": "hacker",
        "severity": "high",
        "message": "Unauthorized database access attempt"
    },
    {
        "source": "firewall-01",
        "event_type": "dos_attack",
        "ip_address": "192.0.2.99",
        "severity": "high",
        "message": "DDoS attack detected - 10000 req/sec"
    }
]

for event in high_severity_events:
    response = requests.post("http://localhost:5000/api/logs", json=event)
    print(f"Sent: {event['event_type']} - {response.status_code}")
    time.sleep(1)
```

---

### Test 3: Diverse Log Sources

```python
import requests
import random
import time

sources = ["web-server", "mail-server", "firewall", "vpn-gateway", "database"]
event_types = ["login", "logout", "file_access", "network_traffic", "error"]
ips = [f"192.168.1.{i}" for i in range(1, 51)]

for i in range(20):
    log = {
        "source": random.choice(sources),
        "event_type": random.choice(event_types),
        "ip_address": random.choice(ips),
        "severity": random.choice(["low", "medium", "high"])
    }
    
    response = requests.post("http://localhost:5000/api/logs", json=log)
    print(f"Log {i+1}/20: {response.status_code}")
    time.sleep(0.5)
```

---

## 📈 Verification Checklist

After running tests, verify:

### ✅ MongoDB Compass Checks:
- [ ] `siem_db` database exists
- [ ] `logs` collection has documents
- [ ] Each log has `timestamp`, `source`, `event_type`, `ip_address`
- [ ] `_id` field is ObjectId (auto-generated)
- [ ] Indexes exist (check Indexes tab)
- [ ] After brute force test: `alerts` collection has alert

### ✅ API Checks:
- [ ] `GET /api/health` returns 200 with "healthy"
- [ ] `POST /api/logs` returns 201 with `log_id`
- [ ] `GET /api/logs` returns array of logs
- [ ] `GET /api/alerts` returns alerts (after Test 3)
- [ ] `GET /api/logs/stats` shows correct counts

### ✅ Dashboard Checks:
- [ ] Open `http://localhost:5000/`
- [ ] Total Logs count updates
- [ ] Recent logs table shows entries
- [ ] After alert: Alert count increases
- [ ] Charts display data

---

## 🎓 Understanding Detection Rules

### Current Rule: Brute Force Detection

**Trigger Condition:**
```
IF failed_login_count >= 10 
   AND within 2 minutes (120 seconds)
   FROM same ip_address
   THEN create alert
```

**How it works:**
1. Detection engine runs every 30 seconds (configurable)
2. Queries MongoDB for failed_login events in last 2 minutes
3. Groups by IP address and username
4. Counts attempts per IP
5. If count >= 10, creates alert in `alerts` collection
6. Broadcasts alert via WebSocket to dashboard

**MongoDB Query (actual):**
```javascript
db.logs.aggregate([
  {
    $match: {
      event_type: 'failed_login',
      timestamp: { $gte: ISODate('2026-04-01T17:14:00Z') }
    }
  },
  {
    $group: {
      _id: { ip_address: '$ip_address', username: '$username' },
      count: { $sum: 1 },
      first_attempt: { $min: '$timestamp' },
      last_attempt: { $max: '$timestamp' }
    }
  },
  {
    $match: { count: { $gte: 10 } }
  }
])
```

---

## 🔧 Troubleshooting

### Issue: "Connection refused"
**Solution:** Make sure SIEM is running
```bash
cd backend
python app.py
```

### Issue: "No module named 'requests'"
**Solution:** Install requests
```bash
pip install requests
```

### Issue: "Logs not appearing in MongoDB"
**Solution:** Check response status
```python
response = requests.post(...)
print(response.status_code)  # Should be 201
print(response.text)  # Check error message
```

### Issue: "Alert not created"
**Solution:**
1. Make sure you sent 10+ failed_login events
2. Wait 30 seconds for detection engine
3. Check scheduler is running in app.py output

---

## 📚 Example Use Cases

### Use Case 1: Monitor Failed Logins
```python
# Send failed login
requests.post("http://localhost:5000/api/logs", json={
    "source": "auth-server",
    "event_type": "failed_login",
    "ip_address": "203.0.113.50",
    "username": "admin",
    "severity": "medium"
})

# Query all failed logins
response = requests.get("http://localhost:5000/api/logs?event_type=failed_login")
logs = response.json()['logs']
print(f"Total failed logins: {len(logs)}")
```

### Use Case 2: Track High-Severity Events
```javascript
// In MongoDB Compass Filter:
{ "severity": "high" }

// Or in mongosh:
db.logs.find({severity: "high"}).count()
```

### Use Case 3: Find Suspicious IPs
```javascript
// Top IPs by log count
db.logs.aggregate([
  { $group: { _id: "$ip_address", count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 10 }
])
```

---

## 🎉 Success Indicators

Your SIEM is working correctly when:

✅ **API Accepts Logs:**
- POST requests return 201 status
- Response includes `log_id`
- No error messages

✅ **MongoDB Stores Data:**
- Logs visible in Compass
- Proper field types (Date, String, etc.)
- Indexes present

✅ **Detection Works:**
- After 12 failed logins + 30 sec wait
- Alert appears in `alerts` collection
- Alert has correct IP and count

✅ **Real-time Updates:**
- Dashboard shows new logs immediately
- Charts update automatically
- WebSocket connection established

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Start SIEM | `cd backend && python app.py` |
| Run Tests | `cd backend && python test_siem.py` |
| Check Health | `curl http://localhost:5000/api/health` |
| Send Log | `curl -X POST http://localhost:5000/api/logs -H "Content-Type: application/json" -d '{...}'` |
| View Dashboard | Open browser: `http://localhost:5000/` |
| Connect Compass | `mongodb://localhost:27017/` |
| MongoDB Shell | `mongosh` then `use siem_db` |

---

## 🚀 Next Steps

1. ✅ Run the test script: `python test_siem.py`
2. ✅ Verify in MongoDB Compass
3. ✅ Check web dashboard
4. ✅ Try custom log scenarios
5. ✅ Explore API endpoints
6. 📖 Add custom detection rules (see services/detection_engine.py)
7. 🎨 Customize dashboard (see frontend/)

---

**🎯 You now have a fully functional SIEM platform!**

Need help? Check the other documentation files:
- `MONGODB_SETUP_GUIDE.md` - MongoDB configuration
- `MONGODB_COMPASS_REFERENCE.md` - Query examples
- `README.md` - Full project documentation
