import pygame as pg

from code.game import Game
from code.gui import MainMenu


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((1280, 720))
        pg.scrap.init()
        pg.key.set_repeat(400, 50)
        self.clock = pg.time.Clock()
        self.running = True

        self.game = Game()
        self.state = 'menu'
        self.main_menu = MainMenu(self.game)

    def run(self):
        self.main_menu.main_menu()


if __name__ == '__main__':
    game = App()
    game.run()
