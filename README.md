# AwesomeDEP

-----------

A network monitoring system designed to detect, prevent, and mitigate data exfiltration.


### Overview
-----------


This project aims to develop and implement methods to protect sensitive information from unauthorized access and theft. It utilizes a combination of packet capture, analysis, and alerting mechanisms to identify and respond to potential security threats.

### Features
------------

* Packet capture and analysis using Scapy
* Alerting system for suspicious network activity
* Web-based dashboard for monitoring and visualization
* Integration with SQLite database for storing and querying network activity

### Requirements
------------

* Python 3.x
* Scapy
* Flask
* Flask-SocketIO
* requests
* win10toast
* SQLite3

**Important Note: Remember the passwords you create, as ADEP is designed to stop all internet until it recieves the password by design. The admin password will stop logging as soon as it is entered whereas the user password will be required every time a suspicious packet is detected. If the main is stopped without the password and internet is blocked, restarting the machine will fix the problem.**


### Usage
------------
DISCLAIMER: **This will block your internet access untill an override/admin password is entered.**

To run the application, follow these steps:

1. Make sure you are in network_monitor directory: `cd network-monitor`
2. Install dependencies: `pip install -r requirements.txt`
3. Initialise the databse:`python -c "from database import init_db; init_db()"`
4. Open a second terminal and navigate to the simulate directory inside network-monitor and run sim1: `sudo python sim1.py`
5. Open a third terminal and navigate to the simulate directory inside network-monitor and run sim2: `sudo python sim2.py`
6. Run the application in teh original terminal: `sudo python main.py`
    a. Enter the admin and the user password
    b. When asked for, enter the admin password to stop the logging or user passsword to continue the logging.
7. After the main file has stopped running, open the web dashboard from the terminal main.py ran in: `python web_dashboard.py`
8. Then open the link given by web_dashboard.py in a web browser to view the dashboard
