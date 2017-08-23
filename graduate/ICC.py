#uncoding:utf-8
import sqlite3
import xlwt
import json
import Queue
import Estimate
import time
import Estimate_rou


class ICC():
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
        #没有度的点
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

    #画出节点的度
    '''
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
    #广搜计算节点v到所有节点的平均距离
    def BFS(self, v):
        visited = [False] * self.n
        #LL = self.n * self.n * self.n
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

    #计算所有节点的逆亲密中心
    def travelBFS(self):
        print 'travelBFS'
        closeCentrality = {}
        for k,v in self.graph.items():
            #print '计算',k,'逆亲密中心'
            closeCentrality[k] = float(self.BFS(k)) / float(self.n - 1)
            print k," the closeCentrality is : ",closeCentrality[k]
            #print '逆亲密中心为：',closeCentrality[k]
        return closeCentrality
    #返回k个结构洞
    def algorithmICC(self, k, closeCentrality):
        print 'algorithmICC'
        q = Queue.PriorityQueue()
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
        print 'algorithmICC over'
        return  list


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

    def icc_savePRF(self, k_end):
        print 'icc_sacePRF'
        graph = {}
        graph_Excel = {}
        e = Estimate.Estimate()
        rou = Estimate_rou.Estimate_rou()
        x = [i for i in range(5, k_end, 5)]  # X轴的k值
        RTy = []
        Py = []
        Ry = []
        Fy = []
        closeCentrality = {}
        with open('closeCentrality.json') as json_file:
            data = json.load(json_file)
        for k, v in data.items():
            closeCentrality[int(k)] = v
        for i in range(5, k_end, 5):
            ST = time.time()
            list = self.algorithmICC(i, closeCentrality)
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
        self.wExcel(graph_Excel, 'icc.xls')
        self.wFile('icc_structural_holes.xls', graph)

if __name__=='__main__':
    icc = ICC()
    icc.icc_savePRF(105)