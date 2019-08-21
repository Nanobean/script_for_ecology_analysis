# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 17:28:29 2019

@author: 73902
"""


import pandas as pd
import numpy as np
import os
import tqdm

def classi(cla,obj):#定义分类函数，接收一个分类标准和被分类对象，返回被分类后的数组，不用管细节
    for i in tqdm.trange(len(obj[0])):#对待分类对象进行遍历
        a=obj[2][i]
        for j in range(len(cla)): #对分类标准进行遍历，符合条件的则加入到
            if a==cla[j]:
                smalllist=[]
                for k in range(len(obj)):#
                    smalllist.append(obj[k][i])
                largelist[j].append(smalllist)
    return largelist



os.chdir('D:\python')
we = pd.read_csv("insetmerge.csv")
weyear=we['year']
weaou=we['aou']
wepos=we['pos']
webridnum=we['num']
webridmass=we['mass']
#读取数据，记得把文件的xlsx扩展名改成csv

#———————————————————————————阿尔法多样性—————————————————————————————————
ifelse=list(set(wepos))
#生成分类时用到的判断列表
ob=[weyear,weaou,wepos,webridnum,webridmass]    
#打包数据
largelist=[]
for i in range(len(ifelse)):
    largelist.append([])
#准备空列表容器
    
largelist=classi(ifelse,ob)
#按照地点进行分类
tlargelist=map(lambda x:np.array(x).T,largelist) 
#方便之后操作，对按地点分类后的数据统一进行转置



from collections import Counter

aph=list(map(lambda x:Counter(x[0]),tlargelist))
#计算每个地点的阿尔法多样性，具体直接对当地物种数量进行计数就得到了

#—————————————————————————————伽马多样性———————————————————————————————————
ifelse=list(set(weyear))
#这次把分类时的判断列表换成年
ob=[wepos,weaou,weyear,webridnum,webridmass] 
#打包待分类数据
largelist=[]
for i in range(len(ifelse)):
    largelist.append([])
#准备空列表容器

largelist=classi(ifelse,ob)
#按照年份进行分类
tlargelist=list(map(lambda x:np.array(x).T,largelist))
#方便之后操作，对按地点分类后的数据统一进行转置

tlargelist=tlargelist[22:]
#数据是从1966年开始的，但我们只需要1988年以后的数据，于是从第22年开始往后取数据

gama=list(map(lambda x:len(list(set(x[1]))),tlargelist))
#得到每年的全局物种数量，即每年的伽马多样性
#———————————————————————————————贝塔多样性—————————————————————————————————


beta=[]
for i in range(len(aph)):
    pos=[]
    for year in range(1988,2018):
        pos.append((aph[i][str(year)])/gama[year-1988])
    beta.append(pos)

#用每年每个地点的α多样性和伽马相除,得到每年每个地点的β多样性列表
#—————————————————————输出到excel，循环用的太多了，待优化————————————————————

ifelse=list(set(wepos))
import xlsxwriter   
workbook = xlsxwriter.Workbook("Diversity.xlsx") 
worksheet = workbook.add_worksheet('aph&gama')
worksheet.write(1,0,'gama')

for year in range(1988,2018):#这个循环遍历年份，根据年份写当年对应的gama多样性
    worksheet.write(0,(year-1987),str(year)) #在表头写好年份
    worksheet.write(1,(year-1987),gama[(year-1988)])  
    
for pos in range(len(ifelse)):#遍历地点，随后再遍历这个地点的年份，把阿尔法多样性写出来
    worksheet.write(pos+2,0,ifelse[pos])
    for year in range(1988,2018):
        worksheet.write((pos+2),(year-1987),str(aph[pos][str(year)]))
        
worksheet = workbook.add_worksheet('beta')#新开一个sheet，遍历地点年份，写出每个地点每年的贝塔多样性
for year in range(1988,2018):
    worksheet.write(0,(year-1987),str(year))
for pos in range(len(ifelse)):
    worksheet.write(pos+1,0,ifelse[pos])
    for year in range(1988,2018):
        worksheet.write((pos+1),(year-1987),str(beta[pos][year-1988]))
workbook.close()





#以下为测试代码，用来统计不同体重区间的物种数量的分布并作图
c,d=[],[]
for i in range(5):
   c.append([])
   d.append([])
for i in sorted(set(webridmass)):
    for j in range(100):
        if i<(j*100+100) and (j*100)<i:
           d[j].append(i)
   
fdictmass=[]
for i in range(len(np.log(sorted(set(webridmass))))):
    for j in range(10):
       if i<(j+2) and j<i:
           c[j].append(i)
           d[j].append(fdictmass)
e=[]
for i in c:
    e.append(len(i))

import matplotlib.pyplot as plt

plt.plot(range(7),e)
#不管用什么方法分段，总之最后得到一个物种转段的表给另一个文件用