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
        for j in range(len(cla)):
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


ifelse=list(set(wepos))#生成分类时用到的判断列表

largelist=[]
for i in range(len(ifelse)):
    largelist.append([])
    
ob=[weyear,weaou,wepos,webridnum,webridmass]                
                
largelist=classi(ifelse,ob)#按照地点进行分类

tlargelist=map(lambda x:np.array(x).T,largelist) #方便之后操作进行转置

from collections import Counter

words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around',
    'the', 'eyes', "don't", 'look', 'around', 'the', 'eyes',
    'look', 'into', 'my', 'eyes', "you're", 'under'
]
counter = Counter(words)
print(counter.common())
aph=list(map(lambda x:Counter(x[0]),tlargelist))#计算每个地点的多样性，具体直接对当地物种数量进行计数就得到了

ifelse=list(set(weyear))
ob=[wepos,weaou,weyear,webridnum,webridmass] 

largelist=[]
for i in range(len(ifelse)):
    largelist.append([])
    
largelist=classi(ifelse,ob)#按照地点进行分类
tlargelist=list(map(lambda x:np.array(x).T,largelist))
tlargelist=tlargelist[22:]

gama=list(map(lambda x:len(list(set(x[1]))),tlargelist))#得到每年的全局物种数量

beta=[]
for i in range(len(aph)):
    pos=[]
    for year in range(1988,2018):
        pos.append((aph[i][str(year)])/gama[year-1988])
    beta.append(pos)

#用每个地点的α多样性和伽马相除,得到每个地点的β多样性列表
    

ifelse=list(set(wepos))
import xlsxwriter
workbook = xlsxwriter.Workbook("Di.xlsx") 
worksheet = workbook.add_worksheet()
worksheet.write(1,0,'gama')
for year in range(1988,2018):
    worksheet.write(0,(year-1987),str(year))
    worksheet.write(1,(year-1987),gama[(year-1988)])
for pos in range(len(ifelse)):
    worksheet.write(pos+2,0,ifelse[pos])
    for year in range(1987,2018):
        worksheet.write((pos+2),(year-1986),str(aph[pos][str(year)]))
worksheet = workbook.add_worksheet()
for year in range(1988,2018):
    worksheet.write(0,(year-1987),str(year))
for pos in range(len(ifelse)):
    worksheet.write(pos+1,0,ifelse[pos])
    for year in range(1988,2018):
        worksheet.write((pos+1),(year-1987),str(beta[pos][year-1988]))
workbook.close()