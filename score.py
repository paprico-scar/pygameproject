import pygame.font


class Score:
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.font = pygame.font.Font('font_kurasov/space_invaders.ttf', 30)
        self.score = 0
        self.image_score()

    def image_score(self):
        self.score_image = self.font.render(('SCORE: ' + str(self.score)), True, pygame.Color('white'))
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 60
        self.score_rect.bottom = self.screen_rect.bottom - 10

    def draw_score(self):
        self.screen.blit(self.score_image, self.score_rect)
