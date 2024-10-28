# directory_monitor.py
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import config

class DirectoryEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f"Detected change in directory: {event.src_path}")
        self.block_transfer()

    def block_transfer(self):
        print("Blocking file transfer")
        if os.uname().sysname == 'Darwin':  # macOS
            self.block_with_pf()
        else:
            self.block_with_iptables()

    def block_with_pf(self):
        pf_rules = "block all\npass in quick on lo0 all\npass out quick on lo0 all"
        os.system(f"echo '{pf_rules}' | sudo pfctl -ef -")
        os.system("sudo pfctl -E")

    def block_with_iptables(self):
        os.system("sudo iptables -A OUTPUT -m owner --uid-owner $(id -u) -j DROP")

def monitor_directory(path):
    event_handler = DirectoryEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print(f"Monitoring directory: {path}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    directory_to_watch = '/path/to/directory'  # Specify your directory here
    monitor_directory(directory_to_watch)
