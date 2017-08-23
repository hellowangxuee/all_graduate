#uncoding:utf-8
import networkx as nx
import community
import his
import matplotlib.pyplot as plt
import json
from networkx.readwrite import json_graph

#G = nx.connected_caveman_graph(10,5)
G = nx.relaxed_caveman_graph(10, 5, 0.1, seed=42)
area = []
graph = {}
edge = 0
partition = community.best_partition(G)
for n in G:
    area.append(partition[n])
    graph[n] = []
    for k, v in G.edge[n].items():
        graph[n].append(k)
        edge += 1

# his = his.HIS(graph, area, edge)
# print his.structure_hole_min_max_faster(10)

nx.draw(G)
plt.show()
