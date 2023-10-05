import socket
import os
import sys
import pickle
import json
from dict2xml import dict2xml
from Crypto.Cipher import AES

from samples.dict_sample import dictionary

PORT = 8080
HOST = "localhost"
SERVER_ADDR = (HOST, PORT)

# Provide your own key. It has to be 16 bites.
KEY = b"YourOwnSecretKey"
# Provide a nonce. It has to be 16 bites.
NONCE = b"YourOwnSecretNce"


# This function should set a dictionary to binary, JSON or XML format, and
# send it to the server
def send_dictionary(socket, dictionary, data_format):
    serialized_dict = ""
    dict_size = sys.getsizeof(dictionary)
    socket.send(str(dict_size).encode())

    # B for BINARY
    if data_format == "B":
        serialized_dict = pickle.dumps(dictionary)
        socket.send(f"SEND_D|{data_format}".encode())
        socket.sendall(serialized_dict)

    # J for JSON
    elif data_format == "J":
        serialized_dict = json.dumps(dictionary)
        socket.send(f"SEND_D|{data_format}".encode())
        socket.sendall(serialized_dict.encode())

    # X for XML
    elif data_format == "X":
        serialized_dict = dict2xml(dictionary, wrap='root', indent="   ")
        socket.send(f"SEND_D|{data_format}".encode())
        socket.sendall(serialized_dict.encode())


# This function should provide the option to encrypt a file, and
# send it to the server
def send_file(socket, file, encrypt):

    # Opening a file
    with open(file, "rb") as f:
        data = f.read()

        # T for TRUE
        if encrypt == "T":
            cipher = AES.new(KEY, AES.MODE_EAX, NONCE)

            # Encrypting the file
            encrypted_data = cipher.encrypt(data)
            file_size = os.path.getsize(file)
            socket.send(str(file_size).encode())
            socket.send(f"SEND_F|{encrypt}".encode())
            socket.send(encrypted_data)

        # F for FALSE
        elif encrypt == "F":
            file_size = os.path.getsize(file)
            socket.send(str(file_size).encode())
            socket.send(f"SEND_F|{encrypt}".encode())
            socket.send(data)


def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDR)

    command = input("[SENT_ITEM] Are you sending a DICTIONARY OR a FILE (D/F)? \n> ")

    if command == "D":
        data_format = input("[DATA_FORMAT] In which format are you sending the dictionary, "
                            "BINARY, JSON or XML (B/J/X)? \n> ")

        # Call send_dictionary function to send a dictionary to the server
        send_dictionary(client_socket, dictionary, data_format)

    elif command == "F":
        encrypt = input("[ENCRYPTION] Are you sending an encrypted file? Use ´T´ for ´Encrypted´ and "
                        "´F´ for ´decrypted´ \n> ")

        # Call send_file function to send a file to the server
        send_file(client_socket, "../samples/file_sample.txt", encrypt)

    client_socket.close()


if __name__ == "__main__":
    connect()
