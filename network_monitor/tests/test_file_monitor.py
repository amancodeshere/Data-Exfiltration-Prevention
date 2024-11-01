import os
import time
import unittest
from unittest.mock import patch
from network_monitor.file_monitor import FileMonitor
from network_monitor.database import Database

class TestFileMonitor(unittest.TestCase):
    def setUp(self):
        self.monitored_dir = '/tmp/test_file_monitor'
        self.file_monitor = FileMonitor(self.monitored_dir)
        self.db = Database()

    def tearDown(self):
        self.file_monitor.stop()
        self.db.close()

    def test_monitor_files(self):
        # Create a test file
        test_file = os.path.join(self.monitored_dir, 'test_file.txt')
        with open(test_file, 'w') as f:
            f.write('Test content')

        # Start the file monitor
        self.file_monitor.start()

        # Modify the test file
        with open(test_file, 'a') as f:
            f.write('Modified content')

        # Wait for the file monitor to detect the change
        time.sleep(1)

        # Check if the database was updated
        self.assertTrue(self.db.get_file_modifications(test_file))

    def test_update_database(self):
        # Create a test file
        test_file = os.path.join(self.monitored_dir, 'test_file.txt')
        with open(test_file, 'w') as f:
            f.write('Test content')

        # Simulate a file modification
        self.file_monitor.update_database(test_file)

        # Check if the database was updated
        self.assertTrue(self.db.get_file_modifications(test_file))

    def test_monitor_files_indefinitely(self):
        # Create a test file
        test_file = os.path.join(self.monitored_dir, 'test_file.txt')
        with open(test_file, 'w') as f:
            f.write('Test content')

        # Start the file monitor
        self.file_monitor.start()

        # Modify the test file multiple times
        for _ in range(5):
            with open(test_file, 'a') as f:
                f.write('Modified content')
            time.sleep(1)

        # Check if the database was updated for each modification
        self.assertEqual(self.db.get_file_modifications(test_file), 5)

if __name__ == '__main__':
    unittest.main()