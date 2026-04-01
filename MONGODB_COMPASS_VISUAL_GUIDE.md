# 🔌 MongoDB Compass Connection - Step-by-Step Visual Guide

## 📥 Step 1: Open MongoDB Compass

1. Launch **MongoDB Compass** from your applications
2. You'll see the connection screen

---

## 🔗 Step 2: Enter Connection String

### Connection Screen Layout:

```
┌────────────────────────────────────────────────────────────┐
│  MongoDB Compass                                      [X]   │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  New Connection                                              │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ URI                                                 │    │
│  │                                                     │    │
│  │  mongodb://localhost:27017/                        │◄─── PASTE HERE
│  │                                                     │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Advanced Connection Options ▼                              │
│                                                              │
│         [Save & Connect]  [Connect]                         │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

### What to Enter:

**In the URI field, paste:**
```
mongodb://localhost:27017/
```

**That's it!** No username, password, or other settings needed for local development.

---

## ✅ Step 3: Click Connect

Click the **Connect** button

### What Happens:
```
Connecting to MongoDB...
  ↓
Testing connection...
  ↓
✓ Connected successfully!
  ↓
Loading databases...
```

---

## 🗄️ Step 4: View Your Database

After connecting, you'll see the database list:

```
┌────────────────────────────────────────────────────────────┐
│  MongoDB Compass                                      [X]   │
├──────────────┬─────────────────────────────────────────────┤
│              │                                              │
│ Databases ▼  │  Database: siem_db                          │
│              │                                              │
│ ► admin      │  Collections:                               │
│ ► config     │                                              │
│ ▼ siem_db    │  ┌────────────────────────────────────┐    │
│   • logs     │  │ 📄 logs                             │    │
│   • alerts   │  │    Documents: 0                     │    │
│   • users    │  │    Avg Doc Size: --                 │    │
│              │  └────────────────────────────────────┘    │
│              │                                              │
│              │  ┌────────────────────────────────────┐    │
│              │  │ 🚨 alerts                           │    │
│              │  │    Documents: 0                     │    │
│              │  │    Avg Doc Size: --                 │    │
│              │  └────────────────────────────────────┘    │
│              │                                              │
│              │  ┌────────────────────────────────────┐    │
│              │  │ 👤 users                            │    │
│              │  │    Documents: 1                     │◄── Admin user
│              │  │    Avg Doc Size: 234 B              │    │
│              │  └────────────────────────────────────┘    │
│              │                                              │
└──────────────┴─────────────────────────────────────────────┘
```

**Note:** If you don't see `siem_db`, run the SIEM application first:
```cmd
cd backend
python app.py
```

---

## 📊 Step 5: Explore Collections

### Click on "logs" Collection:

```
┌────────────────────────────────────────────────────────────┐
│  siem_db > logs                                       [X]   │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  [Documents] [Aggregations] [Schema] [Indexes] [Validation] │
│                                                              │
│  Filter: { event_type: "failed_login" }    [Find] [Reset]  │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ No documents found                                  │    │
│  │                                                     │    │
│  │ Send some logs via the API to see them here!      │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

### After Sending Logs:

