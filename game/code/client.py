import time
import threading

import pygame as pg

from pygame_networking import Networking


ADDRESS = ('192.168.0.104', 47353)
BUFFER = 1024


class Client(Networking):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if Client.__instance is None:
            Client.__instance = super().__new__(cls)
        return Client.__instance

    def __init__(self):
        super().__init__()
        self.address = None

        self.type = 'CLIENT'
        self.id = None
        self.server_timeout = 5000
        self.running = False
        self.connecting = False
        self.connected = False

        self.time = pg.time.get_ticks()
        self.ping = 0

        self.add_signal('connected', self.__on_connection)
        self.add_signal('disconnected', self.__on_disconnection)
        self.add_signal('game_data', self.__update_game_data)
        self.add_signal('ping', self.__update_ping)

        self.game_data = {}

    def __signal_handler(self):
        while self.running:
            message, address = self.receive()
            signal = message['signal']
            data = message['data']
            function = self._signals[signal]
            function(data)

    def __on_connection(self, data):
        if data['connected']:
            self.log('connected')
            self.id = data['id']
            self.game_data['player_data'] = data['player_data']
            self.connecting = False
            self.connected = True

    def __on_disconnection(self, data):
        self.connected = False
        self.running = False

    def send(self, signal, data=None):
        self._send(self.address, signal, data)

    def connect(self, address):
        threading.Thread(target=self.__connect, args=(address,)).start()

    def __connect(self, address):
        self.address = address
        self.connecting = True
        for i in range(4):
            if self.connected:
                return
            self.send('please_connect')
            self.log(f'connecting [{i + 1}/4]')
            time.sleep(1)
        self.connecting = False

    def disconnect(self):
        self.send('please_disconnect')
        self.connected = False
        self.running = False

    def send_ping(self):
        self.send('ping', {})
        current_time = pg.time.get_ticks()
        self.ping = current_time - self.time
        if self.ping > self.server_timeout:
            self.__on_disconnection({'reason': 'timeout'})

    def __update_ping(self, data):
        self.time = pg.time.get_ticks()

    def __update_game_data(self, data):
        self.game_data = data

    def start(self):
        self.running = True
        threading.Thread(target=self.__signal_handler).start()


if __name__ == '__main__':
    client = Client()
    client.start()
    client.connect(('192.168.0.104', 47353))
