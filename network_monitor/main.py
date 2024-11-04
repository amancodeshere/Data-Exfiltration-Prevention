# main.py
import logging
from scapy.all import sniff, IP, TCP
from config import allowed_countries, BLACKLISTED_IPS
from database import logPackets, initDB
from geo_ip import get_geo_location
from os_alerts import sendAlerts
from limiter import limiter
import os
import time
import getpass

logging.basicConfig(level=logging.INFO)

# Initialize the database
initDB()

# Initialize the alert flag
alertsTriggered = False

# Initialize the limiter
blocker = limiter()
blocker.admin_password = getpass.getpass('Enter admin password (Note you will need to regain internet access, please remember it): ')
blocker.password = getpass.getpass('Enter override password (Note you will need to regain internet access, please remember it): ')

def process_packet(packet):
    """
    Process a packet and raise an alert if it is deemed suspicious.

    Arguments:
        packet : scapy.packet.Packet
            The packet to process.

    Returns:
        None
    """
    global alertsTriggered
    timestamp = time.strftime("%H:%M:%S")
    if packet.haslayer(IP) and packet.haslayer(TCP):
        sourceIp = packet[IP].src
        destIp = packet[IP].dst
        geoInfo = get_geo_location(sourceIp)
        if geoInfo['status'] == 'fail':
            if sourceIp in BLACKLISTED_IPS:  # Define allowed countries list
                logPackets(sourceIp, destIp, timestamp)  # Log to database
                sendAlerts(f"Suspicious activity detected: {sourceIp} to {destIp}")
                alertsTriggered = True
        else:
            if geoInfo['country'] not in allowed_countries or sourceIp in BLACKLISTED_IPS:
                logPackets(sourceIp, destIp, timestamp)  # Log to database
                sendAlerts(f"Suspicious activity detected: {sourceIp} to {destIp}")
                alertsTriggered = True

        if alertsTriggered:
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
