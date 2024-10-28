# directory_monitor.py
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import config
import getpass

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
        rule = "block out quick proto tcp from any to any port 22"
        pf_conf = "/tmp/pf.conf"
        with open(pf_conf, "w") as f:
            f.write(f"{rule}\n")
        print(f"Applying pf rule: {rule}")
        os.system(f"sudo pfctl -f {pf_conf}")
        os.system("sudo pfctl -e")
        print("pf rule applied")
        self.prompt_for_override()

    def block_with_iptables(self):
        print("Applying iptables rule to block port 22")
        os.system("sudo iptables -A OUTPUT -p tcp --dport 22 -j DROP")
        print("iptables rule applied")
        self.prompt_for_override()

    def prompt_for_override(self):
        password = "override123"  # Change to a secure password
        user_input = getpass.getpass("Enter override password to restore internet access: ")
        if user_input == password:
            self.restore_internet()
        else:
            print("Incorrect password. Internet access remains blocked.")

    def restore_internet(self):
        if os.uname().sysname == 'Darwin':
            os.system("sudo pfctl -F all -f /etc/pf.conf")
        else:
            os.system("sudo iptables -F")
        print("Internet access restored.")

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
