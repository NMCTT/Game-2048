import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from game.rl.dqn_model import QNet
from game.rl.memory import ReplayMemory

class DQNAgent:
    def __init__(self, lr=1e-6, gamma=0.99, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.05, memory_size=10000, batch_size=64):
        self.policy_net = QNet()
        self.target_net = QNet()
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.memory = ReplayMemory(memory_size)
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.batch_size = batch_size

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 3)
        else:
            state_tensor = torch.FloatTensor(state.flatten()).unsqueeze(0)
            with torch.no_grad():
                q_values = self.policy_net(state_tensor)
            return int(torch.argmax(q_values).item())

    def push_memory(self, state, action, reward, next_state, done):
        self.memory.push(state.copy(), action, reward, next_state.copy(), done)

    def train_step(self):
        if len(self.memory) < self.batch_size:
            return
        states, actions, rewards, next_states, dones = self.memory.sample(self.batch_size)

        states_np = np.array([s.flatten() for s in states], dtype=np.float32)
        states_tensor = torch.from_numpy(states_np)
        next_states_np = np.array([s.flatten() for s in next_states], dtype=np.float32)
        next_states_tensor = torch.from_numpy(next_states_np)
        actions_tensor = torch.LongTensor(actions).unsqueeze(1)
        rewards_tensor = torch.FloatTensor(rewards)
        dones_tensor = torch.FloatTensor(dones)

        q_pred = self.policy_net(states_tensor).gather(1, actions_tensor).squeeze()
        with torch.no_grad():
            q_next = self.target_net(next_states_tensor).max(1)[0]
            q_target = rewards_tensor + self.gamma * q_next * (1 - dones_tensor)

        loss = nn.MSELoss()(q_pred, q_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # Epsilon decay
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_target_net(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())
