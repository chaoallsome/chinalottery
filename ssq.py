#!/usr/bin/env python
#coding: utf-8 
u"""
    ssq.py
    11/04/2012
    ~~~~~~~~

    Description of test.py
        自动从中彩网网站获取双色球开奖数据
    按照一定规则筛选下期开奖号码。
    分析：按照彩票中奖指南所提供的方法，给出中奖号码各个指标分析。
    选号：按照分析指标，采用权值的方式，选出最初一批供选择的号码。
    杀号：根据必不能选原则，对低概率模式组合号码进行删除，对高概率模式组合号码予以优先。
    出号：选出1到多注准备投注的号码，并予以保存。待开奖后，由程序自动判定中奖情况。
    Copyright
    过滤器：连号过滤，历史号码过滤，区间过滤
"""

__version__ = ''
__author__ = 'HaiBin Fu <haibinfu@gmail.com>'
__url__ = 'https://plus.google.com/116482646689120533058'
__license__ = ''
__docformat__ = 'restructuredtext'
__all__ = []

import sys
import getopt

USAGE = u"""
使用说明
"""


import cmd
from ballAnalytics import BallAnalytics
from db import SsqDb

#from historyFetcher import HistoryFetcher



u'''该类检查是否中奖以及奖金数额'''
class CheckMax:
    def __init__(self,ssqDb,ballAnalytics):
        ssqDb.updateDb()
        self.db = ssqDb
        self.data = ssqDb.fetchAll()
        self.redBalls = ssqDb.fetchAllRedBall()
        self.blueBalls = ssqDb.fetchAllBlueBall()
        self.ba = ballAnalytics

        self.redWeightA = 1 #红球最近未出现的期数
        self.redWeightB = 1 #红球出现的总次数
        self.redWeightC = 1 #最近33期中红球出现的总次数
        self.redWeightD = 1
        self.redWeightE = 1

        self.blueWeightA = 1 #蓝球最近未出现的期数
        self.blueWeightB = 1 #红球出现的总期数
        self.blueWeightC = 1 #最近16期中红球出现的次数
        self.blueWeightD = 1
        self.blueWeightE = 1

        self.oeWeight = 0   #奇数偶数偏差追踪
        self.tzWeight = 0   #三分区偏差最总
        self.bsWeight = 0   #大数小数偏差追踪
        self.svWeight = 0   #和值偏差追踪
        self.onWeight = 0   #遗漏数字偏差追踪
        self.lnWeight = 0   #尾数偏差追踪

        #self.redWeight = [0]*33


    u'''检查所给号码是否中奖以及是几等奖,返回0为未中奖'''
    def checkAward(self,target,data):
        blueBall = 0
        redBall = 0
        award = 0
        if data[-1] == target[-1]:
            blueBall = 1
        for item in data[0:-1]:
            if item in target[0:-1]:
                redBall += 1

        if blueBall and  (redBall < 3):
            award = 6
        if (blueBall + redBall) == 4:
            award = 5
        if (blueBall + redBall) == 5:
            award = 4
        if blueBall and (redBall == 5):
            award = 3
        if (blueBall == 0) and (redBall == 6):
            award = 2
        if blueBall and (redBall == 6):
            award = 1
        return award
        
    u'''检查奖金数额,输入为几等奖及注数'''
    def checkMoney(self,award,number):
        awards = (0,10000000,500000,3000,200,10,5)
        return awards[award] * number

    u'''检查所给红球号码中了几个号码'''
    def checkRed(self,target,data):
        redball = 0
        for item in data:
            if item in target:
                redball += 1

        return redball

    u'''检查所给蓝球号码是否为中奖号码'''
    def checkBlue(self,target,data):
        blueball = 0
        if data == target:
            blueball += 1

        return blueball


    u'''权值相加'''
    def addWeight(self,data,weight,base):
        res = map(lambda x,y:x+y, [weight*x for x in data], base)
        return res

    u'''红球权值计算'''
    def redWeight(self,data):
        #red = map(lambda x,y,z:x+y+z,[self.redWeightA*x for x in a],[self.redWeightB*x for x in b],[self.redWeightC*x for x in c])
        #print red
        red = [0]*33
        red = self.addWeight(self.ba.oddAndEvenWeight(data[:5]),self.oeWeight,red)
        red = self.addWeight(self.ba.threeZonesWeight(data[:5]),self.tzWeight,red)
        red = self.addWeight(self.ba.bigAndSmallWeight(data[:5]),self.bsWeight,red)
        red = self.addWeight(self.ba.sumValueWeight(data[:5]),self.svWeight,red)
        red = self.addWeight(self.ba.omittedNumberWeight(data,5),self.onWeight,red)
        red = self.addWeight(self.ba.lastNumberWeight(data[:5]),self.lnWeight,red)

        return red



    
    u'''蓝球权值计算'''
    def blueWeight(self,a,b,c):
        blue = map(lambda x,y,z:x+y+z, [self.blueWeightA*x for x in a],[self.blueWeightB*x for x in b],[self.blueWeightC*x for x in c])
        #print  blue
        return blue

    u'''将所给数据赋予序号后进行排序'''
    def order(self,data):
        t = [0]*len(data)
        for i in range(0,len(data)):
            t[i] = (i+1, data[i])
        t = sorted(t, key=lambda x:x[1], reverse = True)
        #print t
        return t

    u'''在当前权值下，选出最优号码'''
    def bestBall(self,redWeight,blueWeight):
        res = []
        for x in range(0,6):
            res.append(self.order(redWeight)[x][0])
        res.append(self.order(blueWeight)[0][0])
        #print(u"当前最优号码：" + str(res))
        return res
    u'''在当前权值下，选出最优红球号码'''
    def bestRed(self,redweight):
        topNumber = []
        res = []
        for x in range(0,8):
            topNumber.append(self.order(redweight)[x][0])
        tmp = self.ba.generateRedNumber(topNumber,6)
        flag = [True]*len(tmp)
        for x in range(0,len(tmp)):
            if self.ba.isHistoryNumber(tmp[x],self.data):  #历史数据去掉
                flag[x] = False
            if self.ba.isConsecutiveNumber(tmp[x]):
                flag[x] = False
        for x in range(0,len(tmp)):
            if flag[x]:
                res = tmp[x]
        return res


    u'''在当前权值下的当期中奖情况'''
    def currentWeightAward(self,target,data):
        #rWeight = self.redWeight(self.ba.redDistance([x[2:8] for x in data]),self.ba.redTimes([x[2:8] for x in data]),self.ba.redTimes([x[2:8] for x in data[0:5]]))
        #bWeight = self.blueWeight(self.ba.blueDistance([x[8] for x in data]),self.ba.blueTimes([x[8] for x in data]),self.ba.blueTimes([x[8] for x in data[0:5]]))
        #bb = self.bestBall(rWeight,bWeight)
        #res = self.checkAward(target,bb)
        #print (u'''当前最优号码：''' + str(bb))
        #print (u'''当前中奖号码：''' + str(target))
        #print (u'''当前预测结果：''' + str(res))
        #return res
        pass

    def getgetget(self):
        res = [0]*9
        tLen = len(self.redBalls)-33
        for x in range(tLen,0,-1):
            #print (u'''期号：''' + str(self.data[x][0]))
            award = self.checkRed(self.redBalls[x],self.bestRed(self.redWeight(self.redBalls[x+1:])))
            res[award] += 1
            res[8] += award
            if award > 2:
                res[7] += 1

                #res[9] += self.checkMoney(award,1)
                

        #print (u'''总期数：''' + str(tLen))
        #print (u'''中奖期数：''' + str(res[7]))
        #print (u'''奖项之和：''' + str(res[8]))
        #print (u'''总奖金：''' + str(res[9]))
        #print (u'''总花费：''' + str(tLen*2))
        #print (u'''总收益：''' + str((res[9]-tLen)*100/tLen*2) + '%') 
        #print (u'''奖项分布：''' + str([res]))
        return res
    
    def bestWeight(self):
        weight = [0]*6
        maxAward = [0]*9
        for a in range(0,10):
            self.oeWeight = a
            for b in range(0,1):
                self.tzWeight = b
                for c in range(0,10):
                    self.bsWeight = c
                    for d in range(0,10):
                        self.svWeight = d
                        for e in range(0,10):
                            self.onWeight = e
                            for f in range(0,10):
                                self.lnWeightC = f
                                res = self.getgetget()
                                #print (u'''当前权值：''' + str(f))
                                if res[7] >  maxAward[7]:
                                    maxAward = [x for x in res]
                                    weight[0] = self.oeWeight
                                    weight[1] = self.tzWeight
                                    weight[2] = self.bsWeight
                                    weight[3] = self.svWeight
                                    weight[4] = self.onWeight
                                    weight[5] = self.lnWeight
                                    print (u'''当前最佳权值:''' + str(weight))
                                    print (u'''当前最佳成绩:''' + str(res))
                                
        print(u'''-------------------------------------------------------------------''')
        print(u'''最佳权值：''' + str(weight))
        print(u'''最佳成绩：''' + str(maxAward))

        print(u'''-------------------------------------------------------------------''')



