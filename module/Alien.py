import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, saveEarth_game):
        super().__init__()
        self.screen = saveEarth_game.screen
        self.image = pygame.image.load('resource/img/alien.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.settings = saveEarth_game.settings
        self.direction = 1

    def update(self, reachEdge):
        if reachEdge:
            self.direction *= -1
            self._move_down()
        self.x += self.settings.alien_speed * self.direction
        self.rect.x = self.x

    def reach_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return  True

    def reach_bottom(self):
        screen_rect = self.screen.get_rect()
        if self.rect.bottom >= screen_rect.bottom:
            return True

    def _move_down(self):
        self.rect.y += self.settings.fleet_drop_speed