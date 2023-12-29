import threading
import sys
import pickle

import pygame as pg

from pygame_networking import Networking

BUFFER = 1024


class Server(Networking):
    def __init__(self):
        super().__init__()
        self.type = 'SERVER'
        self.__connections = {}

        self.add_signal('player_data', self.set_player_data)
        self.add_signal('ping', self.__ping)

    def __connected(self, address):
        if address in self.__connections:
            return True

    def __connection_checker(self):
        while self.running:
            try:
                for address, connection in self.__connections.items():
                    if not connection.connected():
                        self.__on_disconnection(address)

                self.clock.tick(60)
            except RuntimeError:
                pass

    def __signal_handler(self, signal, data, address):

        if not self.__connected(address):
            if signal == 'please_connect':
                self.__on_connection(address)
                return
            else:
                self.log(f'{address} is not connected')
                return
        elif signal == 'please_disconnect':
            self.__on_disconnection(address)

        elif signal == 'please_connect':
            self.log(f'{address} already connected')

        if signal not in self._signals:
            return

        connection = self.__connections[address]

        function = self._signals[signal]
        function(address, data)

        connection.time = pg.time.get_ticks()

    def send(self, address, signal, data):
        self._send(address, signal, data)

    def send_for_all(self, signal, data):
        message = {'signal': signal,
                   'data': data}
        message = pickle.dumps(message)
        for address in self.__connections.keys():
            self.socket.sendto(message, address)

    def __server_receive(self):
        while self.running:
            message, address = self.receive()
            if message:
                signal = message['signal']
                data = message['data']
                threading.Thread(target=self.__signal_handler, args=(signal, data, address), daemon=True).start()

    def __on_connection(self, address):
        expected_id = 0
        ids = []
        for connection in self.__connections.values():
            ids.append(connection.id)

        for id in sorted(ids):
            if id == expected_id:
                expected_id += 1
                continue
            break
        id = expected_id

        self.__connections[address] = Connection(id)
        data = {
            'connected': True,
            'id': id,
            'player_data': {
                'pos': (100, 100)
                }
            }
        self.__connections[address].set_data(data['player_data'])
        self.send(address, 'connected', data)
        self.log(f'{address} connected')

    def __on_disconnection(self, address):
        self.__connections.pop(address)
        self.log(f'{address} disconnected')
        self.send(address, 'disconnected', {'reason': ''})

    def set_player_data(self, address, data):
        player = self.__connections[address]
        player.set_data(data)

    def __ping(self, address, data):
        self.send(address, 'ping', True)

    def send_game_data(self):
        players = {}

        for player in self.__connections.values():
            player_data = player.get_data()
            if not player_data:
                continue
            players[player.id] = player.get_data()

        data = {
            'players': players
        }
        self.send_for_all('game_data', data)

    def run(self, address):
        self.socket.bind(address)
        self.running = True

        threading.Thread(target=self.__connection_checker, daemon=True).start()
        threading.Thread(target=self.__server_receive, daemon=True).start()

        self.log('running')
        while self.running:
            try:
                self.send_game_data()
            except RuntimeError:
                pass
            self.clock.tick(60)


class Connection:
    def __init__(self, id):
        self.id = id

        self.__timeout = 5000
        self.time = pg.time.get_ticks()

        self.__game_data = None

    def connected(self):
        current_time = pg.time.get_ticks()
        if current_time - self.time < self.__timeout:
            return True

    def set_data(self, data):
        if not self.__game_data == data:
            self.__game_data = data

    def get_data(self):
        return self.__game_data


if __name__ == '__main__':
    server = Server()
    try:
        server.run(('192.168.0.104', 47353))
    except KeyboardInterrupt:
        print()
        server.log('shutting down')
        sys.exit()
