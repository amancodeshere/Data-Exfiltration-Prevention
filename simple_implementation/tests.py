from unittest.mock import patch, MagicMock
import unittest
import sqlite3
import dep_monitor  # Ensure path is correct to import dep_monitor

class TestDEPMonitor(unittest.TestCase):

    @patch('dep_monitor.psutil.net_if_addrs')
    def test_auto_detect_interface(self, mock_net_if_addrs):
        """Test automatic interface detection."""
        mock_net_if_addrs.return_value = {
            'en0': [MagicMock(family=2, address='192.168.1.2')],  # AF_INET
            'lo0': [MagicMock(family=2, address='127.0.0.1')]  # Loopback
        }
        interface = dep_monitor.auto_detect_interface()
        self.assertEqual(interface, 'en0')

    @patch('dep_monitor.sqlite3.connect')
    def test_log_to_database(self, mock_connect):
        """Test logging alerts to the database."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        dep_monitor.log_to_database("Test alert message")
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO Alerts (timestamp, alert_message) VALUES (?, ?)",
            unittest.mock.ANY
        )
        mock_conn.commit.assert_called_once()

    @patch('dep_monitor.send_os_notification')
    def test_send_os_notification(self, mock_notify):
        """Test sending OS-level notifications."""
        dep_monitor.send_os_notification("Test notification")
        mock_notify.assert_called_once_with("Test notification")

    @patch('dep_monitor.pyshark.LiveCapture')
    def test_monitor_packets(self, mock_live_capture):
        """Test packet monitoring functionality."""
        mock_capture = mock_live_capture.return_value
        mock_packet = MagicMock()
        mock_packet.ip.dst = '203.0.113.50'
        mock_packet.length = 6000000  # Size in bytes
        mock_capture.sniff_continuously.return_value = [mock_packet]
        dep_monitor.reset_data_tracking()
        dep_monitor.monitor_packets(mock_capture)
        self.assertIn('203.0.113.50', dep_monitor.data_volume_per_ip)
        self.assertGreater(dep_monitor.data_volume_per_ip['203.0.113.50'], 5 * 1024 * 1024)

    def tearDown(self):
        conn = sqlite3.connect("exfiltration_alerts.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Alerts")
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()
