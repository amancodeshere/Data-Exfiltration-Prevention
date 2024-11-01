from scapy.all import sniff

def capture_packets(packet):
    print(packet.summary())  # Replace with your packet processing logic

# Capture on localhost (lo) and filter based on desired protocols, like TCP, UDP, or ICMP
sniff(iface="lo0", prn=capture_packets, filter="tcp or udp or icmp")
