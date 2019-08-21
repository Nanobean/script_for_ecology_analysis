# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 11:08:39 2019

@author: 73902
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 22:15:12 2019

@author: 73902
"""


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


def listgroup(ind,x,y):
     xlist=[]
     ylist=[]
     i=0
     newxlist=[]
     newylist=[]
     o=len(x)
     
     for i in range(0,o):
        if i==o-1:         
            xlist.append(x[i])
            ylist.append(y[i])
            newxlist.append(xlist)
            newylist.append(ylist)
        else:
            if i==0:
                 xlist.append(x[i])
                 ylist.append(y[i])
            elif pd.notnull(ind[i+1]):
                 xlist.append(x[i])
                 ylist.append(y[i])
                 newxlist.append(xlist)
                 newylist.append(ylist)
                 xlist=[]
                 ylist=[]
                 
            else:
                 xlist.append(x[i])
                 ylist.append(y[i]) 
     return(newxlist,newylist)     

os.chdir('D:\python')
data= pd.read_excel('c-year-numfile.xlsx')

lisy,lisx=listgroup(data['code'],data['year'],data['num'])



def qiepian(x,y,up,down):
    yearlist=[]
    numlist=[]
    newyearlist=[]
    newnumlist=[]
    for j in range(len(x)):
        for i in range(len(x[j])):
           if x[j][i]>down and x[j][i]<up:
              yearlist.append(x[j][i])
              numlist.append(y[j][i])
        newyearlist.append(yearlist)  
        newnumlist.append(numlist)     
        yearlist=[]
        numlist=[]     
    return  newyearlist,newnumlist


lisy30,lisx30=qiepian(lisy,lisx,2018,1987)

#得到后三十年的数据,


nonapos=data['code'].dropna(axis=0,how='all')#删掉所有空值
def myf(n,lisx,lisy,yr):
    newlisp,newlisx,newlisy=[],[],[]   
    for i in range(0,len(lisx)):
      if (yr-(len(lisx[i])))<n:
          newlisx.append(lisx[i])
          newlisp.append(list(nonapos)[i])
          newlisy.append(lisy[i])
    return newlisx,newlisp,newlisy
#输入一个阈值和大列表，以及年数，筛选掉大列表中小列表数量小于阈值的小列表。也可以用来筛选地点。



lisxs,lisps,lisys=myf(1,lisx30,lisy30,30)

#输入大year列表和大num列表，得到被切过后（第30-50年）的大列表。
alllisy,alllisx=[],[]
for i in range(1987,2017,5):
        bigyearlist,bignumlist=qiepian(lisys,lisxs,i+6,i)
        alllisy.append(bigyearlist)
        alllisx.append(bignumlist)

allallcorr=[]
for i in alllisx:
    allcorr=np.corrcoef(np.array(i))       
    allallcorr.append(allcorr)
arrayallcorr=np.array(allallcorr)     
#得到分类数据，先按照距离分类，然后按照年段分类，最后是具体的相关系数，查看时按照【距离】【年段序号】来查看


toklist=arrayallcorr


import xlsxwriter
workbook = xlsxwriter.Workbook("bridcodecorr.xlsx") 
for year in range(len(toklist)):
     worksheet = workbook.add_worksheet() 
     worksheet.write('A1', year)
     for lie in range(len(toklist[year])):
         for hang in range(len(toklist[year][lie])):
 #            if pd.isnull(toklist[year][lie][hang]):
 #                 toklist[year][lie][hang]=0
             worksheet.write((hang+1), lie, toklist[year][lie][hang])

workbook.close()  
#test