#!/usr/bin/env python
#coding: utf-8 
u"""
    ballAnalytics.py
    xx/xx/20xx
    ~~~~~~~~

    Description of ballAnalytics.py
    Copyright
    区间分析，将号码分为3个区，统计落在每个区的号码情况。
    奇数偶数分析：分析中奖号码奇数偶数分布比例。
    大小数字模式分析：统计大小数字落在各个区的模式概率，并记入数据库，用于对所选号码进行中奖概率评估。
    相邻数字分析：给相邻数字赋予权值，用于生成胆码。统计相邻数字出现情况。
    统计数字连续出现的情况：统计各号码在过去5期连续出现的情况，并统计概率。
    统计数字连续遗漏的情况：统计各号码在过去5期连续遗漏的情况，并统计概率。
    和值统计：统计中奖号码红球和值分布范围。
    冷号，热号，温号统计：在规定期数出现X次以上算热号，出现Y次以下算冷号，介于两者之间算温号。
    尾号情况：68%的红球尾号中有2个相同，3个以上相同的仅占7%，0个尾号相同的约占25%。所以，应杀3个以上尾号相同的，优先选2个尾号相同的。

"""

__version__ = ''
__author__ = 'HaiBin Fu <haibinfu@gmail.com>'
__url__ = 'https://plus.google.com/116482646689120533058'
__license__ = ''
__docformat__ = 'restructuredtext'
__all__ = []

import sys
import getopt
from db import SsqDb
import types

