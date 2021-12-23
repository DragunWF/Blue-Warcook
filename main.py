import pygame
from random import choice
from sprite_classes.player import Player, bullet
from sprite_classes.enemies import Enemies
from sprite_classes.gun import Gun
from sprite_classes.explode import Explode
from ui_elements import main_menu, score_ui
from sys import exit


def collision_check():
    global gun_picked_up, score_value, cooldown, gameover, miliseconds, cog
    if player.sprite:
        if player.sprite.health > 0:
            if pygame.sprite.spritecollide(player.sprite, gun, False):
                background_music()
                for item in gun:
                    item.picked_up()
                player.sprite.armed = True
                gun_picked_up = True
            if pygame.sprite.spritecollide(player.sprite, enemies, False):
                if cooldown == 0:
                    effect.add(
                        Explode(player.sprite.rect.x, player.sprite.rect.y))
                    player.sprite.damaged()
                    miliseconds = 250
                    pygame.time.set_timer(cooldown_timer, miliseconds)
                    cooldown += 1
    else:
        if cog:
            miliseconds_i = 3000
            pygame.time.set_timer(gameover_timer, miliseconds_i)
            pygame.time.set_timer(spawn_timer, 0)
            if gun_picked_up:
                background_music(True)
            cog = False
    collided = pygame.sprite.groupcollide(enemies, bullet, False, True)
    for enemy in collided:
        effect.add(Explode(enemy.rect.x, enemy.rect.y))
        enemy.kill()
        score_value += 5


def scale_difficulty():
    global scaling_level
    if scaling_level > 1:
        scaling_level -= 1
        pygame.time.set_timer(spawn_timer, 100 * scaling_level)


def background_music(quit=False):
    global music
    music.set_volume(song_volume)
    if not quit:
        music.play(loops=-1)
    else:
        music.fadeout(2)


pygame.init()
pygame.display.set_caption('Blue Warcook')
icon = pygame.image.load('Graphics/Player/player_walk1.png')
pygame.display.set_icon(icon)
ground = pygame.image.load('Graphics/Ground.png').convert()
background = pygame.image.load('Graphics/Sky.png').convert()
music = pygame.mixer.Sound('Audio/music.wav')
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
gameover = True
audio_paused, song_volume = False, 0.2

player = pygame.sprite.GroupSingle()

gun = pygame.sprite.GroupSingle()
# bullet = pygame.sprite.Group()

enemies = pygame.sprite.Group()
effect = pygame.sprite.Group()

spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_timer, 1000)

score_value = 0
score_timer = pygame.USEREVENT + 2
pygame.time.set_timer(score_timer, 1500)

scaling_timer = pygame.USEREVENT + 3
pygame.time.set_timer(scaling_timer, 25000)
scaling_level = 10

cooldown_timer, miliseconds, cooldown = pygame.USEREVENT + 4, 250, 0
gameover_timer, miliseconds_i, cog = pygame.USEREVENT + 5, 0, True
gun_cooldown, miliseconds_x, on_cd = pygame.USEREVENT + 6, 0, False

while True:  # Game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not gameover:
            if event.type == pygame.MOUSEBUTTONDOWN and player.sprite:
                if not on_cd:
                    player.sprite.shoot()
                    miliseconds_x = 100
                    pygame.time.set_timer(gun_cooldown, miliseconds_x)
                    on_cd = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    song_volume = 0 if song_volume > 0 else 0.2
                    music.set_volume(song_volume)
                if event.key == pygame.K_q:
                    audio_paused = True if not audio_paused else False
            if event.type == gun_cooldown:
                miliseconds_x = 0
                pygame.time.set_timer(gun_cooldown, miliseconds_x)
                on_cd = False
            if gun_picked_up:
                if event.type == spawn_timer:
                    enemies.add(
                        Enemies(choice(('Worm', 'Worm', 'Worm', 'Bee', 'BlueBee'))))
                if event.type == score_timer:
                    score_value += 1
                if event.type == scaling_timer:
                    scale_difficulty()
                if event.type == cooldown_timer:
                    cooldown += 1
                    if cooldown >= 4:
                        cooldown, miliseconds = 0, 0
                        pygame.time.set_timer(cooldown_timer, miliseconds)
            if event.type == gameover_timer:
                miliseconds_i = 0
                pygame.time.set_timer(gameover_timer, miliseconds_i)
                gameover = True
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                score_value = 0
                player.add(Player())
                player.sprite.health = 3
                gun.add(Gun())
                enemies.empty()
                scaling_level = 10
                pygame.time.set_timer(spawn_timer, 1000)
                gun_picked_up, gameover, cog = False, False, True

    if gameover:
        screen.fill((24, 123, 205))
        main_menu(score_value)
    else:
        if audio_paused:
            pygame.mixer.pause()
        else:
            pygame.mixer.unpause()

        screen.blit(background, (0, 0))
        screen.blit(ground, (0, 300))

        score_ui(score_value)

        bullet.draw(screen)
        bullet.update()

        gun.draw(screen)
        gun.update()

        player.draw(screen)
        player.update()

        enemies.draw(screen)
        enemies.update()

        effect.draw(screen)
        effect.update()

        collision_check()

    pygame.display.update()
    clock.tick(60)
