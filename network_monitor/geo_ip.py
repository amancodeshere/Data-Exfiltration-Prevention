# geo_ip.py
import requests
import ipaddress

def is_private_ip(ip):
    """
    Checks if an IP address is in a private range according to RFC1918.

    Args:
        ip (str): The IP address to check.

    Returns:
        bool: True if the IP is in a private range, False if it is not.
    """
    return ipaddress.ip_address(ip).is_private

def get_geo_location(ip):
    """
    Retrieves the location information for a given IP address.

    Args:
        ip (str): The IP address

    Returns:
        data: The geolocation data or a failure message if the IP address is in a private range.
    """
    if is_private_ip(ip):
        return {'status': 'fail', 'message': 'private range', 'query': ip}

    response = requests.get(f"http://ip-api.com/json/{ip}")

    data = response.json()
    # print(f"Geo-IP response for {ip}: {data}")

    return data