```
┌────────────────────────────────────────────────────────────┐
│  siem_db > logs                                       [X]   │
├────────────────────────────────────────────────────────────┤
│  Filter: { }                               [Find] [Reset]  │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ _id: ObjectId("66abc123...")                        │    │
│  │ timestamp: 2026-04-01T15:30:00.000Z                │    │
│  │ source: "windows-server-01"                        │    │
│  │ event_type: "failed_login"                         │    │
│  │ ip_address: "192.168.1.100"                        │    │
│  │ username: "admin"                                   │    │
│  │ severity: "medium"                                  │    │
│  │ details: {                                          │    │
│  │   event_id: 4625                                    │    │
│  │   logon_type: 3                                     │    │
│  │ }                                                   │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Showing 1-20 of 245 documents                    [1][2][3] │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

---

## 🔍 Step 6: Run Queries

### Using the Filter Bar:

**Example 1: Find Failed Logins**
```javascript
Filter: { "event_type": "failed_login" }
```

**Example 2: Find Logs from Specific IP**
```javascript
Filter: { "ip_address": "192.168.1.100" }
```

**Example 3: Recent Logs (Last Hour)**
```javascript
Filter: { "timestamp": { "$gte": new Date(Date.now() - 3600000) } }
```

**Example 4: High Severity Events**
```javascript
Filter: { "severity": "high" }
```

### Filter Bar Interface:

```
┌───────────────────────────────────────────────────────┐
│ Filter ▼                                               │
│                                                        │
│  {                                                     │
│    "event_type": "failed_login"                       │◄── Type your query
│  }                                                     │
│                                                        │
│        [Options ▼]  [Reset]  [Find]                   │
└───────────────────────────────────────────────────────┘
```

---

## 📈 Step 7: View Indexes

Click the **Indexes** tab:

```
┌────────────────────────────────────────────────────────────┐
│  siem_db > logs > Indexes                             [X]   │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Name: _id_                                          │    │
│  │ Keys: { _id: 1 }                                    │    │
│  │ Properties: Default                                │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Name: timestamp_-1_event_type_1                    │    │
│  │ Keys: { timestamp: -1, event_type: 1 }             │    │
│  │ Properties: Compound                               │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Name: ip_address_1                                  │    │
│  │ Keys: { ip_address: 1 }                            │    │
│  │ Properties: Single field                           │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Name: timestamp_1                                   │    │
│  │ Keys: { timestamp: 1 }                             │    │
│  │ Properties: TTL (expireAfterSeconds: 7776000)      │◄── 90 days
│  └────────────────────────────────────────────────────┘    │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

---

## 🎯 Step 8: View Schema

Click the **Schema** tab to analyze your data structure:

```
┌────────────────────────────────────────────────────────────┐
│  siem_db > logs > Schema                              [X]   │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  Analyzing schema... [■■■■■■■■■■] 100%                     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │ Field Name        │ Type        │ % Present         │    │
│  ├──────────────────┼─────────────┼──────────────────┤    │
│  │ _id               │ ObjectId    │ 100%              │    │
│  │ timestamp         │ Date        │ 100%              │    │
│  │ source            │ String      │ 100%              │    │
│  │ event_type        │ String      │ 100%              │    │
│  │ ip_address        │ String      │ 100%              │    │
│  │ username          │ String      │ 95%               │    │
│  │ severity          │ String      │ 100%              │    │
│  │ details           │ Object      │ 80%               │    │
│  └──────────────────┴─────────────┴──────────────────┘    │
│                                                              │
│  [Export Schema]                                            │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

---

## 🧮 Step 9: Run Aggregations

Click the **Aggregations** tab for complex queries:

```
┌────────────────────────────────────────────────────────────┐
│  siem_db > logs > Aggregations                        [X]   │
├────────────────────────────────────────────────────────────┤
│                                                              │
│  Stage 1: $match                                            │
│  ┌────────────────────────────────────────────────────┐    │
│  │ { "event_type": "failed_login" }                   │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  [+ Add Stage]                                              │
│                                                              │
│  Stage 2: $group                                            │
│  ┌────────────────────────────────────────────────────┐    │
│  │ {                                                   │    │
│  │   _id: "$ip_address",                              │    │
│  │   count: { $sum: 1 }                               │    │
│  │ }                                                   │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  [+ Add Stage]                                              │
│                                                              │
│  Stage 3: $sort                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │ { "count": -1 }                                     │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  Results: (15 documents)                       [Run] [Save] │
│                                                              │
└────────────────────────────────────────────────────────────┘
```

---

## 💾 Step 10: Export Data

To export collection data:

```
1. Click "Collection" menu at top
2. Select "Export Collection"
3. Choose format:
   
   ┌────────────────────────────────────┐
   │ Export Collection                   │
   ├────────────────────────────────────┤
   │                                     │
   │ Format:                             │
   │ ( ) JSON  (•) CSV                  │
   │                                     │
   │ Query: { }                          │
   │                                     │
   │ Fields to export:                   │
   │ [x] _id                             │
   │ [x] timestamp                       │
   │ [x] source                          │
   │ [x] event_type                      │
   │ [x] ip_address                      │
   │                                     │
   │ [Cancel]        [Export]            │
   └────────────────────────────────────┘

