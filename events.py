import pygame, sys
from random import choice
from bullet import Bullet
from enemies import Invader
from ufo import UFO
from subprocess import call


def events(screen, gun, bullets):
    shoot = pygame.mixer.Sound('data/music_and_sounds/shoot.wav')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            call(['python', 'first_window.py'])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pygame.mixer.music.pause()
            if event.key == pygame.K_e:
                pygame.mixer.music.play(-1)
            if event.key == pygame.K_UP:
                if len(bullets) == 0:
                    new_bullet = Bullet(screen, gun)
                    bullets.add(new_bullet)
                    shoot.play()
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
    for i in enemies:
        if i.y >= 550:
            endgame(screen, sc)
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


def update_bullets(enemies, ufo, bullets, w1, w2, w3, w4, screen, sc, gun):
    kill_invader = pygame.mixer.Sound('data/music_and_sounds/invaderkilled.wav')
    bullets.update()
    for bullet in bullets.sprites():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        if pygame.sprite.collide_mask(bullet, w1):
            if w1.hp != 0:
                bullets.remove(bullet)
                w1.hp -= 1
            if w1.hp == 0:
                if w1.wall:
                    gun.wall_hp -= 1
                    w1.wall = False
                    if gun.wall_hp == 0:
                        endgame(screen, sc)

        if pygame.sprite.collide_mask(bullet, w2):
            if w2.hp != 0:
                bullets.remove(bullet)
                w2.hp -= 1
            if w2.hp == 0:
                if w2.wall:
                    gun.wall_hp -= 1
                    w2.wall = False
                    if gun.wall_hp == 0:
                        endgame(screen, sc)

        if pygame.sprite.collide_mask(bullet, w3):
            if w3.hp != 0:
                bullets.remove(bullet)
                w3.hp -= 1
            if w3.hp == 0:
                if w3.wall:
                    gun.wall_hp -= 1
                    w3.wall = False
                    if gun.wall_hp == 0:
                        endgame(screen, sc)

        if pygame.sprite.collide_mask(bullet, w4):
            if w4.hp != 0:
                bullets.remove(bullet)
                w4.hp -= 1
            if w4.hp == 0:
                if w4.wall:
                    gun.wall_hp -= 1
                    w4.wall = False
                    if gun.wall_hp == 0:
                        endgame(screen, sc)
    collide1 = pygame.sprite.groupcollide(bullets, enemies, True, True)
    if collide1:
        for i in collide1.values():
            kill_invader.play()
            sc.score += 10
            sc.image_score()
            new_record(sc)
    if len(enemies) == 0:
        ufo.empty()
        crete_army(screen, enemies, ufo)
        for i in enemies:
            i.speed += 0.5
    points = ['50', '100', '150', '200']
    collide2 = pygame.sprite.groupcollide(bullets, ufo, True, True)
    if collide2:
        p = int(choice(points))
        sc.score += p
        sc.image_score()
        new_record(sc)
        u = UFO(screen)
        ufo.add(u)


def update_enemies(enemies):
    enemies.update()


def crete_army(screen, enemies, ufo):
    enemy = Invader(screen)
    width = enemy.rect.width
    height = enemy.rect.height
    u = UFO(screen)
    ufo.add(u)
    for y in range(5):
        for x in range(11):
            enemy = Invader(screen)
            enemy.x = width * 1.3 * x
            enemy.y = height * 1.3 * y
            enemy.rect.x = enemy.x
            enemy.rect.y = enemy.y
            enemies.add(enemy)


def new_record(sc):
    if sc.score > sc.hi_score:
        sc.hi_score = sc. score
        sc.image_hi_score()
        with open('data/db/hight_score.txt', 'w') as f:
            f.write(str(sc.hi_score))


def endgame(screen, sc):
    intro_text = ["           ИГРА ОКОНЧЕНА", "",
                  "Лучший счёт: ",
                  "Счёт: ", "",
                  'Нажмите кнопку "Enter", чтобы начать заново!']
    score = str(sc.score)
    with open('data/db/hight_score.txt', 'r') as f:
        hi_score = f.readline()
    screen.fill((0, 0, 0))
    font = pygame.font.Font('data/font/CustomFontTtf16H30.ttf', 40)
    text_coord = 200
    for line in intro_text:
        string_rendered = font.render(line, True, 'white')
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 300
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    score_im = font.render(score, True, 'white')
    score_rect = score_im.get_rect()
    score_rect.top = 360
    score_rect.x = 410
    hi_score_im = font.render(hi_score, True, 'white')
    hi_score_rect = hi_score_im.get_rect()
    hi_score_rect.top = 310
    hi_score_rect.x = 540
    screen.blit(score_im, score_rect)
    screen.blit(hi_score_im, hi_score_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                call(['python', 'first_window.py'])
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.quit()
                call(['python', 'main.py'])
                sys.exit()
        pygame.display.flip()
