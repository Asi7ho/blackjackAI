# Import libraries

import os
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.autograd as autograd
from torch.autograd import Variable


# Architecture of the neural network

class Network(nn.Module):

    def __init__(self, input_size, num_action):
        super(Network, self).__init__()
        self.input_size = input_size
        self.num_action = num_action

        self.fc1 = nn.Linear(input_size, 32)
        self.fc2 = nn.Linear(32, 32)
        self.fc3 = nn.Linear(32, num_action)

    def forward(self, state):
        x = self.fc1(state)
        x = F.sigmoid(x)
        x = self.fc2(x)
        x = F.sigmoid(x)
        x = self.fc3(x)

        return x


# Experience Replay

class ReplayMemory(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, event):
        self.memory.append(event)

        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        samples = zip(*random.sample(self.memory, batch_size))

        return map(lambda x: Variable(torch.cat(x, dim=0)), samples)


# Deep Q Learning

class Dqn():
    def __init__(self, input_size, num_action, gamma):
        self.model = Network(input_size, num_action)
        self.memory = ReplayMemory(10)
        self.gamma = gamma
        self.reward_window = []
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-2)
        self.last_state = torch.Tensor(input_size).unsqueeze(0)
        self.last_action = 0
        self.last_reward = 0
        self.last_vicDealer = 0
        self.last_vicPlayer = 0

    def select_action(self, state):
        probs = F.softmax(self.model(state) * 10, dim=1)
        action = probs.multinomial(num_samples=1)

        return action.data[0, 0]

    def learn(self, batch_state, batch_next_state, batch_reward, batch_action):
        outputs = self.model(batch_state).gather(
            1, batch_action.unsqueeze(1)).squeeze(1)
        next_outputs = self.model(batch_next_state).detach().max(1)[0]
        targets = batch_reward + self.gamma * next_outputs  # Bellman equation
        td_loss = F.mse_loss(outputs, targets)

        self.optimizer.zero_grad()
        td_loss.backward()
        self.optimizer.step()

    def update(self, reward, new_signal):
        new_state = torch.Tensor(new_signal).float().unsqueeze(0)
        self.memory.push((self.last_state, new_state,
                          torch.LongTensor([int(self.last_action)]), torch.Tensor([self.last_reward])))
        action = self.select_action(new_state)

        if len(self.memory.memory) > 100:
            batch_state, batch_next_state, batch_action, batch_reward = self.memory.sample(
                100)
            self.learn(batch_state, batch_next_state,
                       batch_reward, batch_action)

        self.last_action = action
        self.last_reward = reward
        self.last_state = new_state

        self.reward_window.append(reward)
        if len(self.reward_window) > 1000:
            del self.reward_window[0]

        return action

    def score(self):
        return sum(self.reward_window) / (len(self.reward_window) + 1e-8)

    def save(self, vicDealer, vicPlayer):
        torch.save({"state_dict": self.model.state_dict(),
                    "optimizer": self.optimizer.state_dict(),
                    "vicDealer": vicDealer,
                    "vicPlayer": vicPlayer,
                    "reward_window": self.reward_window}, "last_brain.pth")

    def load(self):
        if (os.path.isfile("last_brain.pth")):
            checkpoint = torch.load("last_brain.pth")
            self.model.load_state_dict(checkpoint["state_dict"])
            self.optimizer.load_state_dict(checkpoint["optimizer"])
            self.last_vicDealer = checkpoint["vicDealer"]
            self.last_vicPlayer = checkpoint["vicPlayer"]
            self.reward_window = checkpoint["reward_window"]
        else:
            print("File does not exist")
