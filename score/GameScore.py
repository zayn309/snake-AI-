import pygame
from abc import ABC, abstractmethod

from GameComponents.const import *


class GameScore(ABC):
    def __init__(self, font_path,color = WHITE):
        pygame.font.init()
        self.value = 0
        self.font = pygame.font.Font(font_path, SCORE_FONT_SIZE)
        self.color = color

    def increase(self, amount=1):
        self.value += amount

    def reset(self):
        self.value = 0

    @abstractmethod
    def draw(self, screen, x, y):
        pass
    
    @abstractmethod
    def get_score(self):
        pass