USAGE = """
.py usage...
"""
u'''
该类对双色球数据进行分析
'''
class BallAnalytics:
    def __init__(self):
        pass

    u'''计算蓝球最近未出现的期数'''
    def blueDistance(self,data):
        b = [100]*16
        for i in range(1,17):
            #for x in range(0,len(data)):
            for x in range(0,5):
                if data[x] == i: 
                    b[i-1] = x
                    break
        return b

    u'''计算红球最近未出现的期数,所给数据为最新到最旧倒序排列'''
    def redDistance(self,data):
        r = [100]*33
        for i in range(1,34):
            #for x in range(0,len(data)):
            for x in range(0,5):
                if i in data[x]:
                    r[i-1] = x
                    break
        return r
    
    u'''计算所给数据中蓝色球出现的总次数'''
    def blueTimes(self,data):
        b = [0]*16
        for item in data:
            b[item-1] += 1
        return b

    u'''计算所给数据中红色球出现的总次数'''
    def redTimes(self,data):
        r = [0]*33            
        for item in data:
            for i in range(0,6):
                r[item[i]-1] += 1
        return r

    u'''计算所给的数据中奇数和偶数的个数，输入为一个列表，输出结果为一个包含两个整数项的元组，第一项为奇数个数，第二项为偶数个数'''
    def oddAndEven(self,data):
        odd = 0
        even = 0
        if (type(data[0]) is types.IntType):
            for item in data:
                if item % 2 == 0:
                    even += 1
                else:
                    odd += 1
        else:
            for item in data:
                for x in item:
                    if x % 2 == 0:
                        even += 1
                    else:
                        odd += 1
        return (odd,even)

    u'''计算奇偶数权值，输入为3期、5期、10期等的红球数据列表，输出为有33个项的奇偶数权值列表'''
    def oddAndEvenWeight(self,data):
        res = [0]*33
        tmp = self.oddAndEven(data)
        oe = tmp[0] - tmp[1]
        weight = (2*abs(oe))/len(data)
        if oe > 0:
            for x in range(1,33,2):
                res[x] += weight
        else:
            for x in range(0,33,2):
                res[x] += weight
        return res


    u'''计算所给数据中号码在三个区域中的分布情况：1-11为0区，12-22为1区，23-33为2区，输入为一个列表，返回一个三个整数项的元组'''
    def threeZones(self,data):
        zone0 = zone1 = zone2 = 0
        if (type(data[0]) is types.IntType):
            for item in data:
                if item <= 11:
                    zone0 += 1
                elif item <= 22:
                    zone1 += 1
                else:
                    zone2 += 1
        else:
            for item in data:
                for x in item:
                    if x <= 11:
                        zone0 += 1
                    elif x <= 22:
                        zone1 += 1
                    else:
                        zone2 += 1
        return (zone0,zone1,zone2)

    u'''计算三分区权值情况，输入为一个列表，输出为按三分区调整后的权值情况列表'''
    def threeZonesWeight(self,data):
        res = [0]*33
        
        return res

    u'''给定n个号码，(n>=6)，列出这n个号码可能产生的所有p个红球组合，输入为1个列表，输出为所有可能号码列表'''
    def generateRedNumber(self,data,number):
        res = []
        if number == 1:
            for item in data:
                res.append([item])
        else:
            for x in range(0,len(data)-number+1):
                tmp = [data[x]]
                for item in self.generateRedNumber(data[x+1:],number-1):
                    tmp += item
                    res.append(tmp)
                    tmp = [data[x]]

        return res




    u'''计算所给数据中大数和小数分布情况，小于等于17为小数，大于17为大数，返回一个二元元组，小数在前，大数在后'''
    def bigAndSmall(self,data):
        big = small = 0
        if (type(data[0]) is types.IntType):
            for item in data:
                if item <= 17:
                    small += 1
                else:
                    big += 1
        else:
            for item in data:
                for x in item:
                    if x <= 17:
                        small += 1
                    else:
                        big += 1
        return (small,big)

    u'''计算大小数权值，输入为3期，5期，10期等红球数据列表，输出为有33个项的大小数权值列表'''
    def bigAndSmallWeight(self,data):
        res = [0]*33
        tmp = self.bigAndSmall(data)
        bs = tmp[0] - tmp[1]
        weight = 2*abs(bs)/len(data)
        if bs > 0:
            for x in range(17,33):
                res[x] += weight
        else:
            for x in range(0,17):
                res[x] += weight

        return res



    u'''计算所给数据的和值，返回一个整数'''
    def sumValue(self,data):
        sumvalue = 0 
        for item in data:
            sumvalue += item
        return sumvalue

    u'''计算一组数据的平均和值，返回平均数(平均数取下整数)'''
    def averageSumValue(self,data):
        averagesumvalue = 0
        for item in data:
            averagesumvalue += self.sumValue(item)
        return averagesumvalue/(len(data))

    u'''计算给定范围内的和值钟形曲线最顶端部分的比例,输入为1个宽度和历史数据列表，输出为以102为中心，两边各扩展宽度范围内的和值所占比例'''
    def maxSumValue(self,width,data):
        count = 0
        for item in data:
            if (self.sumValue(item) >= 102-width) and (self.sumValue(item) <= 102+width):
                count += 1
        res = count/(len(data) + 0.0)
        res = res*100
        return res  

    u'''计算和值追踪权值，输入为近期红球数据列表，输出为和值追踪系数'''
    def sumValueWeight(self,data):
        res = [0]*33
        sv = 0
        if type(data[0]) is types.IntType:
            sv = self.sumValue(data) - 102
        else:
            sv = self.averageSumValue(data) - 102
        if abs(sv) > 40:
            weight = 2
        else:
            weight = 1
        if sv > 0:
            for x in range(0,6):
                res[x] += 2*weight
            for x in range(6,12):
                res[x] += weight
        elif sv < 0:
            for x in range(21,27):
                res[x] += weight
            for x in range(27,33):
                res[x] += 2*weight

        return res





    u'''计算所给数据的末位数字相同的个数，输入为1个列表，输出为末位数字相同的数字个数'''
    def sameLastNumber(self,data):
        count = 1
        maxCount = 1
        lst = list(data)
        lst = [x%10 for x in lst]
        lst.sort()
        for x in range(0,len(lst)-1):
            if lst[x+1] == lst[x]:
                count += 1
                if count > maxCount:
                    maxCount = count
            else:
                count = 1
        return maxCount







    u'''计算所给红球数据是否为历史中奖数据,是则返回1，否则返回0'''
    def isHistoryNumber(self,target,data):
        t = tuple(target)
        if t in data:
            return 1
        else:
            return 0

    u'''判断所给号码是否为连续数字，如有4个以上（含4个）连续数字，则返回1，否则返回0'''
    def isConsecutiveNumber(self,data):
        lst = list(data)
        lst.sort()
        cCount = 1
        maxCount = 1
        for x in range(0,len(lst)-1):
            if lst[x+1] - lst[x] == 1:
                cCount += 1
                if cCount > maxCount:
                    maxCount = cCount
            else:
                cCount = 1
        if maxCount < 4:
            return 0
        else:
            return 1

    u'''计算所给号码的相邻号码，输入为一个包含6个数字项的列表，输出为33项整数组成的列表'''
    def neighborNumber(self,data):
        lst = [0]*33
        for item in data:
            lst[(item+1)%33] += 1
            lst[(item-1)%33] += 1

        res = lst[1:]
        res.append(lst[0])
        return res


    u'''计算某期数据遗漏情况，输入为2项，1是当期开奖数据，2是当期之前的历史开奖数据,输出为1个7项列表'''
    def hotColdNumber(self,target,data):
        res = [0]*7
        for x in range(0,len(target)):
            for y in range(0,len(data)):
                res[x] = y
                if target[x] in data[y]:
                    break
        for item in res[0:6]:
            res[6] += item
        #print res
        return res

    u'''遗漏数字偏差追踪,输入为历史数据列表data，和要计算的期数number,输出为1个遗漏数字统计列表，'''
    def omittedNumber(self,data,number):
        res = [0]*number
        t = [0]*number
        for x in range(0,number):
            tmp = self.hotColdNumber(data[x],data[x+1:])
            for i in range(0,number):
                if i in tmp:
                    res[i] += 1
        
        for m in range(0,number):
            t[m] = (m,res[m])   
        t = sorted(t, key=lambda x:x[1], reverse = False)
        t = [x[0] for x in t]
        return t

    u'''计算绝对遗漏数字统计表，也就是到如果数字在下一期出现，遗漏值是多少'''
    def absoluteOmittedNumber(self,data):
        res = [0]*33
        for x in range(0,33):
            for y in range(0,len(data)):
                res[x] = y
                if (x+1) in data[y]:
                    break
        return res

    u'''遗漏数字权重计算'''
    def omittedNumberWeight(self,data,number):
        res = [0]*33
        on = self.omittedNumber(data,number)
        ao = self.absoluteOmittedNumber(data)
        #print ao
        for x in range(0,number):
            for m in range(0,33):
                if ao[m] == on[x]:
                    res[m] += 2*(number - x)
        return res

    u'''计算末尾数字偏差追踪权重'''
    def lastNumberWeight(self,data):
        res = [0]*33
        lastnumber = [0]*10
        t = [0]*10
        for item in data:
            for x in item:
                lastnumber[x%10] += 1
        for m in range(0,10):
            t[m] = (m,lastnumber[m])
        t = sorted(t, key=lambda x:x[1], reverse = False)
        #print t
        t = [x[0] for x in t]
        for i in range(0,10):
            for j in range(t[i],34,10):
                if j != 0:
                    res[j-1] += (10-i)

        return res




        












