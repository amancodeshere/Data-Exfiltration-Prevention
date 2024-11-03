# geo_ip.py
import requests
import ipaddress

def is_private_ip(ip):
    return ipaddress.ip_address(ip).is_private

def get_geo_location(ip):
    if is_private_ip(ip):
        return {'status': 'fail', 'message': 'private range', 'query': ip}
    response = requests.get(f"http://ip-api.com/json/{ip}")
    data = response.json()
    print(f"Geo-IP response for {ip}: {data}")  # Debug log
    return data
