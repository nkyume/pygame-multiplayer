import pygame as pg

from gui import InputBox
from settings import *

class ChatInput():
    def __init__(self) -> None:
        self.self.input_box = InputBox(
            (200,200),
            (200,30),
            self.font,
            'lightskyblue3',
            'gray10',
            'gray',
            'white',
            max_len=64
        )


class Chat():
    def __init__(self) -> None:
        self.display_surf = pg.display.get_surface()

        self.messages = []
        self.message_timeout = 600

    def recive_message(self, pos):
        message = Message()

    def send_message(self):
        pass

    def __message_timer(self):
        current_time = pg.time.get_ticks()
        messages_tmp = []
        for message in self.messages:
            if current_time - message.time <= self.message_timeout:
                messages_tmp.append(message)
        
        self.messages = messages_tmp

    def run(self):
        self.__message_timer()
        

class Message():
    def __init__(self):
        self.time = pg.time.get_ticks()
        self.text_surf = TEXT_FONT_SMALL

    def draw(self, pos):
        pass


            




            

