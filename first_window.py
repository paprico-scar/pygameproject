import pygame
from settings import *
from subprocess import call


pygame.init()  # initiate pygame
pygame.display.set_caption('Choose the game')  # set the window name
clock = pygame.time.Clock()  # set up the clock
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)  # initiate screen
waiting = True
font = pygame.font.SysFont('arial', 40)

while waiting:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_h:
                waiting = False
                call(['python', 'game.py'])
            if event.key == pygame.K_j:
                waiting = False
                call(['python', 'test.py'])
    draw_text('Welcome to RELAX', WHITE, WIDTH / 2, HEIGHT / 4, screen, font)
    draw_text('To play in first game press "j"', WHITE, WIDTH / 2, HEIGHT / 3 + 40, screen, font)
    draw_text('To play in second game press "h"', WHITE, WIDTH / 2, HEIGHT / 3 + 120, screen, font)
    pygame.display.flip()
