# -*- coding: utf-8 -*-
"""
Created on Fri May 24 11:01:43 2019

@author: forth
"""


import pandas as pd
import os
import numpy as np

os.chdir('D:\python')
N=['P','T','LAI'] #待处理文件的首字母，P：降水，T：温度
for i in N:
    if i=='P' or i=='T':
        we= pd.read_csv(i+'extractionmonthlytozb.csv') #根据不同的首字母获得对应的文件
    else:
        we=pd.read_csv('LAIextracttostat.csv')
    data=[]
    for pos in range(1,319):#遍历每一列来读取文件
        try:
            data.append(list(we[str(pos)]))
        except:
            data.append([9999 for i in range(len(we['1']))])
        
    bli=[]
    for pos in range(len(data)):
        sli=[]
        for year in range(28):#遍历每一年来把数据按年切割
            sli.append(data[pos][(year*12):((year+1)*12)])
        bli.append(sli)
    
    import xlsxwriter #准备写入文件
    if i=='P' or i=='T':
        workbook = xlsxwriter.Workbook(i+"finalinset.xlsx")
    else:
        workbook = xlsxwriter.Workbook("Laifinalinset.xlsx")
    workmean = workbook.add_worksheet('mean')
    workmax=workbook.add_worksheet('max')
    workmin=workbook.add_worksheet('min')
    workstd=workbook.add_worksheet('std')
    for pos in range(len(bli)):
        workmean.write(pos+1,0,pos)
        workmax.write(pos+1,0,pos)
        workmin.write(pos+1,0,pos)
        workstd.write(pos+1,0,pos)
        for year in range(28):
            workmean.write(0,year+1,str(year+1988))
            workmax.write(0,year+1,str(year+1988))
            workmin.write(0,year+1,str(year+1988))
            workstd.write(0,year+1,str(year+1988))
            workmean.write((pos+1),year+1,np.mean(bli[pos][year]))
            workmax.write((pos+1),year+1,np.max(bli[pos][year]))
            workmin.write((pos+1),year+1,np.min(bli[pos][year]))
            workstd.write((pos+1),year+1,np.std(bli[pos][year]))
    workbook.close()  