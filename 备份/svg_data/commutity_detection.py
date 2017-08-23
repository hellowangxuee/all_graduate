import community
import networkx as nx
import matplotlib.pyplot as plt

#better with karate_graph() as defined in networkx example.
#erdos renyi don't have true community structure
G = nx.erdos_renyi_graph(30, 0.05)

#first compute the best partition
partition = community.best_partition(G)

print 'G : ', G.nodes()
print 'partition : ', partition

max = 0
for k,v in partition.items():
    max = v if v > max else max

print 'max : ',max
print 'partition.length : ',len(partition)
ll = []
l2 = []
for k,v in partition.items():
    if v == 4:
        ll.append(k)
    elif v == 1:
        l2.append(k)
print '4 communities: ',ll
print '1 communities: ',l2
print 'll jiao l2 : ', set(ll) & set(l2)


#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))


nx.draw_networkx_edges(G,pos, alpha=0.5)
plt.show()