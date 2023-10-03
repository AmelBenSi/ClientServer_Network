import socket
import threading
import pickle
import json
import ast
import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet


PORT = 8080
HOST = ""
#HOST = socket.gethostbyname(socket.gethostname())
SERVER_ADDR = (HOST, PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDR)


def handle_dict(received_dict):

    decoded_dict = received_dict.decode()
    split = decoded_dict.split("|")
    header = split[0]
    data_format = split[1]
    serialized_dict = split[2]
    print(header, data_format, serialized_dict, sep="\n")

    if header == "SEND_DICTIONARY":

        if data_format == "BINARY":
            binary_dict = ast.literal_eval(serialized_dict)
            original_dict = pickle.loads(binary_dict)

        elif data_format == "JSON":
            original_dict = json.loads(serialized_dict)

        elif data_format == "XML":
            root = ET.fromstring(serialized_dict)
            original_dict = {child.tag: child.text for child in root}

        else:
            raise ValueError("Received data is neither valid JSON, binary, nor XML.")

        print(f"[PRINT_TO_SCREEN] Dictionary was sent in {data_format} format: {original_dict}")
        with open("print_to_file.txt", "w") as file:
            file.write(str(original_dict))


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




