import socket
import pickle
import json
from dict2xml import dict2xml
#import xml.etree.ElementTree as ET
from cryptography.fernet import Fernet

PORT = 8080
HOST = socket.gethostbyname(socket.gethostname())
SERVER_ADDR = (HOST, PORT)


# This function should set a dictionary to binary, JSON or XML format, and
# send it to the server
def send_dictionary(socket, dictionary, data_format):
    if data_format == "BINARY":
        serialized_dict = pickle.dumps(dictionary)
    elif data_format == "JSON":
        serialized_dict = json.dumps(dictionary)
    elif data_format == "XML":
        serialized_dict = dict2xml(dictionary).decode()

    socket.send(f"SEND_DICTIONARY|{data_format}|{serialized_dict}".encode())


        #root = ET.Element("root")
        #for key, value in dictionary.items():
        #    ET.SubElement(root, key).text = value
        #serialized_dict = ET.tostring(root).decode()
        #"""



"""
# This function should provide the option to encrypt a file, and
# send it to the server
def send_file(socket, file, encrypt=False):
    # opening a file to encrypt
    with open(file, "rb") as file:
        original_file = file.read()

        if encrypt:
            # key generation
            key = Fernet.generate_key()

            # using the generated key
            fernet = Fernet(key)

            # encrypting the file
            encrypted_file = fernet.encrypt(original_file)

    socket.send(f"SEND_FILE:{file}|{encrypt}|{encrypted_data.decode()}".encode())
"""


def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDR)

    # Create a dictionary
    dictionary = {
        "year": 2023,
        "month": "September",
        "day": 28
    }

    # Call send_dictionary function to send the dictionary to the server
    send_dictionary(client_socket, dictionary, "BINARY")

    client_socket.close()
"""
    # Call send_file function to send a file to the server
    send_file(client_socket, "file_example.txt", encrypt=True)
"""

if __name__ == "__main__":
    connect()





