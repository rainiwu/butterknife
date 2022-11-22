import numpy as np
import matplotlib.pyplot as plt

class Application_env(object):
    def __init__(self, app_size, lr, batch_size):
        # Initialize QoE and priority_list list
        self.app_size = app_size
        self.batch_size = batch_size
        self.QoE_list = np.ones(app_size)
        self.priority_list = np.ones(app_size)
        self.priority_list /= np.sum(self.priority_list)
        self.previous_reward = 0
        self.previous_QoE_list = np.ones(app_size)
        # Initialize state space
        self.state_space = []
        for i in range(app_size):
            self.state_space.append(i)
        
        # Initialize action space
        self.action_space = [lr, -lr] * app_size

    def step(self, action_num):
        # Convert/decode action into specific application and behavior
        action_index = action_num // 2
        print(self.priority_list)
        print(self.QoE_list)
        # update the priority list
        self.priority_list[action_index] += self.action_space[action_num]
        self.priority_list -= np.min(self.priority_list)
        self.priority_list /= np.sum(self.priority_list)
        
        self.previous_QoE_list = np.copy(self.QoE_list)
        # get new QoE list anc calculate reward
        self.calculate_QoE()
        reward = self.calculate_reward()
        self.previous_reward = reward
        print("Reward: %f" % reward)
        observation = np.zeros(self.app_size * 2)
        observation[action_num] = 0
        return observation, reward, True, None

    def reset(self):
        # reset QoE list
        self.QoE_list = np.ones(self.app_size)
        self.QoE_list /= np.sum(self.QoE_list)

        # reset action Index
        self.action_index = 0
        return np.zeros(self.app_size * 2)

    def calculate_QoE(self):
        # temporary QoE calculation
        self.previous_QoE_list = np.copy(self.QoE_list)
        for i in range(len(np.array(self.QoE_list))):
            self.QoE_list[i] += self.priority_list[i]
        #self.QoE_list /= np.sum(self.QoE_list)

    def calculate_reward(self):
        min_index = np.argmin(self.QoE_list)
        if (self.QoE_list[min_index] - self.previous_QoE_list[min_index]) > 0:
            reward = 1
        else:
            reward = -1
        return reward
    
        
        

