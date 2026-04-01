// MongoDB Initialization Script
// Run this script with: mongosh < init_mongodb.js

// Switch to SIEM database
use siem_db;

print("🔐 SIEM Platform - Database Initialization");
print("===========================================\n");

// Create logs collection with validation
db.createCollection("logs", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["timestamp", "source", "event_type", "ip_address"],
      properties: {
        timestamp: { bsonType: "date" },
        source: { bsonType: "string" },
        event_type: { bsonType: "string" },
        ip_address: { bsonType: "string" }
      }
    }
  }
});

// Create indexes for logs
db.logs.createIndex({ "timestamp": -1, "event_type": 1 });
db.logs.createIndex({ "ip_address": 1 });
db.logs.createIndex({ "source": 1 });
db.logs.createIndex({ "event_type": 1 });
db.logs.createIndex({ "timestamp": 1 }, { expireAfterSeconds: 7776000 }); // 90 days TTL

print("✓ Logs collection created with indexes");

// Create alerts collection
db.createCollection("alerts");

// Create indexes for alerts
db.alerts.createIndex({ "timestamp": -1 });
db.alerts.createIndex({ "ip_address": 1 });
db.alerts.createIndex({ "status": 1 });
db.alerts.createIndex({ "severity": 1 });
db.alerts.createIndex({ "status": 1, "severity": 1, "timestamp": -1 });

print("✓ Alerts collection created with indexes");

// Create users collection
db.createCollection("users");

// Create indexes for users
db.users.createIndex({ "username": 1 }, { unique: true });
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "role": 1 });

print("✓ Users collection created with indexes");

// Insert default admin user (password: admin123)
db.users.insertOne({
  username: "admin",
  email: "admin@siem.local",
  password_hash: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5LS2LZq3s0BKi",
  role: "admin",
  permissions: ["view_logs", "view_alerts", "export_data", "manage_users"],
  created_at: new Date(),
  last_login: null,
  is_active: true
});

print("✓ Default admin user created (username: admin, password: admin123)");

// Insert sample logs
print("\nInserting sample logs...");

const sampleLogs = [
  {
    timestamp: new Date(),
    source: "windows-server-01",
    source_type: "windows",
    event_type: "failed_login",
    ip_address: "192.168.1.100",
    username: "admin",
    severity: "medium",
    details: {
      event_id: 4625,
      logon_type: 3,
      failure_reason: "Unknown user name or bad password"
    }
  },
  {
    timestamp: new Date(),
    source: "linux-web-01",
    source_type: "linux",
    event_type: "successful_login",
    ip_address: "10.0.0.45",
    username: "ubuntu",
    severity: "low",
    details: {
      session_id: "12345",
      auth_method: "publickey",
      port: 22
    }
  },
  {
    timestamp: new Date(),
    source: "firewall-01",
    source_type: "firewall",
    event_type: "firewall_block",
    ip_address: "45.123.67.89",
    severity: "high",
    details: {
      destination_ip: "192.168.1.50",
      destination_port: 445,
      protocol: "TCP",
      rule_name: "BLOCK_SMB_EXTERNAL"
    }
  }
];

db.logs.insertMany(sampleLogs);

print("✓ Sample logs inserted");

// Show statistics
print("\nDatabase Statistics:");
print("-------------------");
print("Logs count: " + db.logs.countDocuments());
print("Alerts count: " + db.alerts.countDocuments());
print("Users count: " + db.users.countDocuments());

print("\n===========================================");
print("✅ MongoDB initialization complete!");
print("===========================================\n");
