
# Snake AI

# Overview
Snake AI is a deep reinforcement learning project that trains an AI agent to play the classic Snake game. The goal of the project is to demonstrate the ability of reinforcement learning algorithms to learn from experience and adapt to changing environments. Our trained AI agent was able to achieve a high score in the game, demonstrating its ability to learn from experience and adapt to changing environments.

# Requirements
To run this project, you will need Python 3.6 or higher and to get the required modules navigate to the directory where the project is and run the command "pip install -r requirements.txt"

# Approach
We used a deep Q-learning approach to train our AI agent. The agent receives the current game state as input and outputs an action. The model was trained using experience replay to reduce correlations between consecutive updates and stabilize the learning process. We also used an epsilon-greedy exploration strategy to encourage the agent to explore new actions. Our approach is based on state-of-the-art reinforcement learning techniques, and we fine-tuned the model for optimal performance.

# Dataset
We used the visual input from the Snake game as our dataset. The game environment provides the agent with the current game state, which includes the positions of the snake and the food, as well as other relevant information about the game. We preprocessed the visual input and used it as the input to our neural network.

# Results
Our trained AI agent was able to achieve a high score in the game, demonstrating its ability to learn from experience and adapt to changing environments. We experimented with different hyperparameters and analyzed their effect on the model's performance. Our approach achieves state-of-the-art results on the Snake game.
<p align="center">
  <img src="https://user-images.githubusercontent.com/102887305/227445771-33651827-1081-451b-9600-4355e598563b.gif" alt="Sublime's custom image"/>
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/102887305/227445623-a5795bcf-2016-453c-9b1d-5a9184e3f685.png" alt="Sublime's custom image"/>
</p>

# Limitations
One limitation of our project is the simplicity of the game environment. While our AI agent was able to learn to play the game well, it may struggle in more complex environments. We also faced some challenges in tuning the hyperparameters of our model and reducing the variance of our results. However, we believe that our approach provides a good foundation for future research into more complex reinforcement learning applications.

# Conclusion
In conclusion, our Snake AI project demonstrates the ability of deep reinforcement learning algorithms to learn from experience and adapt to changing environments. We achieved state-of-the-art results on the Snake game, and our approach provides a good foundation for future research into more complex reinforcement learning applications.
