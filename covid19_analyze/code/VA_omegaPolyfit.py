# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 10:42:36 2021

@author: sjy
"""

import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize
from matplotlib.pyplot import MultipleLocator
import pandas as pd
from datetime import datetime,date
import Polyfit_Optimize as pfo
import random
import math

#新墨西哥数据
df = pd.read_excel("D:/项目/毕业设计/资料/covidtracking/VA弗吉尼亚(全)/弗吉尼亚20201101-20210123.xlsx")
#日期
#numdate = df['date']
#人数
positivenum = df['positiveIncrease']

recoverednum = df['recoveredIncrease']

##分隔日期
#newdate1 = date(2020,11,14)
#newdate2 = date(2021,1,15)
#
##newdate4 = date(2020,12,4)
#
#newdate1 = pd.to_datetime(newdate1, format="%Y-%m-%d")
#newdate2 = pd.to_datetime(newdate2, format="%Y-%m-%d")
#
##控制期数据
#i = 0
#count1 = 0
#for i in numdate.index:
#	if (newdate1 <= numdate[i] and numdate[i] <= newdate2):
#		count1 = count1 + 1
#print(count1)


#A = []
#B = []
#C = []
#D = []
#E = []
#F = []
#G = []
#H = []
omega=[]
for i in range(16,76):
    #天数
    xdata1 = range(15,i)
    
    xdata1 = np.array(xdata1)
    
    #确诊
    ydata1 = positivenum[15:i]
    
    ydata1 = np.array(ydata1)
    
    #康复
    zdata1 = recoverednum[15-15:i-15]
    
    zdata1 = np.array(zdata1)
    
    result = pfo.omega_optimize_amend(xdata1,ydata1,zdata1,0.01,15,i)
    
#    print('MSE：')
#    print(result[0])
#    print('RMSE：')
#    print(RMSE(result[3],ydata1,len(ydata)))
#    print('AFER：')
#    print(AFER(result[3],ydata1,len(ydata)))
    print('复阳率：')
    print(result[1])
    omega.append(result[1])
#    print('a、b、c、d：')
#    print(result[2])
    #print(result[3])
date=['2020-11-01','2020-11-15','2020-11-30','2020-12-15','2020-12-30','2021-1-15','2021-1-30','2021-2-15']

print(omega)
#
#yy = pd.DataFrame(omega)
#
#writer = pd.ExcelWriter('D:/项目/毕业设计/资料/covidtracking/NY纽约(全)/omega1.xlsx')
#
#yy.to_excel(writer,'Sheet1')
#
#writer.save()

#plt.plot(range(0,len(omega)), omega, 'o')
#plt.xticks(xdata1, date, rotation=45)
##把x轴的刻度间隔设置为1，并存在变量里
#x_major_locator=MultipleLocator(15)
#ax=plt.gca()
##把x轴的主刻度设置为1的倍数
#ax.xaxis.set_major_locator(x_major_locator)
#plt.title('omega')
#plt.xlabel('Date') #设置x轴名称
#plt.ylabel('No. of infect person') #设置y轴名称
#plt.title("secondary infection rate")


#f = np.polyfit(range(0,len(omega)), omega, 1)
#p = np.poly1d(f)
##yvals = p(xdata)  
#print(f)
#
#result=[]
##画拟合直线
#x = range(0,95)  ##在150-190直接画100个连续点
#y = f[0] * x + f[1]  ##函数式
#
#result.append(y)
#
#yy = pd.DataFrame(result)
#
#writer = pd.ExcelWriter('D:/项目/毕业设计/资料/covidtracking/NY纽约(全)/omega2.xlsx')
#
#yy.to_excel(writer,'Sheet1')
#
#writer.save()

#plt.plot(range(0,95), y, color="red", linewidth=2, label='Predicted')
plt.plot(range(0,len(omega)), omega, 'o',color="red",linestyle='dashed',label='fitted')
plt.xticks(xdata1, date, rotation=45)
#把x轴的刻度间隔设置为1，并存在变量里
x_major_locator=MultipleLocator(15)
ax=plt.gca()
#把x轴的主刻度设置为1的倍数
ax.xaxis.set_major_locator(x_major_locator)
plt.title('omega')
#plt.xlabel('Date') #设置x轴名称
plt.ylabel('Value of ω') #设置y轴名称
plt.title("Secondary infection rate")
plt.legend(loc='upper right')  # 绘制图例
plt.show()


#    t = np.linspace(15, i, 15-i)
#    print('预测确诊函数图像：')
#    plt.plot(t, result[4], 's', label='true')
#    plt.plot(t, result[3], label='pridect')
#    plt.show()
#    print(result[5])

#    res = pfo.ABCD_optimize(xdata1,ydata1,zdata1)
#    
#    A.append(res[0][0])
#    B.append(res[0][1])
#    C.append(res[0][2])
#    D.append(res[0][3])
#    E.append(res[1][0])
#    F.append(res[1][1])
#    G.append(res[1][2])
#    H.append(res[1][3])
#    
#print(res[0],res[1])
#
#for i in A:
#    print(i)
#print('......................')
#for i in E:
#    print(i)

#plt.plot(A, E, 'o')
#plt.show()
#A/E
#AEres = []
#for i in range(0,len(A)):
#    if abs(A[i]/E[i]) < 20:
#        AEres.append(abs(A[i]/E[i]))
#print(AEres)
#    
#f = np.polyfit(range(0,len(AEres)), AEres, 1)
#p = np.poly1d(f)
##yvals = p(xdata)  
#print(f)

#AEres = []
#for i in range(0,len(A)):
#    if abs(A[i]/E[i]) < 20:
#        AEres.append(abs(A[i]/E[i]))
#print(AEres)

#axis x: A,axis y:E
#f = np.polyfit(D, H, 1)
#p = np.poly1d(f)
##yvals = p(xdata)  
#print(f)

# 画拟合直线
#x = np.linspace(-100, 400, 100000)  ##在150-190直接画100个连续点
#y = f[0] * x + f[1]  ##函数式
#plt.plot(x, y, color="red", label="line", linewidth=2)
#plt.plot(D, H, 'o')
#plt.title('axis x: D,axis y: H')
#plt.legend()  # 绘制图例
#plt.show()

##i = 0
##omega = 3 * A[i] / (B[i] + 42 * A[i] - A[i] / E[i] * F[i])
##print(omega)
#
#求omega
#omega = []
#for i in range(0,len(A)):
#    temp = 3 * A[i] / (B[i] + 42 * A[i] - A[i] / E[i] * F[i])
#    if temp > 0 and temp < 1:
#        #omega.append(null)
#        omega.append(temp)
#
#print(omega)
##for i in omega:
##    print(i)
#plt.plot(range(0,len(omega)), omega, 'o')
#plt.title('omega')
#plt.show()

#omegaf = np.polyfit(range(0,len(omega)), omega, 1)
#omegap = np.poly1d(omegaf)
##yvals = p(xdata)  
#print(omegaf)
#
# 画拟合直线
#x = np.linspace(0, 30, 100)  ##在150-190直接画100个连续点
#y = omegaf[0] * x + omegaf[1]  ##函数式
#plt.plot(x, y, color="red", label="line", linewidth=2)
#plt.plot(range(0,len(omega)), omega, 'o')
#plt.title('omega')
#plt.legend()  # 绘制图例
#plt.show()



#求lambd
#lambd = []
#for i in range(0,len(omega)):
#    temp = (omega[i] * E[i]) / A[i]
#    #if temp > 0 and temp < 1:
#        #omega.append(null)
#    lambd.append(temp)
#
#for i in lambd:
#    print(i)
#plt.plot(range(0,len(lambd)), lambd, 'o')
#plt.title('lambd')
#plt.show()
#
#for i in range(0,len(omega)):
#    print(omega[i]/0.01)
#
#lambdf = np.polyfit(range(0,len(lambd)), lambd, 1)
#lambdp = np.poly1d(lambdf)
##yvals = p(xdata)  
#print(lambdf)

## 画拟合直线
#x = np.linspace(0, len(lambd), 100)  ##在150-190直接画100个连续点
#y = lambdf[0] * x + lambdf[1]  ##函数式
#plt.plot(x, y, color="red", label="line", linewidth=2)
#plt.plot(range(0,len(lambd)), lambd, 'o')
#plt.title('lambd')
#plt.legend()  # 绘制图例
#plt.show()



#print(len(AEres))
#散点
#plt.plot(range(0,len(AEres)), AEres, 'o')
#plt.show()
##曲线
#plt.plot(range(0,len(A)), A, 'o')
#plt.plot(range(0,len(E)), E, '.')