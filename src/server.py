import socket
import threading
import pickle
import json
import ast
import xml.etree.ElementTree as ET
from Crypto.Cipher import AES


PORT = 8080
HOST = ""
SERVER_ADDR = (HOST, PORT)
KEY = b"TheNeuralNineKey"
NONCE = b"TheNeuralNineNce"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDR)


def handle_dict(data_format, serialized_dict):

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

    print(f"[DICT_TO_SCREEN] Dictionary was sent in {data_format} format: {original_dict}")
    with open("dict_to_file.txt", "w") as file:
        file.write(str(original_dict))


def handle_file(encryption, file_data):

    if encryption == "False":
        with open("file_server.txt", "w") as file:
            file.write(file_data)
        print(f"[PRINT_TO_SCREEN] The content of a file: {file_data}")

    elif encryption == "True":
        cipher = AES.new(KEY, AES.MODE_EAX, NONCE)
        binary_data = ast.literal_eval(file_data)
        decrypt_data = cipher.decrypt(binary_data).decode()
        print(f"[PRINT_TO_SCREEN] The content of a file sent encrypted: {decrypt_data}")
        with open("file_server.txt", "w") as dec_file:
            dec_file.write(decrypt_data)


def handle_data(received_data):

    decoded_data = received_data.decode()
    split = decoded_data.split("|")
    header = split[0]
    data_format = split[1]
    data = split[2]
    print(header, data_format, sep="\n")

    if header == "SEND_DICTIONARY":
        handle_dict(data_format, data)

    elif header == "SEND_FILE":
        handle_file(data_format, data)


# This function should handle all the communications between the client and the server
def handle_client(client_socket, client_addr):

    print(f"[NEW CONNECTION] {client_addr} is connected to the server")

    connected = True
    while connected:
        received_data = client_socket.recv(1024)
        handle_data(received_data)
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




