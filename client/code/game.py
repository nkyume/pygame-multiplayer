import sys
import time
import threading

import pygame as pg

import client
import ui
from debug import debug

class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        pg.scrap.init()
        pg.key.set_repeat(400,50)

        self.clock = pg.time.Clock()
        self.client = client.Client()
        self.running = True
        
        self.player = None
        self.characters = {}
        # self.character_surf = pg.Surface((10,10))
        # self.character_surf.fill('blue')
        
        self.font = pg.font.Font('../font/8bitOperatorPlus8-Regular.ttf', 48)
        self.state = 'menu'
        self.main_menu = ui.MainMenu(self.client)
        
        self.catgirl_button = ui.Button(
                        (300, 200),
                        (100, 100),
                        'Catgirl',
                        self.font,
                        'grey',
                        'azure4',
                        'grey10',
                        'white'
                    )
        self.girl_button = ui.Button(
                        (300, 400),
                        (100, 100),
                        'Girl',
                        self.font,
                        'grey',
                        'azure4',
                        'grey10',
                        'white'
                    )

    def create_player(self, char_class):
        char_class, *_ = char_class
        self.client.get_player(char_class)
        self.player = Player((200, 200), char_class)
            
    def send_player(self):
        data = {
            'pos': self.player.rect.topleft
        }
        self.client.send_player_data()

    def update_characters(self):
        for id, character in self.client.characters.items():
            if id == self.client.player['id']:
                pass
            elif id in self.characters.keys():
                self.characters[id].rect.topleft = character['pos']
            else:
                # player connected
                self.characters[id] = Character(character['pos'], character['char_class'])
            
        # player disconnected
        try:
            for id, character in self.characters.items():
                character.draw(self.screen)
                if id == self.client.player['id']:
                    continue
                if not id in self.client.characters.keys():
                    character.destroy()
                    self.characters.pop(id)
        except RuntimeError:
            pass
                
    def run(self):
        while True:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                    if self.client._connected:
                        self.client.disconnect()
                    pg.quit()
                    sys.exit()

            self.screen.fill('black')
            if self.state == 'menu':
                self.main_menu.draw(events)
                if self.client._connected:
                    print('connected')
                    self.state = 'game'

            if self.state == 'game':
                if self.player:
                    self.update_characters()
                    self.client.send_player_data({'pos': self.player.rect.topleft})
                    self.player.draw(self.screen)
                else:
                    self.catgirl_button.draw(self.screen, events, self.create_player, 'catgirl')
                    self.girl_button.draw(self.screen, events, self.create_player, 'girl')

                if not self.client._connected:
                    self.player = None
                    self.state = 'menu'

            # debug
            debug(f'{"%.0f" % ((self.client._ping)*1000)}ms', 30)
            debug(int(self.clock.get_fps()))

            pg.display.flip()
            self.clock.tick(60)

class Player(pg.sprite.Sprite):
    def __init__(self, pos, char_class):
        super().__init__()
        self.char_class = char_class
        self.surf = pg.image.load(f'../graphics/characters/{self.char_class}.png').convert_alpha()
        self.rect = self.surf.get_rect(topleft=pos)
        
    def move(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.rect.y -= 3
        elif keys[pg.K_DOWN]:
            self.rect.y += 3
        if keys[pg.K_LEFT]:
            self.rect.x -= 3
        elif keys[pg.K_RIGHT]:
            self.rect.x += 3

    def destroy(self):
        self.kill()

    def draw(self, display_surf):
        self.move()
        display_surf.blit(self.surf, self.rect)


class Character(Player):
    def draw(self, display_surf):
        display_surf.blit(self.surf, self.rect)

game = Game()
game.run()