import socket
import pickle
import json
from dict2xml import dict2xml
from cryptography.fernet import Fernet

PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
SERVER_ADDR = (HOST, PORT)
FORMAT = "utf-8"


# This function should set a dictionary to binary, JSON or XML format, and
# send it to the server
def send_dictionary(socket_conn, dictionary, data_format):
    if data_format == "binary":
        serialized_dict = pickle.dumps(dictionary)
    elif data_format == "JSON":
        serialized_dict = json.dumps(dictionary).encode(FORMAT)
    elif data_format == "XML":
        serialized_dict = dict2xml(dictionary)

    socket_conn.send(serialized_dict)


# This function should provide the option to encrypt a file, and
# send it to the server
def send_file():
    pass


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(SERVER_ADDR)

    dictionary = {
        "month": "February",
        "year": 2020,
        "day": 21}

    send_dictionary(client_socket, dictionary, "JSON")

    client_socket.close()


if __name__ == "__main__":
    main()

