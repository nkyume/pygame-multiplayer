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
        self.clock = pg.time.Clock()
        self.client = client.Client()
        self.running = True
        
        self.player = None
        self.character_surf = pg.Surface((10,10))
        self.character_surf.fill('blue')
        
        self.state = 'menu'
        self.main_menu = ui.MainMenu(self.client)

    def create_player(self):
        self.client.get_player()
        if self.client.player:
            pos = self.client.player['pos']
            self.player = Player(pos)
                
    def send_player(self):
        data = {
            'pos': self.player.rect.topleft
        }
        self.client.send_player_data()

    def draw_characrers(self):
        for id, character in self.client.characters.items():
            if id == self.client.player['id']:
                continue
            self.screen.blit(self.character_surf, character['pos'])

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
                    self.draw_characrers()
                    self.client.send_player_data({'pos': self.player.rect.topleft})
                    self.player.draw(self.screen)
                else:
                    self.create_player()
                if not self.client._connected:
                    self.player = None
                    self.state = 'menu'

            # debug
            debug(f'{"%.0f" % ((self.client._ping)*1000)}ms', 30)
            debug(int(self.clock.get_fps()))

            pg.display.flip()
            self.clock.tick(60)

class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        self.surf = pg.Surface((10,10))
        self.surf.fill('green')
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