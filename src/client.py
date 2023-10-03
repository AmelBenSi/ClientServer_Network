import socket
import pickle
import json
from dict2xml import dict2xml
from Crypto.Cipher import AES

PORT = 8080
HOST = "localhost"
SERVER_ADDR = (HOST, PORT)
KEY = b"TheNeuralNineKey"
NONCE = b"TheNeuralNineNce"


# This function should set a dictionary to binary, JSON or XML format, and
# send it to the server
def send_dictionary(socket, dictionary, data_format):
    serialized_dict = ""
    if data_format == "BINARY":
        serialized_dict = pickle.dumps(dictionary)
    elif data_format == "JSON":
        serialized_dict = json.dumps(dictionary)
    elif data_format == "XML":
        serialized_dict = dict2xml(dictionary, wrap='root', indent="   ")

    socket.send(f"SEND_DICTIONARY|{data_format}|{serialized_dict}".encode())


# This function should provide the option to encrypt a file, and
# send it to the server
def send_file(socket, file, encrypt):

    # opening a file
    with open(file, "rb") as file:
        data = file.read()

        if encrypt:
            cipher = AES.new(KEY, AES.MODE_EAX, NONCE)

            # encrypting the file
            data = cipher.encrypt(data)
            socket.send(f"SEND_FILE|{encrypt}|{data}".encode())
        else:
            socket.send(f"SEND_FILE|{encrypt}|{data.decode()}".encode())


def connect():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDR)

    # Create a dictionary
    dictionary = {
        "year": 2023,
        "month": "September",
        "day": 28
    }
    command = input("[SENT_ITEM] Are you sending a DICTIONARY OR a FILE? ")
    if command == "DICTIONARY":
        # Call send_dictionary function to send a dictionary to the server
        send_dictionary(client_socket, dictionary, "XML")
    if command == "FILE":
        # Call send_file function to send a file to the server
        send_file(client_socket, "file_example.txt", encrypt=True)

    client_socket.close()


if __name__ == "__main__":
    connect()
