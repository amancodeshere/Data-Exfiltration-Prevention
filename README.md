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



### Usage
------------
DISCLAIMER: **This will block you internet access untill an override/admin password is entered.**

To run the application, follow these steps:

1. Make sure you are in network_monitor directory: `cd network-monitor`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application in one terminal: `python simulate/sim1.py`
4. Run the application in a second terminal: `python simulate/sim2.py`
5. Run the application in a third terminal: `python main.py`
6. Open the web dashboard from the terminal main.py ran in: `python web_dashboard.py`
7. Then open the link given by web_dashboard.py in a web browser to view the dashboard
