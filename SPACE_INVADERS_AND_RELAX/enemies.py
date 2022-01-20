import pygame


class Invader(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Invader, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('data/images/enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = self.rect.x
        self.y = self.rect.y
        self.speed = 1.5

    def draw_invader(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += self.speed
        self.rect.x = self.x
        if self.rect.x >= 1234:
            self.y += self.rect.height + 58
            self.rect.y = self.y
            self.x = 0
            self.rect.x = self.x
