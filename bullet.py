import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, gun):
        super(Bullet, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('data/images/bullet.png')
        self.rect = self.image.get_rect()
        self.speed = 7
        self.rect.centerx = gun.gun_rect.centerx
        self.rect.top = gun.gun_rect.top
        self.y = self.rect.y

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)
