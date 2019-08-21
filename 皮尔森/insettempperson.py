# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 22:15:12 2019

@author: 73902
"""


import pandas as pd
import numpy as np
import os

os.chdir('D:\python')

we = pd.read_excel("weather20181109.xlsx")
pos=we['locationID']
year=we['Year']
temp=we['Temp']

intsetdata=pd.read_excel('finalinset.xlsx')
inset=list(intsetdata['inset'])
    
newyear,newtemp,newpos=[],[],[]
#提供筛选后数据的容器

for i,j,k in zip(pos,year,temp):
       if i in inset:
           newyear.append(j)
           newtemp.append(k)
           newpos.append(i)#


df = pd.DataFrame({'pos' :newpos,
    'year' : newyear,
    'temp' : newtemp})


tempgroup= pd.DataFrame(df['temp'].groupby([df['pos'],df['year']]).mean())


tempfile= pd.ExcelWriter('p-year-tempfileinset.xlsx')
tempgroup.to_excel(tempfile,'page_1',float_format='%.5f')
tempfile.save()

'------------生成数据----------------'


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
data= pd.read_excel('p-year-tempfileinset.xlsx')

lisy,lisx=listgroup(data['pos'],data['year'],data['temp'])



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
      if (yr-(len(lisx[i])))<n:
          newlisx.append(lisx[i])
          newlisp.append(list(nonapos)[i])
          newlisy.append(lisy[i])
    return newlisx,newlisp,newlisy
#输入一个阈值和大列表，以及年数，筛选掉大列表中小列表数量小于阈值的小列表。也可以用来筛选地点。



lisxs,lisps,lisys=myf(1,lisx30,lisy30,30)
'#---------------'
newardatat=np.array(lisx30).T
argnewdata=[np.mean(i) for i in newardatat]


import matplotlib.pyplot as plt
plt.plot(argnewdata)



import xlsxwriter
workbook = xlsxwriter.Workbook("tempnum_inset.xlsx") 
worksheet = workbook.add_worksheet() 
for i in range(len(lisps)):
    worksheet.write(0, (i+1), lisps[i])
for year in range(len(newardatat)):
         worksheet.write((year+1), 0, year)
         for pos in range(len(newardatat[year])):
             worksheet.write((year+1), (pos+1), newardatat[year][pos])
             
workbook.close()  
'--------------#-'
alllisy,alllisx=[],[]
for i in range(1987,2017,5):
        bigyearlist,bignumlist=qiepian(lisys,lisxs,i+6,i)
#输入大year列表和大num列表，得到被切过后（第30-50年）的大列表。
        alllisy.append(bigyearlist)
        alllisx.append(bignumlist)

allallcorr=[]
for i in alllisx:
    allcorr=np.corrcoef(np.array(i))       
    allallcorr.append(allcorr)
arrayallcorr=np.array(allallcorr)    



#接下来处理距离数据
we = pd.read_csv("mergedData.csv")

position=we['NewID']

date = pd.DataFrame({
        'pos':position,
        'jing':we['Latitude'],
         'wei':we['Longitude'] })
    
import string
def deldel(la,lb,lc):
   l2,l3,l4=[],[],[]   
   a=0
   for i,j,k in zip(la,lb,lc):
       if a!=i:
          l2.append(i)
          l3.append(j)
          l4.append(k)
          a=i
   return l2,l3,l4
newpos,newjing,newwei=[],[],[]

newpos,newjing,newwei=deldel(date['pos'],date['jing'],date['wei'])
#得到没有重复数据的mergedata
 

def guolv(x,y,z,a):
    
   newlati,newlongi=[],[]
#提供筛选后数据的容器
   newbiglisp=a[:]
   for i,j,k in zip(x,y,z):
       newi=float(i.translate(str.maketrans('', '', string.punctuation)))
       if newi in newbiglisp:
           newlati.append(j)
           newlongi.append(k)
           newbiglisp.remove(newi)#
   return newlati,newlongi
#根据给出的地点得到这个地点对应的经纬度

allnewlati,allnewlongi=[],[]
for i in range(len(alllisy)):
    newlati,newlongi=guolv(newpos,newjing,newwei,lisps)
    allnewlati.append(newlati)
    allnewlongi.append(newlongi)
#依次对每个年段的地点列表得到这个年段的地点的的经纬列表

from math import radians, cos, sin, asin, sqrt

alldistence=[]
for a,b in zip(allnewlati,allnewlongi):
    latilonggi=[a,b]
    bigdistence=[]
    for i in range(len(a)):
        distence=[]
        for j in range(len(b)):
            lon1, lat1, lon2, lat2 = map(radians, [latilonggi[1][i],latilonggi[0][i],latilonggi[1][j],latilonggi[0][j]])
            dlon = lon2 - lon1 
            dlat = lat2 - lat1 
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a)) 
            r = 6371 # 地球平均半径，单位为公里
            distence.append(c*r*1000)
        bigdistence.append(distence)
    
    alldistence.append(bigdistence)
alldistence=np.array(alldistence)   

#根据经纬表计算出距离表


allfirlist,allseclist,allthirlist,allfourlist,allfiflist=[],[],[],[],[]
allfifposlist=[]
for k in range(len(alldistence)):
    firlist,seclist,thirlist,fourlist,fiflist=[],[],[],[],[]
    fifposlist=[]
    le=len(alldistence[k])
    for i in range(le):
        for j in range(le):
            if alldistence[k][i][j]>2500000:
                firlist.append(arrayallcorr[k][i][j])
            elif alldistence[k][i][j]>1000000:
                seclist.append(arrayallcorr[k][i][j])
            elif alldistence[k][i][j]>500000:
                thirlist.append(arrayallcorr[k][i][j])
            elif alldistence[k][i][j]>250000:
                fourlist.append(arrayallcorr[k][i][j])
            else :
                fiflist.append(arrayallcorr[k][i][j])
                fifposlist.append(alldistence[k][i][j])
    allfirlist.append(firlist)
    allseclist.append(seclist)
    allthirlist.append(thirlist)
    allfourlist.append(fourlist)
    allfiflist.append(fiflist)
    allfifposlist.append(fifposlist)          
oklist=[allfirlist,allseclist,allthirlist,allfourlist,allfiflist]
#得到分类数据，先按照距离分类，然后按照年段分类，最后是具体的相关系数，查看时按照【距离】【年段序号】来查看


for i in range(len(oklist)):
    print(np.mean(oklist[i][6]))

from matplotlib import pyplot as plt



plt.rcParams['figure.figsize'] = (32.0, 16.0)
plt.plot(fifposlist,fiflist,'ro')

for i in range(len(alldistence[0])):
     plt.plot(alldistence[0][i],arrayallcorr[0][i],'ro')

toklist=np.array(oklist).T

import xlsxwriter
workbook = xlsxwriter.Workbook("temp(inset).xlsx") 
for year in range(len(toklist)):
     worksheet = workbook.add_worksheet() 
     worksheet.write('A1', year)
     for lie in range(len(toklist[year])):
         for hang in range(len(toklist[year][lie])):
             worksheet.write((hang+1), lie, toklist[year][lie][hang])
             
workbook.close()        
#test