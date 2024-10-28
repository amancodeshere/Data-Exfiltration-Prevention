# file_tracker.py
import os
from scapy.all import sniff, IP
import config
from geo_ip import get_geo_location, is_private_ip
from database import log_blocked_transfer

def block_ip(ip):
    os.system(f"sudo iptables -A OUTPUT -d {ip} -j DROP")

def monitor_file_transfer():
    def process_packet(packet):
        if packet.haslayer(IP):
            dest_ip = packet[IP].dst
            if dest_ip in config.BLACKLISTED_IPS:
                block_ip(dest_ip)
                log_blocked_transfer(dest_ip, "Blacklisted IP")
                print(f"Blocked file transfer to blacklisted IP: {dest_ip}")
            elif not is_private_ip(dest_ip):
                geo_info = get_geo_location(dest_ip)
                if geo_info.get('country', 'N/A') not in config.allowed_countries:
                    block_ip(dest_ip)
                    log_blocked_transfer(dest_ip, "Prohibited location")
                    print(f"Blocked file transfer to prohibited location: {geo_info.get('country', 'N/A')}")
                
    sniff(prn=process_packet, store=0)

if __name__ == "__main__":
    monitor_file_transfer()
