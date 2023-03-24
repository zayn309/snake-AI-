import pygame
from pygame.locals import *
from .sensors import sensors

import os

from .Snake import Snake
from .Food import Food
from score.maxScore import MaxScore
from score.Score import Score
from collisionSystem.lineCollisions import lineCollision

from collisionSystem.snakeCollision import snakeCollision

from .const import *
class Game:

    def __init__(self, width: int, height: int, fps: int):
        self.width = width
        self.height = height
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.snake = Snake(self.width//2, self.height//2, BLOCK_SIZE , BLOCK_SIZE)
        self.food = Food(self.width-12, self.height-12, BLOCK_SIZE, RED ,self.snake)
        self.score = Score(os.path.join(os.path.join(os.path.dirname(__file__), '..', 'fonts'), "arial.ttf"))
        self.max_score = MaxScore('max score.txt',os.path.join(os.path.join(os.path.dirname(__file__), '..', 'fonts'), "arial.ttf"))
        self.snakeCollisionDetector = snakeCollision(self.snake,self.food,self.width,self.height)
        self.lineCollisionDetector = lineCollision(self.snake,self.food,self.width,self.height)
        self.Sensors = sensors(self.screen, self.snake,self.food)
        self.frame_iteration = 0
        self.clock = pygame.time.Clock()

    def check_snake_food_collision(self):
        if self.snakeCollisionDetector.snake_food_collision():
            self.snake.grow()
            self.food.spawn()
            self.score.increase()
            return True
        
        return False
    
    def check_snake_body_collision(self):
        if self.snakeCollisionDetector.snake_body_collision():
            return True
        return False
    
    def check_snake_wall_collision(self):
        if self.snakeCollisionDetector.snake_wall_collision():
            return True
        return False
    
    def draw(self,draw_score = True , draw_sensor = False):
        self.screen.fill(BLACK)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        if draw_score:
            self.score.draw(self.screen, 10, 10)
            self.max_score.draw(self.screen,10,30)
        if draw_sensor:
            self.Sensors.draw_lines()
        
            

    def game_over(self):
        
        #update max score 
        self.max_score.save_max_score(self.score.get_score())
        
        # Reset the score
        self.score.reset()
        
        self.frame_iteration = 0
        
        # Reset the snake
        self.snake.reset()
        
        # Reset the food
        self.food.spawn()
        