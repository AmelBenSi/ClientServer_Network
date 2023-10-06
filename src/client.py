import socket
import os
import sys
import pickle
import json
from dict2xml import dict2xml
from Crypto.Cipher import AES

# Import the dictionary data from an external file
from samples.dict_sample import dictionary

PORT = 8080
HOST = "localhost"
SERVER_ADDR = (HOST, PORT)

# Provide a 16-byte long key and nonce for encryption.
KEY = b"YourOwnSecretKey"
NONCE = b"YourOwnSecretNce"


# Function to serialize a dictionary and send it to the server
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


# Function to send a file with or without encryption to the server
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


# Function to establish a connection to the server
def connect():
    # create an INET, STREAMing socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect to the web server on port 8080
    client_socket.connect(SERVER_ADDR)

    command = input("[DATA_TYPE] Please specify the type of data you want to send: "
                    "Is it a DICTIONARY (D) or a FILE (F)? \n> ")
    if command == "D":
        data_format = input("[DATA_FORMAT] Please select the format in which you would like to send the dictionary: "
                            "BINARY (B), JSON (J), or XML (X)? \n> ")
        # Call send_dictionary function to send a dictionary to the server
        send_dictionary(client_socket, dictionary, data_format)
    elif command == "F":
        encrypt = input("[ENCRYPTION] Would you like to send the file with encryption? "
                        "Please enter ´T´ for ´Encrypted´ or ´F´ for ´Decrypted´ transmission: \n> ")
        # Call send_file function to send a file to the server
        send_file(client_socket, "../samples/file_sample.txt", encrypt)

    # Send a close message to the server
    client_socket.close()


if __name__ == "__main__":
    connect()
