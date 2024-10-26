# analyzer.py
from collections import defaultdict
import time
from scapy.all import *

user_activity = defaultdict(list)

def analyze_packet(packet):
    if packet.haslayer(SSL):
        return True
    user_activity[packet.ip.src].append(time.time())
    if len(user_activity[packet.ip.src]) > 10 and (max(user_activity[packet.ip.src]) - min(user_activity[packet.ip.src])) < 60:
        return True
    # Existing analysis logic
    return False
