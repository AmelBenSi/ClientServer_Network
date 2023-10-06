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

# Provide a 16-byte long key.
KEY = b"YourOwnSecretKey"
# Provide a 16-byte long key nonce
NONCE = b"YourOwnSecretNce"


# This function serializes a dictionary in BINARY, JSON or XML format, then
# sends it to the server
def send_dictionary(conn, dict, data_format):
    # Get the dictionary´s size
    dict_size = sys.getsizeof(dict)
    # Send the dictionary´s size to the server
    conn.send(str(dict_size).encode())

    # B for BINARY
    if data_format == "B":
        # Serialize the dictionary in BINARY format
        serialized_dict = pickle.dumps(dict)
        # Send information to the server: Header "SEND_D" and Data Format
        conn.send(f"SEND_D|{data_format}".encode())
        # Send the serialized dictionary to the server
        conn.sendall(serialized_dict)

    # J for JSON
    elif data_format == "J":
        # Serialize the dictionary in JSON format
        serialized_dict = json.dumps(dict)
        # Send information to the server: Header "SEND_D" and Data Format
        conn.send(f"SEND_D|{data_format}".encode())
        # Send the serialized dictionary to the server
        conn.sendall(serialized_dict.encode())

    # X for XML
    elif data_format == "X":
        # Serialize the dictionary in XML format
        serialized_dict = dict2xml(dict, wrap='root', indent="   ")
        # Send information to the server: Header "SEND_D" and Data Format
        conn.send(f"SEND_D|{data_format}".encode())
        # Send the serialized dictionary to the server
        conn.sendall(serialized_dict.encode())

    else:
        # Raise an Error if the user types an incorrect value
        raise ValueError("Only ´B´, ´J´ and ´X´ allowed!")


# This function allows to choose whether to encrypt or not a file, then
# sends the file to the server
def send_file(conn, file, encrypt):
    # Opening a file
    with open(file, "rb") as f:
        data = f.read()

        # T for TRUE
        if encrypt == "T":
            # Initialize and AES encryption object
            cipher = AES.new(KEY, AES.MODE_EAX, NONCE)

            # Encrypting the file
            encrypted_data = cipher.encrypt(data)
            # Get the file´s size
            file_size = os.path.getsize(file)
            # Send the file´s size to the server
            conn.send(str(file_size).encode())
            # Send information to the server: Header "SEND_F" and encryption status
            conn.send(f"SEND_F|{encrypt}".encode())
            # Send the encrypted file to the server
            conn.send(encrypted_data)

        # F for FALSE
        elif encrypt == "F":
            # Get the file´s size
            file_size = os.path.getsize(file)
            # Send the file´s size to the server
            conn.send(str(file_size).encode())
            # Send information to the server: Header "SEND_F" and encryption status
            conn.send(f"SEND_F|{encrypt}".encode())
            # Send the file to the server
            conn.send(data)

        else:
            # Raise an Error if the user types an incorrect value
            raise ValueError("Only ´T´ and ´F´ allowed!")


def connect():

    # create an INET, STREAMing socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # now connect to the web server on port 8080
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
