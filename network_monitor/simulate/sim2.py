import time
from scapy.layers.inet import TCP, IP
from scapy.sendrecv import send

"""
Simulate sending packets to a target IP address from a spoofed source IP.
"""
target_ip = "www.example.com"
spoofed_ip = "1.32.232.0"# This IP-address is not in th blacklist, as this is being blocked based on its location unlike the IP-address in the other sim file.
target_port = 80

while True:
    packet = IP(src=spoofed_ip, dst=target_ip)/TCP(dport=target_port, flags="S")
    send(packet, count=10)
    time.sleep(1)
