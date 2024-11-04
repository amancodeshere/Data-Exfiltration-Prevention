# os_alerts.py
import os
import platform


def sendAlerts(message):
    """
    Send an OS-level notification for alerts.

    Arguments:
        message (str): The message to be displayed in the alert.
    Returns:
        None

    Notes:
        Currently, this only works on macOS and Linux systems. On Windows,
        the alert will not work.
    """
    if platform.system() == 'Darwin':
        os.system(f"osascript -e 'display notification \"{message}\" with title \"Network Monitor Alert\"'")
    elif platform.system() == 'Linux':
        os.system(f'notify-send "Network Monitor Alert" "{message}"')
