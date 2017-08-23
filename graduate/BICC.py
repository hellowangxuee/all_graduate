#uncoding:utf-8
import sqlite3
import xlwt
import numpy as np
#import matplotlib.pyplot as plt
import Queue
from Estimate import *
import time
import Estimate_rou
import json


class BICC():
    #进行数据初始化
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
        self.loadData()

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

    '''
    #画出节点的度
    def drawDegree(self):
        # X轴，Y轴数据
        x = [i for i in range(self.n)]
        y = [len(self.graph[i]) for i in range(self.n)]
        plt.figure(figsize=(800, 600))  # 创建绘图对象
        plt.plot(x, y, "o-", linewidth=1)  # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
        plt.xlabel("Node")  # X轴标签
        plt.ylabel("degree")  # Y轴标签
        plt.title("The degree of the nodes")  # 图标题
        plt.show()  # 显示图
        plt.savefig("degree.jpg")  # 保存图
    '''

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
        with open('closeCentrality.json') as json_file:
            data = json.load(json_file)
        cC = {}
        for k, v in data.items():
            cC[int(k)] = v
        closeCentrality = {}
        while not H.empty():
            tmp = H.get()
            closeCentrality[tmp[1]] = cC[tmp[1]]
            # closeCentrality[tmp[1]] = float(self.BFS(tmp[1])) /  float(self.n - 1)
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

    def wFile(self, filename, dict):
        dic = dict.items()
        dic.sort()
        file = open(filename, 'a+')
        for i in range(len(dic)):
            file.write(str(dic[i]) + '\n')

        file.close()

    def wExcel(self, dict, outfile):
        w = xlwt.Workbook()
        sheet = w.add_sheet('sheet1')
        sheet.write(0, 0, str('k_value').decode('utf8'))
        sheet.write(0, 1, str('runtime').decode('utf8'))
        sheet.write(0, 2, str('precision').decode('utf8'))
        sheet.write(0, 3, str('recall').decode('utf8'))
        sheet.write(0, 4, str('F1_score').decode('utf8'))
        sheet.write(0, 5, str('rou').decode('utf-8'))

        graph = dict.items()
        graph.sort()
        i = 1
        for k,v in graph:
            sheet.write(i, 0, str(k).decode('utf8'))
            sheet.write(i, 1, str(v[0]).decode('utf8'))
            sheet.write(i, 2, str(v[1]).decode('utf8'))
            sheet.write(i, 3, str(v[2]).decode('utf8'))
            sheet.write(i, 4, str(v[3]).decode('utf8'))
            sheet.write(i, 5, str(v[4]).decode('utf-8'))
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

    def bicc_savePRF(self, k_end):
        graph = {}
        graph_Excel = {}
        e = Estimate()
        rou = Estimate_rou.Estimate_rou()
        x = [i for i in range(5, k_end, 5)]  # X轴的k值
        RTy = []
        Py = []
        Ry = []
        Fy = []
        for i in range(5, k_end, 5):
            ST = time.time()
            list = self.algorithmBICC(i, 2*i, 4)
            ET = time.time()
            RT = ET - ST
            graph[i] = list  # 存储给定k值下的结构洞
            P, R, F = e.calPRF(set(list))
            num = rou.rou(list)
            RTy.append(RT)
            Py.append(P)
            Ry.append(R)
            Fy.append(F)
            g_list = [RT, P, R, F, num]
            graph_Excel[i] = g_list
        self.wExcel(graph_Excel, 'bicc.xls')
        #self.wFile('bicc_structural_holes.txt', graph)
        self.wStructural(graph, 'bicc_structural_holes.xls')



if __name__ == '__main__':
    bicc = BICC()
    # #bicc.cou()
    # e = Estimate()
    # # for k in range(50, 150, 10):
    # #     list = bicc.algorithmBICC(k,2*k,3)
    # #     print e.calPRF(set(list))
    #
    # list = bicc.algorithmBICC(5,10,3)
    # print e.calPRF(set(list))
    bicc.bicc_savePRF(105)