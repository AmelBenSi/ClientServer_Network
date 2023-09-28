import socket
import threading
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet


PORT = 5050
HOST = ""
SERVER_ADDR = (HOST, PORT)
FORMAT = "utf-8"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDR)


# comment later
def receive_date(received_data):

    # Try to decode as JSON
    try:
        decoded_data = json.loads(received_data.decode())
        return decoded_data
    except (json.JSONDecodeError, UnicodeDecodeError):
        pass

    # Try to decode as binary
    try:
        decoded_data = pickle.loads(received_data)
        return decoded_data
    except pickle.UnpicklingError:
        pass

    # Try to decode as XML
    try:
        root = ET.fromstring(received_data.decode())
        decoded_data = {child.tag: child.text for child in root}
        return decoded_data
    except ET.ParseError:
        raise ValueError("Received data is neither valid JSON, binary, nor XML.")


# This function should handle all the communications between the client and the server
def handle_client(client_socket, client_addr):
    print(f"[NEW CONNECTION] {client_addr} is connected to the server")

    connected = True

    while connected:

        received_data = client_socket.recv(4096)
        dictionary = receive_date(received_data)
        print(dictionary)
        connected = False


# This function should handle the connection with the client
def start():
    server_socket.listen(5)

    while True:
        client_socket, client_addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
        thread.start()


if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()
