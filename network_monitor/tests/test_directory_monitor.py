# tests/test_directory_monitor.py
import os
import shutil
import unittest
import tempfile
from watchdog.observers import Observer
from directory_monitor import DirectoryEventHandler
import subprocess
import time
import getpass

class TestDirectoryMonitor(unittest.TestCase):
    def setUp(self):
        # Create temporary directories
        self.test_dir = tempfile.mkdtemp()
        self.destination_dir = tempfile.mkdtemp()
        self.event_handler = DirectoryEventHandler()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.test_dir, recursive=True)
        self.observer.start()

    def tearDown(self):
        # Stop observer and remove temporary directories
        self.observer.stop()
        self.observer.join()
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.destination_dir)

    def test_blocking_file_transfer(self):
        # Simulate file creation
        test_file_path = os.path.join(self.test_dir, "testfile.txt")
        with open(test_file_path, "w") as test_file:
            test_file.write("This is a test file.")
        
        # Give some time for the observer to detect changes
        time.sleep(1)

        # Perform scp to simulate network transfer
        scp_command = f"scp {test_file_path} {os.path.join(self.destination_dir, 'testfile.txt')}"
        print(f"Executing command: {scp_command}")
        process = subprocess.Popen(scp_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        print(f"scp stdout: {stdout}")
        print(f"scp stderr: {stderr}")

        # Check if the file transfer was blocked
        self.assertNotEqual(process.returncode, 0, "The file transfer should be blocked.")
        self.assertFalse(os.path.exists(os.path.join(self.destination_dir, "testfile.txt")), "File should not exist in the destination directory.")

        # Prompt for override to restore internet access
        self.prompt_for_override()

    def prompt_for_override(self):
        password = "override123"  # Same as in directory_monitor.py
        user_input = getpass.getpass("Enter override password to restore internet access: ")
        if user_input == password:
            self.restore_internet()
        else:
            print("Incorrect password. Internet access remains blocked.")
            self.fail("Incorrect password. Internet access remains blocked.")

    def restore_internet(self):
        if os.uname().sysname == 'Darwin':
            os.system("sudo pfctl -F all -f /etc/pf.conf")
        else:
            os.system("sudo iptables -F")
        print("Internet access restored.")

if __name__ == '__main__':
    unittest.main()
