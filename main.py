
import pygame
from model import Linear_QNet
import torch
from GameComponents.Game import Game
from GameComponents.const import *

pygame.init()

def get_move(game,model):
    final_move = [0,0,0]
    input = game.Sensors.get_neuralNetwork_input()
    input_tensor = torch.tensor(input, dtype=torch.float)
    prediction = model(input_tensor)
    move = torch.argmax(prediction).item()
    final_move[move] = 1
    return final_move

def handle_event():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def test_model(model_path):
    game = Game(WIDTH, LENGHT, 20)
    model = Linear_QNet(11, 256, 3)
    model.load_state_dict(torch.load(model_path))
    
    
    while True:
        
        handle_event()
        
        action = get_move(game,model)
        
        game.snake.change_direction(action)
        
        game.snake.move()
        
        lost = game.check_snake_body_collision() or game.check_snake_wall_collision()
        
        game.check_snake_food_collision()
        
        if lost:
            game.game_over()
            
        # Draw the game
        game.draw(
            draw_sensor=True,
            )
        game.clock.tick(game.fps)
        pygame.display.update()
        
if __name__ == '__main__':
    test_model('model.pth')