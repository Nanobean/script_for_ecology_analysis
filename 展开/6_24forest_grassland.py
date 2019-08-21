# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 20:00:17 2019

@author: forth
"""



    

import pandas as pd
import numpy as np
import os

import xlsxwriter
os.chdir('D:\python')
ind=['forest','grassland']
for i in ind:
    workbook=xlsxwriter.Workbook(i+'out.xlsx')
    worksheet=workbook.add_worksheet()
    g=0
    for j in range(10):
        try:
          for k in range(4):
              df=pd.read_csv(i+'all.csv',usecols=[(j*4+k)])
              list(map(lambda x:worksheet.write((x+1)+g*len(df),k,df.iloc[x]),[i for i in range(len(df))]))
          g=g+1  #计数成功了的话就加1，失败了不记，方便待会计算所处行数
        except:
            continue
    workbook.close()