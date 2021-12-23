import pygame


class Explode(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        frame1 = pygame.image.load(
            'Graphics/Misc/Explode1.png').convert_alpha()
        frame2 = pygame.image.load(
            'Graphics/Misc/Explode2.png').convert_alpha()
        frame3 = pygame.image.load(
            'Graphics/Misc/Explode3.png').convert_alpha()
        self.frames = [frame3, frame2, frame1]
        self.index = 0
        self.image = self.frames[self.index]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=(x_pos + 10, y_pos + 30))

    def animate(self):
        try:
            self.index += 0.1
            self.image = self.frames[int(self.index)]
            self.image = pygame.transform.scale(self.image, (64, 64))
        except IndexError:
            self.kill()

    def update(self):
        self.animate()
        