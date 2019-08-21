# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 00:09:42 2019

@author: 73902
"""


import pandas as pd
import numpy as np
import os

os.chdir('D:\python')

we = pd.read_excel("temp1987-2017juneOK2 .xlsx")
pos=list(we['newID'])
intsetdata=pd.read_excel('finalinset.xlsx')
inset=set(intsetdata['inset'])

bd=[]
for i in range(1988,2018):
    print(i)
    d=[]    
    d=list(we['t'+str(i)]) 
    bd.append(d)

bdt=np.array(bd).T



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





newbdt=[]
for i in range(len(pos)):
    if pos[i] in inset:
        newbdt.append(bdt[i])