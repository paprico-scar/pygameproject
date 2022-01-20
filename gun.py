import pygame
from settings import *


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.gun_image = pygame.image.load('data/images/own_caracter.png')
        self.gun_image.set_colorkey(WHITE)
        self.gun_rect = self.gun_image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.gun_rect.centerx = self.screen_rect.centerx
        self.gun_rect.bottom = self.screen_rect.bottom - 73
        self.move_right = False
        self.move_left = False
        self.wall_hp = 4

    def draw_gun(self):
        self.screen.blit(self.gun_image, self.gun_rect)

    def update_gun(self):
        if self.move_right and self.gun_rect.right < self.screen_rect.right:
            self.gun_rect.centerx += 6
        if self.move_left and self.gun_rect.left > self.screen_rect.left:
            self.gun_rect.centerx -= 6
