# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 01:24:06 2018

@author: 73902
"""



import pandas as pd
import numpy as np
import os


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
data= pd.read_excel('p-year-numfile.xlsx')

lisy,lisx=listgroup(data['pos'],data['year'],data['num'])

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




#求出所有皮尔斯相关系数
'---------------'
#接下来要根据刚刚筛出的地点找出对应地点的经纬度，并计算距离
we = pd.read_csv("mergedData.csv")

position=we['NewID']

date = pd.DataFrame({
        'pos':position,
        'jing':we['Latitude'],
         'wei':we['Longitude'] })
    

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
#为了方便待会遍历找经纬度，现在先把总数据里的重复项删掉，速度会提升很大

def guolv(x,y,z,a):
    
   newlati,newlongi=[],[]
#提供筛选后数据的容器
   newbiglisp=a[:]
   for i,j,k in zip(x,y,z):
       if i in newbiglisp:
           newlati.append(j)
           newlongi.append(k)
           newbiglisp.remove(i)#
   return newlati,newlongi
#定义出根据给出的地点得到这个地点对应的经纬度的函数

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
allfirlist,allseclist,allthirlist,allfourlist,allfiflist,allsixlist=[],[],[],[],[],[]
for k in range(len(alldistence)):
    firlist,seclist,thirlist,fourlist,fiflist,sixlist=[],[],[],[],[],[]
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
            elif alldistence[k][i][j]>100000:
                fiflist.append(arrayallcorr[k][i][j])
            else :
                sixlist.append(arrayallcorr[k][i][j])
    allfirlist.append(firlist)
    allseclist.append(seclist)
    allthirlist.append(thirlist)
    allfourlist.append(fourlist)
    allfiflist.append(fiflist)     
    allsixlist.append(sixlist)
oklist=[allfirlist,allseclist,allthirlist,allfourlist,allfiflist,allsixlist]
#得到分类数据，先按照距离分类，然后按照年段分类，最后是具体的相关系数，查看时按照【距离】【年段序号】来查看
toklist=np.array(oklist).T

'写入excel'
import xlsxwriter
workbook = xlsxwriter.Workbook("posperson.xlsx") 
for year in range(len(toklist)):
     worksheet = workbook.add_worksheet() 
     worksheet.write('A1', year)
     for lie in range(len(toklist[year])):
         for hang in range(len(toklist[year][lie])):
             worksheet.write((hang+1), lie, toklist[year][lie][hang])
             
workbook.close()        
#test
    
