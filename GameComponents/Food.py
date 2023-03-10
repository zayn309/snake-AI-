import pygame
import random

class Food:
    def __init__(self, x_range, y_range, size, color,snake):
        self.x_range = x_range
        self.y_range = y_range
        self.size = size
        self.color = color
        self.snake = snake
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self.spawn()

    def spawn(self):
        # Get a list of all available positions that are divisible by 10
        available_positions = [pygame.Rect(x, y, self.size, self.size)
                                for x in range(0, self.x_range, 10) 
                                for y in range(0, self.y_range, 10)
                                if not any(segment.colliderect(pygame.Rect(x, y, self.size, self.size)) for segment in self.snake.body_segments)]

        # Choose a random position from the available positions
        if available_positions:
            self.rect = random.choice(available_positions)
        else:
            # If there are no available positions, spawn at a random location
            x = random.randint(0, self.x_range)
            y = random.randint(0, self.y_range)
            self.rect = pygame.Rect(x, y, self.size, self.size)

    def draw(self, screen):
        # Draw the food on the screen
        pygame.draw.rect(screen, self.color, self.rect)

    def get_rect(self):
        # Get the Rect object representing the food
        return self.rect
