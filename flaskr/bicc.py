#uncoding:utf-8
import Queue


class BICC():
    def __init__(self, Graph, edge):
        self.graph = Graph
        self.n = Graph.__len__()
        self.m = edge
        self.noDegree = []
        for k,v in Graph.items():
            if len(v) == 0:
                self.noDegree.append(k)

    #寻找0节点所在的连通分量中度最小的点
    def found_small_degree(self):
        Q = Queue.Queue()
        q = Queue.PriorityQueue()
        Q.put(0)
        q.put(len(self.graph[0]))
        vis = [False] * self.n
        vis[0] = True
        while not Q.empty():
            tmp = Q.get()
            for i in self.graph[tmp]:
                if vis[i] == False:
                    Q.put(i)
                    q.put(len(self.graph[i]))
                    vis[i] = True
        return q.get()


    #计算0节点所在连通分量的所有点对的最短路径和
    def cou(self):
        Q=Queue.Queue()
        q = Queue.Queue()
        co = 0
        vis = [False] * self.n
        virtex = self.found_small_degree()
        vis[virtex] = True
        Q.put(virtex)
        q.put(virtex)
        while not Q.empty():
            tmp = Q.get()
            step = q.get()
            co += step
            for i in self.graph[tmp]:
                if vis[i] == False:
                    Q.put(i)
                    q.put(step + 1)
                    vis[i] = True
        print co

    # 广搜计算节点v到L层次邻居节点的平均距离
    def BFS(self, v):
        visited = [False] * self.n
        #LL = self.n * self.n
        LL = 576497
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
    def BFS_L(self, v, L):
            visited = [False] * self.n
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
                if step != L:
                    for i in self.graph[temp]:
                        if visited[i] == False:
                            q.put(i)
                            deq.put(step + 1)
                            visited[i] = True
            return count

    # 计算所有节点的L界逆亲密中心
    def travelBFS_L(self, L):
            closeCentrality_L = {}
            for k, v in self.graph.items():
                closeCentrality_L[k] = float(self.BFS_L(k, L)) / float(self.n - 1)
            return closeCentrality_L
    def algorithmBICC(self, k, K, L):
        closeCentrality_L = self.travelBFS_L(L)
        H = Queue.PriorityQueue()
        for i in range(self.n):
            if i not in self.noDegree:
                if H.qsize() < K:
                    H.put((closeCentrality_L[i], i))
                else:
                    tmp = H.get()
                    if closeCentrality_L[i] > tmp[0]:
                        H.put((closeCentrality_L[i],i))
                    else:
                        H.put(tmp)

        closeCentrality = {}
        while not H.empty():
            tmp = H.get()
            closeCentrality[tmp[1]] = float(self.BFS(tmp[1])) /  float(self.n - 1)
            #print tmp[1], " the closeCentrality is : ", closeCentrality[tmp[1]]
        Vs = Queue.PriorityQueue()
        for x,y in closeCentrality.items():
            if Vs.qsize() < k:
                Vs.put((-closeCentrality[x],x))
            else:
                tmp = Vs.get()
                if closeCentrality[x] < -tmp[0]:
                    Vs.put((-closeCentrality[x], x))
                else:
                    Vs.put(tmp)
        li = []
        while not Vs.empty():
            li.append(Vs.get()[1])
        return li