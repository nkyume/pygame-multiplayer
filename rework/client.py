import sys
import time
import threading

import pygame as pg

from pygame_networking import Networking


ADDRESS = ('192.168.0.104', 47353)
BUFFER = 1024


class Client(Networking):
    instance = None

    def __new__(cls, *args, **kwargs):
        if Client.instance is None:
            Client.instance = super().__new__(cls)
        return Client.instance

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
        self.add_signal('game_data', self.__update_game_data)
        self.add_signal('ping', self.__update_ping)

        self.game_data = {}

    def __signal_handler(self):
        while self.running:
            message = self.__receive()
            signal, data = message['signal'], message['data']
            function = self.__signals[signal]
            function(data)

    def __on_connection(self, data):
        if data['connected']:
            self.log('connected')
            self.id = data['id']
            self.connecting = False
            self.connected = True

    def __on_disconnection(self, data):
        print(data['reason'])
        self.connected = False
        self.running = False

    def send(self, signal, data=None):
        self.__send(self.address, signal, data)

    def connect(self, address):
        self.address = address
        self.connecting = True
        for i in range(4):
            if self.connected:
                break
            self.send('please_connect')
            self.log(f'connecting [{i + 1}/4]')
            time.sleep(1)

    def disconnect(self):
        self.send('please_disconnect')
        self.connected = False
        self.running = False

    def __send_ping(self):
        self.send('ping', {})
        current_time = pg.time.get_ticks()
        self.ping = current_time - self.time
        if self.ping > self.server_timeout:
            self.__on_disconnection({'reason': 'timeout'})

    def __update_ping(self, data):
        self.time = pg.time.get_ticks()

    def __update_game_data(self, data):
        self.game_data = data

    def run(self):
        self.running = True
        threading.Thread(target=self.__signal_handler, daemon=True).start()
        while self.running:
            if self.connected:
                self.__send_ping()
                # print(self.ping)
                self.clock.tick(60)


if __name__ == '__main__':
    client = Client()
    client.run()
    client.connect(('192.168.0.104', 47353))



