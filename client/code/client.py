import socket
import sys
import pickle
import time
import threading

import pygame as pg

class Client():
    def __init__(self):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._connected = False
        self._connecting = False

        self._ping = 0
        self.__time = time.time()
        self.__current_time = time.time()
        self.__timeout = 2
        self.__client.settimeout(2)
        self.__clock = pg.time.Clock()

        self.address = None
        self.player = {}
        self.characters = []
        self.projectiles = []
        
    def __connect(self):
        self._connecting = True
        for i in range(4):
            msg = {
            'signal': 'please_connect',
            'data': None
            }
            self.__send(msg)
            try:
                msg = self.__recive()
                data = msg['data']
                signal = msg['signal']
            except TimeoutError:
                print(f'cannot connect to {self.address} [{i+1}/{4}]')
            else:
                if not signal == 'connected':
                    continue
                if data:
                    self._connected = True
                    print(f'connected to {self.address}')
                    self._connecting = False
                    return True
                print(f'connection rejected')
        self._connecting = False
        
    # TODO: address validation

    def send_player_data(self, data):
        msg = {
            'signal': 'recive_player_data',
            'data': data
        }
        self.__send(msg)

    def get_player(self):
        msg = {
            'signal': 'create_player',
            'data': None
        }
        self.__send(msg)

    def disconnect(self):
        msg = {
            'signal': 'please_disconnect',
            'data': None
            }
        self.__send(msg)
        self._ping = 0
        self._connected = False

    def __send(self, data):
        data = pickle.dumps(data)
        self.__client.sendto(data, self.address)

    def __recive(self):
        data, address = self.__client.recvfrom(1024)
        if not data:
            raise TimeoutError
        data = pickle.loads(data)
        return data

    def __connection_checker(self):
        msg = {
            'signal': 'ping',
            'data': None
        }
        while self._connected:
            if self.__current_time - self.__time > self.__timeout:
                self.disconnect()
            self.__current_time = time.time()
            self._ping = self.__current_time - self.__time
            self.__send(msg)
            self.__clock.tick(60)
            
    def __signal_handler(self):
        while self._connected:
            try:
                msg = self.__recive()
            except TimeoutError:
                continue
            data = msg['data']
            signal = msg['signal']
            match signal:
                case 'ping':
                    self.__time = time.time()
                case 'disconnected':
                    self._connected = False
                case 'message':
                    pass
                case 'game_data':
                    self.characters = data
                case 'create_player':
                    self.player = data
        return

    def connect(self, address):
        self.__time = time.time()
        self.__current_time = time.time()
        self.address = address
        self.player = {}
        self.characters = {}

        try:
            if not self.__connect():
                raise FailedToConnect

            signals = threading.Thread(target=self.__signal_handler)
            signals.start()

            connection = threading.Thread(target=self.__connection_checker)
            connection.start()

        except FailedToConnect as e:
            print(e)

            
class FailedToConnect(Exception):
    "Failed to connect"