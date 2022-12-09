from DQN import Agent
from Environment import Application_env
import time
import numpy as np
import matplotlib.pyplot as plt
import zmq
import zmq.asyncio
import asyncio
class rl_control_server:
    def __init__(self, LEARNING_RATE: float = 0.2, 
                    BATCH_SIZE: int = 64, 
                    sl_address: str = "tcp://localhost:5556",
                    sr_address: str = "tcp://*:5557"):
        # Initialize ZMQ server
        self.context: zmq.asyncio.Context = zmq.asyncio.Context(1)
        self.socket_sl: zmq.asyncio.Socket = self.context.socket(zmq.REQ)
        self.socket_sr: zmq.asyncio.Socket = self.context.socket(zmq.REP)
        self.socket_sl.connect(sl_address)
        self.socket_sr.bind(sr_address)
        self.running = True
        self.counter_plot = 0
        # Request for number of clients
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.get_num_of_clients())
        loop.close()

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
        self.ID = []
        for i in range(self.app_size):
            self.QoE_matrix.append([])

    async def get_num_of_clients(self):
        # Request for number of clients
        msg = "-1"
        while msg == "-1":
            self.socket_sl.send(b"GET quantity")
            msg = await self.socket_sl.recv_string()
            if (msg != "-1"):
                self.app_size = len(msg)

    async def get_dictionary(self):
        while self.running:
            await self.socket_sl.send(b"GET qoedict")
            print("QoE request sent")
            dictionary = await self.socket_sl.recv_pyobj()
            print(dictionary)
            self.ID = []
            QoE_list = []
            if len(dictionary) != 0:
                for key in dictionary.keys():
                    self.ID.append(key)
                    QoE_list.append(float(dictionary[key]))
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
                self.counter_plot += 1
                if self.counter_plot == 5000:
                    self.counter_plot = 0
                    self.plot()
            else:
                print("Received empty dictionary")
    
    async def send_priority(self):
        while self.running:
            message = await self.socket_sr.recv_string()
            if message == "GET priority":
                result = self.ID[np.argmax(self.env.priority_list)]
                await self.socket_sr.send_string(result)
            else:
                await self.socket_sr.send_string("Unrecognize request")
            
    def run(self):
        loop = asyncio.new_event_loop()
        loop.create_task(self.get_dictionary())
        loop.create_task(self.send_priority())
        try:
            loop.run_forever()
        finally: 
            self.running = False

    def plot(self):
        x = [i+1 for i in range(self.times)]
        for i in range(self.app_size):
            plt.plot(x[100:], self.QoE_matrix[i][100:], label=self.ID[i])
        plt.legend(loc="upper right")
        plt.title("Reinforcement Learning for Scheduling")
        plt.xlabel("Scenes")
        plt.ylabel("QoE")
        plt.savefig('RL_result.png')

c = rl_control_server(0.2, 64, "tcp://localhost:5556", "tcp://*:5557")
c.run()

