from DQN import Agent
from Environment import Application_env
import numpy as np

if __name__ == '__main__':
    # Parameters
    APP_SIZE = 3
    LEARNING_RATE = 0.1

    # Initialize environment and agent
    env = Application_env(app_size=APP_SIZE, lr=LEARNING_RATE)
    agent = Agent(gamma=0.99, epsilon=1.0, batch_size=64, n_actions=4,
            eps_end=0.01, input_dims=[8], lr=0.003)
    scores, eps_history = [], []

    times = 500
    for i in range(times):
        score = 0
        done = False
        observation = env.reset()
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

        print('epsilon ', i, 'score %.2f' % score, 'average score %.2f' % avg_score, 'epsilon %.2f' % agent.epsilon)
    x = [i+1 for i in range(times)]