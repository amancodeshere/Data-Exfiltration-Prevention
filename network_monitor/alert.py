# alert.py
import os

def send_alert(message):
    os.system(f"osascript -e 'display notification \"{message}\" with title \"Alert!\"'")


# # alert.py
# import smtplib
# from email.mime.text import MIMEText

# def send_email_alert(message):
#     msg = MIMEText(message)
#     msg['Subject'] = 'Suspicious Network Activity Detected'
#     msg['From'] = 'youremail@example.com'
#     msg['To'] = 'alertrecipient@example.com'

#     with smtplib.SMTP('smtp.example.com', 587) as server:
#         server.starttls()
#         server.login('youremail@example.com', 'yourpassword')
#         server.send_message(msg)

