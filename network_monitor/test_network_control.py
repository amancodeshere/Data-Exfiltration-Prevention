# test_network_control.py

import unittest
import tempfile
import os
import time
import threading  # Import threading
from unittest.mock import patch
from traffic_control import block_traffic, restore_traffic_prompt
from directory_monitor import monitor_directory

class TestNetworkControl(unittest.TestCase):

    @patch('traffic_control.getpass.getpass', return_value='your_secure_password')
    @patch('traffic_control.os.system')
    def test_block_and_restore_traffic_correct_password(self, mock_os_system, mock_getpass):
        # Create a temporary directory and file
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "test_file.txt")
            with open(temp_file_path, 'w') as temp_file:
                temp_file.write("Initial content")

            # Start monitoring the temporary directory
            monitor_thread = threading.Thread(target=monitor_directory, args=(temp_dir,))
            monitor_thread.daemon = True
            monitor_thread.start()

            # Simulate file modification
            with open(temp_file_path, 'a') as temp_file:
                temp_file.write("Modified content")

            # Allow some time for the monitor to detect the change
            time.sleep(2)

            # Check if the block command was executed
            mock_os_system.assert_any_call('echo "block out all" | sudo pfctl -ef -')

            # Restore traffic with correct password
            restore_traffic_prompt()
            mock_os_system.assert_any_call('sudo pfctl -f /etc/pf.conf -e')

            print("Test for correct password passed.")

    @patch('traffic_control.getpass.getpass', return_value='wrong_password')
    @patch('traffic_control.os.system')
    def test_block_and_restore_traffic_incorrect_password(self, mock_os_system, mock_getpass):
        # Create a temporary directory and file
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "test_file.txt")
            with open(temp_file_path, 'w') as temp_file:
                temp_file.write("Initial content")

            # Start monitoring the temporary directory
            monitor_thread = threading.Thread(target=monitor_directory, args=(temp_dir,))
            monitor_thread.daemon = True
            monitor_thread.start()

            # Simulate file modification
            with open(temp_file_path, 'a') as temp_file:
                temp_file.write("Modified content")

            # Allow some time for the monitor to detect the change
            time.sleep(2)

            # Check if the block command was executed
            mock_os_system.assert_any_call('echo "block out all" | sudo pfctl -ef -')

            # Attempt to restore traffic with incorrect password
            restore_traffic_prompt()
            mock_os_system.assert_called_once_with('echo "block out all" | sudo pfctl -ef -')

            print("Test for incorrect password passed.")

if __name__ == '__main__':
    unittest.main()
