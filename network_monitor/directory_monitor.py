# directory_monitor.py
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from scapy.all import sniff, IP
import config
from geo_ip import get_geo_location, is_private_ip
from database import log_blocked_transfer
import subprocess

class DirectoryEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f"Detected change in directory: {event.src_path}")
        self.block_transfer()

    def block_transfer(self):
        print("Blocking file transfer")
        if os.system("uname -s") == "Darwin":  # macOS
            self.block_with_pf()
        else:
            self.block_with_iptables()

    def block_with_pf(self):
        pf_rules = "block out all"
        with open("/etc/pf.anchors/block_rules", "w") as f:
            f.write(pf_rules)
        os.system("echo 'rdr pass on lo0' | sudo pfctl -ef -")

    def block_with_iptables(self):
        os.system("sudo iptables -A OUTPUT -m owner --uid-owner $(id -u) -j DROP")

def monitor_directory(path):
    event_handler = DirectoryEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Monitoring directory: {path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

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

def monitor_file_transfer():
    sniff(prn=process_packet, store=0)

if __name__ == "__main__":
    directory_to_watch = '/path/to/directory'  # Specify your directory here
    monitor_directory(directory_to_watch)
