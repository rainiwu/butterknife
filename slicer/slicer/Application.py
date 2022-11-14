
from __init__ import __init__
import matplotlib as plt
import Memory
import torch
import torch.optim as optim
import torch.nn as nn
import numpy as np
import DQN
from __init__ import NUM_EPISODES, LEARNING_RATE, DISCOUNT_RATE
env, model, optimizer, rewards, memory, loss_function= __init__()
steps_done = 0
Q = np.zeros([env.observation_space.shape, env.action_space.shape])
for i in range (NUM_EPISODES):
    rewards_sum_i = 0
    t = 0
    done = False
    s = env.reset()
    while not done:
        a = np.argmax(Q[s, :])
        s1, reward, done, _ = env.step(a)
        # Update Q table
        Q[s, a] = (1 - LEARNING_RATE) * Q[s, a] + \
            LEARNING_RATE * (reward + DISCOUNT_RATE * np.max(Q[s1, :]))
        # Update cummulative rewards
        rewards_sum_i += reward * DISCOUNT_RATE ** t
        s = s1
        t += 1
    rewards[i] = rewards_sum_i
