#uncoding:utf-8
import matplotlib.pyplot as plt
import random
import xlrd
#一次性画出所有算法的衡量指标对比图

class total():
    def __init__(self):
        self.x = [i for i in range(5, 50, 5)]
        self.y = [[],[],[],[]]

    def loady(self, filename, vertex, col):
        data1 = xlrd.open_workbook(filename)
        table = data1.sheets()[0]
        nrow = table.nrows
        for i in range(1, 10):
            self.y[vertex].append(table.row(i)[col].value)

    def loadParam(self, i):
        self.y = [[], [], [], []]
        self.loady("HIS/his.xls", 0, i)
        self.loady("ICC/icc.xls", 1, i)
        self.loady("BICC/bicc.xls", 2, i)
        self.loady("bangbd.xls", 3, i)

    def draw_Runtime(self):
        plt.figure()
        self.y = [[], [], [], []]
        self.loady("HIS/his.xls", 0, 1)
        self.loady("ICC/icc.xls", 1, 1)
        self.loady("BICC/bicc.xls", 2, 1)
        self.loady("bangbd.xls", 3, 1)

        plt.plot(self.x, self.y[0], label='HIS', marker='o', color='r')
        plt.plot(self.x, self.y[1], label='ICC', marker='o', color='g')
        plt.plot(self.x, self.y[2], label='BICC', marker='o', color='b')
        plt.plot(self.x, self.y[3], label='bangbd', marker='o', color='y')
        plt.xlabel("k_value")
        plt.ylabel("Runtime")
        plt.legend()
        plt.savefig('ALL/Runtime.jpg')

    def draw_Precision(self):
        plt.figure()
        self.y = [[], [], [], []]
        self.loady("HIS/his.xls", 0, 2)
        self.loady("ICC/icc.xls", 1, 2)
        self.loady("BICC/bicc.xls", 2, 2)
        self.loady("bangbd.xls", 3, 2)
        plt.plot(self.x, self.y[0], label = 'HIS', marker = 'o', color = 'r')
        plt.plot(self.x, self.y[1], label = 'ICC', marker = 'o', color = 'g')
        plt.plot(self.x, self.y[2], label = 'BICC', marker = 'o', color = 'b')
        plt.plot(self.x, self.y[3], label = 'bangbd', marker = 'o', color = 'y')
        plt.xlabel("k_value")
        plt.ylabel("Precision")
        plt.legend()
        plt.savefig('ALL/Precision.jpg')

    def draw_Recall(self):
        plt.figure()
        self.y = [[], [], [], []]
        self.loady("HIS/his.xls", 0, 3)
        self.loady("ICC/icc.xls", 1, 3)
        self.loady("BICC/bicc.xls", 2, 3)
        self.loady("bangbd.xls", 3, 3)

        plt.plot(self.x, self.y[0], label='HIS', marker='o', color='r')
        plt.plot(self.x, self.y[1], label='ICC', marker='o', color='g')
        plt.plot(self.x, self.y[2], label='BICC', marker='o', color='b')
        plt.plot(self.x, self.y[3], label='bangbd', marker='o', color='y')
        plt.xlabel("k_value")
        plt.ylabel("recall")
        plt.legend()
        plt.savefig('ALL/Recall.jpg')

    def draw_F1_score(self):
        plt.figure()
        self.y = [[], [], [], []]
        self.loady("HIS/his.xls", 0, 4)
        self.loady("ICC/icc.xls", 1, 4)
        self.loady("BICC/bicc.xls", 2, 4)
        self.loady("bangbd.xls", 3, 4)

        plt.plot(self.x, self.y[0], label='HIS', marker='o', color='r')
        plt.plot(self.x, self.y[1], label='ICC', marker='o', color='g')
        plt.plot(self.x, self.y[2], label='BICC', marker='o', color='b')
        plt.plot(self.x, self.y[3], label='bangbd', marker='o', color='y')
        plt.xlabel("k_value")
        plt.ylabel("F1_score")
        plt.legend()
        plt.savefig('ALL/F1_score.jpg')

    def draw_rou_value(self):
        plt.figure()
        self.y = [[], [], [], []]
        self.loady("HIS/his.xls", 0, 5)
        self.loady("ICC/icc.xls", 1, 5)
        self.loady("BICC/bicc.xls", 2, 5)
        self.loady("bangbd.xls", 3, 5)

        plt.plot(self.x, self.y[0], label='HIS', marker='o', color='r')
        plt.plot(self.x, self.y[1], label='ICC', marker='o', color='g')
        plt.plot(self.x, self.y[2], label='BICC', marker='o', color='b')
        plt.plot(self.x, self.y[3], label='bangbd_graph', marker='o', color='y')
        plt.xlabel("k_value")
        plt.ylabel("rou_value")
        plt.legend()
        plt.savefig('ALL/rou_value.jpg')

    def draw_All(self):
        self.draw_Precision()
        self.draw_F1_score()
        self.draw_Recall()
        self.draw_Runtime()
        self.draw_rou_value()

if __name__=='__main__':
    t = total()
    t.draw_All()