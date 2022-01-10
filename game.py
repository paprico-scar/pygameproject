import pygame  # import pygame and sys
from pygame.locals import *  # import pygame modules
from settings import *
import random
import sqlite3
from subprocess import call

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()  # initiate pygame
pygame.mixer.set_num_channels(64)
pygame.display.set_caption(WINDOW_TITLE)  # set the window name
clock = pygame.time.Clock()  # set up the clock
screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)  # initiate screen
display = pygame.Surface(WINDOW_SIZE)

# moving
moving_right = False
moving_left = False
player_y_momentum = 0
air_timer = 0
true_scroll = [0, 0]

# font
font = pygame.font.Font('data/font/Dico.ttf', 20)

# lvl count
lvl_count = '1'


def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


animation_frames = {}


def load_animations(path, frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        ims_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(ims_loc).convert()
        animation_image.set_colorkey((255, 255, 255))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


# animation
animation_datebase = {}
animation_datebase['run'] = load_animations('data/player_animations/run', [10, 10, 10, 10])
animation_datebase['idle'] = load_animations('data/player_animations/idle', [40])

player_action = 'idle'
player_frame = 0
player_flip = False

# map
game_map = load_map(f'data/leveles/lvl_{lvl_count}/lvl_{lvl_count}')
game_map_bg = load_map(f'data/leveles/lvl_{lvl_count}/lvl_{lvl_count}_bg')
game_map_world = load_map(f'data/leveles/lvl_{lvl_count}/lvl_{lvl_count}_world')

# sounds and music
jumping_sound = pygame.mixer.Sound('data/music_and_sounds/jump.wav')
grass_sound = [pygame.mixer.Sound('data/music_and_sounds/grass_0.wav'),
               pygame.mixer.Sound('data/music_and_sounds/grass_1.wav')]
grass_sound[0].set_volume(0.4)
grass_sound[1].set_volume(0.4)

pygame.mixer.music.load('data/music_and_sounds/music.wav')
pygame.mixer.music.play(-1)

grass_sound_timer = 0

# player
sprite = pygame.sprite.Sprite()
player_rect = pygame.Rect(250, 160, 17, 22)

# environment
# lvl_?
# grass
lefttop_grass = pygame.image.load('data/tailes/grass/lefttop_grass.png')
righttop_grass = pygame.image.load('data/tailes/grass/righttop_grass.png')
top_grass = pygame.image.load('data/tailes/grass/top_grass.png')
top_leftgrass = pygame.image.load('data/tailes/grass/top_leftgrass.png')
top_rightgrass = pygame.image.load('data/tailes/grass/top_rightgrass.png')
lefttop_grass.set_colorkey(WHITE)
righttop_grass.set_colorkey(WHITE)
top_grass.set_colorkey(WHITE)
top_leftgrass.set_colorkey(WHITE)
top_rightgrass.set_colorkey(WHITE)
# dirt
center_dirt = pygame.image.load('data/tailes/dirt/center_dirt.png')
center_dirt_with_stone = pygame.image.load('data/tailes/dirt/center_dirt_with_stone.png')
left_dirt = pygame.image.load('data/tailes/dirt/left_dirt.png')
lefttop_dirt = pygame.image.load('data/tailes/dirt/lefttop_dirt.png')
right_dirt = pygame.image.load('data/tailes/dirt/right_dirt.png')
righttop_dirt = pygame.image.load('data/tailes/dirt/righttop_dirt.png')
top_dirt = pygame.image.load('data/tailes/dirt/top_dirt.png')
center_dirt.set_colorkey(WHITE)
center_dirt_with_stone.set_colorkey(WHITE)
left_dirt.set_colorkey(WHITE)
lefttop_dirt.set_colorkey(WHITE)
right_dirt.set_colorkey(WHITE)
righttop_dirt.set_colorkey(WHITE)
top_dirt.set_colorkey(WHITE)
# spike
spike = pygame.image.load('data/tailes/spike.png')
spike.set_colorkey(WHITE)
# teleport
teleport = pygame.image.load('data/tailes/teleport/teleport.png')
teleport.set_colorkey(WHITE)

# lvl_?_bg
# background
bg = pygame.image.load('data/tailes/background/bg.png')
top_bg_grass = pygame.image.load('data/tailes/background/top_bg_grass.png')
topright_bg_grass = pygame.image.load('data/tailes/background/topright_bg_grass.png')
right_bg_grass = pygame.image.load('data/tailes/background/right_bg_grass.png')
bottomright_bg_grass = pygame.image.load('data/tailes/background/bottomright_bg_grass.png')
bottom_bg_grass = pygame.image.load('data/tailes/background/bottom_bg_grass.png')
bottomleft_bg_grass = pygame.image.load('data/tailes/background/bottomleft_bg_grass.png')
left_bg_grass = pygame.image.load('data/tailes/background/left_bg_grass.png')
topleft_bg_grass = pygame.image.load('data/tailes/background/topleft_bg_grass.png')
bg_1 = pygame.image.load('data/tailes/background/bg_1.png')
bg_2 = pygame.image.load('data/tailes/background/bg_2.png')
topleft_bg = pygame.image.load('data/tailes/background/topleft_bg.png')
topright_bg = pygame.image.load('data/tailes/background/topright_bg.png')
bottomright_bg = pygame.image.load('data/tailes/background/bottomright_bg.png')
bottomleft_bg = pygame.image.load('data/tailes/background/bottomleft_bg.png')
water = pygame.image.load('data/tailes/background/water.png')
bg.set_colorkey(WHITE)
top_bg_grass.set_colorkey(WHITE)
topright_bg_grass.set_colorkey(WHITE)
right_bg_grass.set_colorkey(WHITE)
bottomright_bg_grass.set_colorkey(WHITE)
bottom_bg_grass.set_colorkey(WHITE)
bottomleft_bg_grass.set_colorkey(WHITE)
left_bg_grass.set_colorkey(WHITE)
topleft_bg_grass.set_colorkey(WHITE)
bg_1.set_colorkey(WHITE)
bg_2.set_colorkey(WHITE)
topleft_bg.set_colorkey(WHITE)
topright_bg.set_colorkey(WHITE)
bottomright_bg.set_colorkey(WHITE)
bottomleft_bg.set_colorkey(WHITE)

# lvl_?_world
# herb
herb = pygame.image.load('data/tailes/herb/herb.png')
chamomile = pygame.image.load('data/tailes/herb/chamomile.png')
chamomile_2 = pygame.image.load('data/tailes/herb/chamomile_2.png')
orange_flower = pygame.image.load('data/tailes/herb/orange_flower.png')
orange_flower_2 = pygame.image.load('data/tailes/herb/orange_flower_2.png')
herb.set_colorkey(WHITE)
chamomile.set_colorkey(WHITE)
chamomile_2.set_colorkey(WHITE)
orange_flower.set_colorkey(WHITE)
orange_flower_2.set_colorkey(WHITE)
# stone
stone_1 = pygame.image.load('data/tailes/stone/stone_1.png')
stone_2 = pygame.image.load('data/tailes/stone/stone_2.png')
stone_1.set_colorkey(WHITE)
stone_2.set_colorkey(WHITE)
# world
box = pygame.image.load('data/tailes/world/box.png')
desk = pygame.image.load('data/tailes/world/desk.png')
desk_arrow = pygame.image.load('data/tailes/world/desk_arrow.png')
fence_1 = pygame.image.load('data/tailes/world/fence_1.png')
fence_2 = pygame.image.load('data/tailes/world/fence_2.png')
fence_3 = pygame.image.load('data/tailes/world/fence_3.png')
fenceb_1 = pygame.image.load('data/tailes/world/fenceb_1.png')
fenceb_2 = pygame.image.load('data/tailes/world/fenceb_2.png')
fenceb_3 = pygame.image.load('data/tailes/world/fenceb_3.png')
box.set_colorkey(WHITE)
desk.set_colorkey(WHITE)
desk_arrow.set_colorkey(WHITE)
fence_1.set_colorkey(WHITE)
fence_2.set_colorkey(WHITE)
fence_3.set_colorkey(WHITE)
fenceb_1.set_colorkey(WHITE)
fenceb_2.set_colorkey(WHITE)
fenceb_3.set_colorkey(WHITE)

TILE_SIZE = top_grass.get_width()
BOX_TLIE_SIZE = box.get_width()
running = True
playing = True


def collision_test(rect, tiles):
    global lvl_count, player_rect, game_map_bg, game_map, game_map_world, screen
    hit_list = []
    test = True
    for i, tile in tiles.items():
        if rect.colliderect(tile[0]):
            hit_list.append(tile[0])
            if rect.colliderect(tile[0]) and tile[1] == 'M':
                test = False
            if rect.colliderect(tile[0]) and tile[1] == 'O':
                player_rect.x = 250
                player_rect.y = 316
                if lvl_count == '2':
                    the_end(screen)
                    pygame.quit()
                    call(['python', 'first_window.py'])
                else:
                    lvl_count = str(int(lvl_count) + 1)
                    new_level(screen)
    return hit_list, test


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list, test = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list, test = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types, test


def draw_text(text, color, x, y, screen, font):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def show_start_screen(sc):
    # game splash/start screen
    font = pygame.font.Font('data/font/Dico.ttf', 40)
    sc.fill(BGCOLOR)
    draw_text(WINDOW_TITLE, RED, WIDTH / 3 * 1.5, HEIGHT / 5, sc, font)
    font = pygame.font.Font('data/font/Dico.ttf', 25)
    draw_text("Arrows to move", WHITE, WIDTH / 4, HEIGHT / 3, sc, font)
    draw_text("Space to jump", WHITE, WIDTH / 4, HEIGHT / 3 + 40, sc, font)
    draw_text('To stop music press "w" key', WHITE, WIDTH / 4 * 3, HEIGHT / 3, sc, font)
    draw_text('To play music press "e" key', WHITE, WIDTH / 4 * 3, HEIGHT / 3 + 40, sc, font)
    draw_text('jump only on the chest to go to the next level', WHITE, WIDTH / 2, HEIGHT / 2, sc, font)
    draw_text("Press any key to play", WHITE, WIDTH / 2, HEIGHT * 3 / 4, sc, font)
    pygame.display.flip()
    wait_for_key()


def new_level(sc):
    font = pygame.font.Font('data/font/Dico.ttf', 40)
    sc.fill(BGCOLOR)
    draw_text('Level 2', WHITE, WIDTH / 2, HEIGHT / 2, sc, font)
    pygame.display.flip()
    wait_for_key()


def the_end(sc):
    global running, playing, score_timer
    final_score = score_timer // 60
    con = sqlite3.connect('data/db/game.db')
    cur = con.cursor()
    max_score = cur.execute('''SELECT MAX(score) FROM tb_score''').fetchone()
    font = pygame.font.Font('data/font/Dico.ttf', 40)
    sc.fill(BGCOLOR)
    draw_text('Thanks for playing', WHITE, WIDTH / 2, HEIGHT / 4, sc, font)
    draw_text(f'Best score: {max_score[0]}', WHITE, WIDTH / 2, HEIGHT / 3, sc, font)
    draw_text(f"Score: {final_score}", WHITE, WIDTH / 2, HEIGHT / 2, sc, font)
    pygame.display.flip()
    wait_for_key()


def show_go_screen(sc):
    # game over/continue
    global score_timer, another_air_timer, lvl_count
    final_score = score_timer // 60
    con = sqlite3.connect('data/db/game.db')
    cur = con.cursor()
    max_id = cur.execute('''SELECT MAX(id) FROM tb_score''').fetchone()
    new_id = max_id[0] + 1
    add_in_db = [new_id, final_score]
    cur.execute('''INSERT INTO tb_score VALUES(?,?);''', add_in_db)
    con.commit()
    max_score = cur.execute('''SELECT MAX(score) FROM tb_score''').fetchone()
    font = pygame.font.Font('data/font/Dico.ttf', 40)
    global running
    if running:
        return
    score_timer = 0
    another_air_timer = 0
    lvl_count = '1'
    sc.fill(BGCOLOR)
    draw_text("GAME OVER", WHITE, WIDTH / 2, HEIGHT / 5, sc, font)
    draw_text(f'Best score: {max_score[0]}', WHITE, WIDTH / 2, HEIGHT / 3, sc, font)
    draw_text(f"Score: {final_score}", WHITE, WIDTH / 2, HEIGHT / 2, sc, font)
    draw_text("Press any key to play again", WHITE, WIDTH / 2, HEIGHT * 3 / 4, sc, font)
    pygame.display.flip()
    wait_for_key()


def wait_for_key():
    waiting = True
    global clock, running, playing, moving_right, moving_left, player_rect, another_air_timer, score_timer
    global game_map, game_map_bg, game_map_world, lvl_count
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                playing = False
                running = False
                pygame.quit()
                call(['python', 'first_window.py'])
            if event.type == pygame.KEYUP:
                waiting = False
                running = True
                player_rect.x = 250
                player_rect.y = 316
                moving_right = False
                moving_left = False
                game_map = load_map(f'data/leveles/lvl_{lvl_count}/lvl_{lvl_count}')
                game_map_bg = load_map(f'data/leveles/lvl_{lvl_count}/lvl_{lvl_count}_bg')
                game_map_world = load_map(f'data/leveles/lvl_{lvl_count}/lvl_{lvl_count}_world')


score_timer = 0
another_air_timer = 0

show_start_screen(screen)
while playing:  # game loop
    while running:
        score_timer += 1
        display.fill((146, 244, 255))
        true_scroll[0] += (player_rect.x - true_scroll[0] - 152) / 30
        true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 30
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        if grass_sound_timer > 0:
            grass_sound_timer -= 1

        display.blit(water, (0, 120, 400, 200))
        y = 0
        for row in game_map_bg:
            x = 0
            for tile in row:
                if tile == '1':
                    display.blit(bg, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '2':
                    display.blit(top_bg_grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '3':
                    display.blit(topright_bg_grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '4':
                    display.blit(right_bg_grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '5':
                    display.blit(bottomright_bg_grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '6':
                    display.blit(bottom_bg_grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '7':
                    display.blit(bottomleft_bg_grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '8':
                    display.blit(left_bg_grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '9':
                    display.blit(topleft_bg_grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '<':
                    display.blit(bg_1, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '^':
                    display.blit(bg_2, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'i':
                    display.blit(topleft_bg, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'o':
                    display.blit(topright_bg, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'l':
                    display.blit(bottomright_bg, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'k':
                    display.blit(bottomleft_bg, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                x += 1
            y += 1

        y = 0
        for row in game_map_world:
            x = 0
            for tile in row:
                if tile == '1':
                    display.blit(box, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '2':
                    display.blit(desk, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '3':
                    display.blit(desk_arrow, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '7':
                    display.blit(fenceb_1, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '8':
                    display.blit(fenceb_2, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '9':
                    display.blit(fenceb_3, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'S':
                    display.blit(stone_2, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'g':
                    display.blit(chamomile_2, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'j':
                    display.blit(orange_flower_2, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                x += 1
            y += 1

        tile_rect = {}
        y = 0
        for row in game_map:
            x = 0
            for tile in row:
                if tile == '1':
                    display.blit(top_grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '2':
                    display.blit(top_leftgrass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '3':
                    display.blit(top_rightgrass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '4':
                    display.blit(lefttop_grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '5':
                    display.blit(righttop_grass, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '6':
                    display.blit(top_dirt, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '7':
                    display.blit(lefttop_dirt, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '8':
                    display.blit(righttop_dirt, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '9':
                    display.blit(center_dirt, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '^':
                    display.blit(center_dirt_with_stone, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '>':
                    display.blit(right_dirt, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '<':
                    display.blit(left_dirt, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'M':
                    display.blit(spike, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'O':
                    display.blit(teleport, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '^', '>', '<', 'M', 'O']:
                    tile_rect[str(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))] = pygame.Rect(
                        x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), tile
                x += 1
            y += 1

        player_movement = [0, 0]
        if moving_right:
            player_movement[0] += 2
        if moving_left:
            player_movement[0] -= 2
        player_movement[1] += player_y_momentum
        player_y_momentum += 0.2
        if player_y_momentum > 3:
            player_y_momentum = 3

        if player_movement[0] > 0:
            player_action, player_frame = change_action(player_action, player_frame, 'run')
            player_flip = False
        if player_movement[0] == 0:
            player_action, player_frame = change_action(player_action, player_frame, 'idle')
        if player_movement[0] < 0:
            player_action, player_frame = change_action(player_action, player_frame, 'run')
            player_flip = True
        player_rect, collisions, running = move(player_rect, player_movement, tile_rect)

        if not collisions['bottom'] and not collisions['top'] and not collisions['left'] and not collisions['right']:
            another_air_timer += 1
        else:
            another_air_timer = 0

        if another_air_timer / 60 >= 5:
            running = False

        if collisions['bottom']:
            player_y_momentum = 0
            air_timer = 0
            if player_movement[0] != 0:
                if grass_sound_timer == 0:
                    grass_sound_timer = 30
                    random.choice(grass_sound).play()
        else:
            air_timer += 1

        player_frame += 1
        if player_frame >= len(animation_datebase[player_action]):
            player_frame = 0
        player_img_id = animation_datebase[player_action][player_frame]
        player_image = animation_frames[player_img_id]
        display.blit(pygame.transform.flip(player_image, player_flip, False),
                     (player_rect.x - scroll[0], player_rect.y - scroll[1]))

        y = 0
        for row in game_map_world:
            x = 0
            for tile in row:
                if tile == 'w':
                    display.blit(herb, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'f':
                    display.blit(chamomile, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'h':
                    display.blit(orange_flower, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 's':
                    display.blit(stone_1, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '4':
                    display.blit(fence_1, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '5':
                    display.blit(fence_2, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == '6':
                    display.blit(fence_3, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                x += 1
            y += 1
            draw_text(str(score_timer // 60), WHITE, 20, 5, display, font)

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:  # check for window quit
                running = False
                playing = False
                call(['python', 'first_window.py'])
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_w:
                    pygame.mixer.music.fadeout(1000)
                if event.key == K_e:
                    pygame.mixer.music.play(-1)
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_SPACE:
                    if air_timer < 6:
                        jumping_sound.play()
                        player_y_momentum = -5
            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False
                if event.key == K_LEFT:
                    moving_left = False
        surf = pygame.transform.scale(display, SCREEN_SIZE)
        screen.blit(surf, (0, 0))
        pygame.display.update()  # update display
        clock.tick(60)  # maintain 60 fps
    show_go_screen(screen)
