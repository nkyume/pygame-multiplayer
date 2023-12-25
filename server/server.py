import socket
import threading
import time
import pickle
import sys
import pygame as pg

from settings import *

class Server():
    def __init__(self):
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__server.bind(ADDR)
        self.__clock = pg.time.Clock()
        self.__players = {}

        self.__running = True
    
    def send(self, data, address):
        data = pickle.dumps(data)
        self.__server.sendto(data, address)

    def receive(self):
        data, address = self.__server.recvfrom(1024)
        data = pickle.loads(data)
        return(data, address)
    
    def send_for_all(self, data):
        data = pickle.dumps(data)
        for connection in self.__players.values():
            self.__server.sendto(data, connection._address)

    # TODO signal function
    # def function_name(signal, data):
        # msg = {
        # 'signal': signal,
        # 'data': data,
        # }

    def __console_message(self, message: str, sender='[SERVER]'):
        local = time.localtime()
        print(f'{local.tm_hour}:{local.tm_min}:{local.tm_min} {sender} {message}')

    def __find_connection(self, address):
        for connection in self.__players.values():
            if connection._address == address:
                return connection
    
    def __signal_handler(self, data, address):
        signal = data['signal']
        data = data['data']
        
        # check if connected
        connection = self.__find_connection(address)
        match signal:
            case 'please_connect':
                if connection:
                    self.__console_message(f'{address} already connected')
                    return
            case _:
                if not connection:
                    self.__console_message(f'{address} is not connected. Rejected.')
                    return
        
        match signal:
            case 'please_connect':
                self.__connect(address)
                self.__console_message(f'{address} connected')
                return
            case 'please_disconnect':
                self.__disconnect(connection)
                return
            case 'create_player':
                msg = {
                    'signal': 'create_player',
                    'data': {
                        'id': connection._id,
                        'pos': (200,200),
                    }
                }
                connection._char_class = data
                connection.player = True
                self.send(msg, address)
            case 'recive_player_data':
                connection._pos = data['pos']
            case 'ping':
                msg = {
                    'signal': 'ping',
                    'data': None
                }
                self.send(msg, address)
            case 'chat_message':
                self.__console_message(f'{data}', sender={address})

        connection._time = time.time()

    def __update_game_data(self):
        while self.__running:
            try:
                data = {}
                if not self.__players:
                    self.__clock.tick(60)
                    continue
                for id, player in self.__players.items():
                    if not player.player:
                        continue
                    data[id] = player.get_data()

                msg = {
                    'signal': 'game_data',
                    'data': data
                }

                self.send_for_all(msg)
                self.__clock.tick(60)
            except RuntimeError as e:
                print(e)
                
    def __connect(self, address):
        # unique id system 
        expected_id = 0
        for id in self.__players.keys():
            if id == expected_id:
                expected_id += 1
                continue
            break
        id = expected_id

        connection = _Player(address, id)
        self.__players[id] = connection
        msg = {
            'signal': 'connected',
            'data': True
            }
        self.send(msg, address)
        
    def __disconnect(self, connection):
        self.__console_message(f'{connection._address} disconnected')
        self.__players.pop(connection._id)

    def __connection_checker(self):
        while self.__running:
            try:   
                for connection in self.__players.values():
                    if not connection.is_connected():
                        self.__disconnect(connection)
                self.__clock.tick(1)
            except RuntimeError as e: 
                print(e)

    def run(self):
        self.__console_message('running')
        threading.Thread(target=self.__update_game_data).start()
        threading.Thread(target=self.__connection_checker).start()
        try:
            while self.__running:
                data, address = self.receive()
                if data:
                    threading.Thread(target=self.__signal_handler, args=(data, address)).start()
        except KeyboardInterrupt:
            self.__running = False
            self.__console_message(f'shutting down...')
            sys.exit()
        
class _Player():
    def __init__(self, address, id):
        # connection data
        self._id = id
        self._address = address
        self._time = time.time()
        self._ping = 0
        self.__timeout = 10

        # game data
        self.player = False
        self._pos = (200, 200)
        self._char_class = None
        self._state = 'idle'

    def is_connected(self):
        current_time = time.time()
        self._ping = current_time - self._time
        if self._ping < self.__timeout:
            return True
    
    def get_data(self):
        # TODO: create function that returns dict with all necessary player data
        data = {
            'pos': self._pos,
            'char_class': self._char_class
            }
        return data


if __name__ == '__main__':
    server = Server()
    server.run()