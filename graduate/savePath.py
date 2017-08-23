#uncoding:utf-8
import Queue
import json


class SPath():
    def __init__(self, graphName, communityName):
        self.graph = {}
        self.area = []
        self.noDegree = []
        t = True
        with open(graphName, 'r') as df:
            for d in df:
                if t:
                    self.n = int(d.strip().split(' ')[0])
                    self.m = int(d.strip().split(' ')[1])
                    for i in range(self.n):
                        self.graph[i] = []
                    t = False
                else:
                    self.graph[int(d.strip().split(' ')[0])].append(int(d.strip().split(' ')[1]))
                    self.graph[int(d.strip().split(' ')[1])].append(int(d.strip().split(' ')[0]))
        with open(communityName, 'r') as df:
            for d in df:
                self.area.append(int(d.strip()))
        for i in range(self.n):
            if len(self.graph[i]) == 0:
                self.noDegree.append(i)

    #广搜计算节点v到所有节点的平均距离
    def BFS(self, v):
        visited = [False] * self.n
        LL = self.n * self.n * self.n
        deq = Queue.Queue()
        q = Queue.Queue()
        visited[v] = True
        q.put(v)
        deq.put(0)
        count = 0
        while not q.empty():
            temp = q.get()
            step = deq.get()
            count += step
            for i in self.graph[temp]:
                if visited[i] == False:
                    q.put(i)
                    deq.put(step+1)
                    visited[i] = True
        for i in visited:
            if i == False:
                count += LL
        return count

    #计算所有节点的逆亲密中心
    def travelBFS(self):
        print 'travelBFS'
        closeCentrality = {}
        for k,v in self.graph.items():
            #print '计算',k,'逆亲密中心'
            closeCentrality[k] = float(self.BFS(k)) / float(self.n - 1)
            #print k," the closeCentrality is : ",closeCentrality[k]
            #print '逆亲密中心为：',closeCentrality[k]
        json_closeCentrility = json.dumps(closeCentrality)
        file = open('closeCentrality.json','w')
        file.write(json_closeCentrility)
        file.close()
        return closeCentrality

if __name__=='__main__':
    cC = SPath('Twitter/twitter.dat','Twitter/community.txt')
    cC.travelBFS()