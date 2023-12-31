import unittest
import socket
import pickle
import json
import xml.etree.ElementTree as ET
from Crypto.Cipher import AES
import sys


# Import the functions to be tested from the server code
from src.server import handle_dict, handle_file

# Constants for testing
PORT = 8080
SERVER_ADDR = ("localhost", PORT)
KEY = b"YourOwnSecretKey"
NONCE = b"YourOwnSecretNce"
BUFFER = 1024


class TestServer(unittest.TestCase):

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print(f"[ERROR] Error creating socket: {e}")
        sys.exit(1)

    try:
        # Bind the server socket to the specified address and port
        server_socket.bind(SERVER_ADDR)
    except socket.error as e:
        print(f"[ERROR] Socket binding failed with error: {e}")
        sys.exit(1)

    def test_handle_dict_binary(self):
        # Test handle_dict with binary data format
        data_format = "B"
        data = {"United States": "Washington D.C.", "Italy": "Rome", "England": "London"}
        serialized_data = pickle.dumps(data)
        handle_dict(data_format, serialized_data)
        # Check if the output file contains the same dictionary
        with open("dict_to_file.txt", "r") as file:
            file_content = file.read()
        self.assertEqual(file_content, str(data))

    def test_handle_dict_json(self):
        # Test handle_dict with JSON data format
        data_format = "J"
        data = {"Germany": "Berlin", "Egypt": "Cairo", "Canada": "Ottawa"}
        serialized_data = json.dumps(data)
        handle_dict(data_format, serialized_data)
        # Check if the output file contains the same dictionary
        with open("dict_to_file.txt", "r") as file:
            file_content = file.read()
        self.assertEqual(file_content, str(data))

    def test_handle_dict_xml(self):
        # Test handle_dict with XML data format
        data_format = "X"
        data = {"Austria": "Vienna", "Netherlands": "Amsterdam", "Maldives": "Male"}
        root = ET.Element("root")
        for key, value in data.items():
            child = ET.Element(key)
            child.text = value
            root.append(child)
        serialized_data = ET.tostring(root).decode()
        handle_dict(data_format, serialized_data)
        # Check if the output file contains the same dictionary
        with open("dict_to_file.txt", "r") as file:
            file_content = file.read()
        self.assertEqual(file_content, str(data))

    def test_handle_file_plain_text(self):
        # Test handle_file with plain text (no encryption)
        encryption = "F"
        file_data = b"We are connected!"
        handle_file(encryption, file_data)
        # Check if the output file contains the same data
        with open("file_server.txt", "r") as file:
            file_content = file.read()
        self.assertEqual(file_content, file_data.decode())

    def test_handle_file_encrypted(self):
        # Test handle_file with encrypted data
        encryption = "T"
        plaintext = "We are connected!"
        cipher = AES.new(KEY, AES.MODE_EAX, NONCE)
        encrypted_data = cipher.encrypt(plaintext.encode())
        handle_file(encryption, encrypted_data)
        # Check if the output file contains the decrypted data
        with open("file_server.txt", "r") as file:
            file_content = file.read()
        self.assertEqual(file_content, plaintext)


if __name__ == "__main__":
    unittest.main()
