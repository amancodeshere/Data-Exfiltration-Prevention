# os_alerts.py
import os
import platform

def send_os_alert(message):
    if platform.system() == 'Darwin':  # macOS
        os.system(f"osascript -e 'display notification \"{message}\" with title \"Network Monitor Alert\"'")
    elif platform.system() == 'Linux':
        os.system(f'notify-send "Network Monitor Alert" "{message}"')
    elif platform.system() == 'Windows':
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast("Network Monitor Alert", message, duration=10)
