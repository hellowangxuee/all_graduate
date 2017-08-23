#uncoding:utf-8

from networkx import *

G = Graph()

list1 = []
list2 = []
with open("Twitter/twitter.dat") as df:
    for d in df:
        list1.append(int(d.strip().split(' ')[0]))
        list2.append(int(d.strip().split(' ')[1]))

G.add_edges_from(list(zip(list1, list2)))
pathlengths=[]

print("source vertex {target:length, }")
for v in G.nodes():
    spl=single_source_shortest_path_length(G,v)
    #print('%s %s' % (v,spl))
    for p in spl.values():
        pathlengths.append(p)
    print v,' single_source_shortest_path_length : ', sum(pathlengths),' inverse close centrility : ', sum(pathlengths)/len(G.node)

print('')
print("average shortest path length %s" % (sum(pathlengths)/len(pathlengths)))

# histogram of path lengths
dist={}
for p in pathlengths:
    if p in dist:
        dist[p]+=1
    else:
        dist[p]=1


print 'dist : \n', dist
print('')
print("length #paths")
verts=dist.keys()
for d in sorted(verts):
    print('%s %d' % (d,dist[d]))

print("radius: %d" % radius(G))
print("diameter: %d" % diameter(G))
print("eccentricity: %s" % eccentricity(G))
print("center: %s" % center(G))
print("periphery: %s" % periphery(G))
print("density: %s" % density(G))