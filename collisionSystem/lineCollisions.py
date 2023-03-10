from .CollisionDetector import CollisionDetector
from GameComponents.Snake import Snake
from GameComponents.Food import Food

class lineCollision(CollisionDetector):
    def __init__(self,snake: Snake,food:Food, width: int = 0, height: int = 0):
        super().__init__(snake,food,width,height)

    def line_food_collision(self,x: int,y : int) -> bool :
        return self.food.get_rect().collidepoint(x, y)
    
    def line_body_collision(self, x: int, y: int) -> bool:
        """
        Returns True if the line passing through the point (x, y) intersects with
        the snake's body.
        """
        # Check if the point is inside the snake's body
        for segment in self.snake.body_segments:
            if segment.collidepoint(x, y):
                return True
        
        # If no collision was found, return False
        return False
    
    def line_wall_danger(self, x, y,screen):
        if x <= 0 or x>= screen.get_width() or y <= 0 or y >= screen.get_height():
            return True
        return False
            