import requests
import time

def send_http_requests(url='http://127.0.0.1:8000'):
    while True:
        response = requests.get(url)
        print(f"Request: Status code {response.status_code}")
        time.sleep(1)  # Delay between requests (adjust as needed)

send_http_requests()
