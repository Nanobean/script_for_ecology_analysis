# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 15:14:27 2019

@author: 73902
"""


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

import pandas as pd
import numpy as np
import os

os.chdir('D:\python')
we = pd.read_excel("insetmerge.xlsx")
weyear=we['year']
weaou=we['aou']
wepos=we['pos']
webridnum=we['num']
webridmass=we['mass']


os.chdir('D:\python')
da= pd.read_excel('species_trait0303.xlsx')
daaou=da['AOU']
damass=da['BodyMass.Value']

nonuaou,nonumass=[],[]
for i in range(len(daaou)):
    if pd.notnull(damass[i]):
        nonuaou.append(daaou[i])
        nonumass.append(damass[i])
#删掉空的体重数据        


setweaou=set(weaou)
intaou,intmass=[],[]
for i in range(len(nonuaou)):
    if nonuaou[i] in setweaou:
        intaou.append(nonuaou[i])
        intmass.append(nonumass[i])
#获得纯粹的体重数据与merge数据的交集

#_______________________________________________按照平均个体质量排序
#vmas=[intaou[i] for i in np.argsort(intmass)]  #按照质量进行排序并得到对应的aou
#vmas.reverse()
#ifelse=vmas[0:50]


#_______________________________________________按照总质量排序
os.chdir('D:\python')
data= pd.read_excel('a-year-numfileinset.xlsx')
lisy,lisx=listgroup(data['aou'],data['year'],data['num'])


def qiepian(x,y,up,down):
    yearlist=[]
    numlist=[]
    newyearlist=[]
    newnumlist=[]
    for j in range(len(x)):
        for i in range(len(x[j])):
           if (float(x[j][i])>down) and (float(x[j][i])<up):
              yearlist.append(float(x[j][i]))
              numlist.append(y[j][i])
        newyearlist.append(yearlist)  
        newnumlist.append(numlist)     
        yearlist=[]
        numlist=[]     
    return  newyearlist,newnumlist


lisy30,lisx30=qiepian(lisy,lisx,2018,1987)

#得到后三十年的数据


nonapos=data['aou'].dropna(axis=0,how='all')#删掉所有空值
def myfilter(n,lisx,lisy,yr):
    newlisp,newlisx,newlisy=[],[],[]   
    for i in range(0,len(lisx)):
      if (yr-(len(lisx[i])))<n and pd.notnull(lisx[i]).all() :
          newlisx.append(lisx[i])
          newlisp.append(list(nonapos)[i])
          newlisy.append(lisy[i])
    return newlisx,newlisp,newlisy
lisxs,lisps,lisys=myfilter(1,lisx30,lisy30,30)#这里lisps是物种编号的列表，lisxs是一个大列表，里面每一项是对应的aou，每个aou里面是这个aou的每一年的总数量


dictmass=dict(zip(nonuaou,nonumass))
#生成物种和质量的字典
lisms=[]
for i in lisps:
    lisms.append(dictmass[int(i)])

def pod(x,y):
    return np.mean(x)*y
podlist=list(map(pod,lisxs,lisms))#对每个aou列表取从起始年到结束年的时间平均值，然后计算时间平均质量

vortpodmass=[lisps[i] for i in np.argsort(podlist)]  #按照质量进行排序并得到对应的aou
vortpodmass.reverse()
ifelse=vortpodmass[0:50]


#-----------------------------------------------------

form tqdm import tqdm  
newpos,newyear,newaou,newbridnum=[],[],[],[]
for i in tqdm(range(len(weaou))):
    if weaou[i] in ifelse:
        newyear.append(weyear[i])
        newaou.append(weaou[i])
        newpos.append(wepos[i])
        newbridnum.append(webridnum[i])
#根据鸟的列表过滤数据
newallmass=[]
for i in range(len(newaou)):
    ms=newbridnum[i]*dictmass[float(newaou[i])]
    newallmass.append(ms)

df = pd.DataFrame({'pos' :newpos,
    'year' : newyear,
    'mass' : newallmass})
    


posgroup= pd.DataFrame(df['mass'].groupby([df['pos'],df['year']]).sum())
posfile= pd.ExcelWriter('p-year-massfileinset.xlsx')
posgroup.to_excel(posfile,'page_1',float_format='%.5f')
posfile.save()

#生成中间文件



os.chdir('D:\python')
data= pd.read_excel('p-year-massfileinset.xlsx')

lisy,lisx=listgroup(data['pos'],data['year'],data['mass'])
#转成二维数组
lisy30,lisx30=qiepian(lisy,lisx,2018,1987)
#切到只剩1987-2018区间内的数据


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
#过滤数量不足的数据



alllisy,alllisx=[],[]
for i in range(1987,2017,5):
        bigyearlist,bignumlist=qiepian(lisys,lisxs,i+6,i)
        alllisy.append(bigyearlist)
        alllisx.append(bignumlist)
#按照五年一段来对数据分段。


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
        'jing':we['Longitude'],
         'wei':we['Latitude'] })
    

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
    newlati,newlongi=guolv(newpos,newwei,newjing,lisps)
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

aoupearson,aoudis=arrayallcorr,alldistence


def segmen(x):
    aouoklist=[]
    for duan in range(len(aoupearson)):
        mapearson,madis=aoupearson[duan],aoudis[duan]
        oklist=[]
        for i in range(x):
                oklist.append([])
        for k in range(len(madis)):
            pearson,dis=mapearson[k],madis[k]
            for j in range(len(dis)):
                for i in range(x):
                    if dis[j]==0:
                        oklist[0].append(pearson[j])
                    elif dis[j]<(10*(2**i)*1000) and dis[j]>(10*(2**(i-1))*1000):
                        oklist[i].append(pearson[j])
                        break
        aouoklist.append(oklist)
    return aouoklist


duannum=9
aouoklist=segmen(duannum)
#输入值是你要给距离分的段数


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
          #空值太多了专门定义了把空值转0的函数
          
          
toklist=aouoklist
os.chdir('D:\python')
import xlsxwriter
workbook = xlsxwriter.Workbook('bridmass_oktable.xlsx') 
worksheet = workbook.add_worksheet()
worksheet.write(0,0,'year')
worksheet.write(0,1,'dis')
worksheet.write(0,2,'bridmasscorr')
for year in range(6):
    for dis in range(duannum):
        worksheet.write((year*duannum+dis+1),1,(10*(2**dis)))
        worksheet.write((year*duannum+dis+1),2,meann(toklist[year][dis]))
        if dis==0:
             worksheet.write((((year*duannum)+dis)+1),0,(1987+(year*5)))        
          
workbook.close()        


ws=pd.read_excel('bridmass_oktable.xlsx')
bridmasscorr=ws['bridmasscorr']
workbook = xlsxwriter.Workbook('bridmass_oktable_2.xlsx') 
worksheet = workbook.add_worksheet()
worksheet.write(0,0,'dis')
for dis in range(duannum):
    worksheet.write((dis+1),0,(10*(2**dis)))
worksheet.write(0,1,'bridmasscorr')
for year in range(6):
    worksheet.write(0,year+1,'year'+str(year))
    for dis in range(duannum):
        worksheet.write(dis+1,year+1,bridmasscorr[(year*duannum+dis)])
workbook.close()               