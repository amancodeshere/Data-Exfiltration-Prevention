# directory_monitor.py

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from traffic_control import block_traffic  # Import block_traffic from traffic_control.py

class DirectoryMonitorHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory

    def on_modified(self, event):
        if event.is_directory:
            return
        if event.src_path.startswith(self.directory):
            print(f"Modification detected in monitored directory: {event.src_path}")
            block_traffic()  # Block the network traffic when a file modification is detected

def monitor_directory(directory):
    event_handler = DirectoryMonitorHandler(directory)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
