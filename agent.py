
import torch
import torch.nn as nn
import torch.nn.functional as F

class Agent:

    def __init__(self):
        pass

        self.policy = None

    def get_transition_probability(self, states, actions, mask):
        prob = torch.rand_like(neighbors) 
        prob[~mask.bool()] = -float('inf')
        return torch.softmax(prob, dim=1)
    