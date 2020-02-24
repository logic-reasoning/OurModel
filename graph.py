
import collections
import networkx 
import torch
import torch.nn as nn
import torch.nn.functional as F

class RelationNotFoundError(Exception):
    def __init__(self, vertex, relation):
        self.vertex = vertex
        self.relation = relation

class EntityNotFoundError(Exception):
    def __init__(self, vertex):
        self.vertex = vertex

class Relation:
    def __init__(self):
        pass

    def __iter__(self):
        pass


class RelationGraph(dict):
    
    def __init__(self):
        self.__graph_dict__ = collections.defaultdict(
                lambda: collections.defaultdict(list)
            )
        self.__relations__ = set() 
        self.__edges__ = set()

        self.__relation_to_ends__ = collections.defaultdict(list)

        self.evocab = set()
        self.rvocab = set()
        self.ePAD = 0
        self.rPAD = 0

    def __len__(self):
        return len(self.__graph_dict__)

    def sanity_check(self):
        pass

    def __getitem__(self, idx):
        '''
        # private member leakage!!
        if idx in self.__graph_dict__:
            return self.__graph_dict__[idx]
        raise EntityNotFoundError(idx)'''
        return self.get_relations(idx)

    def get_relations(self, idx):
        if idx not in self.__graph_dict__:
            raise EntityNotFoundError(idx)

        return self.__graph_dict__[idx].keys()

    def get_relations_batch(self, idx, padding=None):
        """ Return relations of batch 
        
        Arguments:
            idx {[type]} -- [description]
        
        Keyword Arguments:
            padding {[type]} -- [description] (default: {None})
        
        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError

    def get_neighbors_by(self, idx, relations, padding=None):
        """ TODO: reutrn batch of neighbors by relations 
        
        Arguments:
            idx {[type]} -- [description]
        
        Keyword Arguments:
            padding {int} -- [description] (default: {0})
        
        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError

    @property
    def relation_ends(self):
        return self.__relation_to_ends__

    def degree(self, idx):
        raise NotImplementedError

    @property
    def nodes(self):
        return list(self.__graph_dict__.keys())

    def get_neighbors_by(self, idx, rel):
        if idx not in self.__graph_dict__:
            raise EntityNotFoundError(idx)
        if rel not in self.__graph_dict__[idx]:
            raise RelationNotFoundError(idx, rel)
        return self.__graph_dict__[idx][rel]    

    def add_edge(self, src, rel, tgt):
        self.__graph_dict__[src][rel].append(tgt)
        if (src, tgt, rel) not in self.__relations__:
            self.__relations__.add((src, rel, tgt))

        self.__relation_to_ends__[rel].append((src, tgt))
        # TODO: update vocab 
        # entity vocab is not required since it is in __graph_dict__


    def add_edges_from(self, edgelist):
        for e in edgelist:
            self.add_edge(e[0], e[1], e[2])


    def add_edges_from_file(self, f):
        lines = f.readlines()
        lines = [[x.strip() for x in y.split()] for y in lines] 
        self.add_edges_from(lines)


    def make_reverse_relations(self):
        raise NotImplementedError


    def __pad(self, seq, max_len, pad):
        new_seq = seq.copy()
        new_seq = seq[max(len(seq) - max_len, 0):] + [pad] * max(0, max_len - len(seq))
        return new_seq

    def __indexize(self):
        self.r2id = {}
        self.e2id = {}
        self.r2id['<PAD>'] = self.rPAD
        self.e2id['<PAD>'] = self.ePAD

        def push_to_dict(D, x):
            if x not in D:
                D[x] = len(D)

        for e in self.__relations__:
            push_to_dict(self.r2id, e[1])
            push_to_dict(self.e2id, e[0])
            push_to_dict(self.e2id, e[2])


    def batchify(self, max_relations=128, max_neighbors=1024, device='cuda'):

        self.__indexize()

        self.relations_torch = [[self.r2id[x] for x in self.get_relations(x)] for x in self.nodes]
        self.neighbors_torch = [[[self.e2id[t] for t in self.get_neighbors_by(x, r)] for r in self.get_relations(x)] 
                                for x in self.nodes]
        self.rmask = []
        self.nmask = []

        max_relations = min(max_relations, max(map(len, self.relations_torch))) 
        max_neighbors = min(max_neighbors, max(map(lambda x: max(map(len, x)), self.neighbors_torch)))
        
        print('max neighbors: {}'.format(max(map(lambda x: max(map(len, x)), self.neighbors_torch))))
        print('max relations: {}'.format(max(map(len, self.relations_torch)))) 

        self.relations_torch = [
            self.__pad(x, max_relations, self.rPAD) for x in self.relations_torch
        ]
        self.neighbors_torch = [
            self.__pad(x, max_relations, [self.ePAD] * max_neighbors) for x in self.neighbors_torch
        ]
        self.neighbors_torch = [[self.__pad(x, max_neighbors, self.ePAD) for x in y]  
            for y in self.neighbors_torch
        ]
         
        self.relations_torch = torch.tensor(self.relations_torch).long().to(device)
        self.neighbors_torch = torch.tensor(self.neighbors_torch).long().to(device)


    def to_networkx(self, rel_as_nodes=False, directional=False):

        if directional:
            G = networkx.DiGraph()
        else:
            G = networkx.Graph()

        if rel_as_nodes:
            for r in self.__relations__:
                G.add_edge(r[0], r[1], weight=1)
                G.add_edge(r[1], r[2], weight=1)
                if directional:
                    G.add_edge('reverse ' + r[1], r[0], weight=1)
                    G.add_edge(r[2], 'reverse ' + r[1], weight=1)
        else:
            for r in self.__relations__:
                G.add_edge(r[0], r[2], relation=r[1], weight=1)
                if directional:
                    G.add_edge(r[2], r[0], relation='reverse ' + r[1], weight=1)

        return G
