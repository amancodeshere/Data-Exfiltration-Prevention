# geo_ip.py
import requests

def get_geo_location(ip):
    response = requests.get(f"http://ip-api.com/json/{ip}")
    return response.json()
