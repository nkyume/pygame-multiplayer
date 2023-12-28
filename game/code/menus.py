import sys

import pygame as pg

import ui
from client import Client
from settings import *


class MainMenu:
    def __init__(self, game):
        self.screen = pg.display.get_surface()
        self.clock = pg.time.Clock()

        self.client = Client()
        # self.settings = Settings()
        self.game = game

        # main screen
        self.title_text_surf = TEXT_FONT_BIG.render('Cool Catgirls RPG', False, 'white')
        self.title_text_rect = self.title_text_surf.get_rect(center=(400, 150))

        self.version_text_surf = TEXT_FONT_SMALL.render('pre pre alpha v0.3', False, 'white')
        self.version_text_rect = self.version_text_surf.get_rect(center=(400, 200))

        # loading screen
        self.loading_text_surf = TEXT_FONT_SMALL.render('connecting', False, 'white')
        self.loading_rect = self.loading_text_surf.get_rect(center=(400, 300))

    def connecting(self):
        active = True
        while active:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()

            self.screen.fill('black')
            self.screen.blit(self.loading_text_surf, self.loading_rect)
            if self.client.connected:
                self.game.create_player()
            if self.game.player:
                self.game.run()
            pg.display.flip()

        return

    # def settings(self):
    #     active = True
    #     while active:
    #         events = pg.event.get()
    #         for event in events:
    #             if event.type == pg.QUIT:
    #                 active = False
    #                 pg.quit()
    #                 sys.exit()
    #             if event.type == pg.K_ESCAPE:
    #                 active = False
    #
    #         self.screen.fill('black')
    #         self.settings.draw()
    #         pg.display.flip()
    #         self.clock.tick(FPS)

    def main_menu(self):
        connect_box = ui.InputBox(
            (400, 300),
            (100, 30),
            TEXT_FONT_SMALL,
            'lightskyblue3',
            'gray10',
            'gray',
            'white',
            max_len=21
        )

        running = True
        self.client.start()
        while running:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()

            self.screen.fill('black')

            self.screen.blit(self.title_text_surf, self.title_text_rect)
            self.screen.blit(self.version_text_surf, self.version_text_rect)
            address = connect_box.draw(self.screen, events)
            if address:
                ip, port = address.split(':')
                port = int(port)
                self.client.connect((ip, port))
                self.connecting()

            pg.display.flip()
            self.clock.tick(FPS)


class IngameMenu:
    def __init__(self):
        pass

    def draw(self):
        pass


class Settings:
    def __init__(self):
        pass

    def draw(self):
        pass





