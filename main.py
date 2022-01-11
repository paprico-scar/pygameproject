import pygame
import events
import pygame.font
from gun import Gun
from wall import Wall
from pygame.sprite import Group
from score import Score

pygame.init()
size = WIDTH, HEIGHT = 1300, 750
screen = pygame.display.set_mode(size)
pygame.display.set_caption('SPACE INVADERS')
pygame.display.set_icon(pygame.image.load('images/icon.png'))


def main():
    gun = Gun(screen)
    sc = Score(screen)
    w1 = Wall(screen, 100, 500)
    w2 = Wall(screen, 418, 500)
    w3 = Wall(screen, 736, 500)
    w4 = Wall(screen, 1056, 500)
    bullets = Group()
    enemies = Group()
    ufo = Group()
    events.crete_army(screen, enemies, ufo)

    while True:
        events.events(screen, gun, bullets)
        gun.update_gun()
        ufo.update()
        events.update_screen(screen, gun, enemies, ufo, bullets, w1, w2, w3, w4, sc)
        events.update_bullets(enemies, ufo, bullets, w1, w2, w3, w4, screen, sc)
        events.update_enemies(enemies)


def start_screen():
    intro_text = ["            SPACE INVADERS", "",
                  "                   Controls:",
                  "right and left arrow to move",
                  "          up arrow to shoot", "",
                  "        Press a key to play!"]
    screen.fill((0, 0, 0))
    font = pygame.font.Font('font_kurasov/space_invaders.ttf', 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 400
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


start_screen()
main()
