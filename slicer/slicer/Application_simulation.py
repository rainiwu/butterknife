from DQN import Agent
from Environment import Application_env
import time
import numpy as np
import matplotlib.pyplot as plt
import zmq
import zmq.asyncio
import asyncio
from client_simulation import client_simulation
RUN_MODEL = True
class rl_control_server_simulation:
    def __init__(self, LEARNING_RATE: float = 0.2, 
                    BATCH_SIZE: int = 64):
        self.running = True
        self.app_size = 4

        # Initialize environment and agent
        self.learning_rate = LEARNING_RATE
        self.batch_size = BATCH_SIZE
        self.env = Application_env(app_size=self.app_size, lr=0.1, batch_size=BATCH_SIZE)
        self.agent = Agent(gamma=0.99, epsilon=1, batch_size=BATCH_SIZE, n_actions=self.app_size * 2,
            eps_end=0.01, input_dims=[self.app_size * 2], lr=0.003)
        self.scores = []
        self.eps_history = []
        self.times = 0
        self.observation = self.env.reset()
        self.QoE_matrix = [[]]
        self.ID = ["70", "71", "72", "73"]
        self.buffer = [[]]
        self.index_counter = 0
        self.fill_counter = 0
        for i in range(self.app_size):
            self.QoE_matrix.append([])
        self.begin_time = time.time()
        # 70: High throughput buffered
        self.id_70 = client_simulation(True, 0.008)
        # 71: Low throughput buffered
        self.id_71 = client_simulation(True, 0.016)
        # 72: High throughput unbuffered
        self.id_72 = client_simulation(False, 0.008)
        # 73: Low throughput unbuffered
        self.id_73 = client_simulation(False, 0.016)
        self.runtime = 200000

    def get_dictionary(self):
        for j in range(self.runtime):
            QoE_list = self.simulation()
            score = 0
            action = self.agent.choose_action(self.observation)
            observation_, reward, done, info = self.env.step(action, np.asarray(QoE_list))
            for i in range(self.app_size):
                self.QoE_matrix[i].append(self.env.QoE_list[i])
            score += reward
            self.agent.store_transition(self.observation, action, reward, observation_, done)
            self.agent.learn()
            self.observation = observation_
            self.eps_history.append(self.agent.epsilon)
            self.times += 1
            
    def run(self):
        self.get_dictionary()

    def simulation(self):
        if self.fill_counter == 2:
            if RUN_MODEL:
                result = self.ID[np.argmax(self.env.priority_list)]
            else:
                result = self.ID[self.index_counter]
            self.index_counter = (self.index_counter + 1) % self.app_size
            if result == self.ID[0]:
                self.id_70.fill_buffer()
            elif result == self.ID[1]:
                self.id_71.fill_buffer()
            elif result == self.ID[2]:
                self.id_72.fill_buffer()
            elif result == self.ID[3]:
                self.id_73.fill_buffer()
        self.fill_counter = (self.fill_counter + 1) % 3
        self.id_70.consume_buffer()
        self.id_71.consume_buffer()
        self.id_72.consume_buffer()
        self.id_73.consume_buffer()
        QoE_list = []
        QoE_list.append(self.id_70.calculate_QoE())
        QoE_list.append(self.id_71.calculate_QoE())
        QoE_list.append(self.id_72.calculate_QoE())
        QoE_list.append(self.id_73.calculate_QoE())
        #print(QoE_list)
        return QoE_list
        
    def plot(self):
        x = [i+1 for i in range(self.runtime)]
        labels = ["High throughput buffered", "Low throughput buffered", "High throughput unbuffered", "Low throughput unbuffered"]
        for i in range(self.app_size):
            plt.plot(x[100:], self.QoE_matrix[i][100:], label=labels[i])
        plt.legend(loc="upper right")
        if RUN_MODEL:
            plt.title("Reinforcement Learning for Scheduling")
        else:
            plt.title("Round Robin Scheduling")
        plt.xlabel("Scenes")
        plt.ylabel("QoE")
        plt.show()

c = rl_control_server_simulation(0.2, 64)
c.run()
c.plot()

