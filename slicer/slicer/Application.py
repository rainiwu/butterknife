from DQN import Agent
from Environment import Application_env
import time
import numpy as np
import matplotlib.pyplot as plt
import zmq
import zmq.asyncio
import asyncio
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
        self.ID = []
        for i in range(self.app_size):
            self.QoE_matrix.append([])

        # Initialize ZMQ server
        self.context: zmq.asyncio.Context = zmq.asyncio.Context(1)
        self.socket: zmq.asyncio.Socket = self.context.socket(zmq.REQ)
        self.socket.connect(address)
        self.running = True

    async def get_dictionary(self):
        while self.running:
            await self.socket.send(b"GET qoedict")
            dictionary = await self.socket.recv_pyobj()
            print(len(dictionary))
            self.ID = []
            QoE_list = []
            if len(dictionary) != 0:
                for key in dictionary.keys():
                    self.ID.append(key)
                    QoE_list.append(dictionary[key])
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
            else:
                print("Received empty dictionary")
    
    async def send_priority(self):
        while self.running:
            #message = await self.socket.recv()
            continue
            #QoE_list = self.env.QoE_list


    def run(self):
        loop = asyncio.new_event_loop()
        loop.create_task(self.get_dictionary())
        #loop.create_task(self.send_priority())
        try:
            loop.run_forever()
        finally: 
            self.running = False

    def plot(self):
        x = [i+1 for i in range(self.times)]
        for i in range(self.app_size):
            plt.plot(x, self.QoE_matrix[i])
        plt.show()

c = control_server(2, 0.2, 64, "tcp://localhost:5556")
c.run()