u'''命令行界面'''
class CmdUI(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
    def help_EOF(self):
        print u"系统退出!!!"
    def do_EOF(self,line):
        print u"系统退出!!!"
        sys.exit()

    def help_getbyid(self):
        print u"这是一个命令行测试!"
    def do_test(self,id):
        print "System Exit"
        sys.exit()

if __name__ == '__main__':
    #par = HistoryFetcher()
    urlStr =  'http://kaijiang.zhcw.com/zhcw/html/ssq/list_'
    
    #i = 1
    #while i <= 66:
    #    content = urllib.urlopen(urlStr + str(i) + '.html').read()
    #    par.feed(content)
    #    i += 1

    #print len(par.items)

    #db = SsqDb('ssqdb')
    #ba = BallAnalytics()
    cm = CheckMax(SsqDb('ssqdb'),BallAnalytics())
    #cm.getgetget()
    #print cm.redWeight(cm.redBalls)
    cm.bestWeight()

    #db.crateTableSsq()
    #i = len(par.items)
    #items = handle_items(par.items)
    #while i > 0:
    #    i -= 1
    #    db.insertToSsq(items[i])
    #    print items[i]
    #db.printSsq()
    #print db.fetchAll()
    #print db.fetchAllRedBall()
    #db.updateDb()
    #print db.fetchLatest()

    #print db.fetchLatest()
    #c = CmdUI()
    #c.cmdloop()