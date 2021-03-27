# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 15:15:51 2021

@author: sjy
"""

import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from scipy import integrate, optimize
import pandas as pd
from datetime import datetime,date
import heapq
import random

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
        a = omega[i] * e / lambd
        b = (omega[i] * f + 3 * e) / lambd
        c = (omega[i] * g + 2 * f) / lambd
        d = (omega[i] * h + g) / lambd
#        a = omega[i] * e / lambd
#        b = (omega[i] * f + 3 * e - 42 * omega[i] * e) / lambd
#        c = (omega[i] * g + 2 * f + 588 * omega[i] * e - 28 * omega[i] * f) / lambd
#        d = (omega[i] * h + g - 2744 * omega[i] * e + 196 * omega[i] * f - 14 * omega[i] * g) / lambd
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
    zdata = recoverednum[count1-14:count2-14]
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


def polyfit_show(df, omega, lambd, xdata, ydata, zdata, sdata, numsum, count1, count2):
    res1 = polyfit_result(df,lambd,count1,count2)
    
    res2 = polyfit_optimize(xdata,zdata)
    
    res3 = polyfit_optimize(xdata,ydata)
    
    #print(res1[2])
    
    date=['2020-11-01','2020-11-15','2020-11-30','2020-12-15','2020-12-30','2021-1-15','2021-1-30','2021-2-15']
    
    #lambd = 0.01
    
    #omega = 0.23147521650097047
    a1 = res1[2][0]
    b1 = res1[2][1]
    c1 = res1[2][2]
    d1 = res1[2][3]
    
    #e = res2[0][0]
    #f = res2[0][1]
    #g = res2[0][2]
    #h = res2[0][3]
    e = res1[5][0]
    f = res1[5][1]
    g = res1[5][2]
    h = res1[5][3]
    
    #omega = 0.2
    omega2 = omega[0]
    #a2 = omega2 * e / lambd
    #b2 = (omega2 * f + 3 * e) / lambd
    #c2 = (omega2 * g + 2 * f) / lambd
    #d2 = (omega2 * h + g) / lambd
    
    a2 = omega2 * e / lambd
    b2 = (omega2 * f + 3 * e - 42 * omega2 * e) / lambd
    c2 = (omega2 * g + 2 * f + 588 * omega2 * e - 28 * omega2 * f) / lambd
    d2 = (omega2 * h + g - 2744 * omega2 * e + 196 * omega2 * f - 14 * omega2 * g) / lambd
    
    
    
    #omega = 0.235
    omega3 = omega[1]
    #a3 = omega3 * e / lambd
    #b3 = (omega3 * f + 3 * e) / lambd
    #c3 = (omega3 * g + 2 * f) / lambd
    #d3 = (omega3 * h + g) / lambd
    
    a3 = omega3 * e / lambd
    b3 = (omega3 * f + 3 * e - 42 * omega3 * e) / lambd
    c3 = (omega3 * g + 2 * f + 588 * omega3 * e - 28 * omega3 * f) / lambd
    d3 = (omega3 * h + g - 2744 * omega3 * e + 196 * omega3 * f - 14 * omega3 * g) / lambd
    
    #omega = 0.24
    omega4 = omega[2]
    #a4 = omega4 * e / lambd
    #b4 = (omega4 * f + 3 * e) / lambd
    #c4 = (omega4 * g + 2 * f) / lambd
    #d4 = (omega4 * h + g) / lambd
    
    a4 = omega4 * e / lambd
    b4 = (omega4 * f + 3 * e - 42 * omega4 * e) / lambd
    c4 = (omega4 * g + 2 * f + 588 * omega4 * e - 28 * omega4 * f) / lambd
    d4 = (omega4 * h + g - 2744 * omega4 * e + 196 * omega4 * f - 14 * omega4 * g) / lambd
    
    #print(a1,a2,a3,a4)
    
    temp1 = []
    temp1sum = []
    temp1all = numsum
    for t in range(14, count2+40):
        y = a2 * t * t * t + b2 * t * t + c2 * t + d2
        #y = res1[0][0] * t * t * t + res1[0][1] * t * t + res1[0][2] * t + res1[0][3]
        temp1all = temp1all + y
        temp1.append(y)
        temp1sum.append(temp1all)
        #res.append(temp)
    #print('++++++++++++++')
    #print(temp1)
    
    #0.14
    temp2 = []
    temp2sum = []
    temp2all = numsum
    for t in range(14, count2+40):
        y = a1 * t * t * t + b1 * t * t + c1 * t + d1
        #y = res1[0][0] * t * t * t + res1[0][1] * t * t + res1[0][2] * t + res1[0][3]
        temp2all = temp2all + y
        temp2.append(y)
        temp2sum.append(temp2all)
    
    #0.145
    temp3 = []
    temp3sum = []
    temp3all = numsum
    for t in range(14, count2+40):
        y = a3 * t * t * t + b3 * t * t + c3 * t + d3
        #y = res1[0][0] * t * t * t + res1[0][1] * t * t + res1[0][2] * t + res1[0][3]
        temp3all = temp3all + y
        temp3.append(y)
        temp3sum.append(temp3all)
    
    #0.15
    temp4 = []
    temp4sum = []
    temp4all = numsum
    for t in range(14, count2+40):
        y = a4 * t * t * t + b4 * t * t + c4 * t + d4
        #y = res1[0][0] * t * t * t + res1[0][1] * t * t + res1[0][2] * t + res1[0][3]
        temp4all = temp4all + y
        temp4.append(y)
        temp4sum.append(temp4all)
    
    
#    temp5 = []
#    for t in range(0, count1+30):
#        y = e * t * t * t + f * t * t + g * t + h
#        temp5.append(y)
        
    
    t = np.linspace(0, 100, 100)
    #plt.subplot(1,2,1)
    #print("新增确诊真实/预测：")
    plt.axes([0.1, 2.65, 0.7, 0.5])
    #plt.axis = gca()
    #plt.axis.plot_date(dates)
    plt.plot(xdata, ydata, 'o', label='Reported')
    plt.xticks(xdata, date, rotation=45)
    #把x轴的刻度间隔设置为1，并存在变量里
    x_major_locator=MultipleLocator(15)
    ax=plt.gca()
    #把x轴的主刻度设置为1的倍数
    ax.xaxis.set_major_locator(x_major_locator)
    plt.plot(range(14,len(temp1)+14), temp1, label='Predict')
    plt.legend(loc='lower right')
    plt.xlabel('Date') #设置x轴名称
    plt.ylabel('No. of infect person ') #设置y轴名称
    plt.title("PositiveIncrease omega=0.2")
    #plt.show()
    
    
    #plt.subplot(1,2,1)
    #print("新增确诊真实/预测：")
    plt.axes([0.1, 1.8, 0.7, 0.5])
    plt.plot(xdata, ydata, 'o',label='Reported')
    plt.xticks(xdata, date, rotation=45)
    #把x轴的刻度间隔设置为1，并存在变量里
    x_major_locator=MultipleLocator(15)
    ax=plt.gca()
    #把x轴的主刻度设置为1的倍数
    ax.xaxis.set_major_locator(x_major_locator)
    plt.plot(range(14,len(temp2)+14), temp2, label='Predict')
    plt.legend(loc='lower right')
    plt.xlabel('Date') #设置x轴名称
    plt.ylabel('No. of infect person ') #设置y轴名称
    plt.title("PositiveIncrease omega=0.22")
    
    
    #plt.subplot(1,2,1)
    #print("新增确诊真实/预测：")
    plt.axes([0.1, 0.95, 0.7, 0.5])
    plt.plot(xdata, ydata, 'o',label='Reported')
    plt.xticks(xdata, date, rotation=45)
    #把x轴的刻度间隔设置为1，并存在变量里
    x_major_locator=MultipleLocator(15)
    ax=plt.gca()
    #把x轴的主刻度设置为1的倍数
    ax.xaxis.set_major_locator(x_major_locator)
    plt.plot(range(14,len(temp3)+14), temp3, label='Predict')
    plt.legend(loc='lower right')
    plt.xlabel('Date') #设置x轴名称
    plt.ylabel('No. of infect person ') #设置y轴名称
    plt.title("PositiveIncrease omega=0.25")
    
    
    #plt.subplot(1,2,1)
    #print("新增确诊真实/预测：")
    plt.axes([0.1, 0.1, 0.7, 0.5])
    plt.plot(xdata, ydata, 'o',label='Reported')
    plt.xticks(xdata, date, rotation=45)
    #把x轴的刻度间隔设置为1，并存在变量里
    x_major_locator=MultipleLocator(15)
    ax=plt.gca()
    #把x轴的主刻度设置为1的倍数
    ax.xaxis.set_major_locator(x_major_locator)
    plt.plot(range(14,len(temp4)+14), temp4, label='Predict')
    plt.legend(loc='lower right')
    plt.xlabel('Date') #设置x轴名称
    plt.ylabel('No. of infect person ') #设置y轴名称
    plt.title("PositiveIncrease omega=0.3")
    
    #Confirmed cases omega=0.12
    plt.axes([0.98, 2.65, 0.7, 0.5])
    plt.plot(xdata, sdata, 'o',label='Reported')
    plt.xticks(xdata, date, rotation=45)
    #把x轴的刻度间隔设置为1，并存在变量里
    x_major_locator=MultipleLocator(15)
    ax=plt.gca()
    #把x轴的主刻度设置为1的倍数
    ax.xaxis.set_major_locator(x_major_locator)
    plt.plot(range(14,len(temp1sum)+14), temp1sum, label='Predict')
    plt.legend(loc='lower right')
    plt.xlabel('Date') #设置x轴名称
    plt.ylabel('No. of infect person ') #设置y轴名称
    plt.title("Confirmed cases")
    
    #Confirmed cases omega=0.14
    plt.axes([0.98, 1.8, 0.7, 0.5])
    plt.plot(xdata, sdata, 'o',label='Reported')
    plt.xticks(xdata, date, rotation=45)
    #把x轴的刻度间隔设置为1，并存在变量里
    x_major_locator=MultipleLocator(15)
    ax=plt.gca()
    #把x轴的主刻度设置为1的倍数
    ax.xaxis.set_major_locator(x_major_locator)
    plt.plot(range(14,len(temp2sum)+14), temp2sum, label='Predict')
    plt.legend(loc='lower right')
    plt.xlabel('Date') #设置x轴名称
    plt.ylabel('No. of infect person ') #设置y轴名称
    plt.title("Confirmed cases")
    
    #Confirmed cases omega=0.145
    plt.axes([0.98, 0.95, 0.7, 0.5])
    plt.plot(xdata, sdata, 'o',label='Reported')
    plt.xticks(xdata, date, rotation=45)
    #把x轴的刻度间隔设置为1，并存在变量里
    x_major_locator=MultipleLocator(15)
    ax=plt.gca()
    #把x轴的主刻度设置为1的倍数
    ax.xaxis.set_major_locator(x_major_locator)
    plt.plot(range(14,len(temp3sum)+14), temp3sum, label='Predict')
    plt.legend(loc='lower right')
    plt.xlabel('Date') #设置x轴名称
    plt.ylabel('No. of infect person ') #设置y轴名称
    plt.title("Confirmed cases")
    
    #Confirmed cases omega=0.15
    plt.axes([0.98, 0.1, 0.7, 0.5])
    plt.plot(xdata, sdata, 'o',label='Reported')
    plt.xticks(xdata, date, rotation=45)
    #把x轴的刻度间隔设置为1，并存在变量里
    x_major_locator=MultipleLocator(15)
    ax=plt.gca()
    #把x轴的主刻度设置为1的倍数
    ax.xaxis.set_major_locator(x_major_locator)
    plt.plot(range(14,len(temp4sum)+14), temp4sum, label='Predict')
    plt.legend(loc='lower right')
    plt.xlabel('Date') #设置x轴名称
    plt.ylabel('No. of infect person ') #设置y轴名称
    plt.title("Confirmed cases")
    plt.show()