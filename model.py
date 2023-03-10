import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os


class Linear_QNet(nn.Module):
    """
    A neural network model with two linear layers, using ReLU activation function.
    """
    def __init__(self, input_size, hidden_size, output_size):
        """
        Initialize the linear layers with specified input, hidden, and output sizes.

        Args:
            input_size (int): Size of the input layer.
            hidden_size (int): Size of the hidden layer.
            output_size (int): Size of the output layer.
        """
        super().__init__()
        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, hidden_size//2)
        self.linear3 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        """
        Performs forward propagation on the input data x through the two linear layers.

        Args:
            x (tensor): Input tensor of shape (batch_size, input_size).

        Returns:
            tensor: Output tensor of shape (batch_size, output_size).
        """
        x = F.relu(self.linear1(x))
        x = F.relu(self.linear2(x))
        x = self.linear3(x)
        return x

    def save(self, file_name='model.pth'):
        """
        Saves the model's state dictionary to a file with the specified name.

        Args:
            file_name (str): Name of the file to save the state dictionary to.
                Defaults to 'model.pth'.
        """
        model_folder_path = './model'
        if not os.path.exists(model_folder_path):
            os.makedirs(model_folder_path)

        file_name = os.path.join(model_folder_path, file_name)
        torch.save(self.state_dict(), file_name)


class QTrainer:
    """
    A class to handle training of a Q-learning model using PyTorch.
    """
    def __init__(self, model, lr, gamma):
        """
        Initializes the QTrainer with the specified model, learning rate, and discount factor.

        Args:
            model (nn.Module): The Q-learning model to train.
            lr (float): Learning rate for the optimizer.
            gamma (float): Discount factor for future rewards.
        """
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        """
        Performs a single training step for the Q-learning model.

        Args:
            state (ndarray): The current state of the environment.
            action (ndarray): The action taken in the current state.
            reward (float): The reward received from the environment.
            next_state (ndarray): The next state of the environment.
            done (bool): Whether the episode has ended.

        Returns:
            None
        """
        state = torch.tensor(state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))

            target[idx][torch.argmax(action[idx]).item()] = Q_new
    
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
        self.criterion = nn.MSELoss()