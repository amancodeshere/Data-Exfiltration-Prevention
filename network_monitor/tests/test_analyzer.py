# tests/test_analyzer.py
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import MagicMock
from analyzer import analyze_packet

class TestAnalyzer(unittest.TestCase):

    def test_analyze_packet_blacklisted_ip(self):
        # Simulate a packet with a blacklisted IP
        packet = MagicMock()
        packet.ip = MagicMock()  # Mock the IP layer
        packet.ip.src = '127.0.0.1'  # Blacklisted IP
        packet.ip.dst = '8.8.8.8'

        result = analyze_packet(packet)
        self.assertTrue(result, "Packet from blacklisted IP should be flagged as suspicious.")

    def test_analyze_packet_non_blacklisted_ip(self):
        # Simulate a packet with a non-blacklisted IP
        packet = MagicMock()
        packet.ip = MagicMock()  # Mock the IP layer
        packet.ip.src = '192.168.1.10'  # Non-blacklisted IP
        packet.ip.dst = '8.8.8.8'

        result = analyze_packet(packet)
        self.assertFalse(result, "Packet from non-blacklisted IP should not be flagged as suspicious.")

    def test_analyze_packet_known_signature(self):
        # Simulate a packet with a known malware signature
        packet = MagicMock()
        packet.ip = MagicMock()  # Mock the IP layer
        packet.ip.src = '192.168.1.10'
        packet.ip.dst = '8.8.8.8'
        packet.payload = b'KnownMalwareSignature'  # Example payload for a malware signature

        result = analyze_packet(packet)
        self.assertTrue(result, "Packet with known malware signature should be flagged as suspicious.")

    def test_analyze_packet_clean_payload(self):
        # Simulate a clean packet
        packet = MagicMock()
        packet.ip = MagicMock()  # Mock the IP layer
        packet.ip.src = '192.168.1.10'
        packet.ip.dst = '8.8.8.8'
        packet.payload = b'CleanPayload'  # Ensure this payload is not a known signature

        result = analyze_packet(packet)
        self.assertFalse(result, "Packet with clean payload should not be flagged as suspicious.")

if __name__ == '__main__':
    unittest.main()
