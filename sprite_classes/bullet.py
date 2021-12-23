import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, flipped=None):
        super().__init__()
        self.image = pygame.image.load('Graphics/Misc/bullet.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.flipped = flipped
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
        subtractor = 50 if not self.flipped else -50
        self.rect = self.image.get_rect(
            center=(x_pos + subtractor, y_pos + 40))

    def delete(self):
        if self.rect.x >= 900 or self.rect.x <= -100:
            self.kill()

    def move(self):
        if not self.flipped:
            self.rect.x += 15
        else:
            self.rect.x -= 15

    def update(self):
        self.move()
        self.delete()
