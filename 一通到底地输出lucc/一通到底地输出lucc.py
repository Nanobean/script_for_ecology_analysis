# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 15:39:03 2019

@author: forth
"""


import pandas as pd
import numpy as np
import os

import dbfread
import xlsxwriter
os.chdir('D:\zy\\lucc')
workbook=xlsxwriter.Workbook('lucc.xlsx')
worksheet=workbook.add_worksheet()
for year in range(1992,2016):
    df=pd.DataFrame(dbfread.DBF('lucc'+str(year)+'.dbf'))
    oklist,plist=[],[]
    for i in range(74,450):
        try:
            oklist.append(list(df['FID_F_'+str(i)]))
            plist.append(i)
        except:
            continue
            
    
    lengh=len(oklist)*len(oklist[0])
    olist=np.array(oklist).reshape(1,lengh)
    yearhang=(year-1992)*len(olist[0])
    list(map(lambda x:worksheet.write(yearhang+x+1,0,year),[i for i in range(len(olist[0]))])) #写年
    list(map(lambda x:worksheet.write(yearhang+x+1,3,olist[0][x]),[i for i in range(len(olist[0]))]))#写具体数
    for i in range(len(plist)):
        list(map(lambda x:worksheet.write(yearhang+i*len(oklist[0])+1+x,1,plist[i]),[i for i in range(len(oklist[0]))]))  #写地点
        list(map(lambda x:worksheet.write(yearhang+i*len(oklist[0])+1+x,2,df['LABEL'][x]),[i for i in range(len(oklist[0]))])) #写标签 

worksheet.write(0,0,'year')
worksheet.write(0,1,'FID')
worksheet.write(0,2,'LABEL')
worksheet.write(0,3,'num')
workbook.close()            