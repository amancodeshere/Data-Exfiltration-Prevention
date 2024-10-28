# main.py
import logging
from scapy.all import sniff, IP, TCP
from capture import capture_packets
from analyzer import analyze_packet
from alert import send_alert
from config import ALERT_THRESHOLD, allowed_countries, BLACKLISTED_IPS
from database import log_packet, init_db
from anomaly_detection import AnomalyDetector
from geo_ip import get_geo_location
from os_alerts import send_os_alert
from file_tracker import monitor_file_transfer
from directory_monitor import monitor_directory
import numpy as np

logging.basicConfig(level=logging.INFO)

anomaly_detector = AnomalyDetector()
initial_data = np.random.rand(100, 4)
anomaly_detector.fit(initial_data)

def process_packet(packet):
    logging.info("Packet captured.")
    packet_time = packet.time if hasattr(packet, 'time') else packet.sniff_time.timestamp()
    packet_length = len(packet)
    if packet.haslayer(IP) and packet.haslayer(TCP):
        packet_features = [packet_length, packet_time, packet[TCP].sport, packet[TCP].dport]
        if analyze_packet(packet) or anomaly_detector.predict(packet_features):
            src_ip = packet[IP].src
            dest_ip = packet[IP].dst
            geo_info = get_geo_location(src_ip)
            if geo_info['country'] not in allowed_countries:
                log_packet(src_ip, dest_ip)
                suspicious_count += 1
                if suspicious_count >= ALERT_THRESHOLD:
                    send_os_alert(f"Suspicious activity detected: {src_ip} to {dest_ip}")
                    suspicious_count = 0

def main():
    init_db()
    suspicious_count = 0
    logging.info("Starting packet capture, file monitoring, and directory monitoring...")
    monitor_file_transfer()
    # directory_to_watch = '/Users/sashankvermani/Desktop/Wallpapers'  # Specify your directory here
    # monitor_directory(directory_to_watch)
    sniff(prn=process_packet, count=100)

if __name__ == "__main__":
    main()
