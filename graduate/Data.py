#uncoding:utf-8
import sqlite3

class Data():

    #连接数据库
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.conn.close()

    def insertData(self):
        #插入节点关系图数据graph
        self.conn = sqlite3.connect("data.db")
        self.conn.execute('''create table graph
            (first int,
            second int);''')
        with open("Twitter/twitter.dat") as df:
            for d in df:
                sql = "insert into graph(first,second) values(%d,%d)" % (
                int(d.strip().split(' ')[0]), int(d.strip().split(' ')[1]))
                self.conn.execute(sql)
        #self.conn.commit()
        #插入节点所属的社团community
        self.conn.execute('''
                    CREATE TABLE COMMUNITY
                    (only int);
            ''')
        print 'table community create successfully'
        with open("Twitter/community.txt") as df:
            for d in df:
                sql = "insert into community(only) values(%d)" % (int(d.strip()))
                self.conn.execute(sql)

        self.conn.commit()
        self.conn.close()

    def selectGraph(self):
        self.conn = sqlite3.connect("data.db")
        sql = "select * from graph"
        cursor = self.conn.execute(sql)
        self.conn.close()
        return cursor

    def selectCommunity(self):
        self.conn = sqlite3.connect("data.db")
        sql = "select * from community"
        cursor = self.conn.execute(sql)
        self.conn.close()
        return cursor

if __name__=='__main__':
    data = Data()
    data.insertData()
    conn = sqlite3.connect('data.db')
    sql = "select * from graph"
    cursor = conn.execute(sql)
    print cursor.arraysize
    conn.close()