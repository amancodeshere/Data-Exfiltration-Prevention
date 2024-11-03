# main.py
import logging

import numpy as np
from scapy.all import sniff, IP, TCP

from anomaly_detection import AnomalyDetector
from config import allowed_countries, BLACKLISTED_IPS
from database import log_packet, init_db
from geo_ip import get_geo_location
from os_alerts import send_os_alert  # Import the new OS alert function

logging.basicConfig(level=logging.INFO)

# Initialize anomaly detector
anomaly_detector = AnomalyDetector()

# Train the anomaly detector with some initial normal data
initial_data = np.random.rand(100, 4)  # Example: replace with actual features
anomaly_detector.fit(initial_data)

# Initialize the database
init_db()  # Ensure the database and table are created

def process_packet(packet):
    # logging.info("Packet captured.")
    packet_time = packet.time if hasattr(packet, 'time') else packet.sniff_time.timestamp()  # fix it
    packet_length = len(packet)
    if packet.haslayer(IP) and packet.haslayer(TCP):
        packet_features = [packet_length, packet_time, packet[TCP].sport, packet[TCP].dport]  # Example features
        # print(packet_features)
        # if analyze_packet(packet) or anomaly_detector.predict(packet_features):
        src_ip = packet[IP].src
        dest_ip = packet[IP].dst
        geo_info = get_geo_location(src_ip)
        if geo_info['status'] == 'fail':
            if src_ip in BLACKLISTED_IPS:  # Define allowed countries list 
                log_packet(src_ip, dest_ip)  # Log to database
                send_os_alert(f"Suspicious activity detected: {src_ip} to {dest_ip}")
        else:
            if geo_info['country'] not in allowed_countries or src_ip in BLACKLISTED_IPS:  # Define allowed countries list 
                log_packet(src_ip, dest_ip)  # Log to database
                send_os_alert(f"Suspicious activity detected: {src_ip} to {dest_ip}")
    

def main():
    logging.info("Starting packet capture...")
    sniff(prn=process_packet, count=100)

if __name__ == "__main__":
    main()
