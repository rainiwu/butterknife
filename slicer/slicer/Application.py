from DQN import Agent
from Environment import Application_env
import time
import numpy as np
import matplotlib.pyplot as plt
import zmq
import zmq.asyncio
class control_server:
    def __init__(self, APP_SIZE: int = 2, LEARNING_RATE: float = 0.2, 
                    BATCH_SIZE: int = 64, address: str = "tcp://localhost:5556") -> None:
        self.app_size = APP_SIZE
        self.learning_rate = LEARNING_RATE
        self.batch_size = BATCH_SIZE
        # Initialize environment and agent
        self.env = Application_env(app_size=APP_SIZE, lr=0.1, batch_size=BATCH_SIZE)
        self.agent = Agent(gamma=0.99, epsilon=1, batch_size=BATCH_SIZE, n_actions=APP_SIZE * 2,
            eps_end=0.01, input_dims=[APP_SIZE * 2], lr=0.003)
        self.scores = []
        self.eps_history = []
        self.times = 0
        self.observation = self.env.reset()
        self.QoE_matrix = [[]]
        for i in range(self.app_size):
            self.QoE_matrix.append([])

        # Initialize ZMQ server
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        #self.context: zmq.asyncio.Context = zmq.asyncio.Context(1)
        #self.socket: zmq.asyncio.Socket = self.context.socket(zmq.REQ)
        self.socket.connect(address)

    def get_dictionary(self, QoE_list):
        self.socket.send(b"GET qoedict")
        dictionary = self.socket.recv_pyobj()
        print(dictionary)
        score = 0
        action = self.agent.choose_action(self.observation)
        observation_, reward, done, info = self.env.step(action, QoE_list)
        for i in range(self.app_size):
            self.QoE_matrix[i].append(self.env.QoE_list[i])
        score += reward
        self.agent.store_transition(self.observation, action, reward, observation_, done)
        self.agent.learn()
        self.observation = observation_
        self.eps_history.append(self.agent.epsilon)
        self.times += 1
        avg_score = np.mean(self.agent.epsilon)
        return self.env.priority_list
    
    def plot(self):
        x = [i+1 for i in range(self.times)]
        for i in range(self.app_size):
            plt.plot(x, self.QoE_matrix[i])
        plt.show()

c = control_server(2, 0.2, 64, "tcp://localhost:5556")
c.get_dictionary([1, 1])

