#uncoding:utf-8
import sqlite3
import Queue
import xlwt
import Estimate
import Estimate_rou
import time
import json

class wx():
    def loadData(self):
        conn = sqlite3.connect("data.db")
        cursor = conn.execute("select * from community")
        for row in cursor:
            self.area.append(row[0])
        cursor = conn.execute("select * from graph")
        t = True
        for row in cursor:
            if t:
                self.n = row[0]
                self.m = row[1]
                for i in range(self.n):
                    self.graph[i] = []
                t = False
            else:
                if row[1] not in self.graph[row[0]]:
                    self.graph[row[0]].append(row[1])
                    self.graph[row[1]].append(row[0])
        conn.close()
        # 没有度的点
        y = [len(self.graph[i]) for i in range(self.n)]
        for i in range(len(y)):
            if y[i] == 0:
                self.noDegree.append(i)

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

    def __init__(self):
        self.graph = {}
        self.area = []
        self.noDegree = []
        self.n = 0
        self.m = 0
        self.target_communities = [1, 2, 3]
        self.alpha, self.beta = self.set_alpha_beta(len(self.target_communities))
        self.loadData()
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



    def get_page_rank(self):
        cnt = 0
        for k, v in self.graph.items():
            if len(v) > 0:
                self.page_rank[k] = 1
                cnt += 1
        ratio = 0.85
        # print 'cnt = ',cnt
        s = [0.0] * self.n
        for i in range(100):
            for k, v in self.graph.items():
                if len(v) > 0:
                    s[k] = (float)(1.0 - ratio) / cnt
                    for j in v:
                        s[k] += ratio * self.page_rank[j] / len(self.graph[j])
                        # print 's[', k, '] = ',s[k]
            for k, v in self.graph.items():
                if len(v) > 0:
                    self.page_rank[k] = s[k]
            maxp = 0.0
            for k, v in self.graph.items():
                if self.page_rank[k] > maxp:
                    maxp = self.page_rank[k]
            if maxp < 1e-10:
                break
            for k, v in self.graph.items():
                self.page_rank[k] /= maxp
                # print 'maxp = ',maxp
                # print self.page_rank

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
                        cou += 1
                        p = heapsize - 1
                        q = (p - 1) >> 1
                        while p > 0:
                            if tp[heap[p]] > tp[heap[q]]:
                                tmp = heap[p]
                                heap[p] = heap[q]
                                heap[q] = tmp
                            else:
                                break
                            p = q
                            q = (p - 1) >> 1
        # print 'cou : ',cou
        # print 'heapsize : ',heapsize

        while heapsize > 0:
            idx = heap[0]
            tp[idx] = 0.0
            pos[idx] = -1
            heapsize -= 1
            heap[0] = heap[heapsize]
            if heapsize > 0:
                i = 0
                key = heap[0]
                tmp = tp[key]
                j = (i << 1) + 1
                while j < heapsize:
                    if j + 1 < heapsize and tp[heap[j + 1]] > tp[heap[j]]:
                        j += 1
                    if tp[heap[j]] <= tmp: break
                    heap[i] = heap[j]
                    pos[heap[i]] = i
                    i = j
                    j = (i << 1) + 1
                heap[i] = key
                pos[key] = i
            gset = sh[idx]
            gs = influential[idx]
            gset[0] = 1e100
            k = 0
            for set in range(1, self.two(c)):
                if not (self.contain(set, k)):
                    k += 1
                gset[set] = min(gs[k], gset[set ^ self.two(k)])
            exp_inf = [0.0] * c
            for set in range(self.two(c)):
                tmp = self.beta[set] * gset[set]
                if tmp < 1e-13: continue
                for i in range(c):
                    if self.contain(set, i):
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
                        q = (p - 1) >> 1
                        while p > 0:
                            if tp[heap[q]] >= new_inf: break
                            heap[p] = heap[q]
                            pos[heap[p]] = p
                            p = q
                            q = (p - 1) >> 1
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
            weight = int(s2 * 1e5) + int(s3 * 1e5 / c) / 1e5 + len(self.graph[i]) / 1e9
            Q.put((-weight, i))
            # print 's2 = ',s2, '   s3 = ', s3
        list = []
        for i in range(size):
            if i < Q.qsize():
                list.append(Q.get()[1])
        return list

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
    def travelBFS_L(self, list, L):
            closeCentrality_L = {}

            for k in list:
                closeCentrality_L[k] = float(self.BFS_L(k, L)) / float(self.n - 1)
            return closeCentrality_L

    #设置L为4步
    def wX(self, k, closeCentrality_L):
        list = self.structure_hole_min_max_faster(2*k)
        #closeCentrality_L = self.travelBFS_L(list, L)
        H = Queue.PriorityQueue()
        for i in list:
            if i not in self.noDegree:
                if H.qsize() < k:
                    H.put((closeCentrality_L[i], i))
                else:
                    tmp = H.get()
                    if closeCentrality_L[i] > tmp[0]:
                        H.put((closeCentrality_L[i], i))
                    else:
                        H.put(tmp)
        li = []
        while not H.empty():
            li.append(H.get()[1])
        return li

    def wExcel(self, dict, outfile):
        w = xlwt.Workbook()
        sheet = w.add_sheet('sheet1')
        sheet.write(0, 0, str('k_value').decode('utf8'))
        sheet.write(0, 1, str('runtime').decode('utf8'))
        sheet.write(0, 2, str('precision').decode('utf8'))
        sheet.write(0, 3, str('recall').decode('utf8'))
        sheet.write(0, 4, str('F1_score').decode('utf8'))
        sheet.write(0, 5, str('rou_value').decode('utf-8'))

        graph = dict.items()
        graph.sort()
        i = 1
        for k,v in graph:
            sheet.write(i, 0, str(k).decode('utf8'))
            sheet.write(i, 1, str(v[0]).decode('utf8'))
            sheet.write(i, 2, str(v[1]).decode('utf8'))
            sheet.write(i, 3, str(v[2]).decode('utf8'))
            sheet.write(i, 4, str(v[3]).decode('utf8'))
            sheet.write(i, 5, str(v[4]).decode('utf8'))
            i += 1
        w.save(outfile)

    def wStructural(self, graph, outfile):
        w = xlwt.Workbook()
        sheet = w.add_sheet('sheet1')
        dict = graph.items()
        dict.sort()
        t = 0
        for k,v in dict:
            sheet.write(t, 0, str(k).decode('utf-8'))
            for i in range(k):
                sheet.write(t, i+1, str(v[i]).decode('utf-8'))
            t += 1
        w.save(outfile)

    def wx_savePRF(self, end):
        graph = {}
        graph_Excel = {}
        e = Estimate.Estimate()
        rou = Estimate_rou.Estimate_rou()
        x = [i for i in range(5, end, 5)]   #X轴的k值
        RTy = []
        Py = []
        Ry = []
        Fy = []
        Rouy = []
        closeCentrality_L = {}
        with open('closeCentrality_L.json') as json_file:
            data = json.load(json_file)
        for k, v in data.items():
            closeCentrality_L[int(k)] = v
        for i in range(5, end, 5):
            ST = time.time()
            list = self.wX(i, closeCentrality_L)
            ET = time.time()
            RT = ET - ST
            graph[i] = list   #存储给定k值下的结构洞
            P, R, F  = e.calPRF(set(list))
            num = rou.rou(list)
            RTy.append(RT)
            Py.append(P)
            Ry.append(R)
            Fy.append(F)
            g_list = [RT, P, R, F, num]
            graph_Excel[i] = g_list
        #self.draw_HIS(x, RTy, Py, Ry, Fy)
        self.wExcel(graph_Excel, 'wx.xls')
        #self.wFile('his_structural_holes.txt',graph)
        self.wStructural(graph, 'wx_structural_holes.xls')


if __name__=='__main__':
    wx = wx()
    wx.wx_savePRF(105)