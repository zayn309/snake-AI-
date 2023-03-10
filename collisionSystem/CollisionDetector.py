from GameComponents.Snake import Snake
from GameComponents.Food import Food

class CollisionDetector:
    def __init__(self, snake: Snake,food:Food, width: int = 0, height: int = 0):
        self.snake = snake
        self.width = width
        self.height = height
        self.food = food
        