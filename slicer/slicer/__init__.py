import torch
import numpy as np
import DQN
import Environment
import Memory
INPUT_SIZE = 5
OUTPUT_SIZE = 5
LEARNING_RATE = 0.1
DISCOUNT_RATE = 0.95
NUM_EPISODES =  2000
def __init__():
    env = Environment(INPUT_SIZE)
    model = DQN(INPUT_SIZE, OUTPUT_SIZE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    loss_function = torch.nn.MSELoss()
    rewards = np.zeros([NUM_EPISODES])
    memory = Memory(10000)
    return env, model, optimizer, rewards, memory, loss_function