import numpy as np
import pygame
from pygame.locals import *

from .const import *


class Snake:
    def __init__(self, x, y, size, speed):
        self.size = size
        self.start_x = x
        self.start_y = y
        self.speed = speed
        self.direction = "RIGHT"
        self.body = [(x, y), (x-size, y)]
        self.grow_pending = 0

    @property
    def head(self):
        # Return the position of the snake's head
        return pygame.Rect(self.body[0][0], self.body[0][1], self.size, self.size)

    @property
    def body_segments(self):
        # Return the position of the snake's body segments
        return [pygame.Rect(segment[0], segment[1], self.size, self.size) for segment in self.body[1:]]

    def move(self):
        # Move the snake in the current direction
        x, y = self.body[0]
        if self.direction == "RIGHT":
            x += self.speed
        elif self.direction == "LEFT":
            x -= self.speed
        elif self.direction == "UP":
            y -= self.speed
        elif self.direction == "DOWN":
            y += self.speed

        # Update the snake's body
        self.body.pop()
        self.body.insert(0, (x, y))

        # Check if the snake has a pending growth
        if self.grow_pending > 0:
            self.grow_pending -= 1
            self.body.append(self.body[-1])

    def draw(self, screen):
        # Draw the snake on the screen
        for segment in self.body:
            pygame.draw.rect(screen, WHITE, (segment[0], segment[1], self.size, self.size))

    def change_direction(self, action):
        # Change the snake's direction
        index = CLOCK_WISE.index(self.direction)
        new_dir = None
        if np.array_equal(action,[1,0,0]):
            new_dir = CLOCK_WISE[index]
        elif np.array_equal(action,[0,1,0]):
            next_idx = (index + 1) % 4
            new_dir = CLOCK_WISE[next_idx]
        else:
            next_idx = (index - 1) % 4
            new_dir = CLOCK_WISE[next_idx]
        self.direction = new_dir
    
    def grow(self):
        # Increase the size of the snake
        self.grow_pending += 1
    
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = "RIGHT"
        self.body = [(self.x, self.y), (self.x-self.size, self.y)]
        self.grow_pending = 0
