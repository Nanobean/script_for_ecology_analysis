# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 22:15:12 2019

@author: 73902
"""


import pandas as pd
import numpy as np
import os


os.chdir('D:\python')

we = pd.read_excel("temp1987-2017juneOK2.xlsx")
pos=we['newID']
intsetdata=pd.read_excel('finalinset.xlsx')
inset=list(intsetdata['inset'])



bd=[]
for i in range(1988,2018):
    print(i)
    d=[]    
    d=list(we['t'+str(i)]) 
    bd.append(d)
#读取数据
lisxt=np.array(bd).T
newpos,newlisxt=[],[]
for i,j in zip(pos,lisxt):
       if i in inset:
           newlisxt.append(j)
           newpos.append(i)#
#根据交集过滤温度数据


lisyt=[]
for j in range(len(newpos)):
    lisyt.append([i for i in range(1988,2018)])
#因为没有年份列表就手动生成一份对应的年表


posgroup= pd.DataFrame(df['num'].groupby([df['pos'],df['year']]).sum())
posfile= pd.ExcelWriter('p-year-numfileinset.xlsx')
posgroup.to_excel(posfile,'page_1',float_format='%.5f')
posfile.save()









nonapos=newpos#删掉所有空值
def myf(n,lisx,lisy,yr):
    newlisp,newlisx,newlisy=[],[],[]   
    for i in range(0,len(lisx)):
      if (yr-(len(lisx[i])))<n and pd.notnull(lisx[i]).all() :
          newlisx.append(lisx[i])
          newlisp.append(list(nonapos)[i])
          newlisy.append(lisy[i])
    return newlisx,newlisp,newlisy
#输入一个阈值和大列表，以及年数，筛选掉大列表中小列表数量小于阈值的小列表。也可以用来筛选地点。


lisy30,lisx30=lisyt,newlisxt
lisxs,lisps,lisys=myf(1,lisx30,lisy30,30)




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


  
newpos,newjing,newwei=pos,we['LongitudeJingdu'],we['LatitudeWeidu']

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

import xlsxwriter
workbook = xlsxwriter.Workbook("temppearinset(2).xlsx") 
for year in range(len(toklist)):
     worksheet = workbook.add_worksheet() 
     worksheet.write('A1', year)
     for lie in range(len(toklist[year])):
         for hang in range(len(toklist[year][lie])):
             worksheet.write((hang+1), lie, toklist[year][lie][hang])
             
workbook.close()        
#test