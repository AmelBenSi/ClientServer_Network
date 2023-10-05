import socket
import threading
import pickle
import json
import xml.etree.ElementTree as ET
from Crypto.Cipher import AES
import tqdm


PORT = 8080
HOST = ""
SERVER_ADDR = (HOST, PORT)
BUFFER = 1024

# Insert your own key
KEY = b"YourOwnSecretKey"
# Insert your own nonce
NONCE = b"YourOwnSecretNce"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(SERVER_ADDR)


def handle_dict(data_format, serialized_dict):

    if data_format == "B":
        original_dict = pickle.loads(serialized_dict)

    elif data_format == "J":
        original_dict = json.loads(serialized_dict)

    elif data_format == "X":
        root = ET.fromstring(serialized_dict)
        original_dict = {child.tag: child.text for child in root}

    else:
        raise ValueError("Received data is neither valid JSON, binary, nor XML.")

    print(f"[DICT_TO_SCREEN] Dictionary was sent in {data_format} format: {original_dict}")
    with open("dict_to_file.txt", "w") as file:
        file.write(str(original_dict))


def handle_file(encryption, file_data):

    if encryption == "F":
        decoded_file = file_data.decode()
        with open("file_server.txt", "w") as file:
            file.write(decoded_file)
        print(f"[PRINT_TO_SCREEN] Content of the file: {decoded_file}")

    elif encryption == "T":
        cipher = AES.new(KEY, AES.MODE_EAX, NONCE)
        decrypt_data = cipher.decrypt(file_data).decode()
        print(f"[PRINT_TO_SCREEN] Content of the encrypted file: {decrypt_data}")
        with open("file_server.txt", "w") as dec_file:
            dec_file.write(decrypt_data)


def handle_data(received_data, data_info):

    split = data_info.split("|")
    header = split[0]
    data_format = split[1]
    print(header, data_format, sep="\n")

    if header == "SEND_D":
        handle_dict(data_format, received_data)

    elif header == "SEND_F":
        handle_file(data_format, received_data)


# This function should handle all the communications between the client and the server
def handle_client(client_socket, client_addr):

    print(f"[NEW CONNECTION] {client_addr} is connected to the server")

    # Receive the size of sent data
    data_size = int(client_socket.recv(BUFFER).decode())
    data_info = client_socket.recv(8).decode()

    received_data = b""

    progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(data_size))

    while True:
        chunk_of_data = client_socket.recv(BUFFER)
        received_data += chunk_of_data
        progress.update(BUFFER)
        if len(chunk_of_data) < BUFFER:
            break

    handle_data(received_data, data_info)


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