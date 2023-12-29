import pygame as pg

TILESIZE = 64
FPS = 60

# colors
pg.font.init()
TEXT_FONT_SMALL = pg.font.Font('../font/8bitOperatorPlus8-Regular.ttf', 24)
TEXT_FONT_BIG = pg.font.Font('../font/8bitOperatorPlus8-Regular.ttf', 48)
TEXT_COLOR = 'white'

address = '192.168.0.104:47353'

test_map = [
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ','x',' ',' ',' ','p',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ','x','x',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ','x','x',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ','x','x',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ','x','x',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ','x',' ',' ',],
    [' ',' ',' ',' ',' ','x','x',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ','x',' ',' ',],
    [' ',' ',' ',' ',' ','x','x',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ','x',' ',' ',],
    [' ',' ',' ',' ',' ','x','x',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ','x',' ',' ',],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x',' ',' ',' ',' ','x',' ',' ',],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','x','x','x','x','x','x',' ',' ',],
    [' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ','x','x','x',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',],
    [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',]
]