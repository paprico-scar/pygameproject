import pygame.font


class Score:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.font = pygame.font.Font('data/font/CustomFontTtf16H30.ttf', 30)
        self.score = 0
        with open('data/db/hight_score.txt', 'r') as f:
            self.hi_score = int(f.readline())
        self.image_score()
        self.image_hi_score()

    def image_score(self):
        self.score_image = self.font.render(('СЧЁТ: ' + str(self.score)), True, 'white')
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 70
        self.score_rect.bottom = self.screen_rect.bottom - 10

    def image_hi_score(self):
        self.hi_score_image = self.font.render(('РЕКОРД: ' + str(self.hi_score)), True, 'white')
        self.hi_score_rect = self.hi_score_image.get_rect()
        self.hi_score_rect.right = self.screen_rect.right - 250
        self.hi_score_rect.bottom = self.screen_rect.bottom - 10

    def draw_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.hi_score_image, self.hi_score_rect)
