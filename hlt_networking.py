import socket
from hlt import translate_cardinal, GameMap


class HLT:
    def __init__(self, port):
        _connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _connection.connect(('localhost', port))
        print('Connected to intermediary on port #' + str(port))
        self._connection = _connection

    def get_string(self):
        newString = ""
        buffer = '\0'
        while True:
            buffer = self._connection.recv(1).decode('ascii')
            if buffer != '\n':
                newString += str(buffer)
            else:
                return newString

    def sendString(self, s):
        s += '\n'
        self._connection.sendall(bytes(s, 'ascii'))

    def get_init(self):
        myID = int(self.get_string())
        game_map = GameMap(self.get_string(), self.get_string(), self.get_string())
        return myID, game_map

    def send_init(self, name):
        self.sendString(name)

    def send_frame(self, moves):
        self.sendString(' '.join(
            str(move.square.x) + ' ' + str(move.square.y) + ' ' + str(translate_cardinal(move.direction)) for move in
            moves))
