from DQN import Agent
from Environment import Application_env
import numpy as np

if __name__ == '__main__':
    # Parameters
    APP_SIZE = 10
    LEARNING_RATE = 0.2
    BATCH_SIZE = 64

    # Initialize environment and agent
    env = Application_env(app_size=APP_SIZE, lr=0.5/APP_SIZE, batch_size=BATCH_SIZE)
    agent = Agent(gamma=0.99, epsilon=1, batch_size=BATCH_SIZE, n_actions=APP_SIZE*2,
            eps_end=0.01, input_dims=[APP_SIZE * 2], lr=0.003)
    scores, eps_history = [], []

    times = 50000
    observation = env.reset()
    for i in range(times):
        score = 0
        done = False
        while not done:
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.store_transition(observation, action, reward, observation_, done)
            agent.learn()
            observation = observation_
        scores.append(score)
        eps_history.append(agent.epsilon)

        avg_score = np.mean(scores[-100:])
        print(i, 'score %.2f' % score, 'average score %.2f' % avg_score, 'epsilon %.2f' % agent.epsilon)
    x = [i+1 for i in range(times)]