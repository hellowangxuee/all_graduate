import networkx as nx
import json
import community
from networkx.readwrite import json_graph
import Queue
import matplotlib.pyplot as plt

graph = {}
edgelist = []
t = True
with open('../Twitter/twitter.dat') as df:
    for d in df:
        if t == True:
            t = False
            a = int(d.strip().split(' ')[0])
            for i in range(a):
                graph[i] = []
        else:
            a = int(d.strip().split(' ')[0])
            b = int(d.strip().split(' ')[1])
            if b not in graph[a]:
                graph[a].append(b)

Q = Queue.Queue()
Q.put(0)
list = [0]
node_num = 2275
while not Q.empty():
    tmp = Q.get()
    if len(list) == node_num:
        break
    for i in graph[tmp]:
        Q.put(i)
        if len(list) != node_num:
            list.append(i)
        else:
            break

print 'len(list) : ',len(list)
G = nx.Graph()

g_node_name = {}
for i in range(len(list)):
    g_node_name[list[i]] = i
    # if i == 32:
    #     print 'node 32 real is :', list[i]
    G.add_node(i)

for i in list:
    G.node[g_node_name[i]]['name'] = i
    for v in graph[i]:
        if v in list:
            G.add_edge(g_node_name[i], g_node_name[v])




print 'nodes : ',G.nodes()
print 'edges : ',G.edges()
print 'edges : ',len(G.edges())
partation = community.best_partition(G)


for k,v in partation.items():
    G.node[k]['group'] = v

#nx.draw(G)
plt.show()
data = json_graph.node_link_data(G)

s = json.dumps(data)
file = open("D:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/node_link.json","wb")
file.write(s)
file.close()

