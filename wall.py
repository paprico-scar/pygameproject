import pygame


class Wall:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.image = pygame.image.load('data/images/wall.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 30

    def draw_wall(self):
        self.screen.blit(self.image, self.rect)
