import os
import getpass

class WifiBlocker:
    def __init__(self):
        self.password = "1234"

    def block_wifi(self):
        if os.uname().sysname == 'Darwin':
            self.block_specific_with_pf()

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

    def prompt_for_override(self):
        while True:
            user_input = getpass.getpass("Enter override password to restore internet access: ")
            if user_input == self.password:
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
