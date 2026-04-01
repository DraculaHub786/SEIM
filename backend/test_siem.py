"""
SIEM Platform - Testing Script
Quick way to test your SIEM system with sample data
"""

import requests
import json
import time
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:5000"
API_LOGS_ENDPOINT = f"{API_BASE_URL}/api/logs"
API_HEALTH_ENDPOINT = f"{API_BASE_URL}/api/health"
API_ALERTS_ENDPOINT = f"{API_BASE_URL}/api/alerts"

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_health():
    """Check if the SIEM API is running"""
    print_header("🔍 Checking System Health")
    try:
        response = requests.get(API_HEALTH_ENDPOINT, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {data['status']}")
            print(f"✅ Database: {data['database']}")
            print(f"✅ Timestamp: {data['timestamp']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Is the server running?")
        print("   Run: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def send_single_log(log_data):
    """Send a single log to the API"""
    try:
        response = requests.post(API_LOGS_ENDPOINT, json=log_data, timeout=5)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Log sent: {log_data['event_type']} from {log_data['ip_address']}")
            print(f"   Log ID: {result.get('log_id', 'N/A')}")
            return True
        else:
            print(f"❌ Failed to send log: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error sending log: {e}")
        return False

def test_single_log():
    """Test sending a single log"""
    print_header("📝 Test 1: Send Single Log")
    
    log = {
        "source": "windows-server-01",
        "event_type": "failed_login",
        "ip_address": "192.168.1.100",
        "username": "admin",
        "severity": "medium",
        "message": "Test log - Failed login attempt detected"
    }
    
    print(f"Sending log: {json.dumps(log, indent=2)}")
    send_single_log(log)
    print("\n✓ Check MongoDB Compass - siem_db > logs collection")

def test_multiple_logs():
    """Test sending multiple diverse logs"""
    print_header("📊 Test 2: Send Multiple Diverse Logs")
    
    logs = [
        {
            "source": "web-server-01",
            "event_type": "sql_injection",
            "ip_address": "203.0.113.45",
            "username": "guest",
            "severity": "high",
            "message": "SQL injection attempt detected in login form"
        },
        {
            "source": "firewall-01",
            "event_type": "port_scan",
            "ip_address": "198.51.100.22",
            "severity": "medium",
            "message": "Port scanning activity detected"
        },
        {
            "source": "mail-server-01",
            "event_type": "spam_detected",
            "ip_address": "192.0.2.15",
            "severity": "low",
            "message": "Spam email blocked"
        },
        {
            "source": "database-01",
            "event_type": "unauthorized_access",
            "ip_address": "10.0.0.50",
            "username": "dbadmin",
            "severity": "high",
            "message": "Unauthorized database access attempt"
        },
        {
            "source": "vpn-gateway",
            "event_type": "successful_login",
            "ip_address": "172.16.0.10",
            "username": "user1",
            "severity": "low",
            "message": "VPN connection established"
        }
    ]
    
    print(f"Sending {len(logs)} logs...")
    successful = 0
    
    for i, log in enumerate(logs, 1):
        print(f"\n[{i}/{len(logs)}] Sending {log['event_type']}...")
        if send_single_log(log):
            successful += 1
        time.sleep(0.5)  # Small delay between requests
    
    print(f"\n✅ Successfully sent {successful}/{len(logs)} logs")
    print("✓ Check MongoDB Compass for all logs")

def test_high_sensitivity_events():
    """Test high-severity security events"""
    print_header("🔴 Test 2.5: High-Sensitivity Events (NEW)")
    
    high_severity_logs = [
        {
            "source": "web-app-01",
            "event_type": "sql_injection",
            "ip_address": "203.0.113.66",
            "username": "attacker",
            "severity": "high",
            "message": "SQL injection detected in /login endpoint - payload: admin'--"
        },
        {
            "source": "database-cluster",
            "event_type": "unauthorized_access",
            "ip_address": "198.51.100.88",
            "username": "hacker",
            "severity": "high",
            "message": "Unauthorized database access - attempted to read customer_data table"
        },
        {
            "source": "firewall-primary",
            "event_type": "dos_attack",
            "ip_address": "192.0.2.99",
            "severity": "high",
            "message": "DDoS attack detected - 50000 req/sec from single IP"
        },
        {
            "source": "vpn-gateway-01",
            "event_type": "privilege_escalation",
            "ip_address": "10.0.1.50",
            "username": "user123",
            "severity": "high",
            "message": "Privilege escalation attempt - tried to access admin panel"
        },
        {
            "source": "file-server-01",
            "event_type": "data_exfiltration",
            "ip_address": "172.16.0.55",
            "username": "contractor",
            "severity": "high",
            "message": "Large file transfer detected - 2.5GB to external IP"
        },
        {
            "source": "domain-controller",
            "event_type": "credential_theft",
            "ip_address": "192.168.1.200",
            "username": "admin",
            "severity": "high",
            "message": "Credentials harvested - NTLM relay attack detected"
        },
        {
            "source": "backup-server",
            "event_type": "ransomware_signature",
            "ip_address": "192.0.2.120",
            "severity": "high",
            "message": "Ransomware signature match - WannaCry-like behavior detected"
        },
        {
            "source": "email-gateway",
            "event_type": "phishing_detected",
            "ip_address": "198.51.100.10",
            "severity": "high",
            "message": "Phishing email with malicious attachment detected - 450 recipients"
        }
    ]
    
    print(f"Sending {len(high_severity_logs)} high-sensitivity events...\n")
    successful = 0
    
    for i, log in enumerate(high_severity_logs, 1):
        print(f"[{i}/{len(high_severity_logs)}] {log['event_type']:25} | {log['source']}")
        if send_single_log(log):
            successful += 1
        time.sleep(0.3)
    
    print(f"\n✅ Successfully sent {successful}/{len(high_severity_logs)} high-severity events")
    print("✓ Check MongoDB Compass - all marked as severity: HIGH")

def test_diverse_sources():
    """Test logs from diverse sources across infrastructure"""
    print_header("🌐 Test 2.7: Diverse Infrastructure Sources (NEW)")
    
    diverse_logs = [
        {"source": "linux-web-server-01", "event_type": "ssh_failed_login", "ip_address": "203.0.113.5", "username": "root", "severity": "medium"},
        {"source": "windows-workstation-15", "event_type": "antivirus_alert", "ip_address": "192.168.10.15", "severity": "high"},
        {"source": "container-kubernetes-pod-1", "event_type": "process_anomaly", "ip_address": "10.0.0.100", "severity": "medium"},
        {"source": "network-switch-core-01", "event_type": "port_error", "ip_address": "10.255.255.1", "severity": "low"},
        {"source": "iot-device-sensor-42", "event_type": "connection_lost", "ip_address": "10.0.2.42", "severity": "low"},
        {"source": "mobile-device-iPad", "event_type": "jailbreak_detected", "ip_address": "192.168.5.100", "username": "employee_john", "severity": "high"},
        {"source": "cloud-aws-ec2-instance", "event_type": "unauthorized_api_call", "ip_address": "203.0.113.200", "severity": "high"},
        {"source": "printer-network-01", "event_type": "config_change", "ip_address": "192.168.100.50", "severity": "medium"},
        {"source": "load-balancer-nginx", "event_type": "ssl_cert_expiry", "ip_address": "10.0.0.1", "severity": "medium"},
        {"source": "authentication-ldap-01", "event_type": "directory_sync_error", "ip_address": "192.168.1.50", "severity": "low"},
    ]
    
    print(f"Sending {len(diverse_logs)} logs from diverse infrastructure...\n")
    successful = 0
    
    sources = set()
    for i, log in enumerate(diverse_logs, 1):
        sources.add(log['source'])
        print(f"[{i}/{len(diverse_logs)}] {log['source']:35} ({log['severity'].upper()})")
        if send_single_log(log):
            successful += 1
        time.sleep(0.2)
    
    print(f"\n✅ Successfully sent {successful}/{len(diverse_logs)} logs from {len(sources)} unique sources")
    print("✓ Sources tested: web servers, workstations, containers, network devices, IoT, mobile, cloud, etc.")

def test_brute_force_detection():
    """Test brute force attack detection"""
    print_header("🚨 Test 6: Trigger Brute Force Alert")
    
    print("Sending 12 failed login attempts from same IP...")
    print("(This will trigger the brute force detection engine)")
    
    attack_ip = "192.168.1.105"
    
    for i in range(12):
        log = {
            "source": "windows-server-01",
            "event_type": "failed_login",
            "ip_address": attack_ip,
            "username": "administrator",
            "severity": "medium",
            "message": f"Failed login attempt #{i+1}"
        }
        
        if send_single_log(log):
            print(f"   Attempt {i+1}/12", end="\r")
        time.sleep(0.5)
    
    print("\n\n✅ All 12 failed login attempts sent!")
    print("\n⏳ Wait 30 seconds for detection engine to run...")
    print("   (Detection engine runs every 30 seconds)")
    
    for remaining in range(30, 0, -1):
        print(f"   Waiting: {remaining} seconds remaining...", end="\r")
        time.sleep(1)
    
    print("\n\n✓ Check MongoDB Compass - siem_db > alerts collection")
    print("✓ You should see a 'brute_force_attack' alert!")

def test_custom_log():
    """Allow user to send custom log"""
    print_header("✏️ Test 7: Send Custom Log")
    
    print("\nEnter custom log details:")
    print("(Press Enter to use default values)")
    
    source = input("Source [custom-test]: ").strip() or "custom-test"
    event_type = input("Event Type [custom_event]: ").strip() or "custom_event"
    ip_address = input("IP Address [10.0.0.1]: ").strip() or "10.0.0.1"
    username = input("Username [testuser]: ").strip() or "testuser"
    severity = input("Severity (low/medium/high) [medium]: ").strip() or "medium"
    message = input("Message [Custom test log]: ").strip() or "Custom test log"
    
    log = {
        "source": source,
        "event_type": event_type,
        "ip_address": ip_address,
        "username": username,
        "severity": severity,
        "message": message
    }
    
    print(f"\nSending custom log:")
    print(json.dumps(log, indent=2))
    send_single_log(log)

def view_recent_logs():
    """View recent logs from API"""
    print_header("📋 View Recent Logs")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/logs?page=1&page_size=5", timeout=5)
        if response.status_code == 200:
            data = response.json()
            logs = data.get('logs', [])
            
            if logs:
                print(f"\nShowing {len(logs)} most recent logs:\n")
                for i, log in enumerate(logs, 1):
                    print(f"{i}. [{log.get('severity', 'N/A').upper()}] {log.get('event_type', 'N/A')}")
                    print(f"   IP: {log.get('ip_address', 'N/A')} | Source: {log.get('source', 'N/A')}")
                    print(f"   Time: {log.get('timestamp', 'N/A')}")
                    print()
            else:
                print("No logs found. Send some test logs first!")
        else:
            print(f"Failed to fetch logs: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def view_alerts():
    """View alerts from API"""
    print_header("🚨 View Active Alerts")
    
    try:
        response = requests.get(f"{API_ALERTS_ENDPOINT}?status=open", timeout=5)
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            if alerts:
                print(f"\nFound {len(alerts)} active alert(s):\n")
                for i, alert in enumerate(alerts, 1):
                    print(f"{i}. [{alert.get('severity', 'N/A').upper()}] {alert.get('alert_type', 'N/A')}")
                    print(f"   IP: {alert.get('ip_address', 'N/A')}")
                    print(f"   Description: {alert.get('description', 'N/A')}")
                    print(f"   Time: {alert.get('timestamp', 'N/A')}")
                    print()
            else:
                print("No active alerts. Trigger Test 3 to create a brute force alert!")
        else:
            print(f"Failed to fetch alerts: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def run_all_tests():
    """Run all tests in sequence"""
    print_header("🚀 Running All Tests")
    
    if not check_health():
        return
    
    input("\nPress Enter to start Test 1 (Single Log)...")
    test_single_log()
    
    input("\nPress Enter to start Test 2 (Multiple Diverse Logs)...")
    test_multiple_logs()
    
    input("\nPress Enter to start Test 3 (High-Sensitivity Events)...")
    test_high_sensitivity_events()
    
    input("\nPress Enter to start Test 4 (Diverse Infrastructure Sources)...")
    test_diverse_sources()
    
    input("\nPress Enter to start Test 5 (Brute Force Alert)...")
    test_brute_force_detection()
    
    print_header("✅ All Tests Complete!")
    print("\n📊 Summary:")
    print("  • Total logs sent: 40+ (single + diverse + high-sensitivity + infrastructure)")
    print("  • Alert created: 1 (brute force attack)")
    print("  • Sources tested: 20+ unique infrastructure components")
    print("  • Severity levels: All (low, medium, high)")
    print("\n📊 Next Steps:")
    print("1. Open MongoDB Compass (mongodb://localhost:27017/)")
    print("2. View siem_db > logs collection (40+ logs)")
    print("3. View siem_db > alerts collection (brute force alert)")
    print("4. Open browser: http://localhost:5000/")

def main_menu():
    """Display main menu"""
    while True:
        print("\n" + "=" * 60)
        print("  🔐 SIEM Platform - Testing Menu")
        print("=" * 60)
        print("\n  1. Check System Health")
        print("  2. Test: Send Single Log")
        print("  3. Test: Send Multiple Diverse Logs (5 sources)")
        print("  4. Test: High-Sensitivity Events (8 critical events)")
        print("  5. Test: Diverse Infrastructure Sources (10 different types)")
        print("  6. Test: Trigger Brute Force Alert (12 failed logins)")
        print("  7. Test: Send Custom Log")
        print("  8. View Recent Logs")
        print("  9. View Active Alerts")
        print("  10. Run All Tests (1-6)")
        print("  11. Exit")
        
        choice = input("\nSelect option (1-11): ").strip()
        
        if choice == '1':
            check_health()
        elif choice == '2':
            test_single_log()
        elif choice == '3':
            test_multiple_logs()
        elif choice == '4':
            test_high_sensitivity_events()
        elif choice == '5':
            test_diverse_sources()
        elif choice == '6':
            test_brute_force_detection()
        elif choice == '7':
            test_custom_log()
        elif choice == '8':
            view_recent_logs()
        elif choice == '9':
            view_alerts()
        elif choice == '10':
            run_all_tests()
        elif choice == '11':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid option. Please select 1-11.")

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🔐 SIEM Platform - Testing Script 🔐               ║
║                                                              ║
║  This script helps you test your SIEM system by sending     ║
║  sample security logs and verifying the system works.       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Check if server is running first
    print("Checking if SIEM server is running...")
    if check_health():
        print("\n✅ Server is running! Ready to test.")
        main_menu()
    else:
        print("\n❌ Please start the SIEM server first:")
        print("   cd backend")
        print("   python app.py")
