# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 20:35:26 2021

@author: sjy
"""

import scipy.integrate
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize
import pandas as pd
from datetime import datetime,date
import VA_Polyfit_Optimize as pfo
from matplotlib.pyplot import MultipleLocator
import matplotlib.dates as mat
import random
import math


#纽约数据
df = pd.read_excel("D:/项目/毕业设计/资料/covidtracking/VA弗吉尼亚(全)/弗吉尼亚20201101-20210123.xlsx")
#print(df)

#分隔日期
newdate1 = date(2020,11,15)
newdate2 = date(2021,1,15)

newdate1 = pd.to_datetime(newdate1, format="%Y-%m-%d")
newdate2 = pd.to_datetime(newdate2, format="%Y-%m-%d")

date=['2020-11-01','2020-11-15','2020-11-30','2020-12-15','2020-12-30','2021-1-15','2021-1-30','2021-2-15']

#日期
numdate = df['date']

#人数
positivenum = df['positiveIncrease']

recoverednum = df['recoveredIncrease']

positivesum = df['positive']

recoveredsum = df['recovered']


#日期间隔
i = 0
count1 = 14
for i in numdate.index:
	if (newdate1 <= numdate[i] and numdate[i] <= newdate2):
		count1 = count1 + 1
print(count1)

#天数
xdata1 = range(15,count1)

xdata1 = np.array(xdata1)

print(xdata1)

numdate = numdate[15:count1]

numdate = np.array(numdate)

numdate[1] = pd.to_datetime(numdate[1], format="%Y-%m-%d")

print(numdate[1])

#确诊
ydata1 = positivenum[15:count1]

ydata1 = np.array(ydata1)

#康复
zdata1 = recoverednum[15:count1]

zdata1 = np.array(zdata1)

sdata1 = positivesum[15:count1]

sdata1 = np.array(sdata1)

res1 = pfo.polyfit_result(df,0.01,15,count1)

res2 = pfo.polyfit_optimize(xdata1,zdata1)

res3 = pfo.polyfit_optimize(xdata1,ydata1)

print(res1[2])

lambd = 0.01

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

#omega = 0.18
omega2 = 0.18
#a2 = omega2 * e / lambd
#b2 = (omega2 * f + 3 * e) / lambd
#c2 = (omega2 * g + 2 * f) / lambd
#d2 = (omega2 * h + g) / lambd

a2 = omega2 * e / lambd
b2 = (omega2 * f + 3 * e - 42 * omega2 * e) / lambd
c2 = (omega2 * g + 2 * f + 588 * omega2 * e - 28 * omega2 * f) / lambd
d2 = (omega2 * h + g - 2744 * omega2 * e + 196 * omega2 * f - 14 * omega2 * g) / lambd



#omega = 0.195
omega3 = 0.20
#a3 = omega3 * e / lambd
#b3 = (omega3 * f + 3 * e) / lambd
#c3 = (omega3 * g + 2 * f) / lambd
#d3 = (omega3 * h + g) / lambd

a3 = omega3 * e / lambd
b3 = (omega3 * f + 3 * e - 42 * omega3 * e) / lambd
c3 = (omega3 * g + 2 * f + 588 * omega3 * e - 28 * omega3 * f) / lambd
d3 = (omega3 * h + g - 2744 * omega3 * e + 196 * omega3 * f - 14 * omega3 * g) / lambd

#omega = 0.2
omega4 = 0.21
#a4 = omega4 * e / lambd
#b4 = (omega4 * f + 3 * e) / lambd
#c4 = (omega4 * g + 2 * f) / lambd
#d4 = (omega4 * h + g) / lambd

a4 = omega4 * e / lambd
b4 = (omega4 * f + 3 * e - 42 * omega4 * e) / lambd
c4 = (omega4 * g + 2 * f + 588 * omega4 * e - 28 * omega4 * f) / lambd
d4 = (omega4 * h + g - 2744 * omega4 * e + 196 * omega4 * f - 14 * omega4 * g) / lambd

print(a1,a2,a3,a4)

temp1 = []
temp1sum = []
temp1all = 201960
for t in range(14, count1+40):
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
temp2all = 201960
for t in range(14, count1+30):
    y = a1 * t * t * t + b1 * t * t + c1 * t + d1
    #y = res1[0][0] * t * t * t + res1[0][1] * t * t + res1[0][2] * t + res1[0][3]
    temp2all = temp2all + y
    temp2.append(y)
    temp2sum.append(temp2all)

yy = pd.DataFrame(temp2)

writer = pd.ExcelWriter('D:/项目/毕业设计/资料/covidtracking/VA弗吉尼亚(全)/1.xlsx')

yy.to_excel(writer,'Sheet1')

writer.save()
    
yy = pd.DataFrame(temp2sum)

writer = pd.ExcelWriter('D:/项目/毕业设计/资料/covidtracking/VA弗吉尼亚(全)/2.xlsx')

yy.to_excel(writer,'Sheet1')

writer.save()

#0.145
temp3 = []
temp3sum = []
temp3all = 201960
for t in range(14, count1+30):
    y = a3 * t * t * t + b3 * t * t + c3 * t + d3
    #y = res1[0][0] * t * t * t + res1[0][1] * t * t + res1[0][2] * t + res1[0][3]
    temp3all = temp3all + y
    temp3.append(y)
    temp3sum.append(temp3all)

#0.15
temp4 = []
temp4sum = []
temp4all = 201960
for t in range(14, count1+30):
    y = a4 * t * t * t + b4 * t * t + c4 * t + d4
    #y = res1[0][0] * t * t * t + res1[0][1] * t * t + res1[0][2] * t + res1[0][3]
    temp4all = temp4all + y
    temp4.append(y)
    temp4sum.append(temp4all)


temp5 = []
for t in range(14, count1+30):
    y = e * t * t * t + f * t * t + g * t + h
    temp5.append(y)
    
temp5 = map(int,temp5)

yy = pd.DataFrame(temp5)

writer = pd.ExcelWriter('D:/项目/毕业设计/资料/covidtracking/VA弗吉尼亚(全)/3.xlsx')

yy.to_excel(writer,'Sheet1')

writer.save()

t = np.linspace(0, 100, 100)
#plt.subplot(1,2,1)
#print("新增确诊真实/预测：")
#plt.axes([0.1, 2.65, 0.7, 0.5])
#plt.axis = gca()
#plt.axis.plot_date(dates)
plt.plot(xdata1, ydata1, 'o', label='Reported')
plt.xticks(xdata1, date, rotation=45)
#把x轴的刻度间隔设置为1，并存在变量里
x_major_locator=MultipleLocator(15)
ax=plt.gca()
#把x轴的主刻度设置为1的倍数
ax.xaxis.set_major_locator(x_major_locator)
plt.plot(range(14,len(temp1)+14), temp1, label='Predicted')
plt.rcParams['savefig.dpi'] = 200 #图片像素
plt.rcParams['figure.dpi'] = 200 #分辨率
plt.legend(loc='upper right')
#plt.xlabel('Date') #设置x轴名称
plt.ylabel('No. of infect person ') #设置y轴名称
plt.title("New infected cases(ω=0.18)")
plt.show()


#plt.subplot(1,2,1)
#print("新增确诊真实/预测：")
#plt.axes([0.1, 1.8, 0.7, 0.5])
plt.plot(xdata1, ydata1, 'o',label='Reported')
plt.xticks(xdata1, date, rotation=45)
#把x轴的刻度间隔设置为1，并存在变量里
x_major_locator=MultipleLocator(15)
ax=plt.gca()
#把x轴的主刻度设置为1的倍数
ax.xaxis.set_major_locator(x_major_locator)
plt.plot(range(14,len(temp2)+14), temp2, label='Predicted')
plt.legend(loc='upper right')
#plt.xlabel('Date') #设置x轴名称
plt.ylabel('No. of infect person ') #设置y轴名称
plt.title("New infected cases(ω=0.19)")
plt.show()

#plt.subplot(1,2,1)
#print("新增确诊真实/预测：")
#plt.axes([0.1, 0.95, 0.7, 0.5])
plt.plot(xdata1, ydata1, 'o',label='Reported')
plt.xticks(xdata1, date, rotation=45)
#把x轴的刻度间隔设置为1，并存在变量里
x_major_locator=MultipleLocator(15)
ax=plt.gca()
#把x轴的主刻度设置为1的倍数
ax.xaxis.set_major_locator(x_major_locator)
plt.plot(range(14,len(temp3)+14), temp3, label='Predicted')
plt.legend(loc='upper right')
#plt.xlabel('Date') #设置x轴名称
plt.ylabel('No. of infect person ') #设置y轴名称
plt.title("New infected cases(ω=0.2)")
plt.show()

#plt.subplot(1,2,1)
#print("新增确诊真实/预测：")
#plt.axes([0.1, 0.1, 0.7, 0.5])
plt.plot(xdata1, ydata1, 'o',label='Reported')
plt.xticks(xdata1, date, rotation=45)
#把x轴的刻度间隔设置为1，并存在变量里
x_major_locator=MultipleLocator(15)
ax=plt.gca()
#把x轴的主刻度设置为1的倍数
ax.xaxis.set_major_locator(x_major_locator)
plt.plot(range(14,len(temp4)+14), temp4, label='Predicted')
plt.legend(loc='upper right')
#plt.xlabel('Date') #设置x轴名称
plt.ylabel('No. of infect person ') #设置y轴名称
plt.title("New infected cases(ω=0.21)")
plt.show()


xdata2 = range(15,count1, 3)
sdata2 = []
i = 0
while i < len(sdata1):
    sdata2.append(sdata1[i])
    i = i + 3
#Confirmed cases omega=0.12
#plt.axes([0.98, 2.65, 0.7, 0.5])
plt.plot(xdata2, sdata2, 'o',label='Reported')
plt.xticks(xdata1, date, rotation=45)
#把x轴的刻度间隔设置为1，并存在变量里
x_major_locator=MultipleLocator(15)
ax=plt.gca()
#把x轴的主刻度设置为1的倍数
ax.xaxis.set_major_locator(x_major_locator)
plt.plot(range(14,len(temp1sum)+14), temp1sum, label='Predicted')
plt.legend(loc='lower right')
#plt.xlabel('Date') #设置x轴名称
plt.ylabel('No. of infect person ') #设置y轴名称
plt.title("Accumulative infected cases(ω=0.18)")
plt.show()


#Confirmed cases omega=0.14
#plt.axes([0.98, 1.8, 0.7, 0.5])
plt.plot(xdata2, sdata2, 'o',label='Reported')
plt.xticks(xdata1, date, rotation=45)
#把x轴的刻度间隔设置为1，并存在变量里
x_major_locator=MultipleLocator(15)
ax=plt.gca()
#把x轴的主刻度设置为1的倍数
ax.xaxis.set_major_locator(x_major_locator)
plt.plot(range(14,len(temp2sum)+14), temp2sum, label='Predicted')
plt.legend(loc='lower right')
#plt.xlabel('Date') #设置x轴名称
plt.ylabel('No. of infect person ') #设置y轴名称
plt.title("Accumulative infected cases(ω=0.19)")
plt.show()

#Confirmed cases omega=0.145
#plt.axes([0.98, 0.95, 0.7, 0.5])
plt.plot(xdata2, sdata2, 'o',label='Reported')
plt.xticks(xdata1, date, rotation=45)
#把x轴的刻度间隔设置为1，并存在变量里
x_major_locator=MultipleLocator(15)
ax=plt.gca()
#把x轴的主刻度设置为1的倍数
ax.xaxis.set_major_locator(x_major_locator)
plt.plot(range(14,len(temp3sum)+14), temp3sum, label='Predicted')
plt.legend(loc='lower right')
#plt.xlabel('Date') #设置x轴名称
plt.ylabel('No. of infect person ') #设置y轴名称
plt.title("Accumulative infected cases(ω=0.2)")
plt.show()

#Confirmed cases omega=0.15
#plt.axes([0.98, 0.1, 0.7, 0.5])
plt.plot(xdata2, sdata2, 'o',label='Reported')
plt.xticks(xdata1, date, rotation=45)
#把x轴的刻度间隔设置为1，并存在变量里
x_major_locator=MultipleLocator(15)
ax=plt.gca()
#把x轴的主刻度设置为1的倍数
ax.xaxis.set_major_locator(x_major_locator)
plt.plot(range(14,len(temp4sum)+14), temp4sum, label='Predicted')
plt.legend(loc='lower right')
#plt.xlabel('Date') #设置x轴名称
plt.ylabel('No. of infect person ') #设置y轴名称
plt.title("Accumulative infected cases(ω=0.21)")
plt.show()