import gym
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

MLP_FC1 = 4
MLP_FC2 = 24
MLP_FC3 = 48
MLP_FC4 = 2 

#https://medium.com/analytics-vidhya/introduction-to-reinforcement-learning-rl-in-pytorch-c0862989cc0e
class DQN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(MLP_FC1, MLP_FC2)
        self.fc2 = nn.Linear(MLP_FC2, MLP_FC3)
        self.fc3 = nn.Linear(MLP_FC3, MLP_FC4)

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.fc2(x)
        x = F.relu(x)
        x = self.fc3(x)
        return x 
