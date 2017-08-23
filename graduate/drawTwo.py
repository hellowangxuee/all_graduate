import matplotlib.pyplot as plt
import xlrd
#画出关于ICC以及BICC的运行时间对比图

class drawTwo():
    def __init__(self):
        self.x = []
        self.runtimeYicc = []
        self.runtimeYbicc = []
        self.xlabel = ''
        self.runtimeYlabel = ''
        self.loadExcel('ICC\icc.xls')
        self.loadExcelbicc('BICC\\bicc.xls')


    def loadExcel(self, filename1):
        data = xlrd.open_workbook(filename1)
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        self.xlabel = table.row(0)[0].value
        self.runtimeYlabel = table.row(0)[1].value
        for i in range(1, nrows):
            self.x.append(int(table.row(i)[0].value))
            self.runtimeYicc.append(float(table.row(i)[1].value))

    def loadExcelbicc(self, filename):
        data = xlrd.open_workbook(filename)
        table = data.sheets()[0]
        nrows = table.nrows
        for i in range(1, nrows):
            self.runtimeYbicc.append(float(table.row(i)[1].value))

    def drawTwopicture(self):
        plt.figure()
        plt.xlabel(self.xlabel)
        plt.ylabel(self.runtimeYlabel)
        plt.plot(self.x, self.runtimeYicc, label='ICC', marker='o', color='g')
        plt.plot(self.x, self.runtimeYbicc, label='BICC', marker='o', color='b')
        plt.legend()
        plt.savefig('ALL\iccBicc.jpg')


if __name__ == '__main__':
    drawtwo = drawTwo()
    drawtwo.drawTwopicture()