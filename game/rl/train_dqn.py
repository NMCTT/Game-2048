import torch
from game.core.env_2048 import Game2048Env
from game.rl.agent_dqn import DQNAgent

num_episodes = 20000
update_target_every = 50  # episode

env = Game2048Env()
agent = DQNAgent()

for episode in range(num_episodes):
    state = env.reset()
    total_reward = 0

    done = False
    while not done:
        action = agent.select_action(state)
        next_state, reward, done, _ = env.step(action)
        agent.memory.push(state, action, reward, next_state, done)
        agent.train_step()
        state = next_state
        total_reward += reward

    print(f"Episode: {episode}")

    if episode % update_target_every == 0:
        agent.update_target_net()

    if episode % 3 == 0:
        print(f"Episode {episode}, Total reward: {total_reward}, Epsilon: {agent.epsilon:.3f}")

# Save trained model
torch.save(agent.policy_net.state_dict(), "dqn_2048.pth")
