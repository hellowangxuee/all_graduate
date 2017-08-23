#uncoding:utf-8
import time
import sqlite3
import Queue
import Estimate
import xlwt
import Estimate_rou

class HIS():
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
        #print 'cnt = ',cnt
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
            #print 'maxp = ',maxp
        #print self.page_rank


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
        #print 'cou : ',cou
        #print 'heapsize : ',heapsize

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
                    if  new_inf > (influential[e_id][i] + 1e-13):
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
            #print 's2 = ',s2, '   s3 = ', s3
        list = []
        for i in range(size):
            if i < Q.qsize():
                list.append(Q.get()[1])
        return list


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

    '''
    def draw_zxt(self, x, y, xlabel, ylabel, name):
        plt.figure()
        plt.plot(x, y, "o-", linewidth = 2.0)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        #plt.show()
        plt.savefig(name)
    '''

    def draw_HIS(self, x, RTy, Py, Ry, Fy):
        self.draw_zxt(x, RTy, 'k_value', 'runtime', 'HIS/runtime.jpg')
        self.draw_zxt(x, Py, 'k_value', 'precision', 'HIS/precision.jpg')
        self.draw_zxt(x, Ry, 'k_value', 'recall', 'HIS/recall.jpg')
        self.draw_zxt(x, Fy, 'k_value', 'F1_score', 'HIS/F1_score.jpg')

    def wFile(self, filename, dict):
        dic = dict.items()
        dic.sort()
        file = open(filename, 'a+')
        file.write(str('target_community : ') + str(self.target_communities) + '\n')
        for i in range(len(dic)):
            file.write(str(dic[i]) + '\n')
        file.close()

    def his_savePRF(self, end):
        hi = HIS()
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
        print '1111'
        for i in range(5, end, 5):
            ST = time.time()
            #print 'this is the ',i,' loop'
            list = hi.structure_hole_min_max_faster(i)
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
        self.wExcel(graph_Excel, 'his.xls')
        self.wStructural(graph, 'his_structural_holes.xls')


if __name__=='__main__':
    his = HIS()
    his.his_savePRF(105)
