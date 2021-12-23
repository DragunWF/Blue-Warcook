import pygame

pygame.init()

screen = pygame.display.set_mode((800, 400))

font = pygame.font.Font('Font/Pixeltype.ttf', 50)
title = font.render('Blue Warcook', False, (29, 28, 26))
title_rect = title.get_rect(center=(400, 35))
instructions = font.render('Press Enter to play!', False, (29, 28, 26))
instructions_rect = instructions.get_rect(center=(400, 365))
warcook = pygame.image.load('Graphics/Player/player_walk1.png').convert_alpha()
warcook = pygame.transform.scale(warcook, (258, 258))
warcook_rect = warcook.get_rect(center=(400, 200))


def main_menu(score_value):
    score = font.render(f'Score: {score_value}', False, (29, 28, 26))
    score_rect = score.get_rect(center=(400, 75))
    screen.blit(score, score_rect)
    screen.blit(title, title_rect)
    screen.blit(instructions, instructions_rect)
    screen.blit(warcook, warcook_rect)


def score_ui(score_value):
    score = font.render(f'Score: {score_value}', False, (29, 28, 26))
    score_rect = score.get_rect(center=(400, 35))
    screen.blit(score, score_rect)
