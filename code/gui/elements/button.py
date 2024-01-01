import pygame as pg

class Button:
    def __init__(
            self,
            pos: tuple,
            size: tuple,
            text: str,
            func,
            font: pg.font.Font,
            pressed_color,
            passive_color,
            bg_color,
            font_color,
            *args,
            ):

        self.func = func
        if args:
            self.args = args
        else:
            self.args = None

        self.pressed_color = pressed_color
        self.passive_color = passive_color
        self.bg_color = bg_color
        self.button_rect = pg.Rect(pos, size)
        self.button_rect.center = pos

        self.font = font
        self.font_color = font_color

        self.text_surf = self.font.render(text, False, font_color)
        self.text_rect = self.text_surf.get_rect(center=pos)
        self.button_rect.width = self.text_rect.width

    def draw(self, display_surf, events):
        """run function on click"""
        mouse_keys = pg.mouse.get_pressed()
        color = self.passive_color
        if self.button_rect.collidepoint(pg.mouse.get_pos()):
            color = self.pressed_color
            if mouse_keys[0]:
                if self.args:
                    self.func(self.args)
                else:
                    self.func()

        pg.draw.rect(display_surf, self.bg_color, self.button_rect)
        display_surf.blit(self.text_surf, self.text_rect)
        pg.draw.rect(display_surf, color, self.button_rect, 4)
