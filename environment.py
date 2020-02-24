
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

        self.__graph.batchify()
        self.__sampler = graph.RelationSampler(self.__graph, config.batch_size)

    def play_episode(self, start_idx):
        nrollouts = self.__config.nrollouts

        # 1. get neighbors
        # 2. compute prob with agent
        # 3. transition 


    def play_episodes(self):
        # run episodes; obtain rollouts.

        # step 1. collect batch of data.
        
        # step 2. compute reward.
        # discriminative? 
        return

    @property
    def config(self):
        return str(self.__config)

    @config.setter
    def config(self, value):
        raise NotImplementedError