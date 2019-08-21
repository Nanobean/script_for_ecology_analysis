# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 17:15:37 2019

@author: 73902
"""


import pandas as pd
import os
import numpy as np


os.chdir('D:\python')

we = pd.read_csv("precip1987-2016juneOK2.csv")
pos=we['newid']
intsetdata=pd.read_excel('finalinset.xlsx')
inset=list(intsetdata['inset'])



bd=[]
for i in range(1988,2017):
    print(i)
    d=[]    
    d=list(we[str(i)]) 
    bd.append(d)
#读取数据
lisxt=np.array(bd).T
newpos,newlisxt=[],[]
for i,j in zip(pos,lisxt):
       if i in inset:
           newlisxt.append(j)
           newpos.append(i)#





longi,lati=we['Longitude'],we['Latitude']
newardata,newlongi,newlati=[],[],[]
for i in range(len(pos)):
    if pos[i] in inset:
        newardata.append(lisxt[i])
        newlongi.append(longi[i])
        newlati.append(lati[i])
#根据地点得到该地点的经纬度数据。存储起来
'#---------------'
newardatat=np.array(newardata).T
argnewdata=[np.mean(i) for i in newardatat]


import matplotlib.pyplot as plt
plt.plot(argnewdata)

import xlsxwriter
workbook = xlsxwriter.Workbook("precipnum_inset.xlsx") 
worksheet = workbook.add_worksheet() 
for i in range(len(newpos)):
    worksheet.write(0, (i+1), newpos[i])
for year in range(len(newardatat)):
         worksheet.write((year+1), 0, year)
         for pos in range(len(newardatat[year])):
             worksheet.write((year+1), (pos+1), newardatat[year][pos])
             
workbook.close()  

#获得计算相关性之前的原始数据
'--------------#-'



lisyt=[]
for j in range(len(newpos)):
    lisyt.append([i for i in range(1988,2018)])
#因为没有年份列表就手动生成一份对应的年表

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

lisy29,lisx29=lisyt,newlisxt
lisxs,lisps,lisys=myf(1,lisx29,lisy29,29)



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
for i in range(1987,2016,5):
    if i==2012:
        bigyearlist,bignumlist=qiepian(lisys,lisxs,i+5,i)
        alllisy.append(bigyearlist)
        alllisx.append(bignumlist)
    else:
        bigyearlist,bignumlist=qiepian(lisys,lisxs,i+6,i)
        alllisy.append(bigyearlist)
        alllisx.append(bignumlist)
#输入大year列表和大num列表，得到被切过后（第30-50年）的大列表。    
del bigyearlist,bignumlist


allallcorr=[]
for i in alllisx:
    allcorr=np.corrcoef(np.array(i))       
    allallcorr.append(allcorr)
arrayallcorr=np.array(allallcorr)    

del allallcorr,allcorr,alllisx







from math import radians, cos, sin, asin, sqrt

a,b=list(newlati),list(newlongi)
del newlati,newlongi


latilonggi=np.array([a,b])
bigdistence=[]
for i in range(len(a)):
        distence=[]
        for j in range(len(b)):
            lon1, lat1, lon2, lat2 = map(radians, [latilonggi[1][i],latilonggi[0][i],latilonggi[1][j],latilonggi[0][j]])
            dlon = lon2 - lon1 
            dlat = lat2 - lat1 
            aa = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(aa)) 
            r = 6371 # 地球平均半径，单位为公里
            distence.append(c*r*1000)
        bigdistence.append(distence)
#计算距离
del a,b,aa,c,distence,dlat,dlon,r,lon1,lon2,lat1,lat2,latilonggi


#alldistence=[]
#for i in range(len(alllisy)):
#   alldistence.append(bigdistence)

    
    
    
alldistence=np.array(bigdistence)
del bigdistence


allfirlist,allseclist,allthirlist,allfourlist,allfiflist,allsixlist=[],[],[],[],[],[]
for k in range(len(arrayallcorr)):
    firlist,seclist,thirlist,fourlist,fiflist,sixlist=[],[],[],[],[],[]
    le=len(arrayallcorr[k])
    for i in range(le):
        for j in range(le):
          if pd.notnull(arrayallcorr[k][i][j]):
            if alldistence[i][j]>2500000:
                firlist.append(arrayallcorr[k][i][j])
            elif alldistence[i][j]>1000000:
                seclist.append(arrayallcorr[k][i][j])
            elif alldistence[i][j]>500000:
                thirlist.append(arrayallcorr[k][i][j])
            elif alldistence[i][j]>250000:
                fourlist.append(arrayallcorr[k][i][j])
            elif alldistence[i][j]>100000:
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
del allfirlist,allseclist,allthirlist,allfourlist,allfiflist,firlist,seclist,thirlist,fourlist,fiflist,alldistence,arrayallcorr


print('ok')
toklist=np.array(oklist).T

del oklist


import xlsxwriter
workbook = xlsxwriter.Workbook("precip_inset.xlsx") 
for year in range(len(toklist)):
     worksheet = workbook.add_worksheet() 
     worksheet.write('A1', year)
     for lie in range(len(toklist[year])):
         for hang in range(len(toklist[year][lie])):
             worksheet.write((hang+1), lie, toklist[year][lie][hang])
             
workbook.close()        

alist=[]
for i in toklist:
     blist=[]
     for j in i:
          blist.append(np.mean(j))
     alist.append(blist)


import xlsxwriter
workbook = xlsxwriter.Workbook("precip_inset.xlsx") 

for year in range(len(alist)):
     worksheet = workbook.add_worksheet() 
     worksheet.write('A1', year)
     for lie in range(len(alist[year])):
             worksheet.write(1, lie, alist[year][lie])
             
workbook.close()        


