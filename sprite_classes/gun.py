import pygame


class Gun(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Graphics/Gun.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(midbottom=(400, 300))
        self.cog = None
        self.sound = pygame.mixer.Sound('Audio/clothBelt.ogg')
        self.sound.set_volume(1.5)

    def animate(self):
        if self.rect.y >= 236:
            self.cog = True
        elif self.rect.y <= 226:
            self.cog = False
        self.rect.y += -1 if self.cog else 1

    def picked_up(self):
        self.sound.play()
        self.kill()

    def update(self):
        self.animate()
