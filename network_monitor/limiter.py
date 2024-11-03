import os
import getpass
from scapy.config import conf


class limiter():
    def __init__(self):
        self.password = "1234"  # default password, changed in main.py

    def block_wifi(self):
        """
        Blocks all outgoing traffic on port 22 on macOS systems using PF.
        """
        if os.uname().sysname == 'Darwin':
            interface = conf.iface

            # Construct PF rule to block all outgoing
            rule = f"block out on {interface} all"

            # Write rule to temp file
            pf_conf = "/tmp/pf.conf"
            with open(pf_conf, "w") as f:
                f.write(f"{rule}\n")
            print(f"Writing pf rule to {pf_conf}: {rule}")

            # Load the rule
            result = os.system(f"sudo pfctl -f {pf_conf}")
            print(f"pfctl load result: {result}")

            # Enable PF
            result = os.system("sudo pfctl -e")
            print(f"pfctl enable result: {result}")

    def prompt_for_override(self):
        """
        Prompt the user for a password to override the internet block.
        """
        while True:
            user_input = getpass.getpass("Enter override password to restore internet access: ")
            if user_input == self.password:
                result = os.system("sudo pfctl -F all -f /etc/pf.conf")
                print(f"pfctl restore result: {result}")
                break
            else:
                print("Incorrect password. Please try again.")
