
# Snake AI

# Overview
Snake AI is a deep reinforcement learning project that trains an AI agent to play the classic Snake game. The goal of the project is to demonstrate the ability of reinforcement learning algorithms to learn from experience and adapt to changing environments. Our trained AI agent was able to achieve a high score in the game, demonstrating its ability to learn from experience and adapt to changing environments.

# Requirements
To run this project, you will need the following:

Python 3.6 or higher
Pygame
TensorFlow 2.0 or higher
NumPy
Matplotlib

# Approach
We used a deep Q-learning approach to train our AI agent. The agent receives the current game state as input and outputs an action. The model was trained using experience replay to reduce correlations between consecutive updates and stabilize the learning process. We also used an epsilon-greedy exploration strategy to encourage the agent to explore new actions. Our approach is based on state-of-the-art reinforcement learning techniques, and we fine-tuned the model for optimal performance.

# Dataset
We used the visual input from the Snake game as our dataset. The game environment provides the agent with the current game state, which includes the positions of the snake and the food, as well as other relevant information about the game. We preprocessed the visual input and used it as the input to our neural network.

# Results
Our trained AI agent was able to achieve a high score in the game, demonstrating its ability to learn from experience and adapt to changing environments. We experimented with different hyperparameters and analyzed their effect on the model's performance. Our approach achieves state-of-the-art results on the Snake game.
![2023_03_11_063429_-_Trim_AdobeExpress_AdobeExpress](https://user-images.githubusercontent.com/102887305/227445595-cc5d4f74-526a-48ff-be50-9eba0e81c371.gif)
![vlcsnap-2023-03-24-08h02m35s029](https://user-images.githubusercontent.com/102887305/227445623-a5795bcf-2016-453c-9b1d-5a9184e3f685.png)
