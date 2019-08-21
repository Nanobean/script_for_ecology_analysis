# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 20:25:19 2019

@author: forth
"""

    

import pandas as pd
import numpy as np
import os

import xlsxwriter
os.chdir('D:\python')
n=['LAI','T','P']
workbook = xlsxwriter.Workbook("correlationanalysis_12.xlsx")
for i in n:
    if n=='LAI':
        year=[i for i in range(1988,2017)]
    else:
        year=[i for i in range(1988,2016)]
        
    df= pd.read_excel('correlationanalysis_formal_12tables.xlsx',sheet_name ='EF_'+i )
    oklist=[]
    index=['mean','max','min']
    for ind in index:
        oklist.append(list(map(lambda x:df[str(x)+'_'+i+ind],year)))
    olist=list(map(lambda x:np.array(x).reshape(1,(318*len(year))),oklist))
    worksheet = workbook.add_worksheet(i)
    ind=[j for j in range(318*len(year))]
#    for ij in range(len(olist)):
 #       do=list(map(lambda x:worksheet.write((x+1),(ij*2+2),olist[ij][0][x]),ind))
    for k in range(len(year)):
        for j in range(318):        
            worksheet.write(((k*318)+1+j),0,j)
            worksheet.write(((k*318)+1+j),1,year[k])
    for x in ind:
        for ij in range(len(olist)):
            worksheet.write(0,(ij*2+2),i+index[ij])
            try:
                worksheet.write((x+1),(ij*2+2),olist[ij][0][x])
            except:
                worksheet.write((x+1),(ij*2+2),'99999')
year=[i for i in range(1988,2018)]
df= pd.read_excel('correlationanalysis_formal_12tables.xlsx',sheet_name ='diversity and birdnum' )
oklist=[]
index=['aph','bete','birds']
for ind in index:
        oklist.append(list(map(lambda x:df[ind+str(x)],year)))
olist=list(map(lambda x:np.array(x).reshape(1,(318*len(year))),oklist))
worksheet = workbook.add_worksheet('diversity and birdnum')
ind=[j for j in range(318*len(year))]
for k in range(len(year)):
        for j in range(318):        
            worksheet.write(((k*318)+1+j),0,j)
            worksheet.write(((k*318)+1+j),1,year[k])
for x in ind:
        for ij in range(len(olist)):
            worksheet.write(0,(ij*2+2),index[ij])
            try:
                worksheet.write((x+1),(ij*2+2),olist[ij][0][x])
            except:
                worksheet.write((x+1),(ij*2+2),'99999')
workbook.close() 



workbook = xlsxwriter.Workbook("birdmasstr.xlsx")
year=[i for i in range(1988,2018)]
df= pd.read_excel('birdmasstotransfer.xlsx' )
oklist=[]
index=['birdmass']
for ind in index:
        oklist.append(list(map(lambda x:df[ind+str(x)],year)))
olist=list(map(lambda x:np.array(x).reshape(1,(318*len(year))),oklist))
worksheet = workbook.add_worksheet('diversity and birdnum')
ind=[j for j in range(318*len(year))]
for k in range(len(year)):
        for j in range(318):        
            worksheet.write(((k*318)+1+j),0,j)
            worksheet.write(((k*318)+1+j),1,year[k])
for x in ind:
        for ij in range(len(olist)):
            worksheet.write(0,(ij*2+2),index[ij])
            try:
                worksheet.write((x+1),(ij*2+2),olist[ij][0][x])
            except:
                worksheet.write((x+1),(ij*2+2),'99999')
                
workbook.close()