#uncoding:utf-8
import matplotlib.pyplot as plt
import xlrd
#画出各个算法的衡量指标对比图


class Draw():
    def __init__(self, filename):
        self.x = []
        self.RTy = []
        self.Py = []
        self.Ry = []
        self.Fy = []
        self.Rouy = []
        self.xlabel =''
        self.RTylabel = ''
        self.Pylabel = ''
        self.Rylabel = ''
        self.Fylabel = ''
        self.Rouylabel = ''
        self.loadExcel(filename)

    def loadExcel(self, filename1):
        data = xlrd.open_workbook(filename1)
        table = data.sheets()[0]
        nrows = table.nrows
        ncols = table.ncols
        self.xlabel = table.row(0)[0].value
        self.RTylabel = table.row(0)[1].value
        self.Pylabel = table.row(0)[2].value
        self.Rylabel = table.row(0)[3].value
        self.Fylabel = table.row(0)[4].value
        self.Rouylabel = table.row(0)[5].value
        for i in range(1, nrows):
            self.x.append(int(table.row(i)[0].value))
            self.RTy.append(float(table.row(i)[1].value))
            self.Py.append(float(table.row(i)[2].value))
            self.Ry.append(float(table.row(i)[3].value))
            self.Fy.append(float(table.row(i)[4].value))
            self.Rouy.append(float(table.row(i)[5].value))





    def drawsubplot(self):
        plt.figure()
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212)
        plt.sca(ax1)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.RTylabel)
        plt.plot(self.x,self.RTy)
        plt.sca(ax2)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.Pylabel)
        plt.plot(self.x, self.Py)
        plt.show()

    def drawP(self, foldername, x, y, xlabel, ylabel):
        plt.figure()
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.plot(x, y, "o-", linewidth = 2.0)
        #plt.show()
        plt.savefig(foldername + '/' + ylabel + '.jpg')

    def drawPicture(self, foldername):
        self.drawP(foldername, self.x, self.RTy, self.xlabel, self.RTylabel)
        self.drawP(foldername, self.x, self.Py, self.xlabel, self.Pylabel)
        self.drawP(foldername, self.x, self.Ry, self.xlabel, self.Rylabel)
        self.drawP(foldername, self.x, self.Fy, self.xlabel, self.Fylabel)
        self.drawP(foldername, self.x, self.Rouy, self.xlabel, self.Rouylabel)




if __name__=='__main__':
    '''
    plt.figure(1)  # 创建图表1  
    plt.figure(2)  # 创建图表2  
    ax1 = plt.subplot(211)  # 在图表2中创建子图1  
    ax2 = plt.subplot(212)  # 在图表2中创建子图2  
    x = np.linspace(0, 3, 100)
    for i in xrange(5):
        plt.figure(1)
        plt.plot(x, np.exp(i * x / 3))
        plt.sca(ax1)
        plt.plot(x, np.sin(i * x))
        plt.sca(ax2)
        plt.plot(x, np.cos(i * x))
    plt.show()
    '''
    # d = Draw('HIS/his.xls')
    # d.drawPicture('HIS')

    d = Draw('ICC/icc.xls')
    d.drawPicture('ICC')

    # d = Draw('BICC/bicc.xls')
    # d.drawPicture('BICC')

    # d = Draw('WX/wx.xls')
    # d.drawPicture('WX')
