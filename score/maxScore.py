from .GameScore import GameScore
from GameComponents.const import *


class MaxScore(GameScore):
    def __init__(self, file_name, font_path, color=WHITE):
        super().__init__(font_path, color)
        self.file_name = file_name
        self.max_score = self.load_max_score()

    def load_max_score(self):
        try:
            with open(self.file_name, "r") as f:
                max_score = int(f.read())
        except (IOError, ValueError):
            max_score = 0
        return max_score

    def save_max_score(self, score):
        if score > self.max_score:
            self.max_score = score
            with open(self.file_name, "w") as f:
                f.write(str(score))

    def get_max_score(self):
        return self.max_score

    def draw(self, screen, x, y):
        score_text = self.font.render("Max score: " + str(self.max_score), True, self.color)
        screen.blit(score_text, (x, y))
        
    def get_score(self):
        return self.max_score