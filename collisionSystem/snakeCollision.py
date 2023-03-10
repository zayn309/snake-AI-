from .CollisionDetector import CollisionDetector
from GameComponents.Snake import Snake
from GameComponents.Food import Food
class snakeCollision(CollisionDetector): # three collisions to be considered the snake with (food,wall, body)
    def __init__(self, snake: Snake,food:Food, width: int = 0, height: int = 0):
        super().__init__(snake,food,width,height)
        
    def snake_food_collision(self) -> bool:
        if self.snake.head.colliderect(self.food.get_rect()):
            return True
        
    def snake_wall_collision(self) -> bool:
        head = self.snake.head
        return head.x < 0 or head.x + self.snake.size > self.width or head.y < 0 or head.y + self.snake.size > self.height

    def snake_body_collision(self) -> bool:
        
        for segment in self.snake.body_segments:
            if self.snake.head.colliderect(segment):
                return True
        return False
