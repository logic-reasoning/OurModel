
import graph

import torch
import torch.nn as nn
import torch.nn.functional as F

import agent


class Environment:

    def __init__(self, relation_graph, config):
        self.__graph = relation_graph
        self.__agent = agent.Agent()
        self.__config = config

    def play_episodes(self):
        # run episodes; obtain rollouts.

        # step 1. collect batch of data.

        # step 2. compute reward.
        return

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, value):
        raise NotImplementedError