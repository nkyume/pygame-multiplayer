import socket
import threading
import sys
import time
import pickle

import pygame as pg

BUFFER = 1024


class NetworkServer:
    def __init__(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False

        self.__signals = {}
        self.connections = {}

        self.clock = pg.time.Clock()

    def __receive(self):
        data, address = self.__server.recvfrom(BUFFER)
        data = pickle.loads(data)
        return data, address

    @staticmethod
    def console_message(message: str, sender='[SERVER]'):
        local = time.localtime()
        print(f'{local.tm_hour}:{local.tm_min}:{local.tm_sec} {sender} {message}')

    def __connected(self, address):
        if address in self.connections:
            return True

    def __connection_checker(self):
        while self.running:
            try:
                for address, connection in self.connections.items():
                    if not connection.connected():
                        self.on_disconnection(address)

                self.clock.tick(60)
            except RuntimeError as e:
                pass

    def __signal_handler(self, signal, data, address):

        if not self.__connected(address):
            if signal == 'please_connect':
                self.on_connection(address)
                return
            else:
                self.console_message(f'{address} is not connected')
                return

        elif signal == 'please_disconnect':
            self.on_disconnection(address)
            return

        if signal not in self.__signals:
            return

        connection = self.connections[address]

        function = self.__signals[signal]
        function(address, data)

        connection.time = pg.time.get_ticks()

    def add_signal(self, signal, function):
        self.__signals[signal] = function

    def __send(self, message, address):
        message = pickle.dumps(message)
        self.__server.sendto(message, address)

    def send(self, address, signal, data=None):
        message = {
            'signal': signal,
            'data': data
        }
        self.__send(message, address)

    def send_for_all(self, signal, data):
        message = {'signal': signal,
                   'data': data}
        message = pickle.dumps(message)
        for address in self.connections.keys():
            self.__server.sendto(message, address)

    def start(self, address):
        self.__server.bind(address)
        self.running = True

        threading.Thread(target=self.__connection_checker, daemon=True).start()
        threading.Thread(target=self.__server_receive, daemon=True).start()

        self.console_message('running')

    def __server_receive(self):
        while self.running:
            message, address = self.__receive()
            if message:
                signal = message['signal']
                data = message['data']
                threading.Thread(target=self.__signal_handler, args=(signal, data, address), daemon=True).start()

    def on_connection(self, address):
        pass

    def on_disconnection(self, address):
        pass

    def run(self):
        pass


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


class Server(NetworkServer):
    def __init__(self):
        super().__init__()
        self.clock = pg.time.Clock()
        self.add_signal('player_data', self.get_player_data)
        self.add_signal('ping', self.ping)

    def on_connection(self, address):
        expected_id = 0
        ids = []
        for connection in self.connections.values():
            ids.append(connection.id)

        for id in sorted(ids):
            if id == expected_id:
                expected_id += 1
                continue
            break
        id = expected_id

        self.connections[address] = Connection(id)
        self.send(address, 'connected', {'connected': True, 'id': id})
        self.console_message(f'{address} connected')

    def on_disconnection(self, address):
        self.connections.pop(address)
        self.console_message(f'{address} disconnected')
        self.send(address, 'disconnected', {'reason': ''})

    def get_player_data(self, address, data):
        player = self.connections[address]
        player.set_data(data)

    def ping(self, address, data):
        self.send(address, 'ping', True)

    def send_game_data(self):
        data = {}
        for player in self.connections.values():
            data[player.id] = player.get_data()
        data['players'] = data
        self.send_for_all('game_data', data)

    def run(self):
        while self.running:
            self.send_game_data()
            self.clock.tick(60)


if __name__ == '__main__':
    server = Server()
    server.start(('192.168.0.104', 47353))
    try:
        server.run()
    except KeyboardInterrupt:
        print()
        server.console_message('shutting down')
        sys.exit()
