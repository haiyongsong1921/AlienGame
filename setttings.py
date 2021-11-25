'''管理游戏设置的类'''
class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        self.caption = "保卫地球"
        self.ship_speed = 2
        self.ship_limit = 3
        '''子弹配置'''
        self.bullet_speed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,60,60)
        '''外星人配置'''
        self.alien_speed =2
        self.fleet_drop_speed = 200
        '''外星人分数'''
        self.alien_point = 50
