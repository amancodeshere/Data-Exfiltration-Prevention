# main.py
import logging
import numpy as np
from scapy.all import sniff, IP, TCP
from config import allowed_countries, BLACKLISTED_IPS
from database import log_packet, init_db
from geo_ip import get_geo_location
from os_alerts import send_os_alert

logging.basicConfig(level=logging.INFO)

# Initialize the database
init_db()  # Ensure the database and table are created

def process_packet(packet):
    """
    Process a single packet sniffed from the network.

    This function is a callback for the scapy sniff function. It takes a single
    packet as an argument, and processes it according to the rules defined in
    the config.py file. The packet is logged to the database if it is deemed
    suspicious according to the rules.

    :param packet: a scapy packet object
    :return: None
    """
    packet_time = packet.time if hasattr(packet, 'time') else packet.sniff_time.timestamp()  # fix it
    packet_length = len(packet)
    if packet.haslayer(IP) and packet.haslayer(TCP):
        packet_features = [packet_length, packet_time, packet[TCP].sport, packet[TCP].dport]
        src_ip = packet[IP].src
        dest_ip = packet[IP].dst
        geo_info = get_geo_location(src_ip)
        if geo_info['status'] == 'fail':
            if src_ip in BLACKLISTED_IPS:
                log_packet(src_ip, dest_ip)
                send_os_alert(f"Suspicious activity detected: {src_ip} to {dest_ip}")
        else:
            if geo_info['country'] not in allowed_countries or src_ip in BLACKLISTED_IPS:
                log_packet(src_ip, dest_ip)
                send_os_alert(f"Suspicious activity detected: {src_ip} to {dest_ip}")
    


def main():
    """
    Start the packet capture.

    This function is the main entry point for the script. It starts a packet
    capture using the scapy library, and passes each packet to the
    process_packet function for processing. The number of packets to capture
    is specified by the count argument to the sniff function. When all packets
    have been captured, the function exits.

    :return: None
    """
    logging.info("Starting packet capture...")
    sniff(prn=process_packet, count=100)
    logging.info("Starting packet capture...")
    sniff(prn=process_packet, count=100)

if __name__ == "__main__":
    main()
