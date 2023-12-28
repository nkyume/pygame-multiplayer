import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pg.image.load('../graphics/characters/catgirl.png')
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = pg.Vector2()
        self.obstacle_sprites = obstacle_sprites
        self.speed = 4

    def get_data(self):
        data = {
            'pos': self.rect.topleft,
        }
        return data

    def get_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            self.direction.y = -1
        elif keys[pg.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pg.K_LEFT]:
            self.direction.x = -1
        elif keys[pg.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def movement(self):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.y += self.direction.y * self.speed
        self.collision('vertical')
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.get_input()
        self.movement()

