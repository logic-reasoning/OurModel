
import graph

import torch
import torch.nn as nn
import torch.nn.functional as F

import agent


class Environment:

    def __init__(self, relation_graph):
        self.__graph__ = relation_graph
        self.agent = agent.Agent()
    