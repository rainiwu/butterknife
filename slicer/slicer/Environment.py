import numpy as np
import matplotlib.pyplot as plt

class Application_env(object):
    def __init__(self, app_size, lr):
        # Initialize QoE and priority_list list
        self.app_size = app_size
        self.QoE_list = np.ones(app_size)
        self.priority_list = np.ones(app_size)
        self.priority_list /= np.sum(self.priority_list)

        # Initialize state space
        self.state_space = []
        for i in range(app_size):
            self.state_space.append(i)
        
        # Initialize action space
        self.action_space = {'INC': lr, 'DEC': -lr}
        self.possible_actions = ['INC', 'DEC']
        self.action_index = 0
    
    def step(self, action_num):
        # Convert/decode action into specific application and behavior
        action_index = action_num / 2
        if action_num % 2 == 0:
            action = 'INC'
        else:
            action = 'DEC'

        # update the priority list
        self.priority_list[action_index] = self.priority_list[action_index] + self.action_space[action]
        self.priority_list /= np.sum(self.QoE_list)

        # get new QoE list anc calculate reward
        prev_QoE_list_reward = np.mean(self.QoE_list) + 0.5 * np.var(self.QoE_list)
        self.calculate_QoE()
        reward = np.mean(self.QoE_list) + 0.5 * np.var(self.QoE_list) - prev_QoE_list_reward

        return self.priority_list, reward, True, None

    def reset(self):
        # reset QoE list
        self.QoE_list = np.ones(self.QoE_list_size)
        self.QoE_list /= np.sum(self.QoE_list)

        # reset action Index
        self.action_index = 0
        return self.priority_list

    def calculate_QoE(self):
        # temporary QoE calculation
        raw_data = np.multiply(self.QoE_list, self.priority_list)
        return raw_data/np.sum(raw_data)
    
        
        

