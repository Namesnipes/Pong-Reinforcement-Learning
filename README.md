# Pong-Reinforcement-Learning
This is a simple implementation of Pong game using Pygame and Reinforcement Learning.

# What it does
The game has two paddles, one controlled by the computer (Right paddle) and the other by the reinforcement learning algorithm (Left paddle). The goal of the algorithm is to learn to control the paddle to keep the ball from hitting the player's side and maximize the score. The reinforcement learning algorithm uses a Q-learning algorithm to update the Q-values of the state-action pairs, which is stored in a Q-table. The state is represented by the positions of the ball and the paddles, and the actions are moving the paddle up, staying put, or moving the paddle down.

The Q-learning algorithm updates the Q-values based on the rewards obtained by the agent after taking an action in a state and moving to the next state. The algorithm chooses the action with the highest Q-value in the current state, takes the action, and then updates the Q-value of the state-action pair with the reward received and the highest Q-value in the new state. The agent repeats this process until it reaches the end of the episode.

# Requirements
```
python 3.9
pygame
```

# Usage
To use this program, cd into the folder and simply run the main.py file or run the file in a Python environment. By default, you will be presented with a pre-trained AI model (left) and a basic paddle that always follows the ball (right). 
- To take control press "q" and use "w" and "s" to move the paddle up and down. 
- For fast training press "R", this will disable rendering and speed up the training process significantly, press "P" to resume rendering the game at normal speed.
- Press "B" to save the current model to a file, you can disable loading the model from a file by commenting out the `load_q_table()` line in main.py
```
$ git clone https://github.com/matriley/Pong-Reinforcement-Learning.git
$ python3 train.py
```

# How it works
The game is implemented using Q-Learning algorithm. The Q-table is initialized with random values, and is updated every time the ball is hit. The state is represented by a tuple of five variables: ball x-coordinate, ball y-coordinate, paddle 1 y-coordinate, paddle 2 y-coordinate, and ball direction (dx and dy).

The reward is calculated as the difference between the scores of the two players, and is used to update the Q-table using the following formula:
```
Q(s, a) += alpha * (reward + gamma * max(Q(s', a')) - Q(s, a))
```
Where s is the current state, a is the action taken, s' is the new state after taking the action, alpha is the learning rate, and gamma is the discount factor.
