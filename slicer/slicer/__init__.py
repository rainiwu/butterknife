import gym
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as T
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
def __init__():
    if gym.__version__ < '0.26':
        env = gym.make('CartPole-v0', new_step_api=True, render_mode='single_rgb_array').unwrapped
    else:
        env = gym.make('CartPole-v0', render_mode='rgb_array').unwrapped
    # set up matplotlib
    is_ipython = 'inline' in matplotlib.get_backend()
    if is_ipython:
        from IPython import display

    plt.ion()
    # if gpu is to be used
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return env, device