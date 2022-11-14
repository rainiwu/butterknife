from Application import INPUT_SIZE, OUTPUT_SIZE
import numpy as np
class Environment:
    def __init__(self):
        self.QoE_list = np.zeros([INPUT_SIZE])
        self.action_space = np.zeros([INPUT_SIZE])
        self.observation_space = np.zeros([INPUT_SIZE])
    def step():
        # TODO:  Need to implement
        state = None
        reward = None
        done = None
        return state, reward, done
    def reset():
        # TODO: Need to implement
        return None