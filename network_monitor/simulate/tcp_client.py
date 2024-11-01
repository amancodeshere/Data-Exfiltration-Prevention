import socket
import time

def send_tcp_packets(ip='127.0.0.1', port=8080, message="Hello, Server!"):
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.sendall(message.encode())
        print("Sent packet")
        sock.close()
        time.sleep(1)  # Delay between packets (adjust as needed)

send_tcp_packets()
