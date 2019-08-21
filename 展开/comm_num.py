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
pos=we['pos']
year=we['year']

from tqdm import tqdm  

intsetdata=pd.read_excel('finalinset.xlsx')
inset=set(list(intsetdata['inset']))
inpos,innum,inyear=[],[],[]
for i in tqdm(range(len(pos))):
    if pos[i] in inset:
        inpos.append(pos[i])
        inyear.append(year[i])
        innum.append(num[i])


#for i in range(len(inpos)):
#    po=inpos[i]
 #   for j in range(len(inpos)):
  #      if po==inpos[j]:
df=pd.DataFrame({'pos' :inpos,
    'year' : inyear,
    'num' : innum})            


posgroup= pd.DataFrame(df['num'].groupby([df['pos'],df['year']]).sum())
posfile= pd.ExcelWriter('p-year-numfileinset(2).xlsx')
posgroup.to_excel(posfile,'page_1',float_format='%.5f')
posfile.save()




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
data= pd.read_excel('p-year-numfileinset(2).xlsx')

lisy,lisx=listgroup(data['pos'],data['year'],data['num'])
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


nonapos=data['pos'].dropna(axis=0,how='all')#删掉所有空值

def myf(n,lisx,lisy,yr):
    newlisp,newlisx,newlisy=[],[],[]   
    for i in range(0,len(lisx)):
      if (yr-(len(lisx[i])))<n and pd.notnull(lisx[i]).all() :
          newlisx.append(lisx[i])
          newlisp.append(list(nonapos)[i])
          newlisy.append(lisy[i])
    return newlisx,newlisp,newlisy
lisxs,lisps,lisys=myf(1,lisx30,lisy30,30)
lisxs=np.array(lisxs)



import xlsxwriter
workbook = xlsxwriter.Workbook("comm_num.xlsx") 
worksheet = workbook.add_worksheet()
for year in range(len(lisys[0])):
    worksheet.write(0,year+1,lisys[0][year])#先把表头的年份写了
for pos in range(len(lisps)): 
     worksheet.write(pos+1,0, lisps[pos])#把地点输入进来
     for year in range(len(lisxs[0])):
         worksheet.write(pos+1,year+1,lisxs[pos][year])
workbook.close()        
