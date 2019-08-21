# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 16:56:02 2019

@author: 73902
"""



import pandas as pd
import numpy as np
import os

os.chdir('D:\python')
we = pd.read_excel("insetmerge.xlsx")
num=we['num']
aou=we['aou']
year=we['year']

from tqdm import tqdm  

intsetdata=pd.read_excel('50AOU.xlsx')
inset=set(list(intsetdata['50aou']))
inaou,innum,inyear=[],[],[]
for i in tqdm(range(len(aou))):
    if aou[i] in inset:
        inaou.append(aou[i])
        inyear.append(year[i])
        innum.append(num[i])


#for i in range(len(inaou)):
#    po=inaou[i]
 #   for j in range(len(inaou)):
  #      if po==inaou[j]:
df=pd.DataFrame({'aou' :inaou,
    'year' : inyear,
    'num' : innum})            


aougroup= pd.DataFrame(df['num'].groupby([df['aou'],df['year']]).sum())
aoufile= pd.ExcelWriter('a-year-numfileinset(2).xlsx')
aougroup.to_excel(aoufile,'page_1',float_format='%.5f')
aoufile.save()




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
data= pd.read_excel('a-year-numfileinset(2).xlsx')

lisy,lisx=listgroup(data['aou'],data['year'],data['num'])
#


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


nonaaou=data['aou'].dropna(axis=0,how='all')#删掉所有空值

def myf(n,lisx,lisy,yr):
    newlisp,newlisx,newlisy=[],[],[]   
    for i in range(0,len(lisx)):
      if (yr-(len(lisx[i])))<n and pd.notnull(lisx[i]).all() :
          newlisx.append(lisx[i])
          newlisp.append(list(nonaaou)[i])
          newlisy.append(lisy[i])
    return newlisx,newlisp,newlisy
lisxs,lisps,lisys=myf(1,lisx30,lisy30,30)
lisxs=np.array(lisxs)



import xlsxwriter
workbook = xlsxwriter.Workbook("popmass_num.xlsx") 
worksheet = workbook.add_worksheet()
for year in range(len(lisys[0])):
    worksheet.write(0,year+1,lisys[0][year])#先把表头的年份写了
for aou in range(len(lisps)): 
     worksheet.write(aou+1,0, lisps[aou])#把地点输入进来
     for year in range(len(lisxs[0])):
         worksheet.write(aou+1,year+1,lisxs[aou][year])
workbook.close()        
