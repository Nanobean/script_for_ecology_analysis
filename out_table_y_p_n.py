# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:23:51 2019

@author: forth
"""




import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np





os.chdir('D:\python')
we = pd.read_csv("insetmerge.csv")
weyear=we['year']
weaou=we['aou']
wepos=we['pos']
webridnum=we['num']


ob=np.array([wepos,weyear,webridnum,weaou]).T
newob=[]
for i in range(len(ob)):
    if ob[i][1]>1987:
       newob.append(ob[i]) 
ntob=np.array(newob).T

date = pd.DataFrame({
        'pos':ntob[0],
        'year':ntob[1],
        'num':ntob[2],
        'aou':ntob[3],
        })

    
    
year_aou_num= list(date['num'].groupby([date['year'],date['pos'],date['aou']]))
poslen=len(list(set(date['pos'])))
aoulen=len(list(set(date['aou'])))
dp=dict(zip(list(set(date['pos'])),[i for i in range(poslen)]))
da=dict(zip(list(set(date['aou'])),[i for i in range(aoulen)]))
aouset=list(set(date["aou"]))
posset=list(set(date["pos"]))


import xlsxwriter   
workbook = xlsxwriter.Workbook("2019_7_19.xlsx") 

for i in range(1988,2018):
    globals()['worksheet'+str(i)]= workbook.add_worksheet(str(i))
    list(map(lambda x:eval('worksheet'+str(i)+'.write(0,x+1,aouset[x])'),[i for i in range(aoulen)]))
    list(map(lambda x:eval('worksheet'+str(i)+'.write(x+1,0,posset[x])'),[i for i in range(poslen)]))

a=list(map(lambda x:eval('worksheet'+str(year_aou_num[x][0][0])+'.write(dp[year_aou_num[x][0][1]]+1,da[year_aou_num[x][0][2]]+1,list(year_aou_num[x][1])[0])'),[i for i in range(len(year_aou_num))]))

for year in range(1988,2018):
    for i in range(poslen):
        for j in range(aoulen):
            (1,1)
            eval('worksheet'+str(year)'.write(i+1,j+i,)
workbook.close()
