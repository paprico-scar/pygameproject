import pygame
from random import choice
from bullet import Bullet
from enemies import Invader
from ufo import UFO
from subprocess import call


def events(screen, gun, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            call(['python', 'first_window.py'])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if len(bullets) == 0:
                    new_bullet = Bullet(screen, gun)
                    bullets.add(new_bullet)
            if event.key == pygame.K_RIGHT:
                gun.move_right = True
            if event.key == pygame.K_LEFT:
                gun.move_left = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                gun.move_right = False
            if event.key == pygame.K_LEFT:
                gun.move_left = False


def update_screen(screen, gun, enemies, ufo, bullets, w1, w2, w3, w4, sc):
    fps = 60
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    sc.draw_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    pygame.draw.line(screen, (116, 255, 3), (0, 680), (1300, 680), 3)
    if w1.hp != 0:
        w1.draw_wall()
    if w2.hp != 0:
        w2.draw_wall()
    if w3.hp != 0:
        w3.draw_wall()
    if w4.hp != 0:
        w4.draw_wall()
    gun.draw_gun()
    ufo.draw(screen)
    enemies.draw(screen)
    clock.tick(fps)
    pygame.display.flip()


def update_bullets(enemies, ufo, bullets, w1, w2, w3, w4, screen, sc):
    bullets.update()
    for bullet in bullets.sprites():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        if pygame.sprite.collide_mask(bullet, w1):
            if w1.hp != 0:
                bullets.remove(bullet)
                w1.hp -= 1

        if pygame.sprite.collide_mask(bullet, w2):
            if w2.hp != 0:
                bullets.remove(bullet)
                w2.hp -= 1

        if pygame.sprite.collide_mask(bullet, w3):
            if w3.hp != 0:
                bullets.remove(bullet)
                w3.hp -= 1

        if pygame.sprite.collide_mask(bullet, w4):
            if w4.hp != 0:
                bullets.remove(bullet)
                w4.hp -= 1
    collide1 = pygame.sprite.groupcollide(bullets, enemies, True, True)
    if collide1:
        for i in collide1.values():
            sc.score += 10
            sc.image_score()
    if len(enemies) == 0:
        crete_army(screen, enemies, ufo)
        for i in enemies:
            i.speed += 0.5
    points = ['50', '100', '150', '200']
    collide2 = pygame.sprite.groupcollide(bullets, ufo, True, True)
    if collide2:
        p = int(choice(points))
        sc.score += p
        sc.image_score()
        u = UFO(screen)
        ufo.add(u)


def update_enemies(enemies):
    enemies.update()


def crete_army(screen, enemies, ufo):
    enemy = Invader(screen)
    width1 = enemy.rect.width
    height = enemy.rect.height
    u = UFO(screen)
    ufo.add(u)
    for y in range(5):
        for x in range(11):
            enemy = Invader(screen)
            enemy.x = width1 * 1.3 * x
            enemy.y = height * 1.3 * y
            enemy.rect.x = enemy.x
            enemy.rect.y = enemy.y
            enemies.add(enemy)
