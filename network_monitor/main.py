# main.py
import logging
from scapy.all import sniff, IP, TCP
from config import allowed_countries, BLACKLISTED_IPS
from database import log_packet, init_db
from geo_ip import get_geo_location
from os_alerts import send_os_alert
from limiter import WifiBlocker
import os

logging.basicConfig(level=logging.INFO)

# Initialize the database
init_db()

alert_triggered = False

def process_packet(packet):
    global alert_triggered
    packet_time = packet.time if hasattr(packet, 'time') else packet.sniff_time.timestamp()
    packet_length = len(packet)
    if packet.haslayer(IP) and packet.haslayer(TCP):
        packet_features = [packet_length, packet_time, packet[TCP].sport, packet[TCP].dport]
        src_ip = packet[IP].src
        dest_ip = packet[IP].dst
        geo_info = get_geo_location(src_ip)
        if geo_info['status'] == 'fail':
            if src_ip in BLACKLISTED_IPS:  # Define allowed countries list
                log_packet(src_ip, dest_ip)  # Log to database
                send_os_alert(f"Suspicious activity detected: {src_ip} to {dest_ip}")
                alert_triggered = True
        else:
            if geo_info['country'] not in allowed_countries or src_ip in BLACKLISTED_IPS:
                log_packet(src_ip, dest_ip)  # Log to database
                send_os_alert(f"Suspicious activity detected: {src_ip} to {dest_ip}")
                alert_triggered = True

        if alert_triggered:
            # Block the IP address
            if os.uname().sysname != 'Darwin':
                print('Network monitoring is only supported on macOS.')
            wifi_blocker = WifiBlocker()
            wifi_blocker.block_specific_with_pf()
            wifi_blocker.prompt_for_override()

def main():
    logging.info("Starting packet capture...")
    sniff(prn=process_packet, count=100)

if __name__ == "__main__":
    main()
