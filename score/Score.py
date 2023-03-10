from .GameScore import GameScore
from GameComponents.const import *

class Score(GameScore):
    def __init__(self, font_path, color = WHITE):
        super().__init__(font_path, color)

    def draw(self, screen, x, y):
        score_text = self.font.render("Score: " + str(self.value), True, self.color)
        screen.blit(score_text, (x, y))
        
    def get_score(self):
        return self.value