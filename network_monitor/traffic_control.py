# traffic_control.py

import logging
import os
import getpass  # To securely ask for the password

PASSWORD = "your_secure_password"  # Change this to a secure password of your choice

def block_traffic():
    # Implement logic to block network traffic
    logging.info("Blocking network traffic due to suspicious activity in monitored directory.")
    
    # Command to block all outbound traffic
    os.system('echo "block out all" | sudo pfctl -ef -')
    logging.info("Network traffic has been blocked.")
    
    # Prompt for password to restore traffic
    restore_traffic_prompt()

def restore_traffic():
    # Command to restore network traffic to its default state
    os.system('sudo pfctl -f /etc/pf.conf -e')
    logging.info("Network traffic has been restored to its default state.")

def restore_traffic_prompt():
    # Ask for password before restoring the traffic
    user_password = getpass.getpass("Enter password to restore network traffic: ")
    if user_password == PASSWORD:
        restore_traffic()
    else:
        logging.error("Incorrect password. Network traffic remains blocked.")
