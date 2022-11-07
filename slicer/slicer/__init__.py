from collections import deque
import DQN
import torch
import numpy as np
import math
import random

#https://medium.com/analytics-vidhya/introduction-to-reinforcement-learning-rl-in-pytorch-c0862989cc0e
# Learning parameters
alpha = 0.1
gamma = 0.95
num_episodes = 2000
epsilon = 1.0
epsilon_min = 0.01
epsilon_log_decay = 0.995
alpha_decay = 0.01
n_episodes = 1000
n_win_ticks = 195
batch_size = 64
# array of reward for each episode
rs = np.zeros([num_episodes])

class Application():
    def __init__(self):
        # Set memory
        self.memory = deque(maxlen=100000)

        # Set model paramters
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_log_decay
        self.alpha = alpha
        self.alpha_decay = alpha_decay
        self.n_episodes = n_episodes
        self.n_win_ticks = n_win_ticks
        self.batch_size = batch_size

        # Initalize model
        self.dqn = DQN()
        self.crit = torch.nn.MSELoss()
        self.opt = torch.optim.Adam(self.dpn.parameters(), lr = 0.01)

def get_epsilon(self, t):
    # Calculate epsilon
    return max(self.epsilon_min, min(self.epsilon, 1.0 - math.log10((t + 1) * self.epsilon_decay)))

def preprocess_state(self, state):

    return torch.tensor(np.reshape(state, [1, 4]), dtype=torch.float32) 
    
def choose_action(self, state, epsilon):
    if (np.random.random() <= epsilon):
        return self.env.action_space.sample() 
    else:
        with torch.no_grad():
            return torch.argmax(self.dqn(state)).numpy()

def remember(self, state, action, reward, next_state, done):
    reward = torch.tensor(reward)
    self.memory.append((state, action, reward, next_state, done))
    
def replay(self, batch_size):
    y_batch, y_target_batch = [], []
    minibatch = random.sample(self.memory, min(len(self.memory), batch_size))
    for state, action, reward, next_state, done in minibatch:
        y = self.dqn(state)
        y_target = y.clone().detach()
        with torch.no_grad():
            y_target[0][action] = reward if done else reward + self.gamma * torch.max(self.dqn(next_state)[0])
        y_batch.append(y[0])
        y_target_batch.append(y_target[0])
        
    y_batch = torch.cat(y_batch)
    y_target_batch = torch.cat(y_target_batch)
        
    self.opt.zero_grad()
    loss = self.criterion(y_batch, y_target_batch)
    loss.backward()
    self.opt.step()        
        
    if self.epsilon > self.epsilon_min:
        self.epsilon *= self.epsilon_decay    