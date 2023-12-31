import unittest
import socket
from unittest.mock import Mock
from src.client import send_dictionary


class TestSendFunctions(unittest.TestCase):

    def setUp(self):
        self.conn = Mock(spec=socket.socket)

    def test_send_dictionary_binary(self):
        dictionary = {7: 'Andrews', 9: 'Appleton', 10: 'Artagaveytia', 11: 'Astor', 12: 'Astor',
                      13: 'Aubart', 14: 'Barber', 15: 'Barkworth', 16: 'Bassani', 17: 'Baumann', 18: 'Baxter',
                      19: 'Baxter', 20: 'Beattie', 21: 'Beckwith', 22: 'Beckwith', 23: 'Behr', 24: 'Bessette',
                      25: 'Bidois', 26: 'Bird', 27: 'Birnbaum',  28: 'Bishop', 29: 'Bishop',
                      30: 'Björnström-Steffansson', 31: 'Blackwell', 32: 'Blank', 33: 'Bonnell', 34: 'Bonnell',
                      35: 'Borebank', 36: 'Bowen', 37: 'Bowerman', 38: 'Brady', 39: 'Brandeis', 40: 'Brereton',
                      41: 'Brewe', 42: 'Brown', 43: 'Brown', 44: 'Bucknell', 45: 'Burns', 46: 'Butt', 47: 'Cairns',
                      48: 'Calderhead', 49: 'Candee', 50: 'Cardeza', 51: 'Cardeza', 52: 'Carlsson',
                      53: 'Carraú-Esteves', 54: 'Carrau', 55: 'Carter', 56: 'Carter', 57: 'Carter', 58: 'Carter',
                      59: 'Case', 60: 'Cassebeer', 61: 'Cavendish', 62: 'Cavendish', 63: 'Chaffee', 64: 'Chaffee',
                      65: 'Chambers', 66: 'Chambers', 67: 'Chaudanson', 68: 'Cherry', 69: 'Chevré', 70: 'Chibnall',
                      71: 'Chisholm', 72: 'Clark', 73: 'Clark', 74: 'Cleaver', 75: 'Clifford', 76: 'Colley',
                      77: 'Compton', 78: 'Compton', 79: 'Compton', 80: 'Cornell', 81: 'Crafton', 82: 'Crosby',
                      83: 'Crosby', 84: 'Crosby', 85: 'Cumings', 86: 'Cumings', 87: 'Daly', 88: 'Daniel', 89: 'Daniels',
                      90: 'Davidson', 91: 'Davidson', 92: 'Dick', 93: 'Dick', 94: 'Dodge', 95: 'Dodge', 96: 'Dodge',
                      97: 'Douglas', 98: 'Douglas', 99: 'Douglas', 100: 'Duff Gordon', 101: 'Duff Gordon',
                      102: 'Dulles', 103: 'Earnshaw', 104: 'Endres', 105: 'Eustis', 106: 'Evans', 107: 'Farthing',
                      108: 'Flegenheim', 109: 'Fleming', 110: 'Flynn', 111: 'Foreman', 112: 'Fortune', 113: 'Fortune',
                      114: 'Fortune', 115: 'Fortune', 116: 'Fortune', 117: 'Fortune', 118: 'Francatelli',
                      119: 'Franklin', 120: 'Frauenthal', 121: 'Frauenthal', 122: 'Frauenthal', 123: 'Frölicher',
                      124: 'Frölicher-Stehli', 125: 'Frölicher-Stehli', 126: 'Fry', 127: 'Futrelle', 128: 'Futrelle',
                      129: 'Gee', 130: 'Gibson', 131: 'Gibson', 132: 'Gieger', 133: 'Giglio', 134: 'Goldenberg'}

        send_dictionary(self.conn, dictionary, "B")

        self.conn.send.assert_any_call(b'4688')  # Check if dict size is sent
        self.conn.send.assert_called_with(b'SEND_D|B')  # Check if header and data format are sent
        self.conn.sendall.assert_called()  # Check if serialized dictionary is sent

    def test_send_dictionary_json(self):
        dictionary = {
                      13: 'Aubart', 14: 'Barber', 15: 'Barkworth', 16: 'Bassani', 17: 'Baumann', 18: 'Baxter',
                      19: 'Baxter', 20: 'Beattie', 21: 'Beckwith', 22: 'Beckwith', 23: 'Behr', 24: 'Bessette',
                      25: 'Bidois', 26: 'Bird', 27: 'Birnbaum',  28: 'Bishop', 29: 'Bishop',
                      30: 'Björnström-Steffansson', 31: 'Blackwell', 32: 'Blank', 33: 'Bonnell', 34: 'Bonnell',
                      35: 'Borebank', 36: 'Bowen', 37: 'Bowerman', 38: 'Brady', 39: 'Brandeis', 40: 'Brereton',
                      41: 'Brewe', 42: 'Brown', 43: 'Brown', 44: 'Bucknell', 45: 'Burns', 46: 'Butt', 47: 'Cairns',
                      48: 'Calderhead', 49: 'Candee', 50: 'Cardeza', 51: 'Cardeza', 52: 'Carlsson',
                      53: 'Carraú-Esteves', 54: 'Carrau', 55: 'Carter', 56: 'Carter', 57: 'Carter', 58: 'Carter',
                      59: 'Case', 60: 'Cassebeer', 61: 'Cavendish', 62: 'Cavendish', 63: 'Chaffee', 64: 'Chaffee',
                      65: 'Chambers', 66: 'Chambers', 67: 'Chaudanson', 68: 'Cherry', 69: 'Chevré', 70: 'Chibnall',
                      71: 'Chisholm', 72: 'Clark', 73: 'Clark', 74: 'Cleaver', 75: 'Clifford', 76: 'Colley',
                      77: 'Compton', 78: 'Compton', 79: 'Compton', 80: 'Cornell', 81: 'Crafton', 82: 'Crosby',
                      83: 'Crosby', 84: 'Crosby', 85: 'Cumings', 86: 'Cumings', 87: 'Daly', 88: 'Daniel', 89: 'Daniels',
                      90: 'Davidson', 91: 'Davidson', 92: 'Dick', 93: 'Dick', 94: 'Dodge', 95: 'Dodge', 96: 'Dodge',
                      97: 'Douglas', 98: 'Douglas', 99: 'Douglas', 100: 'Duff Gordon', 101: 'Duff Gordon',
                      102: 'Dulles', 103: 'Earnshaw', 104: 'Endres', 105: 'Eustis', 106: 'Evans', 107: 'Farthing',
                      108: 'Flegenheim', 109: 'Fleming', 110: 'Flynn', 111: 'Foreman', 112: 'Fortune', 113: 'Fortune',
                      114: 'Fortune', 115: 'Fortune', 116: 'Fortune', 117: 'Fortune', 118: 'Francatelli',
                      119: 'Franklin', 120: 'Frauenthal', 121: 'Frauenthal', 122: 'Frauenthal', 123: 'Frölicher',
                      124: 'Frölicher-Stehli', 125: 'Frölicher-Stehli', 126: 'Fry', 127: 'Futrelle', 128: 'Futrelle',
                      129: 'Gee', 130: 'Gibson', 131: 'Gibson', 132: 'Gieger', 133: 'Giglio', 134: 'Goldenberg'}

        send_dictionary(self.conn, dictionary, "J")

        self.conn.send.assert_any_call(b'4688')  # Check if dict size is sent
        self.conn.send.assert_called_with(b'SEND_D|J')  # Check if header and data format are sent
        self.conn.sendall.assert_called()  # Check if serialized dictionary is sent

    def test_send_dictionary_xml(self):
        dictionary = {7: 'Andrews', 9: 'Appleton', 10: 'Artagaveytia', 11: 'Astor',
                      13: 'Aubart', 14: 'Barber', 15: 'Barkworth', 16: 'Bassani', 17: 'Baumann', 18: 'Baxter',
                      19: 'Baxter', 20: 'Beattie', 21: 'Beckwith', 22: 'Beckwith', 23: 'Behr', 24: 'Bessette',
                      25: 'Bidois', 26: 'Bird', 27: 'Birnbaum',  28: 'Bishop', 29: 'Bishop',
                      30: 'Björnström-Steffansson', 31: 'Blackwell', 32: 'Blank', 33: 'Bonnell', 34: 'Bonnell',
                      35: 'Borebank', 36: 'Bowen', 37: 'Bowerman', 38: 'Brady', 39: 'Brandeis', 40: 'Brereton',
                      41: 'Brewe', 42: 'Brown', 43: 'Brown', 44: 'Bucknell', 45: 'Burns', 46: 'Butt', 47: 'Cairns',
                      48: 'Calderhead', 49: 'Candee', 50: 'Cardeza', 51: 'Cardeza', 52: 'Carlsson',
                      53: 'Carraú-Esteves', 54: 'Carrau', 55: 'Carter', 56: 'Carter', 57: 'Carter', 58: 'Carter',
                      59: 'Case', 60: 'Cassebeer', 61: 'Cavendish', 62: 'Cavendish', 63: 'Chaffee', 64: 'Chaffee',
                      65: 'Chambers', 66: 'Chambers', 67: 'Chaudanson', 68: 'Cherry', 69: 'Chevré', 70: 'Chibnall',
                      71: 'Chisholm', 72: 'Clark', 73: 'Clark', 74: 'Cleaver', 75: 'Clifford', 76: 'Colley',
                      77: 'Compton', 78: 'Compton', 79: 'Compton', 80: 'Cornell', 81: 'Crafton', 82: 'Crosby',
                      83: 'Crosby', 84: 'Crosby', 85: 'Cumings', 86: 'Cumings', 87: 'Daly', 88: 'Daniel', 89: 'Daniels',
                      90: 'Davidson', 91: 'Davidson', 92: 'Dick', 93: 'Dick', 94: 'Dodge', 95: 'Dodge', 96: 'Dodge',
                      97: 'Douglas', 98: 'Douglas', 99: 'Douglas', 100: 'Duff Gordon', 101: 'Duff Gordon',
                      102: 'Dulles', 103: 'Earnshaw', 104: 'Endres', 105: 'Eustis', 106: 'Evans', 107: 'Farthing',
                      108: 'Flegenheim', 109: 'Fleming', 110: 'Flynn', 111: 'Foreman', 112: 'Fortune', 113: 'Fortune',
                      114: 'Fortune', 115: 'Fortune', 116: 'Fortune', 117: 'Fortune', 118: 'Francatelli',
                      119: 'Franklin', 120: 'Frauenthal', 121: 'Frauenthal', 122: 'Frauenthal', 123: 'Frölicher',
                      124: 'Frölicher-Stehli', 125: 'Frölicher-Stehli', 126: 'Fry', 127: 'Futrelle', 128: 'Futrelle',
                      129: 'Gee', 130: 'Gibson', 131: 'Gibson', 132: 'Gieger', 133: 'Giglio', 134: 'Goldenberg'}
        send_dictionary(self.conn, dictionary, "X")

        self.conn.send.assert_any_call(b'4688')  # Check if dict size is sent
        self.conn.send.assert_called_with(b'SEND_D|X')  # Check if header and data format are sent
        self.conn.sendall.assert_called()  # Check if serialized dictionary is sent


if __name__ == '__main__':
    unittest.main()
