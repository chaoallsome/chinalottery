#!/usr/bin/env python
#coding: utf-8 
"""
    db.py
    xx/xx/20xx
    ~~~~~~~~

    Description of db.py
    Copyright
"""

__version__ = ''
__author__ = 'HaiBin Fu <haibinfu@gmail.com>'
__url__ = 'https://plus.google.com/116482646689120533058'
__license__ = ''
__docformat__ = 'restructuredtext'
__all__ = []

import sys
import getopt
import sqlite3
from historyFetcher import HistoryFetcher
import urllib

USAGE = """
.py usage...
"""

u'''双色球数据库类，用于对数据库的所有操作进行封装'''
class SsqDb:
    def __init__(self,dbfile):
        self.dbfile = dbfile
    u'''创建主表'''
    def crateTableSsq(self):
        try:
            conn = sqlite3.connect(self.dbfile)
            try:
                c= conn.cursor()
                c.execute('''create table ssq(id integer primary key,open date,r1 integer,r2 integer,r3 integer,r4 integer,r5 integer,r6 integer,b integer,money integer,first integer,second integer)''')
                conn.commit()
            finally:
                conn.close()
        except:
            pass
    u'''在主表中插入一行数据'''
    def insertToSsq(self,data):
        conn = sqlite3.connect(self.dbfile)
        try:
            c = conn.cursor()
            dataStr = ','.join(data)
            c.execute('''insert into ssq values (''' + dataStr + ''')''')
            conn.commit()
        finally:
            conn.close()
    u'''将数据处理为适合插入数据库的模式'''
    def handle_items(self,items):
        for item in items:
            temp = "'" + item[0] +"'"
            item[0] = item[1]
            item[1] = temp
            item[9] = ''.join(item[9].split(','))
        return items
    u'''更新数据库，将双色球开奖数据更新至最新'''
    def updateDb(self):
        hf = HistoryFetcher()
        urlStr =  'http://kaijiang.zhcw.com/zhcw/html/ssq/list_'
        latest = self.fetchLatest()
        i = 1
        while True:
            content = urllib.urlopen(urlStr+str(i)+'.html').read()
            hf.feed(content)
            items = self.handle_items(hf.items)
            flag = False
            for item in items:
                if int(item[0]) > latest[0]:
                    self.insertToSsq(item)
                else:
                    flag = True
                    break
            if flag:
                break


    u'''取得所有开奖数据'''
    def fetchAll(self):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        rec = c.execute('''select * from ssq order by id desc''')
        result = c.fetchall()
        conn.close()
        return result

    u'''在数据库中取得最新一期开奖数据'''
    def fetchLatest(self):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        rec = c.execute('''select * from ssq order by id desc''')
        result = c.fetchone()
        conn.close()
        return result

    u'''取得所有红球的开奖数据''' 
    def fetchAllRedBall(self):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        rec = c.execute('''select r1,r2,r3,r4,r5,r6 from ssq order by id desc''')
        result = c.fetchall()
        conn.close()
        return result

    u'''取得最新一期的红球数据'''
    def fetchLatestRedBall(self):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        rec = c.execute('''select r1,r2,r3,r4,r5,r6 from ssq order by id desc''')
        result = c.fetchone()
        conn.close()
        return result

    u'''取得所有蓝球的开奖数据'''
    def fetchAllBlueBall(self):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        rec = c.execute('''select b from ssq order by id desc''')
        result = c.fetchall()
        conn.close()
        return result

    u'''按期号取得某期开奖数据'''
    def fetchById(self,id):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        rec = c.execute('''select * from ssq where id = '''+str(id))
        result = c.fetchone()
        conn.close()
        return result

    u'''打印数据库中所有内容'''
    def printSsq(self):
        print self.fetchAll()


if __name__ == '__main__':
    db = SsqDb('ssqdb')
    print(u'''数据库模块测试,打印数据库中最新一期数据''')
    print(db.fetchLatest())
    print(u'''更新数据库''')
    db.updateDb()
    print(u'''再次打印最新一期数据''')
    print(db.fetchLatest())
    print(u'''取最新一期红球数据''')
    print(db.fetchLatestRedBall())
    print(u'''打印所有红球数据''')
    print(db.fetchAllRedBall())

