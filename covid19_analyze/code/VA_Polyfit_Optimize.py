# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 15:15:51 2021

@author: sjy
"""

import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt

from scipy import integrate, optimize
import pandas as pd
from datetime import datetime,date
import heapq
import random

# 类似于快排的思想，不同的地方在于每趟只需要往一个方向走
# 按照从小到大的顺序，寻找前K个最小值
def qselect(ary_list, k):
    if len(ary_list) < k:
        return ary_list

    tmp = ary_list[0]
    left = [x for x in ary_list[1:] if x <= tmp] + [tmp]
    llen = len(left)
    if llen == k:
        return left
    if llen > k:
        return qselect(left, k)
    else:
        right = [x for x in ary_list[1:] if x > tmp]
        return left + qselect(right, k-llen)
    pass

#均方误差
def MSE(y, t, n):
    return 1 / n * np.sum((y - t)**2)

def RMSE(y, t, n):
    return pow((1 / n * np.sum((y - t)**2)), 0.5)

def AFER(y, t, n):
    return 1 / n * np.sum(abs((y - t)/y))

#求多项式系数、误差
def polyfit_optimize(xdata,ydata):
    f = np.polyfit(xdata, ydata, 3)
    #print('f1 is :\n',f1)
    p = np.poly1d(f)
    #print('p1 is :\n',p1)
    #也可使用yvals=np.polyval(f1, x)
    yvals = p(xdata)  
    #拟合y值
    #print('yvals is :\n',yvals)
    #绘图
    plt.plot(xdata, ydata, 's',label='original values')
    plt.plot(xdata, yvals, 'r',label='polyfit values')
    plt.show()
    #求误差
    MSEoffset = MSE(np.array(yvals), np.array(ydata), len(ydata))
    RMSEoffset = RMSE(np.array(yvals), np.array(ydata), len(xdata))
    #print('多项式系数：')
    #print(f)
    #print('误差值：' + str(offset))
    return (f,MSEoffset,RMSEoffset)


def omega_optimize(xdata, ydata, zdata, lambd, count1, count2):
    #随机omega
    omega = []
    #newpositivelist = []
    for i in np.arange(-10, 10, 0.1):
        #生成随机数
        #num = random.uniform(0,1)
        num = np.tanh(i)
        #添加到列表中
        num = (num + 1) / 2
        omega.append(num)
    #data1 = polyfit_optimize(xdata,ydata)
    recoverdata = polyfit_optimize(xdata,zdata)
    #lambd = 0.01
    #求恢复曲线系数
    e = recoverdata[0][0]
    f = recoverdata[0][1]
    g = recoverdata[0][2]
    h = recoverdata[0][3]
    #求确诊曲线系数
    ABCDarray = []
    for i in range(0, 100):
        a = omega[i] * e / lambd
        b = (omega[i] * f + 3 * e) / lambd
        c = (omega[i] * g + 2 * f) / lambd
        d = (omega[i] * h + g) / lambd
        temp = [a,b,c,d]
        ABCDarray.append(temp)
        #print(ABCDarray[0][3])
    
    #y = at^3+bt^2+ct+d
    #求确诊曲线的值
    res = []
    for i in range(0, 100):
        temp = []
        for t in range(count1, count2):
            y = ABCDarray[i][0] * t * t * t + ABCDarray[i][1] * t * t + ABCDarray[i][2] * t + ABCDarray[i][3]
            temp.append(y)
        res.append(temp)
    print(res)
    ##
    #误差
    offset = []
    for i in range(0, 100):
        offset.append(MSE(np.array(res[i]), ydata,len(np.array(res[i]))))
    #print(offset)
    #
    #最小误差
    min = offset[0]
    for i in range(0,100):
        if(min > offset[i]):
            min = offset[i]
            index = i
            
    return (min,omega[index],ABCDarray[index],res[index])


#修正确诊人数后
def omega_optimize_amend(xdata, ydata, zdata, lambd, count1, count2):
    #随机omega
    omega = []
    newpositivelist = []
    for i in np.arange(-100, 100, 0.1):
        #生成随机数
        num = random.uniform(0,1)
        #num = np.tanh(i)
        #添加到列表中
        #num = (num + 1) / 2
        omega.append(num)
        #修正后确诊人数
        amendlist = []
        for x,y in zip(ydata,zdata):
            amendlist.append(x - num * y)
        newpositivelist.append(amendlist)
        
    #data1 = polyfit_optimize(xdata,ydata)
    recoverdata = polyfit_optimize(xdata,zdata)
    #lambd = 0.01
    #求恢复曲线系数
    e = recoverdata[0][0]
    f = recoverdata[0][1]
    g = recoverdata[0][2]
    h = recoverdata[0][3]
    #求确诊曲线系数
    ABCDarray = []
    for i in range(0, 1000):
#        a = omega[i] * e / lambd * 30
#        b = (omega[i] * f + 3 * e) / lambd * 30
#        c = (omega[i] * g + 2 * f) / lambd * 30
#        d = (omega[i] * h + g) / lambd * 30
        a = omega[i] * e / lambd
        b = (omega[i] * f + 3 * e - 42 * omega[i] * e) / lambd
        c = (omega[i] * g + 2 * f + 588 * omega[i] * e - 28 * omega[i] * f) / lambd
        d = (omega[i] * h + g - 2744 * omega[i] * e + 196 * omega[i] * f - 14 * omega[i] * g) / lambd
        temp = [a,b,c,d]
        ABCDarray.append(temp)
        #print(ABCDarray[0][3])
    
    #y = at^3+bt^2+ct+d
    #求确诊曲线的值
    res = []
    for i in range(0, 1000):
        temp = []
        for t in range(count1, count2):
            y = ABCDarray[i][0] * t * t * t + ABCDarray[i][1] * t * t + ABCDarray[i][2] * t + ABCDarray[i][3]
            temp.append(y)
        res.append(temp)
    #print(res)
    ##
    #误差
    offset = []
    for i in range(0, 1000):
        offset.append(MSE(np.array(res[i]), newpositivelist[i],len(np.array(res[i]))))
    #print(offset)
    #
    #最小误差
    index = 0
    min = offset[0]
    for i in range(0,1000):
        if(min > offset[i]):
            min = offset[i]
            index = i
    print(index)
    #print(res[index])
    
    result = list(map(offset.index, heapq.nsmallest(6, offset)))
    temp=[]
    Inf = 0
    for i in range(6):
        temp.append(offset.index(max(offset)))
        offset[offset.index(max(offset))]=Inf
    result.sort()
    temp.sort()
    print(result)
    print(temp)
            
    return (min,omega[index],ABCDarray[index],res[index],newpositivelist[index],(e,f,g,h))


#修正确诊人数后，abcd公式增加时延
def omega_optimize_amend_new(xdata, ydata, zdata, lambd, count1, count2):
    #随机omega
    omega = []
    newpositivelist = []
    for i in np.arange(-10, 10, 0.1):
        #生成随机数
        #num = random.uniform(0,1)
        num = np.tanh(i)
        #添加到列表中
        num = (num + 1) / 2
        omega.append(num)
        #修正后确诊人数
        amendlist = []
        for x,y in zip(ydata,zdata):
            amendlist.append(x - num * y)
        newpositivelist.append(amendlist)
        
    #positivedata = polyfit_optimize(xdata,ydata)
    #a = positivedata[0][0]
    #b = positivedata[0][1]
    #c = positivedata[0][2]
    #d = positivedata[0][3]
    recoverdata = polyfit_optimize(xdata,zdata)
    #lambd = 0.01
    #求恢复曲线系数
    e = recoverdata[0][0]
    f = recoverdata[0][1]
    g = recoverdata[0][2]
    h = recoverdata[0][3]
    
    #求确诊曲线系数
    ABCDarray = []
    for i in range(0, 100):
        a = omega[i] * e / lambd
        b = (omega[i] * f + 3 * e - 42 * omega[i] * e) / lambd
        c = (omega[i] * g + 2 * f + 588 * omega[i] * e - 28 * omega[i] * f) / lambd
        d = (omega[i] * h + g - 2744 * omega[i] * e + 196 * omega[i] * f - 14 * omega[i] * g) / lambd
        temp = [a,b,c,d]
        ABCDarray.append(temp)
        #print(ABCDarray[0][3])
        
    #y = at^3+bt^2+ct+d
    #求确诊曲线的值
    res = []
    for i in range(0, 100):
        temp = []
        for t in range(count1, count2):
            y = ABCDarray[i][0] * t * t * t + ABCDarray[i][1] * t * t + ABCDarray[i][2] * t + ABCDarray[i][3]
            temp.append(y)
        res.append(temp)
    print(res)
    ##
    #误差
    offset = []
    for i in range(0, 100):
        offset.append(MSE(np.array(res[i]), newpositivelist[i],len(np.array(res[i]))))
    #print(offset)
    #
    #最小误差
    index = 0
    min = offset[0]
    for i in range(0,100):
        if(min > offset[i]):
            min = offset[i]
            index = i
    
#    result = map(offset.index, heapq.nlargest(3, offset))
#    temp=[]
#    Inf = 0
#    for i in range(3):
#        temp.append(offset.index(max(offset)))
#        offset[offset.index(max(offset))]=Inf
#    result.sort()
#    temp.sort()
#    print(result)
#    print(temp)
            
    return (min,omega[index],ABCDarray[index],res[index],newpositivelist[index],(a,b,c,d),(e,f,g,h))


#def ABCD_optimize(xdata, ydata, zdata):
#    #求确诊曲线系数
#    positivedata = polyfit_optimize(xdata,ydata)
#    a = positivedata[0][0]
#    b = positivedata[0][1]
#    c = positivedata[0][2]
#    d = positivedata[0][3]
#    recoverdata = polyfit_optimize(xdata,zdata)
#    #求恢复曲线系数
#    e = recoverdata[0][0]
#    f = recoverdata[0][1]
#    g = recoverdata[0][2]
#    h = recoverdata[0][3]
#    return ((a,b,c,d),(e,f,g,h))

#求结果 恢复率lambd 开始天数count1 结束天数count2
def polyfit_result(df,lambd,count1,count2):
    #日期
    #numdate = df['date']
    #人数
    positivenum = df['positiveIncrease']
    
    recoverednum = df['recoveredIncrease']
    
    #xdata = numdate.index
    
    #ydata = positivenum
    
    #zdata = recoverednum
    
    #天数
    xdata = range(count1,count2)
    #print(xdata1)
    xdata = np.array(xdata)
    #print(len(xdata1))
    
    #确诊
    ydata = positivenum[count1:count2]
    #print(ydata)
    ydata = np.array(ydata)
    #print(len(ydata))
    
    #康复
    zdata = recoverednum[count1:count2]
    #print(zdata1)
    zdata = np.array(zdata)
    #print(len(ydata1))
    #datax = pfo.polyfit_optimize(xdata1,ydata1)
    #print(datax)
    result = omega_optimize_amend(xdata,ydata,zdata,lambd,count1,count2)
    
    print('MSE：')
    print(result[0])
    print('RMSE：')
    print(RMSE(result[3],ydata,len(ydata)))
    print('AFER：')
    print(AFER(result[3],ydata,len(ydata)))
    print('复阳率：')
    print(result[1])
    print('a、b、c、d：')
    print(result[2])
    #print(result[3])
    
    t = np.linspace(count1, count2, count2-count1)
    print('预测确诊函数图像：')
    plt.plot(t, result[4], 's', label='true')
    plt.plot(t, result[3], label='pridect')
    plt.show()
    print(result[5])
    
    return (result[0],result[1],result[2],result[3],result[4],result[5])