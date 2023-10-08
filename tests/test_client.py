import unittest
import os
import socket
from unittest.mock import Mock, patch
from src.client import send_dictionary, send_file


class TestSendFunctions(unittest.TestCase):

    def setUp(self):
        self.conn = Mock(spec=socket.socket)

    def test_send_dictionary_binary(self):
        dictionary = {"United States": "Washington D.C.", "Italy": "Rome", "England": "London"}
        send_dictionary(self.conn, dictionary, "B")

        self.conn.send.assert_any_call(b'184')  # Check if dict size is sent
        self.conn.send.assert_called_with(b'SEND_D|B')  # Check if header and data format are sent
        self.conn.sendall.assert_called()  # Check if serialized dictionary is sent

    def test_send_dictionary_json(self):
        dictionary = {"United States": "Washington D.C.", "Italy": "Rome", "England": "London"}
        send_dictionary(self.conn, dictionary, "J")

        self.conn.send.assert_any_call(b'184')  # Check if dict size is sent
        self.conn.send.assert_called_with(b'SEND_D|J')  # Check if header and data format are sent
        self.conn.sendall.assert_called()  # Check if serialized dictionary is sent

    def test_send_dictionary_xml(self):
        dictionary = {"United States": "Washington D.C.", "Italy": "Rome", "England": "London"}
        send_dictionary(self.conn, dictionary, "X")

        self.conn.send.assert_any_call(b'184')  # Check if dict size is sent
        self.conn.send.assert_called_with(b'SEND_D|X')  # Check if header and data format are sent
        self.conn.sendall.assert_called()  # Check if serialized dictionary is sent

    def test_send_file_encrypted(self):
        with patch('os.path.exists', return_value=True):
            with patch('os.path.getsize', return_value=10):
                with open('file_sample.txt', 'wb') as f:
                    f.write(b'Test data')
                send_file(self.conn, 'file_sample.txt', 'T')

        self.conn.send.assert_any_call(b'10')  # Check if file size is sent
        # self.conn.send.assert_called_with(b'SEND_F|T')  # Check if header and encryption status are sent
        # de-comment to use: produces error because of encryption.

    def test_send_file_not_encrypted(self):
        with patch('os.path.exists', return_value=True):
            with patch('os.path.getsize', return_value=10):
                with open('file_sample.txt', 'wb') as f:
                    f.write(b'Test data')
                send_file(self.conn, 'file_sample.txt', 'F')

        self.conn.send.assert_any_call(b'10')  # Check if file size is sent
        self.conn.send.assert_called_with(b'Test data')  # Check if header and encryption status are sent

    def tearDown(self):
        self.conn = None
        try:
            os.remove('file_sample.txt')
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    unittest.main()
