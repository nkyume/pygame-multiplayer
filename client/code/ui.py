import threading

import pygame as pg


class MainMenu:
    def __init__(self, client):
        self.display_surface = pg.display.get_surface()
        self.client = client
        self.small_font = pg.font.Font('../font/8bitOperatorPlus8-Regular.ttf', 24)
        self.big_font = pg.font.Font('../font/8bitOperatorPlus8-Regular.ttf', 48)
        self.state = 'main'
        self.connect_box = InputBox(
            (400,300),
            (100,30),
            self.small_font,
            'lightskyblue3',
            'gray10',
            'gray',
            'white',
            max_len=21
            )
        
        # main screen
        self.title_text_surf = self.big_font.render('Cool Catgirls RPG', False, 'white')
        self.title_text_rect = self.title_text_surf.get_rect(center=(400,150))

        self.version_text_surf = self.small_font.render('pre pre alpha v0.3', False, 'white')
        self.version_text_rect = self.version_text_surf.get_rect(center=(400,200))

        # loading screen
        self.loading_text_surf = self.small_font.render('connecting', False, 'white')
        self.loading_rect = self.loading_text_surf.get_rect(center=(400,300))

    def draw(self, events):
        if self.state == 'main':
            self.display_surface.blit(self.title_text_surf, self.title_text_rect)
            self.display_surface.blit(self.version_text_surf, self.version_text_rect)
            address = self.connect_box.draw(self.display_surface, events)
            if address:
                ip, port = address.split(':')
                port = int(port)
                threading.Thread(target=self.client.connect, args=((ip, port),)).start()
                self.state = 'connecting'

        if self.state == 'connecting':
            self.display_surface.blit(self.loading_text_surf, self.loading_rect)
            if not self.client._connecting:
                self.state = 'main'
                    
class InputBox:
    def __init__(
            self,
            pos: tuple,
            size: tuple,
            font: pg.font.Font,
            active_color,
            passive_color,
            bg_color,
            font_color,
            max_len=0,
            placeholder: str = ''):
        
        self.active_color = active_color
        self.passive_color = passive_color
        self.bg_color = bg_color
        self.pos = pos
        self.box_rect = pg.Rect(pos, size)
        self.box_rect.center = (self.pos)
        self.width = self.box_rect.w
        
        self.font = font
        self.font_color = font_color
        self.text = ''
        self.max_len = max_len

        self.active = False

    def draw(self, display_surf, events) -> str:
        """returns string if enter pressed"""
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN:
                if self.box_rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
            if not self.active:
                continue

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_v and event.mod & pg.KMOD_CTRL:
                    self.text += pg.scrap.get("text/plain;charset=utf-8").decode()
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                if event.key == pg.K_RETURN:
                    text = self.text
                    self.text = ''
                    return text

            # restrict string lenght        
            if event.type == pg.TEXTINPUT:
                self.text += event.text
        if self.max_len:
                if len(self.text) >= self.max_len:
                    self.text = self.text[:self.max_len]

        if self.active:
            box_color = self.active_color
        else:
            box_color = self.passive_color

        self.box_rect.center = (self.pos)

        text_surface = self.font.render(self.text, False, 'white')
        self.box_rect.w = max(self.width, text_surface.get_width() + 10)

        pg.draw.rect(display_surf, self.passive_color, self.box_rect)
        pg.draw.rect(display_surf, box_color, self.box_rect, 2)
        display_surf.blit(text_surface, (self.box_rect.x + 5, self.box_rect.y + 7))

class Button:
    def __init__(
            self,
            pos: tuple,
            size: tuple,
            text: str,
            font: pg.font.Font,
            pressed_color,
            passive_color,
            bg_color,
            font_color, 
            ):
        
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

    def draw(self, display_surf, events, func, *args):
        """run function on click"""
        mouse_keys = pg.mouse.get_pressed()
        color = self.passive_color
        if self.button_rect.collidepoint(pg.mouse.get_pos()):
            color = self.pressed_color
            if mouse_keys[0]:
                func(args)
                   
        pg.draw.rect(display_surf, self.bg_color, self.button_rect)
        display_surf.blit(self.text_surf, self.text_rect)
        pg.draw.rect(display_surf, color, self.button_rect, 4)

