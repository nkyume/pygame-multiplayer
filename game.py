import sys
import time
import pygame as pg

import client
from debug import debug

ADDR = ('31.200.237.17', 47353)

class Game():
    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((800, 600))
        self.clock = pg.time.Clock()
        self.client = client.Client()

        self.character_surf = pg.Surface((10,10))
        self.character_surf.fill('blue')
        
    def create_player(self):
        self.client.create_player()
        time.sleep(0.1)
        self.player = Player(self.client.player['pos'], self.client.player['id'])

    def send_player(self):
        data = {
            'pos': self.player.rect.topleft
        }
        self.client.send_player_data()

    # TODO: async player creation

    def draw_characrers(self):
        for character in self.client.characters:
            if character['id'] == self.player.id:
                continue
            self.display.blit(self.character_surf, character['pos'])

    def run(self):
        if not self.client.connect(ADDR):
            pg.quit()
            sys.exit()
        self.create_player()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.client.disconnect()
                    pg.quit()
                    sys.exit()

            self.display.fill('black')
            self.draw_characrers()
            self.client.send_player_data({'pos': self.player.rect.topleft})
            self.player.draw(self.display)

            # debug
            debug(int(self.clock.get_fps()))
            debug(f'{"%.0f" % ((self.client._ping)*1000)}ms', 30)
            pg.display.flip()
            
            self.clock.tick(60)

class Player(pg.sprite.Sprite):
    def __init__(self, pos, id):
        self.id = id
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
            
    def draw(self, display_surf):
        self.move()
        display_surf.blit(self.surf, self.rect)

class Character(Player):
    def draw(self, display_surf):
        display_surf.blit(self.surf, self.rect)

game = Game()
game.run()