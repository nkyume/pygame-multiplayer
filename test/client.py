import socket
import sys
import pickle
import time
import threading

class Client():
    def __init__(self):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__connected = False
        self._ping = 0
        self.__time = time.time()
        self.__current_time = time.time()
        self.__timeout = 10
        self.__client.settimeout(2)
        self.address = None
        self.player = None
        self.characters = []

    def __connect(self):
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
                    self.__connected = True
                    print(f'connected to {self.address}')
                    return True
                print(f'connection rejected')
    
    def send_player_data(self, data):
        msg = {
            'signal': 'recive_player_data',
            'data': data
        }
        self.__send(msg)

    def create_player(self):
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
        self.__connected = False

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
        while self.__connected:
            if self._ping > self.__timeout:
                self.__connected = False
            self.__current_time = time.time()
            self._ping = self.__current_time - self.__time
            self.__send(msg)
            time.sleep(1)
          
    def __signal_handler(self):
        while self.__connected:
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
                    self.__connected = False
                case 'message':
                    pass
                case 'game_data':
                    self.characters = data
                case 'create_player':
                    self.player = data
        return

    def connect(self, address):
        self.address = address
        try:
            if not self.__connect():
                raise FailedToConnect

            signals = threading.Thread(target=self.__signal_handler)
            signals.start()

            connection = threading.Thread(target=self.__connection_checker)
            connection.start()
            return True
        except FailedToConnect as e:
            print(e)
            return False
            

class FailedToConnect(Exception):
    "Failed to connect"