
import pygame
from .Food import Food
from .Snake import Snake 

import math
import numpy as np

from collisionSystem.lineCollisions import lineCollision
from GameComponents.const import *
class sensors:
    def __init__(self, screen: pygame.Surface, snake: Snake, food:Food):
        self.screen = screen
        self.snake = snake
        self.food = food
        self.detector  = lineCollision(self.snake,self.food)
        self.danger = [0,0,0] #strait, right, left
        
    def get_directions(self,direction):

        if direction == "UP":
            return [(0, -1),(1, 0), (-1, 0)]
        elif direction == "DOWN":
            return [(0, 1), (-1, 0), (1, 0)]
        elif direction == "LEFT":
            return [(-1, 0),(0, -1), (0, 1)]
        elif direction == "RIGHT":
            return [(1, 0),(0, 1), (0, -1)]
        else:
            return

    def draw_lines(self) -> None:
        head_pos = self.snake.head.center
        directions  = self.get_directions(self.snake.direction)
        counter = 0
        for dx, dy in directions:
            intersects_food = False
            intersects_obstacle = False
            x, y = head_pos
            while 0 <= x < self.screen.get_width() and 0 <= y < self.screen.get_height():
                x += dx * self.snake.size
                y += dy * self.snake.size

                if self.detector.line_food_collision(x, y):
                    intersects_food = True
                    break

                if (self.detector.line_body_collision(x, y) or self.detector.line_wall_danger(x,y,self.screen)):
                    if math.dist((x, y), head_pos) <= 150:
                        intersects_obstacle = True
                    break

            end_pos = (x - dx * self.snake.size, y - dy * self.snake.size)
            points = [(head_pos[0] + dx * self.snake.size // 2, head_pos[1] + dy * self.snake.size // 2),
                    (end_pos[0] + dx * self.snake.size // 2, end_pos[1] + dy * self.snake.size // 2)]
            
            if intersects_obstacle:
                color = RED  # red for obstacles getting dangerly closer
                self.danger[counter] = 1
            elif intersects_food:
                color = YELLOW  # yellow for food
            else:
                self.danger[counter] = 0
                color = WHITE  # white for empty space

            self.draw_dashed_line(self.screen, color, points[0], points[1])
            counter += 1





    def draw_dashed_line(self,surf, color, start_pos, end_pos, width=1, dash_length=8):
        x1, y1 = start_pos
        x2, y2 = end_pos
        dl = dash_length

        if (x1 == x2):
            ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
            xcoords = [x1] * len(ycoords)
        elif (y1 == y2):
            xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
            ycoords = [y1] * len(xcoords)
        else:
            a = abs(x2 - x1)
            b = abs(y2 - y1)
            c = round(math.sqrt(a**2 + b**2))
            dx = dl * a / c
            dy = dl * b / c

            xcoords = [x for x in np.arange(x1, x2, dx if x1 < x2 else -dx)]
            ycoords = [y for y in np.arange(y1, y2, dy if y1 < y2 else -dy)]

        next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
        last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
        
        for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
            start = (round(x1), round(y1))
            end = (round(x2), round(y2))
            pygame.draw.line(surf, color, start, end, width)
            
    def get_neuralNetwork_input(self):
        head = self.snake.head
        
        dir_r = self.snake.direction== 'RIGHT'
        dir_l = self.snake.direction == 'LEFT'
        dir_u =  self.snake.direction == 'UP'
        dir_d =  self.snake.direction == 'DOWN'

        state = [
            # Danger straight
            self.danger[0],
            # Danger right
            self.danger[1],
            # Danger left
            self.danger[2],
            
            # Move direction
            dir_r,
            dir_l,
            dir_u,
            dir_d,
            
            # Food location 
            self.food.rect.x < head.x,  # food left
            self.food.rect.x > head.x,  # food right
            self.food.rect.y < head.y,  # food up
            self.food.rect.y > head.y  # food down
        ]
        
        return np.array(state, dtype=int) 
