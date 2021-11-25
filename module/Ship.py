'''飞船的管理类'''

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, saveEarth_game):
        super().__init__()
        self.screen = saveEarth_game.screen
        self.screen_rect = saveEarth_game.screen.get_rect()

        self.image = pygame.image.load('resource/img/ship.bmp')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        '''判断飞船是否要持续运动的标志'''
        self.keep_moving = False

        '''控制飞船移动速度'''
        self.settings = saveEarth_game.settings




    def update(self, direction):
        if self.keep_moving:
            tmp_x = self.rect.x
            if direction == pygame.K_RIGHT and self.rect.right < self.screen_rect.right:
                tmp_x += self.settings.ship_speed
            elif direction == pygame.K_LEFT and self.rect.left > 0:
                tmp_x -= self.settings.ship_speed
            self.rect.x = tmp_x

    def blit_me(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
