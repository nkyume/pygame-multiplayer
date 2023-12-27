import pickle
import socket
import time

import pygame as pg

BUFFER = 1024


class Networking:
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.running = False
        self.__signals = {}

        self.clock = pg.time.Clock()

        self.type: str = 'None'

    def __receive(self):
        data, address = self.__socket.recvfrom(BUFFER)
        data = pickle.loads(data)
        return data, address

    def __send(self, address, signal, data=None):
        message = {
            'signal': signal,
            'data': data
        }
        message = pickle.dumps(message)
        self.__socket.sendto(message, address)

    def add_signal(self, signal, function):
        self.__signals[signal] = function

    def log(self, message: str):
        local = time.localtime()
        print(f'{local.tm_hour}:{local.tm_min}:{local.tm_sec} [{self.type}] {message}')
