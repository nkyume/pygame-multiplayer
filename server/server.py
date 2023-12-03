import socket
import threading
import time
import pickle
import sys
import pygame as pg

from settings import *

class Server():
    def __init__(self):
        print('[SERVER] initializing...')
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__server.bind(ADDR)
        self.__clock = pg.time.Clock()
        self.__players = []

        self.__running = True
    
    def send(self, data, address):
        data = pickle.dumps(data)
        self.__server.sendto(data, address)

    def recive(self):
        data, address = self.__server.recvfrom(1024)
        data = pickle.loads(data)
        return(data, address)
    
    def send_for_all(self, data):
        data = pickle.dumps(data)
        for connection in self.__players:
            self.__server.sendto(data, connection._address)

    # TODO signal function
    # def function_name(signal, data):
        # msg = {
        # 'signal': signal,
        # 'data': data,
        # }

    def __find_connection(self, address):
        for connection in self.__players:
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
                    print(f'{address} already connected')
                    return
            case _:
                if not connection:
                    print(f'{address} is not connected. Rejected.')
                    return
        
        match signal:
            case 'please_connect':
                self.__connect(address)
                return
            case 'please_disconnect':
                self.__disconnect(connection)
                return
            case 'message':
                print(data['data'])
            case 'create_player':
                msg = {
                    'signal': 'create_player',
                    'data': {
                        'id': connection._id,
                        'pos': (200,200)
                    }
                }
                self.send(msg, address)
            case 'recive_player_data':
                connection._pos = data['pos']
            case 'ping':
                msg = {
                    'signal': 'ping',
                    'data': None
                }
                self.send(msg, address)
        
        connection._time = time.time()

    def __update_game_data(self):
        while self.__running:
            data = []
            if not self.__players:
                self.__clock.tick(60)
                continue
            for player in self.__players:
                player_data = {
                    'id': player._id,
                    'pos': player._pos
                }
                data.append(player_data)

            msg = {
                'signal': 'game_data',
                'data': data
            }

            self.send_for_all(msg)
            self.__clock.tick(60)
            
    def __connect(self, address):
        
        # unique id system 
        self.__players.sort(key=lambda x: x._id)
        expected_id = 0
        for player in self.__players:
            id = player._id
            if id == expected_id:
                expected_id += 1
                continue
            break
        id = expected_id

        connection = _Player(address, id)
        self.__players.append(connection)
        msg = {
            'signal': 'connected',
            'data': True
            }
        self.send(msg, address)
        
    def __disconnect(self, connection):
        print(f'[SERVER] {connection._address} disconnected')
        self.__players.remove(connection)

    def __connection_checker(self):
        while self.__running:   
            for connection in self.__players:
                if not connection.is_connected():
                    self.__disconnect(connection)
            self.__clock.tick(1)

    def run(self):
        print('[SERVER] running')
        threading.Thread(target=self.__update_game_data).start()
        threading.Thread(target=self.__connection_checker).start()
        try:
            while self.__running:
                data, address = self.recive()
                if data:
                    threading.Thread(target=self.__signal_handler, args=(data, address)).start()
        except KeyboardInterrupt:
            self.__running = False
            sys.exit('\n[SERVER] shuting down...')
        
class _Player():
    def __init__(self, address, id):
        print(f'[SERVER] {address} connected')
        self._id = id
        self._address = address
        self._time = time.time()
        self._ping = 0
        self.__timeout = 10
        self._pos = (200, 200)

    def is_connected(self):
        current_time = time.time()
        self._ping = current_time - self._time
        if self._ping < self.__timeout:
            return True


if __name__ == '__main__':
    server = Server()
    server.run()