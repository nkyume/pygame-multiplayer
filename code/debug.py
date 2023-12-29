import pygame as pg
pg.init()
font = pg.font.Font(None, 30)

def debug(info,y=10,x=10):
    display_surf = pg.display.get_surface()
    debug_surf = font.render(str(info), True, 'White')
    debug_rect = debug_surf.get_rect(topleft = (x,y))
    pg.draw.rect(display_surf,'Black',debug_rect)
    display_surf.blit(debug_surf, debug_rect)

