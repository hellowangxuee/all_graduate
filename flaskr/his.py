#uncoding:utf-8
import Queue

class HIS():
    def __init__(self, Graph, area, edge):
        self.graph = Graph
        self.area = area
        self.n = Graph.__len__()
        self.m = edge
        self.target_communities = [1, 2, 3]
        self.alpha, self.beta = self.set_alpha_beta(len(self.target_communities))
        self.page_rank = [0.0] * self.n
        self.get_page_rank()

    # 计算2的x次方
    def two(self, x):
        return 1 << x

    # 计算 x 的二进制显示中 1 的个数
    def countbit(self, x):
        return 0 if x == 0 else (1 + self.countbit(x & (x - 1)))

    # 计算 s 的第 x 位是否为 1
    def contain(self, s, x):
        return ((s & self.two(x)) != 0)

    def set_alpha_beta(self, c):
        beta = []
        alpha = [0.3] * c
        for i in range(self.two(c)):
            if self.countbit(i) == 0:
                beta.append(0)
            elif self.countbit(i) == 1:
                beta.append(0)
            elif self.countbit(i) == 2:
                beta.append(0.17)
            elif self.countbit(i) == 3:
                beta.append(0.25)
            elif self.countbit(i) == 4:
                beta.append(0.29)
            elif self.countbit(i) == 5:
                beta.append(0.30)
            elif self.countbit(i) >= 6:
                beta.append(0.35)
        return alpha, beta

    def get_page_rank(self):
        cnt = 0
        for k,v in self.graph.items():
            if len(v) > 0:
                self.page_rank[k] = 1
                cnt += 1
        ratio = 0.85
        s = [0.0] * self.n
        for i in range(100):
            for k,v in self.graph.items():
                if len(v) > 0:
                    s[k] = (float)(1.0-ratio)/cnt
                    for j in v:
                        s[k] +=ratio*self.page_rank[j]/len(self.graph[j])
                    #print 's[', k, '] = ',s[k]
            for k,v in self.graph.items():
                if len(v) > 0:
                    self.page_rank[k] = s[k]
            maxp = 0.0
            for k,v in self.graph.items():
                if self.page_rank[k] > maxp:
                    maxp = self.page_rank[k]
            if maxp < 1e-10:
                break
            for k,v in self.graph.items():
                self.page_rank[k] /= maxp

    def structure_hole_min_max_faster(self, size):
        c = len(self.target_communities)
        influential = [[0.0 for col in range(c)] for row in range(self.n)]
        sh = [[0.0 for col in range(self.two(c))] for row in range(self.n)]
        heapsize = 0
        heap = []
        pos = [-1] * self.n
        tp = [0.0] * self.n
        cou = 0
        for k in range(c):
            for i in range(self.n):
                if (self.area[i] & self.target_communities[k]) == self.target_communities[k]:
                    influential[i][k] = self.page_rank[i]
                    if influential[i][k] > (tp[i] + 1e-13):
                        tp[i] = influential[i][k]
                        pos[i] = heapsize - 1
                        heap.append(i)
                        heapsize += 1
                        #cou += 1
                        p = heapsize - 1
                        q = (p-1)>>1
                        while p > 0:
                            if tp[heap[p]] > tp[heap[q]]:
                                tmp = heap[p]
                                heap[p] = heap[q]
                                heap[q] = tmp
                            else: break
                            p = q
                            q = (p-1)>>1
        while heapsize > 0:
            idx = heap[0]
            tp[idx] =0.0
            pos[idx] = -1
            heapsize -= 1
            heap[0] = heap[heapsize]
            if heapsize > 0:
                i = 0
                key = heap[0]
                tmp = tp[key]
                j = (i<<1) + 1
                while j < heapsize:
                    if j+1 < heapsize and tp[heap[j+1]] >tp[heap[j]]:
                        j+=1
                    if tp[heap[j]] <= tmp:break
                    heap[i] = heap[j]
                    pos[heap[i]] = j
                    i = j
                    j = (i<<1) + 1
                heap[i] = key
                pos[key] = i
            gset = sh[idx]
            gs = influential[idx]
            gset[0] = 1e100
            k = 0
            for set in range(1,self.two(c)):
                if not (self.contain(set,k)):
                    k += 1
                gset[set] = min(gs[k],gset[set^self.two(k)])
                #print 'k = ',k,' set = ',set,' gset = min( gs[',k,'], gset[',set^self.two(k),'] ) = ',gset[set]
            exp_inf = [0.0] * c
            for set in range(self.two(c)):
                tmp = self.beta[set] * gset[set]
                if tmp < 1e-13: continue
                for i in range(c):
                    if self.contain(set,i):
                        exp_inf[i] = tmp if tmp > exp_inf[i] else exp_inf[i]
            for e_id in self.graph[idx]:
                for i in range(c):
                    new_inf = self.alpha[i] * gs[i] + exp_inf[i]
                    if new_inf > (influential[e_id][i] + 1e-13):
                        influential[e_id][i] = new_inf
                        if new_inf <= tp[e_id] + 1e-13: continue
                        tp[e_id] = new_inf
                        if pos[e_id] < 0:
                            pos[e_id] = heapsize
                            if heapsize < len(heap):
                                heap[heapsize] = e_id
                            else:
                                heap.append(e_id)
                            heapsize += 1
                        p = pos[e_id]
                        q = (p-1)>>1
                        while p>0:
                            if tp[heap[q]] >= new_inf: break
                            heap[p] = heap[q]
                            pos[heap[p]] = p
                            p = q
                            q = (p-1)>>1
                        heap[p] = e_id
                        pos[e_id] = i
        Q = Queue.PriorityQueue()
        for i in range(self.n):
            s2 = 0.0
            for k in range(self.two(c)):
                if s2 < self.beta[k] * sh[i][k]:
                    s2 = self.beta[k] * sh[i][k]
            s3 = 0.0

            for j in range(c):
                s3 += influential[i][j]
            weight = int(s2 * 1e5) + int(s3*1e5/c)/1e5 + len(self.graph[i])/1e9
            Q.put((-weight,i))
        list = []
        for i in range(size):
            if i < Q.qsize():
                list.append(Q.get()[1])
        return list

if __name__=='__main__':
    his = HIS()
    his.structure_hole_min_max_faster(10)
