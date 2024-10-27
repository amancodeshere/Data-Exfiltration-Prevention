import threading
import logging
import numpy as np
from scapy.all import sniff
from capture import capture_packets
from analyzer import analyze_packet
from alert import send_alert
from config import ALERT_THRESHOLD
from database import log_packet, init_db
from anomaly_detection import AnomalyDetector
from geo_ip import get_geo_location
from os_alerts import send_os_alert
from file_tracker import FileTracker

logging.basicConfig(level=logging.INFO)

# Initialize anomaly detector
anomaly_detector = AnomalyDetector()

# Train the anomaly detector with some initial normal data
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
                send_os_alert(f"Suspicious activity detected: {src_ip} to {dest_ip}")

def run_file_monitor(directory_to_watch):
    file_tracker = FileTracker(directory_to_watch)
    file_tracker.run()

def run_network_monitor():
    sniff(prn=process_packet, store=0)  # Run indefinitely

def main():
    init_db()
    logging.info("Starting packet capture and file monitoring...")

    directory_to_watch = input("Enter the directory to watch: ")
    capture_thread = threading.Thread(target=run_network_monitor)
    file_monitor_thread = threading.Thread(target=run_file_monitor, args=(directory_to_watch,))

    capture_thread.start()
    file_monitor_thread.start()

    capture_thread.join()
    file_monitor_thread.join()

    logging.info("Monitoring stopped.")

if __name__ == "__main__":
    main()
