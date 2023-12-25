import pickle
import socket
import sys
import time
import threading

import pygame as pg


ADDRESS = ('192.168.0.104', 47353)
BUFFER = 1024


class NetworkClient:
    def __init__(self):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = None
        # self.__client.settimeout(2)

        self.id = None
        self.server_timeout = 5000
        self.running = False
        self.connecting = False
        self.connected = False

        self.__signals = {
            'connected': self.on_connection,
            'disconnected': self.on_disconnection
        }

    def __receive(self):
        data, address = self.__client.recvfrom(BUFFER)
        if not data:
            raise TimeoutError
        data = pickle.loads(data)
        return data

    def __send(self, message):
        message = pickle.dumps(message)
        self.__client.sendto(message, self.address)

    def send(self, signal, data=None):
        message = {
            'signal': signal,
            'data': data
        }
        self.__send(message)

    def __signal_handler(self):
        while self.running:
            message = self.__receive()
            signal, data = message['signal'], message['data']
            function = self.__signals[signal]
            function(data)

    def add_signal(self, signal, function):
        self.__signals[signal] = function

    def on_connection(self, data):
        pass

    def on_disconnection(self, data):
        pass

    def start(self):
        self.running = True
        signals = threading.Thread(target=self.__signal_handler)
        signals.daemon = True
        signals.start()


class Client(NetworkClient):
    def __init__(self):
        super().__init__()
        self.clock = pg.time.Clock()

        self.game_data = {}

        # signals
        self.add_signal('game_data', self.set_game_data)
        self.add_signal('ping', self.set_ping)

        self.time = pg.time.get_ticks()
        self.ping = 0

    def connect(self, address):
        self.address = address
        self.connecting = True
        for i in range(4):
            if self.connected:
                break
            self.send('please_connect')
            print(f'connecting [{i+1}/4]')
            time.sleep(1)

    def on_connection(self, data):
        if data['connected']:
            print('connected')
            self.id = data['id']
            self.connecting = False
            self.connected = True

    def on_disconnection(self, data):
        print(data['reason'])
        self.connected = False
        self.running = False

    def set_ping(self, data):
        self.time = pg.time.get_ticks()

    def check_ping(self):
        self.send('ping', {})
        current_time = pg.time.get_ticks()
        self.ping = current_time - self.time
        if self.ping > self.server_timeout:
            self.on_disconnection({'reason': 'timeout'})

    def set_game_data(self, data):
        self.game_data = data

    def disconnect(self):
        self.send('please_disconnect')
        self.connected = False
        self.running = False

    def run(self):
        self.start()
        self.connect(('192.168.0.104', 47353))
        while self.running:
            if self.connected:
                data = {
                    'pos': (20, 424),
                    'direction': (1, 0),
                    'is_alive': True,
                    'attacking': False
                }

                self.send('player_data', data)
                self.check_ping()
                # print(self.ping)
                self.clock.tick(60)


if __name__ == '__main__':
    client = Client()
    try:
        client.run()
    except KeyboardInterrupt:
        sys.exit()


