# config.py
ALERT_THRESHOLD = 2  # Number of suspicious packets to trigger an alert
BLACKLISTED_IPS = ['10.168.201.65', "127.0.0.1:8000", "192.168.1.10", "8.8.8.8", "127.0.0.1", "17.248.155.203", '127.0.0.1', '1.1.1.1', '208.67.222.222' ,'192.168.1.100']  # Sample blacklisted IPs

allowed_countries = ['Australia', 'United States', 'United Kingdom']  # Example list
# config.py
# BLACKLISTED_IPS = ['127.0.0.1', '17.248.155.203', '23.214.88.41']
# ALERT_THRESHOLD = 5
# EMAIL_SETTINGS = {
#     'sender': 'youremail@example.com',
#     'recipient': 'alertrecipient@example.com',
#     'smtp_server': 'smtp.example.com',
#     'smtp_port': 587,
#     'password': 'yourpassword'
# }

