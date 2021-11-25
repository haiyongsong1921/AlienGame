'''游戏资源的管理类'''
import pygame
import sys
from setttings import Settings
from module.Ship import Ship
from module.Bullet import Bullet
from module.Alien import Alien
from time import sleep
from module.GameStats import GameStats

from module.Button import Button
from module.ScoreBoard import ScoreBoard

class SaveEarth:
    def __init__(self):
        pygame.init() #初始化pygame模块

        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        '''全屏显示
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        '''
        pygame.display.set_caption(self.settings.caption) #设置游戏窗口标题
        self.bg_color = self.settings.bg_color  #保存RGB背景色
        self.ship = Ship(self)
        self.currentKeyDown = 0

        #省略
        '''添加外星人'''
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        '''添加子弹'''
        self.bullets = pygame.sprite.Group()

        #省略
        '''创建游戏统计'''
        self.stats = GameStats(self)

        '''添加按钮'''
        self.play_button = Button(self, "Play")
        '''添加计分牌'''
        self.score_board = ScoreBoard(self)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + 2 * alien_number * alien_width
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * row_number * alien_height
        self.aliens.add(alien)

    def _create_fleet(self):
        alien = Alien(self)
        alien_width = alien.rect.width
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (2 * alien_width)

        alien_height = alien.rect.height
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.keep_moving = True
            self.currentKeyDown = pygame.K_RIGHT
        elif event.key == pygame.K_LEFT:
            self.ship.keep_moving = True
            self.currentKeyDown = pygame.K_LEFT
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
            self.ship.keep_moving = False

    def _check_events(self):
        '''处理鼠标键盘的响应消息'''
        for event in pygame.event.get():  # 获取pygame响应事件列表
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_play_button(pygame.mouse.get_pos())

    def _check_play_button(self, mouse_pos):
        button_click = self.play_button.rect.collidepoint(mouse_pos)
        if button_click and not self.stats.game_active:
            self.stats.game_active = True
            '''重置统计信息'''
            self.stats.reset_stats()
            '''清空外星人和子弹'''
            self.aliens.empty()
            self.bullets.empty()
            '''初始化飞船位置'''
            self.ship.center_ship()
            '''初始化记分牌'''
            self.score_board.prep_score()
            '''初始化飞船信息'''
            self.score_board.prep_ships()


    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _draw_bullet(self):
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

    def _update_screen(self):
        '''刷新屏幕'''
        self.screen.fill(self.bg_color)  # 用背景色填充窗口
        self.ship.blit_me()  # 刷新飞船，放到display.flip之前
        self._draw_bullet()  # 绘制子弹
        self.aliens.draw(self.screen)
        self.score_board.show_score()
        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()  # 刷新绘制区域

    def _clear_dirty_bullet(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
                print(len(self.bullets))

    def _check_bullet_alien_collision(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_point * len(aliens)
                self.score_board.prep_score()

    def _check_all_aliens_clean(self):
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _update_bullet(self):
        self.bullets.update()
        self._check_bullet_alien_collision()
        self._clear_dirty_bullet()
        self._check_all_aliens_clean()


    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.reach_edges():
                return True

    def _check_fleet_bottom(self):
        for alien in self.aliens.sprites():
            if alien.reach_bottom():
                return True

    def _ship_hit(self):
        self.stats.ship_left -= 1
        if self.stats.ship_left > 0:
            self.aliens.empty()
            self.bullets.empty()
            self.ship.center_ship()
            sleep(0.5)
        else:
            self.stats.game_active = False
        self.score_board.prep_ships()

    def _update_alien(self):
        reachEdge = self._check_fleet_edges()
       # if reachEdge:
       #     reachBottom = self._check_fleet_bottom()
      #      if reachBottom:
     #           return
        self.aliens.update(reachEdge)
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def run_game(self):
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update(self.currentKeyDown)
                self._update_bullet()
                self._update_alien()
            self._update_screen()

