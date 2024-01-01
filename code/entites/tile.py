import pygame as pg


class Tile(pg.sprite.Sprite):
    def __init__(self, pos, groups) -> None:
        super().__init__(groups)
        self.image = pg.image.load('graphics/characters/box.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
