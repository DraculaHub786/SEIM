"""
Sample Log Data Generator
Generates realistic log data for testing the SIEM platform
"""

import requests
import time
import random
from datetime import datetime, timedelta

API_URL = "http://localhost:5000/api/logs"

# Sample data
sources = [
    "windows-server-01",
    "windows-server-02",
    "linux-web-01",
    "linux-web-02",
    "firewall-01",
    "firewall-02",
    "file-server-01"
]

event_types = {
    "failed_login": ["admin", "administrator", "root", "user1"],
    "successful_login": ["ubuntu", "admin", "jdoe", "service"],
    "file_access": ["admin", "jdoe", "developer"],
    "firewall_block": ["external"]
}

# IP addresses
internal_ips = [
    "192.168.1.100",
    "192.168.1.105",
    "192.168.1.110",
    "10.0.0.45",
    "10.0.0.50",
    "172.16.0.20"
]

external_ips = [
    "45.123.67.89",
    "123.45.67.89",
    "203.0.113.42",
    "198.51.100.23"
]

def generate_log(event_type, ip_address, source, username):
    """Generate a log entry"""
    log = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": source,
        "event_type": event_type,
        "ip_address": ip_address,
        "username": username,
        "severity": random.choice(["low", "medium", "high"])
    }
    
    # Add event-specific details
    if event_type == "failed_login":
        log["details"] = {
            "event_id": 4625,
            "logon_type": random.choice([2, 3, 10]),
            "failure_reason": "Unknown user name or bad password"
        }
    elif event_type == "successful_login":
        log["details"] = {
            "session_id": str(random.randint(10000, 99999)),
            "auth_method": random.choice(["password", "publickey"]),
            "port": random.choice([22, 3389])
        }
    elif event_type == "file_access":
        log["details"] = {
            "file_path": random.choice([
                "C:\\Confidential\\passwords.xlsx",
                "C:\\Users\\Admin\\Documents\\sensitive.docx",
                "/etc/shadow",
                "/var/log/auth.log"
            ]),
            "action": random.choice(["read", "write", "delete"])
        }
    elif event_type == "firewall_block":
        log["details"] = {
            "destination_ip": random.choice(internal_ips),
            "destination_port": random.choice([445, 3389, 22, 80, 443]),
            "protocol": "TCP",
            "rule_name": "BLOCK_EXTERNAL"
        }
    
    return log

def send_log(log):
    """Send log to API"""
    try:
        response = requests.post(API_URL, json=log, timeout=5)
        return response.status_code == 201
    except Exception as e:
        print(f"Error sending log: {e}")
        return False

def generate_normal_traffic(count=50):
    """Generate normal traffic logs"""
    print(f"\n📝 Generating {count} normal traffic logs...")
    
    for i in range(count):
        event_type = random.choice(list(event_types.keys()))
        username = random.choice(event_types[event_type])
        source = random.choice(sources)
        
        # 80% internal IPs, 20% external
        ip_address = random.choice(internal_ips if random.random() < 0.8 else external_ips)
        
        log = generate_log(event_type, ip_address, source, username)
        
        if send_log(log):
            print(f"  ✓ [{i+1}/{count}] {event_type} from {ip_address}")
        else:
            print(f"  ✗ [{i+1}/{count}] Failed to send")
        
        time.sleep(0.2)  # Small delay

def generate_brute_force_attack():
    """Generate brute force attack (triggers alert)"""
    print("\n🚨 Generating brute force attack simulation...")
    
    attack_ip = "192.168.1.105"
    target_source = "windows-server-01"
    
    for i in range(15):  # 15 failed logins
        log = generate_log("failed_login", attack_ip, target_source, "administrator")
        
        if send_log(log):
            print(f"  ⚠️  [{i+1}/15] Failed login from {attack_ip}")
        else:
            print(f"  ✗ [{i+1}/15] Failed to send")
        
        time.sleep(3)  # 3 second delay between attempts
    
    print("  ⏳ Waiting 30 seconds for detection engine...")
    time.sleep(30)
    print("  ✅ Attack simulation complete. Check alerts!")

def generate_mixed_traffic(duration_seconds=300):
    """Generate continuous mixed traffic"""
    print(f"\n🔄 Generating mixed traffic for {duration_seconds} seconds...")
    
    start_time = time.time()
    count = 0
    
    while time.time() - start_time < duration_seconds:
        event_type = random.choice(list(event_types.keys()))
        username = random.choice(event_types[event_type])
        source = random.choice(sources)
        ip_address = random.choice(internal_ips if random.random() < 0.8 else external_ips)
        
        log = generate_log(event_type, ip_address, source, username)
        
        if send_log(log):
            count += 1
            print(f"  ✓ [{count}] {event_type} from {ip_address}")
        
        # Random delay between 1-5 seconds
        time.sleep(random.uniform(1, 5))
    
    print(f"\n✅ Generated {count} logs in {duration_seconds} seconds")

def main():
    """Main menu"""
    print("=" * 60)
    print("🔐 SIEM Platform - Sample Log Generator")
    print("=" * 60)
    print("\nOptions:")
    print("1. Generate normal traffic (50 logs)")
    print("2. Generate brute force attack (15 failed logins)")
    print("3. Generate mixed traffic (5 minutes)")
    print("4. Generate all (normal + attack)")
    print("5. Exit")
    print()
    
    choice = input("Select option (1-5): ")
    
    if choice == "1":
        generate_normal_traffic(50)
    elif choice == "2":
        generate_brute_force_attack()
    elif choice == "3":
        generate_mixed_traffic(300)
    elif choice == "4":
        generate_normal_traffic(50)
        generate_brute_force_attack()
    elif choice == "5":
        print("Goodbye!")
        return
    else:
        print("Invalid choice!")
    
    print("\n" + "=" * 60)
    print("✅ Log generation complete!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
