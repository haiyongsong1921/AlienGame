class GameStats:
    """统计游戏信息"""
    def __init__(self, saveEarth):
        self.settings = saveEarth.settings
        self.game_active = False
        self.reset_stats()

    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.score = 0