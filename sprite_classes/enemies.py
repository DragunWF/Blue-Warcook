import pygame
from random import choice


class Enemies(pygame.sprite.Sprite):
    def __init__(self, type='Worm'):
        super().__init__()
        if type == 'Worm':
            worm1 = pygame.image.load(
                'Graphics/Worm/worm1.png').convert_alpha()
            worm2 = pygame.image.load(
                'Graphics/Worm/worm2.png').convert_alpha()
            self.frames = (worm1, worm2)
            y_pos = 300
        if type == 'Bee':
            bee1 = pygame.image.load('Graphics/Bee/bee1.png').convert_alpha()
            bee2 = pygame.image.load('Graphics/Bee/bee2.png').convert_alpha()
            self.frames = (bee1, bee2)
            y_pos = 230
        if type == 'BlueBee':
            bluebee1 = pygame.image.load(
                'Graphics/BlueBee/BlueBee1.png').convert_alpha()
            bluebee2 = pygame.image.load(
                'Graphics/BlueBee/BlueBee2.png').convert_alpha()
            self.frames = (bluebee1, bluebee2)
            y_pos = 210
        self.index = 0
        self.image = self.frames[self.index]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(midbottom=(choice((-100, 900)), y_pos))
        if self.rect.x >= 850:
            self.direction = 'right'
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.direction = 'left'

    def move(self):
        if self.direction == 'left':
            self.rect.x += 5
        else:
            self.rect.x -= 5

    def animation_state(self):
        self.index += 0.1
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]
        self.image = pygame.transform.scale(self.image, (64, 64))
        if self.direction == 'right':
            self.image = pygame.transform.flip(self.image, True, False)

    def destroy(self):
        if self.rect.x <= -150 or self.rect.x >= 950:
            self.kill()

    def update(self):
        self.move()
        self.animation_state()
        self.destroy()
