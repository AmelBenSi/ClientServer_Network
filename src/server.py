import socket
import pickle
import json
from dict2xml import dict2xml
from cryptography.fernet import Fernet

port = 12345
host = socket.gethostname()


# This function should handle the files sent from the client
def handle_client(client_socket):
    files = client_socket.recv()
    pass


# This function establishes the connection with the client
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"{client_address} is connected to the server")
        handle_client(client_socket)


if __name__ == "__main__":
    main()
