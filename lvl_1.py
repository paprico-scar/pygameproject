import pygame  # import pygame and sys
from pygame.locals import *  # import pygame modules
from settings import *

pygame.init()  # initiate pygame
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


animation_datebase = {}
animation_datebase['run'] = load_animations('data/player_animations/run', [10, 10, 10, 10])
animation_datebase['idle'] = load_animations('data/player_animations/idle', [40])

player_action = 'idle'
player_frame = 0
player_flip = False

game_map = load_map('map')

# player
player_rect = pygame.Rect(100, 100, 17, 22)

# environment
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

TILE_SIZE = top_grass.get_width()
running = True
playing = True


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


def draw_text(text, size, color, x, y, screen):
    font_name = 'arial'
    font = pygame.font.SysFont(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def show_start_screen(sc):
    # game splash/start screen
    sc.fill(BGCOLOR)
    draw_text(WINDOW_TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4, sc)
    draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2, sc)
    draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4, sc)
    pygame.display.flip()
    wait_for_key()


# Надо реализоваить эту функцию
def show_go_screen(sc):
    # game over/continue
    if not running:
        return
    sc.fill(BGCOLOR)
    draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4, sc)
    draw_text("Score: ", 22, WHITE, WIDTH / 2, HEIGHT / 2, sc)
    draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4, sc)
    pygame.display.flip()
    wait_for_key()


def wait_for_key():
    waiting = True
    global clock
    global running
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                running = False
            if event.type == pygame.KEYUP:
                waiting = False


show_start_screen(screen)
while playing:  # game loop
    while running:
        display.fill((146, 244, 255))

        true_scroll[0] += (player_rect.x - true_scroll[0] - 152) / 30
        true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 30
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])

        pygame.draw.rect(display, BGCOLOR, pygame.Rect(0, 120, 400, 200))

        tile_rect = []
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
                if tile in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '^', '>', '<']:
                    tile_rect.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
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
        player_rect, collisions = move(player_rect, player_movement, tile_rect)

        if collisions['bottom']:
            player_y_momentum = 0
            air_timer = 0
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
        for row in game_map:
            x = 0
            for tile in row:
                if tile == 'w':
                    display.blit(herb, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'f':
                    display.blit(chamomile, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'f':
                    display.blit(chamomile_2, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'h':
                    display.blit(orange_flower, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                if tile == 'j':
                    display.blit(orange_flower_2, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
                x += 1
            y += 1

        for event in pygame.event.get():  # event loop
            if event.type == QUIT:  # check for window quit
                running = False
                playing = False
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    moving_right = True
                if event.key == K_LEFT:
                    moving_left = True
                if event.key == K_SPACE:
                    if air_timer < 6:
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
pygame.quit()
