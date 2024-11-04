import os
import getpass
from scapy.config import conf


class limiter():
    def __init__(self):
        # Here we are setting the default password
        # the user can change it in main.py
        self.password = "1234"
        self.admin_password = None

    def block_wifi(self):
        """
        Blocks all outgoing traffic using PF.
        """
        if os.uname().sysname == 'Darwin':
            interface = conf.iface

            rule = f"block out on {interface} all"

            pfConfig = "/tmp/pf.conf"
            with open(pfConfig, "w") as f:
                f.write(f"{rule}\n")
            print(f"Writing pf rule to {pfConfig}: {rule}")

            result = os.system(f"sudo pfctl -f {pfConfig}")
            print(f"pfctl load result: {result}")

            result = os.system("sudo pfctl -e")
            print(f"pfctl enable result: {result}")

    def prompt_for_override(self):
        """
        Prompt the user for a password to override the internet block.
        """
        userInput = getpass.getpass("Enter admin password: ")
        if userInput == self.admin_password:
            result = os.system("sudo pfctl -F all -f /etc/pf.conf")
            print(f"pfctl restore result: {result}")
            exit(0)
        else:
            print("Incorrect password")
        while True:
            userInput = getpass.getpass("Enter override password to restore internet access: ")
            if userInput == self.password:
                result = os.system("sudo pfctl -F all -f /etc/pf.conf")
                print(f"pfctl restore result: {result}")
                break
            else:
                print("Incorrect password. Please try again.")
