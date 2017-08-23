import networkx as nx
import json
from networkx.readwrite import json_graph
# import matplotlib.pyplot as plt
#
# G = nx.Graph()
# H=nx.path_graph(10)
# G.add_nodes_from(H)
# edgelist=[(0,1),(1,2),(2,3)]
# G.add_edges_from(edgelist)
# G.node[1]['room'] = 714
# G.add_edges_from([(1,2,{'color':'blue'}), (2,3,{'weight':8})])
# print G.nodes(data=True)
# print G.nodes()
#
# print G.edges(data=True)
#
# print nx.degree(G)
# print nx.is_connected(G)
# c = list(nx.k_clique_communities(G, 4))
# print c

# from networkx.readwrite import json_graph
#
# G = nx.Graph([(1,2)])
# data = json_graph.node_link_data(G)
# print data
# graph = json_graph.node_link_graph(data)
#
# s = json.dumps(data)
#
# print s
#
# data = json_graph.adjacency_data(G)
#
# s = json.dumps(data)
# print s

G = nx.Graph()
# edgelist = []
# t = True
# with open('Twitter/twitter.dat') as df:
#     for d in df:
#         if t == True:
#             t = False
#         else:
#             a = int(d.strip().split(' ')[0])
#             b = int(d.strip().split(' ')[1])
#             if a < 100 and b < 100:
#                 edgelist.append((a,b))

for i in range(100):
    G.add_node(i)

supposelist = []
import random
import community
#from networkx.algorithms import community
for i in range(100):
    a = random.randrange(100)
    b = random.randrange(100)
    supposelist.append((a,b))
G.add_edges_from(supposelist)

partation = community.best_partition(G)
for k,v in partation.items():
    G.node[k]['group'] = v
data = json_graph.node_link_data(G)

s = json.dumps(data)
file = open("D:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/node_link.json","wb")
file.write(s)
file.close()
