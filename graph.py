
import collections

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

    def get_neighbors_by(self, idx, rel):
        if idx not in self.__graph_dict__:
            raise EntityNotFoundError(idx)
        if rel not in self.__graph_dict__[idx]:
            raise RelationNotFoundError(idx, rel)
        return self.__graph_dict__[idx][rel]    

    def add_edge(self, src, tgt, rel):
        self.__graph_dict__[src][rel].append(tgt)

    def add_edges_from(self, edgelist):
        for e in edgelist:
            self.add_edge(e[0], e[1], e[2])

    def make_reverse_relations(self):
        pass
