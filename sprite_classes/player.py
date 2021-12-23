import pygame
from .bullet import Bullet

bullet = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health, self.cooldown = 3, 0
        self.armed = False
        player_walk_1 = pygame.image.load(
            'Graphics/Player/player_walk1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            'Graphics/Player/player_walk2.png').convert_alpha()
        player_unarmed_idle = pygame.image.load(
            'Graphics/Player/player_idle_unarmed.png').convert_alpha()
        player_unarmed_move = pygame.image.load(
            'Graphics/Player/player_move_unarmed.png').convert_alpha()
        self.player_armed = (player_walk_1, player_walk_2)
        self.player_unarmed = (player_unarmed_idle, player_unarmed_move)
        self.player_index = 0
        self.gravity = 0
        self.flipped = False
        self.image = self.player_unarmed[self.player_index]
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(midbottom=(150, 150))
        self.shoot_sound = pygame.mixer.Sound('Audio/laserRetro_001.ogg')
        self.shoot_sound.set_volume(0.1)
        self.damage_sound = pygame.mixer.Sound('Audio/Damage.wav')
        self.damage_sound.set_volume(0.5)
        self.lose_sound = pygame.mixer.Sound('Audio/Lose.wav')
        self.lose_sound.set_volume(0.5)
        self.jump_sound = pygame.mixer.Sound('Audio/Jump.wav')
        self.jump_sound.set_volume(0.1)

    def animation_state(self, idle=True):
        if not idle:
            self.player_index += 0.1
            if self.rect.bottom >= 300:
                if self.player_index >= len(self.player_unarmed):
                    self.player_index = 0
                if not self.armed:
                    self.image = self.player_unarmed[int(self.player_index)]
                else:
                    self.image = self.player_armed[int(self.player_index)]
            elif self.rect.bottom < 300:
                if not self.armed:
                    self.image = self.player_unarmed[1]
                else:
                    self.image = self.player_armed[1]
        else:
            self.image = self.player_unarmed[0] if not self.armed else self.player_armed[0]
        if self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.transform.flip(self.image, False, False)
        self.image = pygame.transform.scale(self.image, (64, 64))

    def shoot(self):
        if self.armed:
            self.shoot_sound.play()
            if self.flipped:
                bullet.add(Bullet(self.rect.right, self.rect.y, True))
            else:
                bullet.add(Bullet(self.rect.left, self.rect.y, False))

    def damaged(self):
        self.damage_sound.play()
        self.health -= 1

    def player_input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            if self.rect.bottom >= 300:
                self.jump_sound.play()
                self.gravity = -15
                self.rect.y += self.gravity
                self.animation_state(False)
        if key[pygame.K_d]:
            self.rect.x += 3
            self.animation_state(False)
            self.flipped = False
        elif key[pygame.K_a]:
            self.rect.x -= 3
            self.animation_state(False)
            self.flipped = True
        else:
            if self.rect.bottom >= 300:
                self.animation_state(True)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def check_visibility(self):
        if self.rect.x <= -50 or self.rect.x >= 850:
            self.lose_sound.play()
            self.kill()

    def update(self):
        if self.health <= 0:
            self.lose_sound.play()
            self.kill()
        self.check_visibility()
        self.player_input()
        self.apply_gravity()
