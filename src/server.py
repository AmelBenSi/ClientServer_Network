import socket
import threading
import pickle
import json
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet


PORT = 8080
HOST = socket.gethostbyname(socket.gethostname())
SERVER_ADDR = (HOST, PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDR)


def handle_dict(received_data):

    input_data = received_data.decode()
    print(input_data)
    first_split = input_data.split("|")
    print(first_split)
    header = first_split[0]
    data_format = first_split[1]
    serialized_data = first_split[2]
    print(first_split)
    print(header)
    print(data_format)
    print(serialized_data)

    if header == "SEND_DICTIONARY":

        if data_format == "BINARY":
            original_data = pickle.loads(serialized_data).decode()

        elif data_format == "JSON":
            original_data = json.loads(serialized_data)

        elif data_format == "XML":
            root = ET.fromstring(serialized_data)
            original_data = {child.tag: child.text for child in root}

        else:
            raise ValueError("Received data is neither valid JSON, binary, nor XML.")

        print(f"[PRINT_TO_SCREEN] Dictionary sent in format {data_format}: {original_data}")


# This function should handle all the communications between the client and the server
def handle_client(client_socket, client_addr):

    print(f"[NEW CONNECTION] {client_addr} is connected to the server")

    connected = True
    while connected:
        received_data = client_socket.recv(1024)
        handle_dict(received_data)
        connected = False


# This function should handle the connection with the client
def start():
    server_socket.listen()

    while True:
        client_socket, client_addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_addr))
        thread.start()


if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()




