import random
from collections import deque
import pygame
import torch
from GameComponents.Game import Game

from GameComponents.const import *

from helper import plot

from model import QTrainer, Linear_QNet


class Agent:
    """
    This class defines the Agent, which is the player in the game. It makes decisions based on the current state of the game,
    and trains its neural network model to improve its decision-making over time.

    Attributes:
    - n_games (int): The number of games played by the agent.
    - epsilon (float): The randomness factor used in decision-making.
    - gamma (float): The discount rate used in calculating future rewards.
    - memory (deque): A deque data structure used to store the agent's experiences.
    - model (Linear_QNet): A neural network model used to make decisions.
    - trainer (QTrainer): A trainer object used to train the model.
    """

    def __init__(self):
        """
        Initializes a new Agent object with default values.
        """
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self,game):
        """
        Returns the current state of the game as a neural network input.

        Args:
        - game (Game): The current game object.

        Returns:
        - state (np-array): The current state of the game as a np-array.
        """
        return game.Sensors.get_neuralNetwork_input()
    
    def remember(self, state, action, reward, next_state, done):
        """
        Adds the agent's experience to its memory.

        Args:
        - state (torch.tensor): The current state of the game as a tensor.
        - action (int): The action taken by the agent.
        - reward (int): The reward received by the agent.
        - next_state (torch.tensor): The next state of the game as a tensor.
        - done (bool): Whether or not the game is over.
        """
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        """
        Trains the agent's neural network model using experiences stored in its memory.
        """
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        """
        Trains the agent's neural network model using a single experience.

        Args:
        - state (np-array): The current state of the game as a tensor.
        - action (int): The action taken by the agent.
        - reward (int): The reward received by the agent.
        - next_state (np-array): The next state of the game as a tensor.
        - done (bool): Whether or not the game is over.
        """
        self.trainer.train_step(state, action, reward, next_state, done)
        
    def get_action(self, state):
        """
        Choose an action to take based on the current state of the game and the agent's policy.

        Parameters:
            state (np-array): The current state of the game.

        Returns:
            array: A one-hot encoded array representing the agent's chosen action.
        """
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]

        # With probability epsilon, take a random action
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
        # Otherwise, choose the action with the highest Q-value according to the agent's model
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move
    
    def play_step(self,game, action):
        game.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        game.snake.change_direction(action)
        # 2. move
        reward = 0
        
        # if the snake started to go for the food
        if (game.Sensors.get_neuralNetwork_input()[-4:] == True ).sum() == 1:
            reward += 1
            
        game.snake.move()
        # check if the sanke ate food to give positive reward so it identify that it's a good move
        if game.check_snake_food_collision():
            reward += 10
        
        # 3. check if game over
        game_over = False
        lost = game.check_snake_wall_collision() or game.check_snake_body_collision()
        if lost or game.frame_iteration > 100*len(game.snake.body):
            game_over = True
            reward -= 10
            self.n_games += 1
        
        # 5. update ui and clock
        game.draw(draw_sensor=True)
        
        game.clock.tick(game.fps)
        
        return reward, game_over, game.score.value


def train():
    plot_scores = []  # List to store scores for plotting
    plot_mean_scores = []  # List to store mean scores for plotting
    total_score = 0  # Variable to store total score
    record = 0  # Variable to store highest score
    agent = Agent()  # Initialize the agent object
    game = Game(WIDTH, LENGHT,20)  # Initialize the game object

    while True:
        # Get the current state of the game
        state_old = agent.get_state(game)

        # Get the next move from the agent
        final_move = agent.get_action(state_old)

        # Perform the move and get the new state, reward, and done status
        reward, done, score = agent.play_step(game,final_move)
        
        state_new = agent.get_state(game)

        # Train the agent on the short-term memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # Add the experience to the agent's memory
        agent.remember(state_old, final_move, reward, state_new, done)

        pygame.display.update()

        if done:
            # Train the agent on the long-term memory, plot the results
            game.game_over()
            agent.n_games += 1
            agent.train_long_memory()

            # Update the record if the score is higher
            if score > record:
                record = score
                agent.model.save()

            # Print game information and plot the scores
            print('Game', agent.n_games, 'Score', score, 'Record:', record)
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()