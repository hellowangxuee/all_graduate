#uncoding:utf-8
from Data import *
import sqlite3
from BICC import *
if __name__ == '__main__':
    #数据已插入
    data = Data()
    #data.insertData()
    '''icc = ICC()
    icc.loadData()
    #icc.drawDegree()
    q = icc.algorithmICC(10)
    while not q.empty():
        print q.get()'''
    bicc = BICC()
    q = bicc.algorithmBICC(10,20,2)
    while not q.empty():
        print  q.get()