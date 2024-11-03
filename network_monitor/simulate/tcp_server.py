import socket

def start_server(port=8080):
    """
    Starts a TCP server that listens on the given port and prints any received data.

    :param port: The port number to listen on. Defaults to 8080.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(5)
    print(f"Server listening on 127.0.0.1:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        data = client_socket.recv(1024)
        if data:
            print("Received:", data.decode())
        client_socket.close()

start_server()
