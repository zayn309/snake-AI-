# Snake AI — Deep Q-Learning

A Snake game built from scratch in Pygame, plus an agent that learns to play it using **Deep Q-Learning** (reinforcement learning) in PyTorch.

<p align="center">
  <img src="https://user-images.githubusercontent.com/102887305/227445771-33651827-1081-451b-9600-4355e598563b.gif" alt="Trained agent playing Snake"/>
</p>

## How it works

**State (11 features):** at every step the agent observes:
- Danger straight ahead, to the right, and to the left (3)
- The current direction of movement (4)
- Where the food is relative to the head: left, right, up, or down (4)

**Actions (3):** go straight, turn right, or turn left.

**Rewards:** +10 for eating food, +1 shaping bonus for heading towards the food, and −10 for dying or looping without progress (the episode times out after `100 × snake length` frames).

**Model:** a feed-forward Q-network (11 → 256 → 3) that predicts the expected future reward of each action.

**Training:**
- Bellman update: `Q_new = r + γ · max Q(s′)` with γ = 0.9
- **Experience replay:** past transitions are stored in a replay buffer and re-sampled in mini-batches, which reduces correlation between updates and stabilises learning.
- **ε-greedy exploration:** the agent starts mostly random and shifts towards exploiting what it has learned as games go on.
- Short-term training after every step, and long-term training on a replay batch after every game.

The score and the running mean score are plotted live during training.

<p align="center">
  <img src="https://user-images.githubusercontent.com/102887305/227445623-a5795bcf-2016-453c-9b1d-5a9184e3f685.png" alt="Training progress"/>
</p>

## Project structure

```
├── agent.py            # DQN agent: state, memory, ε-greedy policy, training loop
├── model.py            # Linear_QNet and QTrainer
├── test.py             # Watch a trained model play
├── helper.py           # Live training plot
├── GameComponents/     # Game, Snake, Food, sensors, constants
├── collisionSystem/    # Collision detection
├── score/              # Score tracking
└── model.pth           # Trained weights
```

## Getting started

```bash
pip install -r requirements.txt
python agent.py      # train a new agent
python test.py       # watch the trained model play
```

## Limitations and next steps

- The 11-feature state can't see the snake's whole body, so long snakes can trap themselves. A grid- or image-based state with a CNN would fix this.
- Possible improvements include Double DQN, a target network, and prioritised replay.

## License

[MIT](LICENSE)