if __name__ == '__main__':
    db = SsqDb('ssqdb')
    ba = BallAnalytics()
    print (u'''双色球分析模块测试''')
    #print (u'''蓝球最近未出现数''')
    print(u'''最新一期红球数据''')
    print(db.fetchLatestRedBall())
    print(u"最新一期红球奇数偶数个数")
    print(ba.oddAndEven(db.fetchLatestRedBall()))
    print(u'''所有红球奇偶数对比''')
    print(ba.oddAndEven(db.fetchAllRedBall()[0:10]))
    print(u'''过去3期，5期，10期红球奇偶数情况以及权值情况''')
    print(ba.oddAndEven(db.fetchAllRedBall()[0:3]))
    print(ba.oddAndEvenWeight(db.fetchAllRedBall()[0:3]))
    print(ba.oddAndEven(db.fetchAllRedBall()[0:4]))
    print(ba.oddAndEvenWeight(db.fetchAllRedBall()[0:4]))
    print(ba.oddAndEven(db.fetchAllRedBall()[0:5]))
    print(ba.oddAndEvenWeight(db.fetchAllRedBall()[0:5]))
    print(ba.oddAndEven(db.fetchAllRedBall()[0:10]))
    print(ba.oddAndEvenWeight(db.fetchAllRedBall()[0:10]))

    print(u'''最新一期红球区域情况''')
    print(ba.threeZones(db.fetchLatestRedBall()))
    print(u'''所有红球区域情况''')
    print(ba.threeZones(db.fetchAllRedBall()))
    print(u'''最新一期大数小数分布情况''')
    print(ba.bigAndSmall(db.fetchLatestRedBall()))
    print(u'''过去3,4，5,10期红球大小数分布情况以及权值情况''')
    print(ba.bigAndSmall(db.fetchAllRedBall()[0:3]))
    print(ba.bigAndSmallWeight(db.fetchAllRedBall()[0:3]))
    print(ba.bigAndSmall(db.fetchAllRedBall()[0:4]))
    print(ba.bigAndSmallWeight(db.fetchAllRedBall()[0:4]))
    print(ba.bigAndSmall(db.fetchAllRedBall()[0:5]))
    print(ba.bigAndSmallWeight(db.fetchAllRedBall()[0:5]))
    print(ba.bigAndSmall(db.fetchAllRedBall()[0:10]))
    print(ba.bigAndSmallWeight(db.fetchAllRedBall()[0:10]))

    print(u'''所有红球大数小数分布情况''')
    print(ba.bigAndSmall(db.fetchAllRedBall()))
    print(u'''最新一期红球的和值''')
    print(ba.sumValue(db.fetchLatestRedBall()))
    print(u'''所有红球的平均和值''')
    print(ba.averageSumValue(db.fetchAllRedBall()))
    print(u'''过去1,3,4,5,10期间红球和值分布情况以及权值情况''')
    print(ba.sumValue(db.fetchAllRedBall()[0]))
    print(ba.sumValueWeight(db.fetchAllRedBall()[0]))
    print(ba.averageSumValue(db.fetchAllRedBall()[0:3]))
    print(ba.sumValueWeight(db.fetchAllRedBall()[0:3]))
    print(ba.averageSumValue(db.fetchAllRedBall()[0:4]))
    print(ba.sumValueWeight(db.fetchAllRedBall()[0:4]))
    print(ba.averageSumValue(db.fetchAllRedBall()[0:5]))
    print(ba.sumValueWeight(db.fetchAllRedBall()[0:5]))
    print(ba.averageSumValue(db.fetchAllRedBall()[0:10]))
    print(ba.sumValueWeight(db.fetchAllRedBall()[0:10]))
    print(u'''查看某一组红球号码是否在历史上中过奖''')
    print(ba.isHistoryNumber(db.fetchLatestRedBall(),db.fetchAllRedBall()))
    print(ba.isHistoryNumber([1,2,3,4,5,6],db.fetchAllRedBall()))
    
    print(u'''历史上的重复红球号码''')
    count = 0
    redData = db.fetchAllRedBall()
    for x in range(1,len(redData)-1):
        if ba.isHistoryNumber(redData[x+1],redData[0:x]):
            count += 1
            print(redData[x+1])
    print(u'''总共重复期数：''' + str(count))



    print(u'''判断所给号码中是否含有若干个连续号码''')
    print(ba.isConsecutiveNumber([33,31,32,30,29,28]))
    
    count = 0
    for item in db.fetchAllRedBall():
        if ba.isConsecutiveNumber(item):
            count += 1
            print item
    print(u'''历史中奖数据中红球有4个以上连续号码的期数:''' + str(count))

    print(u'''打印一组数字的相邻数字''')
    print(ba.neighborNumber([2,6,10,14,22,26]))

    print(u'''给定单边宽度为40时顶端和值所占比例''')
    print(ba.maxSumValue(40,db.fetchAllRedBall()))

    print(u'''最新一期红球尾数相同的情况''')
    print(ba.sameLastNumber(db.fetchLatestRedBall()))

    print(u'''红球历史数据中尾数相同的号码小于等于2个所占比例''')
    res = 0.0
    for item in db.fetchAllRedBall():
        if ba.sameLastNumber(item) <= 2:
            res += 1
    print((res/(len(db.fetchAllRedBall())+0.0))*100)

    print(u'''测试号码生成函数''')
    print(ba.generateRedNumber([1,2,3,4,5,6,7,8],6))

    print(u'''所有期数平均遗漏情况，平均连号情况，遗漏少于10的号码个数平均情况''')
    #print(ba.omittedNumber(db.fetchAllRedBall()[0],db.fetchAllRedBall()[1:]))
    data = db.fetchAllRedBall()
    count1 = count2 = count3 = 0
    for x in range(0,len(data)-10):
        on = ba.hotColdNumber(data[x],data[x+1:])
        count1 += on[6]
        for item in on[0:6]:
            if item == 0:
                count2 += 1
            if item < 10:
                count3 += 1
    print(count1/(len(data)-10.0),count2/(len(data)-10.0),count3/(len(data)-10.0))

    print(u'''最近5期开奖数据的遗漏情况表''')
    print(ba.omittedNumber(db.fetchAllRedBall(),5))
    print(u'''由最近5期遗漏情况计算权值''')
    print(ba.omittedNumberWeight(db.fetchAllRedBall(),5))

    print(u'''最近5期开奖数据的末位数字偏差追踪表''')
    print(ba.lastNumberWeight(db.fetchAllRedBall()[:5]))

