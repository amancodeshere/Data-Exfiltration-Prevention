# capture.py
import pyshark

def capture_packets(interface='en0'):
    capture = pyshark.LiveCapture(interface=interface)
    return capture
