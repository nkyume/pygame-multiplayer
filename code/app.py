import pygame as pg

from game import Game
import menus


class App:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        pg.scrap.init()
        pg.key.set_repeat(400, 50)
        self.clock = pg.time.Clock()
        self.running = True

        self.game = Game()
        self.state = 'menu'
        self.main_menu = menus.MainMenu(self.game)

    def run(self):
        self.main_menu.main_menu()


if __name__ == '__main__':
    game = App()
    game.run()
