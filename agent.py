import numpy as np
import pickle

class QLearningAgent:
    def __init__(self, state_space_sizes: list, action_space_size: int, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        #state_space_sizes should be a list of integers coresponding to the size of each state eg. [7, 401, 2]
        #action_space_size should be an integer corresponding to how many actions there are
        self.state_space_size = state_space_sizes
        self.action_space_size = action_space_size
        self.learning_rate = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.q_table = np.random.rand(*self.state_space_size, self.action_space_size)

    def get_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            action = np.random.randint(self.action_space_size)
        else:
            action = np.argmax(self.q_table[*state])
        return action

    def update_q_table(self, state, action, reward, next_state):
        self.q_table[*state][action] = self.q_table[*state][action] + self.learning_rate * (reward + self.gamma * np.amax(self.q_table[*next_state]) - self.q_table[*state][action])

    def save_q_table(self):
        with open('q_table.pkl', 'wb') as f:
            print("Saved")
            pickle.dump(self.q_table, f)
    
    def load_q_table(self):
        with open('q_table.pkl', 'rb') as f:
            self.q_table = pickle.load(f)
            print("Loaded")