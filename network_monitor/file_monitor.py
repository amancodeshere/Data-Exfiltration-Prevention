import os
import time
import logging
from network_monitor.database import Database
import threading

logging.basicConfig(level=logging.INFO)

class FileMonitor:
    def __init__(self, monitored_directory, database):
        self.monitored_dir = monitored_directory
        self.last_modified = {}
        self.database = database
        self.stop_monitoring = False

    def monitor(self):
        while not self.stop_monitoring:
            for root, dirs, files in os.walk(self.monitored_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    modified_time = os.path.getmtime(file_path)
                    if file_path not in self.last_modified or modified_time != self.last_modified[file_path]:
                        logging.info(f"File modified: {file_path}")
                        self.database.update_file_modification(file_path)
                        self.last_modified[file_path] = modified_time
            time.sleep(1)  # Adjust the sleep time according to your needs

    def start_monitoring(self):
        monitoring_thread = threading.Thread(target=self.monitor)
        monitoring_thread.start()

    def stop(self):
        self.stop_monitoring = True

if __name__ == "__main__":
    monitored_dir = 'tests/test_file_monitor'
    database = Database()
    file_monitor = FileMonitor(monitored_dir, database)
    file_monitor.start_monitoring()