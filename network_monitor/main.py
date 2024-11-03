# main.py
import logging
from scapy.all import sniff, IP, TCP
from config import allowed_countries, BLACKLISTED_IPS
from database import log_packet, init_db
from geo_ip import get_geo_location
from os_alerts import send_os_alert
from limiter import limiter
import os
import time

logging.basicConfig(level=logging.INFO)

# Initialize the database
init_db()

# Initialize the alert flag
alert_triggered = False

# Initialize the limiter
blocker = limiter()
blocker.password = input('Enter override password (Note you will need to regain internet access, please remember it): ')

def process_packet(packet):
    """
    Process a packet and raise an alert if it is deemed suspicious.

    Arguments:
        packet : scapy.packet.Packet
            The packet to process.

    Returns:
        None
    """
    global alert_triggered
    timestamp = time.strftime("%H:%M:%S")
    # packet_length = len(packet)
    if packet.haslayer(IP) and packet.haslayer(TCP):
        # packet_features = [packet_length, timestamp, packet[TCP].sport, packet[TCP].dport]
        src_ip = packet[IP].src
        dest_ip = packet[IP].dst
        geo_info = get_geo_location(src_ip)
        if geo_info['status'] == 'fail':
            if src_ip in BLACKLISTED_IPS:  # Define allowed countries list
                log_packet(src_ip, dest_ip, timestamp)  # Log to database
                send_os_alert(f"Suspicious activity detected: {src_ip} to {dest_ip}")
                alert_triggered = True
        else:
            if geo_info['country'] not in allowed_countries or src_ip in BLACKLISTED_IPS:
                log_packet(src_ip, dest_ip, timestamp)  # Log to database
                send_os_alert(f"Suspicious activity detected: {src_ip} to {dest_ip}")
                alert_triggered = True

        if alert_triggered:
            # Block the IP address
            if os.uname().sysname != 'Darwin':
                print('Network monitoring is only supported on macOS.')
            blocker.block_wifi()
            blocker.prompt_for_override()

def main():
    logging.info("Starting packet capture...")
    sniff(prn=process_packet, count=100)

if __name__ == "__main__":
    main()
