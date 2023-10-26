from game import PongGame
from agent import QLearningAgent
import numpy as np
from helper import plot
import random

game = PongGame()
agent = QLearningAgent([7,401,2], 3)

agent.load_q_table()
agent.epsilon = 0.000001

episode_rewards = []
mean_rewards = []
games = 0
totalest_reward = 0
score = 0
highest_reward = -10

state = game.get_state()
while True:
    score = 0
    while not game.died:
        score = game.get_score()
        action = agent.get_action(state)
        game.update_game_state(action) 
        reward = game.get_reward() 
        next_state = game.get_state()
        agent.update_q_table(state, action, reward, next_state)
        state = next_state
        game.render()
    games += 1
    #agent.epsilon *= 0.999
    if(reward > highest_reward):
        highest_reward = reward
        #agent.save_q_table()
    totalest_reward += score
    episode_rewards.append(score)
    this_mean = totalest_reward / games
    print(f"Mean reward: {this_mean}")
    mean_rewards.append(this_mean)
    #plot(episode_rewards, mean_rewards)
    game.died = False