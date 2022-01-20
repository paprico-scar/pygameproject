import pygame, sys
from settings import *
from subprocess import call


pygame.init()  # initiate pygame
pygame.display.set_caption(FIRST_WINDOW_TITLE)  # set the window name
clock = pygame.time.Clock()  # set up the clock
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)  # initiate screen
waiting = True
font = pygame.font.SysFont('arial', 40)

while waiting:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            waiting = False
            sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_h:
                pygame.quit()
                call(['python', 'game.py'])
                sys.exit()
            if event.key == pygame.K_j:
                pygame.quit()
                call(['python', 'main.py'])
                sys.exit()
    draw_text(f'Добро пожаловать в {FIRST_WINDOW_TITLE}', WHITE, WIDTH / 2, HEIGHT / 4, screen, font)
    draw_text('Чтобы играть в SPACE INVADERS нажмите "j"', WHITE, WIDTH / 2, HEIGHT / 3 + 40, screen, font)
    draw_text('Чтобы играть в RELAX нажмите "h"', WHITE, WIDTH / 2, HEIGHT / 3 + 120, screen, font)
    pygame.display.flip()



