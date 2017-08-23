#uncoding:utf-8
import sqlite3

class Estimate_rou():
    def __init__(self):
        self.graph = {}
        self.area = []
        self.noDegree = []
        self.n = 0
        self.m = 0
        self.loadData()
        self.crosscommunity = []
        with open("Twitter/cross_community.txt") as df:
            for d in df:
                self.crosscommunity.append(int(d.strip()))

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


    #返回当前解决方案的度量值
    def rou(self, list1):
        num = 0.0
        for i in list1:
            num += self.crosscommunity[i]/(float) (len(self.graph[i]))
        num /= len(list1)
        return num