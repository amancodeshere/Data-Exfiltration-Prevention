# tests/test_directory_monitor.py
import os
import shutil
import unittest
import tempfile
from watchdog.observers import Observer
from directory_monitor import DirectoryEventHandler, monitor_directory

class TestDirectoryMonitor(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        self.test_dir = tempfile.mkdtemp()
        self.event_handler = DirectoryEventHandler()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.test_dir, recursive=True)
        self.observer.start()

    def tearDown(self):
        # Stop observer and remove temporary directory
        self.observer.stop()
        self.observer.join()
        shutil.rmtree(self.test_dir)

    def test_directory_monitor(self):
        # Simulate file creation
        test_file_path = os.path.join(self.test_dir, "testfile.txt")
        with open(test_file_path, "w") as test_file:
            test_file.write("This is a test file.")

        # Give some time for the observer to detect changes
        import time
        time.sleep(1)

        # Check if the file creation was detected
        self.assertTrue(os.path.exists(test_file_path))

    def test_blocking_file_transfer(self):
        # Simulate file modification
        test_file_path = os.path.join(self.test_dir, "testfile.txt")
        with open(test_file_path, "w") as test_file:
            test_file.write("This is a test file.")

        # Simulate a move operation (like a network transfer)
        new_dir = tempfile.mkdtemp()
        shutil.move(test_file_path, new_dir)

        # Give some time for the observer to detect changes
        import time
        time.sleep(1)

        # Check if the file move was detected and blocked
        self.assertFalse(os.path.exists(test_file_path))
        self.assertTrue(os.path.exists(os.path.join(new_dir, "testfile.txt")))

if __name__ == '__main__':
    unittest.main()
