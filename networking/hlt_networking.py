"""The HLT class to handle the connection"""
import socket

from public.hlt import GameMap, translate_cardinal


class HLT:
    """The HLT class to handle the connection"""

    def __init__(self, port):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect(('localhost', port))
        print('Connected to intermediary on port #' + str(port))
        self.connection = connection

    def get_string(self):
        new_string = ""
        buffer = '\0'
        while True:
            buffer = self.connection.recv(1).decode('ascii')
            if buffer != '\n':
                new_string += str(buffer)
            else:
                return new_string

    def send_string(self, s):
        s += '\n'
        self.connection.sendall(bytes(s, 'ascii'))

    def get_init(self):
        my_id = int(self.get_string())
        game_map = GameMap(self.get_string(), self.get_string(), self.get_string())
        return my_id, game_map

    def send_init(self, name):
        self.send_string(name)

    def send_frame(self, moves):
        self.send_string(' '.join(
            str(move.square.x) + ' ' + str(move.square.y) + ' ' + str(translate_cardinal(move.direction)) for move in
            moves))

    def send_frame_custom(self, moves):
        self.send_string(' '.join(
            str(x) + ' ' + str(y) + ' ' + str(translate_cardinal(direction)) for (x, y), direction in moves))
