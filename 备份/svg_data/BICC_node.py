import networkx as nx
import json
import community
from networkx.readwrite import json_graph
import Queue
import matplotlib.pyplot as plt
import xlrd

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

tmp = []
list = []
data = xlrd.open_workbook("../BICC/bicc_structural_holes.xls")
table = data.sheets()[0]
nrows = table.nrows
for i in range(1,101):
    tmp.append(int(table.row(nrows-1)[i].value))
    list.append(int(table.row(nrows-1)[i].value))


for i in tmp:
    for v in graph[i]:
        if v not in list:
            list.append(v)

G = nx.Graph()
g_node_name = {}
for i in range(len(list)):
    g_node_name[list[i]] = i
    G.add_node(i)
    if list[i] in tmp:
        G.node[i]['group'] = 0
    else:
        G.node[i]['group'] = 1

for i in list:
    G.node[g_node_name[i]]['name'] = i
    for v in graph[i]:
        if v in list:
            G.add_edge(g_node_name[i], g_node_name[v])

# nx.draw(G)
# plt.show()

print 'nodes len : ',len(list)
data = json_graph.node_link_data(G)

s = json.dumps(data)
file = open("D:/Program Files (x86)/Apache Software Foundation/Apache2.2/htdocs/BICC_node_link.json","wb")
file.write(s)
file.close()