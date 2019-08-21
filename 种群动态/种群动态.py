# -*- coding: utf-8 -*-
"""
Created on Wed May 29 21:47:57 2019

@author: forth
"""


import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np





os.chdir('D:\python')
we = pd.read_csv("insetmerge.csv")
weyear=we['year']
weaou=we['aou']
wepos=we['pos']
webridnum=we['num']
webridmass=we['mass']

ditcmass=dict(zip(weaou,webridmass))
wemass=[]
for i,j in zip(webridnum,webridmass):
    wemass.append(i*j)


    
b=[]
a=list(set(weaou))
for i in a:
   b.append(ditcmass[i]) 
   
c=[]
for i in range(6):
    c.append([])

for i in range(len(a)):
      for j in range(6):#分段段数
          if (j*2000)<b[i]<((j+1)*2000):#分段间隔
              c[j].append(a[i])
              break
d=[]
for j in range(len(c)):
    d.append(set(c[j]))
newaou=[]
for i in range(len(weaou)):
    for j in range(len(d)):
        if weaou[i] in d[j]:
            newaou.append(j)
#得到一个新的aou列表，被 
ob=np.array([wepos,weyear,webridnum,newaou]).T
newob=[]
for i in range(len(ob)):
    if ob[i][1]>1987:
       newob.append(ob[i]) 
ntob=np.array(newob).T

date = pd.DataFrame({
        'pos':ntob[0],
        'year':ntob[1],
        'num':ntob[2],
        'aou':ntob[3],
        })

    
    
year_aou_num= list(date['num'].groupby([date['pos'],date['year'],date['aou']]))

dictpos=dict(zip(list(set(wepos)),[i for i in range(len(list(set(wepos))))]))


import xlsxwriter   
workbook = xlsxwriter.Workbook("okdmy(num).xlsx") 
worksheet = workbook.add_worksheet()

    
for i in range(len(list(set(wepos)))):
    worksheet.write(0,(i*7),list(set(wepos))[i])
    for j in range(6):
        worksheet.write(0,(i*7+1+j),j)
    for k in range(30):
        worksheet.write((k+1),(i*7),(k+1988))
    
write=list(map(lambda x:worksheet.write((x[0][1]-1987),(dictpos[x[0][0]]*7+x[0][2]+1),np.sum(x[1])),year_aou_num))
workbook.close()
