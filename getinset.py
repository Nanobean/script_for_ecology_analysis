1bao# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 18:13:15 2019

@author: 73902
"""
import pandas as pd
import os
import numpy as np

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

def myf(n,lisx,lisy,yr):
    newlisp,newlisx,newlisy=[],[],[]   
    for i in range(0,len(lisx)):
      if (yr-(len(lisx[i])))<n and pd.notnull(lisx[i]).all() :
          newlisx.append(lisx[i])
          newlisp.append(list(nonapos)[i])
          newlisy.append(lisy[i])
    return newlisx,newlisp,newlisy
#输入一个阈值和大列表，以及年数，筛选掉大列表中小列表数量小于阈值的小列表。也可以用来筛选地点。
    




os.chdir('D:\python')
data= pd.read_excel('p-year-numfile.xlsx')
lisyn,lisxn=listgroup(data['pos'],data['year'],data['num'])

lisy30n,lisx30n=qiepian(lisyn,lisxn,2018,1987)

#得到后三十年的数据,

nonapos=data['pos'].dropna(axis=0,how='all')#删掉所有空值
lisxsn,lispsn,lisysn=myf(1,lisx30n,lisy30n,30)


newlispsn=[]
for i in lispsn:
    newlispsn.append(str(i))#把横杠字符删掉，方便待会取交集
#newlispsn就是鸟类数量数据的地点




os.chdir('D:\python')

we = pd.read_excel("temp1987-2017juneOK2.xlsx")
pos=we['newID']


bd=[]
for i in range(1988,2018):
    print(i)
    d=[]    
    d=list(we['t'+str(i)]) 
    bd.append(d)
#读取数据
lisxt=np.array(bd).T
#

lisyt=[]
for j in range(len(pos)):
    lisyt.append([i for i in range(1988,2018)])
#因为没有年份列表就手动生成一份对应的年表
lisy30t,lisx30t=qiepian(lisyt,lisxt,2018,1987)

nonapos=pos

lisxst,lispst,lisyst=myf(1,lisx30t,lisy30t,30)

#lispt是温度数据的地点

intset=[i for i in newlispsn if i in lispst]  #对鸟类和温度的地点取交集





os.chdir('D:\python')
prdata=pd.read_csv("precip1987-2016juneOK2.csv")
#读取降水数据的地点信息
prpos=prdata['newid']

prbd=[]
for i in range(1988,2017):
    print(i)
    d=[]    
    d=list(prdata[str(int(i))]) 
    prbd.append(d)
#读取数据
lisxpr=np.array(prbd).T


lisypr=[]
for j in range(len(prpos)):
    lisypr.append([i for i in range(1988,2017)])
#因为没有年份列表就手动生成一份对应的年表
    

lisy29pr,lisx29pr=qiepian(lisypr,lisxpr,2018,1987)

nonapos=prpos

lisxspr,lispspr,lisyspr=myf(1,lisx29pr,lisy29pr,29)    
    
newintset=[i for i in lispspr if i in intset]#再对降水数据取交集






os.chdir('D:\python\extractedNDVI0227\extractedNDVI0227')
data=pd.read_excel("extract1987-1991.xlsx")
lispNDVI=data['newid']
finalinset=[i for i in lispNDVI if i in newintset]


finalinset=list(set(finalinset))

import xlsxwriter
workbook = xlsxwriter.Workbook("finalinset.xlsx") 
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'inset')
for i in range(len(finalinset)):
    worksheet.write((i+1), 0, finalinset[i])
             
workbook.close()        