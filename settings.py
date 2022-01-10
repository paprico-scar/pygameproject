# Настройки окна
SCREEN_SIZE = WIDTH, HEIGHT = 800, 600
WINDOW_SIZE = (350, 250)
WINDOW_TITLE = 'RELAX'
FIRST_WINDOW_TITLE = 'SPACE INVADERS AND RELAX'
FPS = 120

# Настроки цветов
BGCOLOR = (7, 80, 75)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def draw_text(text, color, x, y, screen, font):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)
