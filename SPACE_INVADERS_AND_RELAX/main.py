import pygame
import events
import pygame.font
from gun import Gun
from wall import Wall
from pygame.sprite import Group
from score import Score
from subprocess import call
import sys

pygame.init()
pygame.mixer.music.load('data/music_and_sounds/space_invaders_theme.mp3')
pygame.mixer.music.play(-1)
size = WIDTH, HEIGHT = 1300, 750
screen = pygame.display.set_mode(size)
pygame.display.set_caption('SPACE INVADERS')
pygame.display.set_icon(pygame.image.load('data/images/icon.png'))


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
        events.update_bullets(enemies, ufo, bullets, w1, w2, w3, w4, screen, sc, gun)
        events.update_enemies(enemies)


def start_screen():
    intro_text = ["           SPACE INVADERS", "",
                  "Управление:",
                  "Правая и левая стрелочка для передвижения",
                  "Стрелка вверх для стрельбы",
                  'Чтобы отключить музыку нажите "w"',
                  'Чтобы включить музыку нажите "e"',
                  "",
                  "",
                  'Нажмите кнопку "Enter", чтобы начать игру!']
    screen.fill((0, 0, 0))
    font = pygame.font.Font('data/font/CustomFontTtf16H30.ttf', 30)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, True, 'white')
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 330
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                call(['python', 'SPACE_INVADERS_AND_RELAX.py'])
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    pygame.mixer.music.pause()
                if event.key == pygame.K_e:
                    pygame.mixer.music.play(-1)
                if event.key == pygame.K_RETURN:
                    return
        pygame.display.flip()


start_screen()
main()
