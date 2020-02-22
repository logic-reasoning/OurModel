
from graph import RelationGraph
a = [[1,2,3], [4,5,6], [7,8,9]]
G = RelationGraph()
G.add_edges_from(a)

print(G[1])

#print(G[100])
#print(G[1][100])
print(G[1])
print(G.get_neighbors_by(1, 3))