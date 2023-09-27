import socket
import pickle
import json
from dict2xml import dict2xml
from cryptography.fernet import Fernet

port = 12345
host = socket.gethostname()

dictionary = {}
text_file = ()


# This function should set a dictionary to binary, JSON or XML format, and
# send it to the server
def send_dictionary():
    pass


# This function should provide the option to encrypt a file, and
# send it to the server
def send_file():
    pass


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.close()


if __name__ == "__main__":
    main()

