# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 17:52:45 2019

@author: 73902
"""


import pandas as pd
import os
import numpy as np

os.chdir('D:\python')
record=pd.read_excel('temp_record_checked0314.xlsx')
pos=record['newid']
temp=record['checked record temp']
year=record['Year']
prod=pd.read_excel('temp_product0314.xlsx')
def temptran(x):
    return (x-32)*5/9


nulist=pd.isnull(temp)
newtemplist=[]
for i in range(len(temp)):
    if nulist[i]:
        if 1987<year[i]<2018:
            ind=list(prod['newID']).index(pos[i])
            val=prod['t'+str(year[i])][ind]
            newtemplist.append(val)
    else:
        newtemplist.append(temp[i])
        

intsetdata=pd.read_excel('finalinset.xlsx')
inset=list(intsetdata['inset'])



newpos,newtemp,newyear=[],[],[]
for i in range(len(pos)):
    if pos[i] in inset:
        newpos.append(pos[i])
        newtemp.append(newtemplist[i])
        newyear.append(year[i])
        

        
df=pd.DataFrame({
        'pos':newpos,
        'temp':newtemp,
        'year':newyear})

posgroup= pd.DataFrame(df['temp'].groupby([df['pos'],df['year']]).sum())
posfile= pd.ExcelWriter('p-year-tempfilecomset.xlsx')
posgroup.to_excel(posfile,'page_1',float_format='%.5f')
posfile.save()




data=pd.read_excel('p-year-tempfilecomset.xlsx')
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


comset=[]
for i in inset:
    if i not in lisps:
        comset.append(i)
#获得缺失地点        
for i in comset:
    ind=list(prod['newID']).index(i)
    newlis=[]
    for year in range(1988,2018):
        newlis.append(prod['t'+str(year)][ind])
    lisys.append(lisys[0])
    lisps.append(i)
    lisxs.append(newlis)
#根据缺失地点从产品数据里补充数据
    

alllisy,alllisx=[],[]
for i in range(1987,2017,5):
        bigyearlist,bignumlist=qiepian(lisys,lisxs,i+6,i)
        alllisy.append(bigyearlist)
        alllisx.append(bignumlist)
#切成六组
        
        


allallcorr=[]
for i in alllisx:
    allcorr=np.corrcoef(np.array(i))       
    allallcorr.append(allcorr)
arrayallcorr=np.array(allallcorr)    

#求出所有皮尔斯相关系数




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



aoupearson,aoudis=arrayallcorr,alldistence
aouoklist=[]
for duan in range(len(aoupearson)):
        mapearson,madis=aoupearson[duan],aoudis[duan]
        oklist=[]
        for i in range(9):
                oklist.append([])
        for k in range(len(madis)):
            pearson,dis=mapearson[k],madis[k]
            for j in range(len(dis)):
                for i in range(9):
                    if dis[j]==0:
                        oklist[0].append(pearson[j])
                    elif dis[j]<(10*(2**i)*1000) and dis[j]>(10*(2**(i-1))*1000):
                        oklist[i].append(pearson[j])
                        break
        aouoklist.append(oklist)
        


def summ(x):
    summm=0
    for i in range(len(x)):
        if pd.isnull(x[i]):
            a=0
        else:
            a=x[i]
        summm=summm+a
    return summm
def meann(x):
    if len(x)==0:
        return 0
    else:
        return summ(x)/len(x)
     

toklist=aouoklist
os.chdir('D:\python')
import xlsxwriter
workbook = xlsxwriter.Workbook('temp_oktable.xlsx') 
worksheet = workbook.add_worksheet()
worksheet.write(0,0,'year')
worksheet.write(0,1,'dis')
worksheet.write(0,2,'tempcorr')
for year in range(6):
    for dis in range(9):
        worksheet.write((year*9+dis+1),1,(10*(2**dis)))
        worksheet.write((year*9+dis+1),2,meann(toklist[year][dis]))
        if dis==0:
             worksheet.write((((year*9)+dis)+1),0,(1987+(year*5)))        
          
workbook.close()        


ws=pd.read_excel('temp_oktable.xlsx')
tempcorr=ws['tempcorr']
workbook = xlsxwriter.Workbook('temp_oktable_2.xlsx') 
worksheet = workbook.add_worksheet()
worksheet.write(0,0,'dis')
for dis in range(9):
    worksheet.write((dis+1),0,(10*(2**dis)))
worksheet.write(0,1,'tempcorr')
for year in range(6):
    worksheet.write(0,year+1,'year'+str(year))
    for dis in range(9):
        worksheet.write(dis+1,year+1,tempcorr[(year*9+dis)])
workbook.close()               