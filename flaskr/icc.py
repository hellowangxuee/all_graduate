#uncoding:utf-8
import Queue

class ICC():
    def __init__(self, Graph, edge):
        self.graph = Graph
        self.n = Graph.__len__()
        self.m = edge
        self.noDegree = []
        for k,v in Graph.items():
            if len(v) == 0:
                self.noDegree.append(k)

    #广搜计算节点v到所有节点的平均距离
    def BFS(self, v):
        visited = [False] * self.n
        LL = self.n * self.n * self.n
        #LL = 576497
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
        closeCentrality = {}
        for k,v in self.graph.items():
            #print '计算',k,'逆亲密中心'
            closeCentrality[k] = float(self.BFS(k)) / float(self.n - 1)
            #print '逆亲密中心为：',closeCentrality[k]
        return closeCentrality
    #返回k个结构洞
    def algorithmICC(self, k):
        q = Queue.PriorityQueue()
        closeCentrality = self.travelBFS()
        for i in range(self.n):
            if i not in self.noDegree:
                if q.qsize() < k:
                    q.put((-closeCentrality[i], i))
                else:
                    tmp = q.get()
                    if closeCentrality[i] < -tmp[0]:
                        #print 'node ',i,'closeCentrality is small, and =',closeCentrality[i]
                        q.put((-closeCentrality[i], i))
                    else:
                        q.put(tmp)
        list = []
        while not q.empty():
            list.append(q.get()[1])
        return  list