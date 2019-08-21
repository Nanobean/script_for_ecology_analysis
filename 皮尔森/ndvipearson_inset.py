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

    
    
    
alldistence=np.array(bigdistence)

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
            elif alldistence[i][j]>100000 :
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
workbook = xlsxwriter.Workbook("ndvipearson_inset.xlsx") 
for year in range(len(toklist)):
     worksheet = workbook.add_worksheet() 
     worksheet.write('A1', year)
     for lie in range(len(toklist[year])):
         for hang in range(len(toklist[year][lie])):
             worksheet.write((hang+1), lie, toklist[year][lie][hang])
             
workbook.close()        
#test


