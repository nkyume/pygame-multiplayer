import sys

from networking.client import Client
from tile import Tile
from player import Player
from debug import debug
from settings import *


class Game:
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.clock = pg.time.Clock()
        self.client = Client()

        self.camera = Camera()
        self.hitboxes = pg.sprite.Group()

        #self.menu = IngameMenu()
        self.state = 'game'

        self.characters = {}
        self.player = None

    def create_player(self):
        if 'player_data' not in self.client.game_data:
            return
        player_data = self.client.game_data['player_data']
        self.player = Player(player_data['pos'], (self.camera,), self.hitboxes)

    def send_player(self):
        self.client.send('player_data', self.player.get_data())

    def update_characters(self):
        if 'players' not in self.client.game_data.keys():
            return
        players = self.client.game_data['players']
        for id, player in players.items():
            if id in self.characters.keys():
                continue
            if id == self.client.id:
                continue
            else:
                # connect
                character = Player(player['pos'], (self.camera,), self.hitboxes)
                self.characters[id] = character

        for id in list(self.characters):
            # disconnect
            if id not in players.keys():
                self.characters.pop(id).kill()
                continue
            self.characters[id].rect.topleft = players[id]['pos']

    def create_level(self):
        for row_index, row in enumerate(test_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                if col == 'x':
                    Tile((x, y), (self.camera, self.hitboxes))

    def exit(self):
        self.client.disconnect()
        self.camera.empty()
        self.hitboxes.empty()
        self.player = None

    def run(self):
        self.create_level()
        running = True
        while running:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    print('exit')
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        print('esc')
                        self.exit()
                        return

            self.screen.fill('black')

            self.camera.draw(self.player)

            self.player.update()
            self.update_characters()
            self.send_player()
            self.client.send_ping()

            # if self.state == 'menu':
            #     self.menu.draw()
            debug(self.client.game_data)
            pg.display.flip()

            if not self.client.connected:
                return
            self.clock.tick(FPS)


class Camera(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pg.math.Vector2()

    def draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_position = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_position)
