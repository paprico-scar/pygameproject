import pygame


class UFO(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(UFO, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('data/images/ufo.png')
        self.rect = self.image.get_rect()
        self.rect.x = -100
        self.rect.y = 10
        self.speed = -3
        self.x = self.rect.x
        self.y = self.rect.y

    def draw_ufo(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += self.speed
        self.rect.x = self.x
        if self.rect.x <= -2500:
            self.x = 1300
            self.rect.x = self.x