4. Choose save location
5. Click Export
```

---

## 🎨 Compass Interface Overview

```
┌────────────────────────────────────────────────────────────┐
│  MongoDB Compass                    [_] [□] [X]            │
├──────────────┬─────────────────────────────────────────────┤
│              │  Cluster: localhost:27017                   │
│ Connections  ├─────────────────────────────────────────────┤
│              │  Performance  Databases  Cluster            │
│ • localhost  │                                              │
│              │  ┌─────────────────────────────────────┐   │
│ Databases ▼  │  │ Database Name    Collections  Size  │   │
│              │  ├─────────────────────────────────────┤   │
│ ▼ siem_db    │  │ siem_db          3           1.2 MB │   │
│   • logs     │  │ admin            1           32 KB  │   │
│   • alerts   │  │ config           1           16 KB  │   │
│   • users    │  └─────────────────────────────────────┘   │
│              │                                              │
│              │  [Create Database]                          │
│              │                                              │
└──────────────┴─────────────────────────────────────────────┘
```

---

## 🔄 Real-Time Monitoring

To see new logs in real-time:

1. Keep MongoDB Compass open
2. Run your SIEM application
3. Send test logs via API
4. Click the **refresh button** (🔄) in Compass
5. Watch documents appear!

### Refresh Options:

```
Auto-refresh: Off ▼     [🔄 Refresh Now]
```

Enable auto-refresh to automatically see new documents.

---

## 📱 Saved Connections

### Save Your Connection for Quick Access:

1. Click **Saved Connections** in sidebar
2. Click **Add Connection**
3. Enter details:

```
┌────────────────────────────────────┐
│ Save Connection                     │
├────────────────────────────────────┤
│                                     │
│ Connection Name:                    │
│ ┌────────────────────────────────┐ │
│ │ SIEM Database (Local)          │ │
│ └────────────────────────────────┘ │
│                                     │
│ Connection String:                  │
│ ┌────────────────────────────────┐ │
│ │ mongodb://localhost:27017/     │ │
│ └────────────────────────────────┘ │
│                                     │
│ Favorite Color: 🟢 Green            │
│                                     │
│ [Cancel]           [Save]           │
└────────────────────────────────────┘
```

4. Click **Save**
5. Now you can connect with one click!

---

## ⚡ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| New Tab | `Ctrl + T` |
| Close Tab | `Ctrl + W` |
| Refresh | `Ctrl + R` |
| Toggle Sidebar | `Ctrl + B` |
| Find in Docs | `Ctrl + F` |
| Open Settings | `Ctrl + ,` |

---

## ✅ Connection Success Checklist

- [x] MongoDB service is running
- [x] Compass shows "Connected" status
- [x] `siem_db` database is visible
- [x] Three collections exist: logs, alerts, users
- [x] Indexes are present (check Indexes tab)
- [x] Can run queries in Filter bar
- [x] Schema analysis works

---

## 🎓 Pro Tips

1. **Use Aggregation Builder** for complex queries
2. **Enable Auto-Refresh** when monitoring live data
3. **Save Favorite Queries** for quick access
4. **Export Regular Backups** of important data
5. **Check Explain Plan** to optimize queries
6. **Use Schema Tab** to understand data structure
7. **Create Bookmarks** for important views

---

## 🆘 Common Issues

### Can't See Database?
✅ Run SIEM app first: `python app.py`  
✅ Click refresh button in Compass  
✅ Check connection string is correct  

### Collections Are Empty?
✅ Send test logs via API  
✅ Check application is running  
✅ Verify no errors in app console  

### Connection Timeout?
✅ Ensure MongoDB service is running  
✅ Check port 27017 is listening  
✅ Try `127.0.0.1` instead of `localhost`  

---

**🎉 You're now ready to use MongoDB Compass with your SIEM platform!**

**Connection String:** `mongodb://localhost:27017/`  
**Database:** `siem_db`  
**Collections:** logs, alerts, users

**Happy monitoring!** 🔐
