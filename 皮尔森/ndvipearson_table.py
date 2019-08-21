# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 23:39:42 2019

@author: 73902
"""




import pandas as pd
import os
import numpy as np
os.chdir('D:\python\extractedNDVI0227\extractedNDVI0227')

def filename(x):
    return "extract"+str(x)+'-'+str(x+4)+'.xlsx'
#定义文件名函数，方便for循环时读取对应的文件
def sheetname(x):
    return 'n'+str(x)


ypn=[]
for i in range(1987,2015,5):
    if i==2012:
        df=pd.read_excel( "extract"+str(i)+'-'+str(i+3)+'.xlsx')
        for k in range(i,i+4):
            ypn.append(list(df[sheetname(k)]))
#最后一个文件年份数量比较特殊，单独处理            
    
    else:
        df=pd.read_excel(filename(i))
        for j in range(i,i+5):
            if j==2016:
                break
            else:
                ypn.append(list(df[sheetname(j)]))
arrypn=np.array(ypn)

pyn=arrypn.T

os.chdir('D:\python')
intsetdata=pd.read_excel('finalinset.xlsx')
inset=list(intsetdata['inset'])
pos=df['newid']


newpos,newndvi,newlati,newlongi=[],[],[],[]
for i in range(len(pos)):
    if pos[i] in inset:
        newpos.append(pos[i])
        newndvi.append(pyn[i])
        newlati.append(df['Latitude'][i])
        newlongi.append(df['Longitude'][i])
#过滤数据



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
#定义切片函数

x=[]
for j in range(len(newndvi)):
    x2=[]
    for i in range(1987,2016):
        x2.append(i)
    x.append(x2)
#因为没有年份列表就手动生成了一个    
del x2


alllisy,alllisx=[],[]
for i in range(1987,2017,5):
    bigyearlist,bignumlist=qiepian(x,newndvi,i+6,i)
    alllisy.append(bigyearlist)
    alllisx.append(bignumlist)
#输入大year列表和大num列表，得到被切过后（第30-50年）的大列表。    
del x,bigyearlist,bignumlist        
        

allallcorr=[]
for i in alllisx:
    allcorr=np.corrcoef(np.array(i))       
    allallcorr.append(allcorr)
arrayallcorr=np.array(allallcorr)    

del allallcorr,allcorr,alllisx



#读取距离文件




from math import radians, cos, sin, asin, sqrt

a,b=list(newlati),list(newlongi)


latilonggi=[a,b]
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


#alldistence=[]
#for i in range(len(alllisy)):
#   alldistence.append(bigdistence)

    
    
aoupearson,aoudis=arrayallcorr,alldistence
aouoklist=[]
for duan in range(len(aoupearson)):
        mapearson,madis=aoupearson[duan],aoudis
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
workbook = xlsxwriter.Workbook('ndvi_oktable.xlsx') 
worksheet = workbook.add_worksheet()
worksheet.write(0,0,'year')
worksheet.write(0,1,'dis')
worksheet.write(0,2,'ndvicorr')
for year in range(6):
    for dis in range(9):
        worksheet.write((year*9+dis+1),1,(10*(2**dis)))
        worksheet.write((year*9+dis+1),2,meann(toklist[year][dis]))
        if dis==0:
            worksheet.write((((year*9)+dis)+1),0,(1987+(year*5)))        
          
workbook.close()               
    
ws=pd.read_excel('ndvi_oktable.xlsx')
ndvicorr=ws['ndvicorr']
workbook = xlsxwriter.Workbook('ndvi_oktable_2.xlsx') 
worksheet = workbook.add_worksheet()
worksheet.write(0,0,'dis')
for dis in range(9):
    worksheet.write((dis+1),0,(10*(2**dis)))
worksheet.write(0,1,'ndvicorr')
for year in range(6):
    worksheet.write(0,year+1,'year'+str(year))
    for dis in range(9):
        worksheet.write(dis+1,year+1,ndvicorr[(year*9+dis)])
workbook.close()