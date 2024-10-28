# tests/test_file_tracker.py
import unittest
from unittest.mock import patch, MagicMock
from file_tracker import block_ip, monitor_file_transfer

class TestFileTracker(unittest.TestCase):
    @patch('file_tracker.os.system')
    def test_block_ip(self, mock_system):
        block_ip('8.8.8.8')
        mock_system.assert_called_with('sudo iptables -A OUTPUT -d 8.8.8.8 -j DROP')

    @patch('file_tracker.sniff')
    def test_monitor_file_transfer(self, mock_sniff):
        mock_packet = MagicMock()
        mock_packet[IP].dst = '8.8.8.8'
        mock_sniff.side_effect = lambda prn, store: prn(mock_packet)
        
        monitor_file_transfer()
        mock_sniff.assert_called()

if __name__ == '__main__':
    unittest.main()
