import subprocess
import pyshark
import time
import sqlite3
import signal
import sys
import os

# Configuration for monitoring parameters
DATA_THRESHOLD_MB = 5  # Threshold for data volume per IP in MB
SUSPICIOUS_IPS = {'192.168.1.100', '203.0.113.50'}  # Example of suspicious IPs
RESET_INTERVAL = 3600  # Interval to reset data volume tracking (in seconds)

# Path for the database file
DB_FILE = "exfiltration_alerts.db"

# Dictionary to keep track of data volume per destination IP
data_volume_per_ip = {}

def auto_detect_interface():
    """Automatically detect the primary network interface using Scapy."""
    from scapy.all import get_if_addr, get_if_list  # Import here to avoid circular imports
    for interface in get_if_list():
        try:
            # Attempt to get the IP address of the interface
            ip_address = get_if_addr(interface)
            # Return the first interface that has an IP address
            if ip_address != '0.0.0.0':
                return interface
        except Exception as error:
            print('error: ', error)
            pass
    raise RuntimeError("No active network interface with an IP address found.")

def log_to_database(message):
    """Log alerts to the database."""
    # Open a new database connection
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create table if it does not exist (move this logic outside the loop)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        alert_message TEXT
    )
    """)

    # Use a transaction for safety
    try:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO Alerts (timestamp, alert_message) VALUES (?, ?)", (timestamp, message))
        conn.commit()
    except Exception as e:
        print(f"[ERROR] Failed to log to database: {e}")
    finally:
        conn.close()  # Ensure connection is closed

def send_os_notification(message):
    """Send an OS-level notification for alerts."""
    try:
        print(f"[ALERT] {message}")
        subprocess.run([
            "osascript", "-e",
            f'display notification "{message}" with title "Data Exfiltration Alert"'
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to send notification: {e}")

def monitor_packets(capture):
    """Monitor network packets for potential data exfiltration."""
    for packet in capture.sniff_continuously(packet_count=1000):
        try:
            # Ensure packet has IP and TCP layers
            if hasattr(packet, 'ip') and hasattr(packet, 'tcp'):
                ip_dst = packet.ip.dst
                data_size = int(packet.length)  # Packet size in bytes

                # Track data volume for each destination IP
                if ip_dst in data_volume_per_ip:
                    data_volume_per_ip[ip_dst] += data_size
                else:
                    data_volume_per_ip[ip_dst] = data_size

                # Check for data threshold breach per IP
                if data_volume_per_ip[ip_dst] > DATA_THRESHOLD_MB * 1024 * 1024:
                    alert_msg = (f"High data volume to {ip_dst}: "
                                 f"{data_volume_per_ip[ip_dst] / (1024 * 1024):.2f} MB")
                    send_os_notification(alert_msg)
                    log_to_database(alert_msg)
                    print(f"[ALERT] {alert_msg}")

                # Check if the destination IP is in the suspicious IP list
                if ip_dst in SUSPICIOUS_IPS:
                    alert_msg = f"Data transfer to suspicious IP detected: {ip_dst}"
                    send_os_notification(alert_msg)
                    log_to_database(alert_msg)
                    print(f"[ALERT] {alert_msg}")

        except AttributeError:
            # Skip packets that don't have expected attributes
            pass

def reset_data_tracking():
    """Reset data volume tracking dictionary at regular intervals."""
    global data_volume_per_ip
    data_volume_per_ip.clear()
    print("[INFO] Resetting data volume tracking.")

def signal_handler(sig, frame):
    """Handle termination signals for graceful shutdown."""
    print("[INFO] Shutting down gracefully...")
    # Remove the database file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"[INFO] Deleted database file: {DB_FILE}")
    sys.exit(0)

def run_monitoring():
    """Main function to initiate packet capture and monitoring."""
    network_interface = auto_detect_interface()
    print(f"Using network interface: {network_interface}")
    capture = pyshark.LiveCapture(interface=network_interface)
    while True:
        monitor_packets(capture)
        time.sleep(RESET_INTERVAL)
        reset_data_tracking()

# Register signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)

# Start monitoring
if __name__ == "__main__":
    print("Starting Data Exfiltration Prevention monitoring...")
    run_monitoring()
