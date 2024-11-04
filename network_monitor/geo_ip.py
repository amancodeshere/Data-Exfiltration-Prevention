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
    # This function simply calls the is_private method on the ipaddress
    # object, which checks if the IP is in a private range.
    return ipaddress.ip_address(ip).is_private

def get_geo_location(ip):
    """
    Retrieves the location information for a given IP address.

    Args:
        ip (str): The IP address

    Returns:
        data: The geolocation data or a failure message if the IP address is in a private range.
    """
    # Check if the IP address is in a private range
    if is_private_ip(ip):
        return {'status': 'fail', 'message': 'private range', 'query': ip}

    # request the IP-API service to get the geolocation
    response = requests.get(f"http://ip-api.com/json/{ip}")

    # Parse the JSON-response to a dictionary
    data = response.json()
    # print(f"Geo-IP response for {ip}: {data}")

    return data
