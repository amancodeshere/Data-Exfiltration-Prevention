# directory_monitor.py
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import getpass

class DirectoryEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        print(f"Detected change in directory: {event.src_path}")
        self.block_transfer()

    def block_transfer(self):
        print("Blocking specific traffic")
        if os.uname().sysname == 'Darwin':  # macOS
            self.block_specific_with_pf()
        else:
            self.block_specific_with_iptables()

    def block_specific_with_pf(self):
        rule = "block out quick proto tcp from any to any port 22"
        pf_conf = "/tmp/pf.conf"
        with open(pf_conf, "w") as f:
            f.write(f"{rule}\n")
        print(f"Writing pf rule to {pf_conf}: {rule}")
        result = os.system(f"sudo pfctl -f {pf_conf}")
        print(f"pfctl load result: {result}")
        result = os.system("sudo pfctl -e")
        print(f"pfctl enable result: {result}")
        self.prompt_for_override()

    def block_specific_with_iptables(self):
        print("Applying iptables rule to block port 22")
        result = os.system("sudo iptables -A OUTPUT -p tcp --dport 22 -j DROP")
        print(f"iptables result: {result}")
        self.prompt_for_override()

    def prompt_for_override(self):
        password = "override123"  # Change to a secure password
        while True:
            user_input = getpass.getpass("Enter override password to restore internet access: ")
            if user_input == password:
                self.restore_internet()
                break
            else:
                print("Incorrect password. Please try again.")

    def restore_internet(self):
        if os.uname().sysname == 'Darwin':
            result = os.system("sudo pfctl -F all -f /etc/pf.conf")
            print(f"pfctl restore result: {result}")
        else:
            result = os.system("sudo iptables -F")
            print(f"iptables restore result: {result}")
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
    directory_to_watch = '/Users/sashankvermani/Desktop/Wallpapers'  # Specify your directory here
    monitor_directory(directory_to_watch)
