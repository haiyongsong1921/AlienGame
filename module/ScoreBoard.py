import pygame.font
from pygame.sprite import Group
from module.Ship import Ship

class ScoreBoard:
    def __init__(self, saveEarth):
        self.screen = saveEarth.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = saveEarth.settings
        self.stats = saveEarth.stats
        '''积分系统字体信息'''
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()
        '''构造飞船编组'''
        self.save_earth = saveEarth
        self.prep_ships()

    def prep_ships(self):
        self.ships = Group()
        for ship_count in range(self.stats.ship_left):
            ship = Ship(self.save_earth)
            ship.rect.x = 10 + ship_count * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)


    def prep_score(self):
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.ships.draw(self.screen)