# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 20:31:46 2019

@author: 73902
"""

import os
path='D:\python\\Rainfall2000_2017\\Rainf_f_tavg'
g='\\'
fn='Rainf_f_tavg_1.tif'
output="D:\python\\Rainfall2000_2017\\output\\"
os.chdir(path)
for year in os.listdir(path):
    for m in os.listdir(path+g+year):
        on='rainfall_'+year+m.zfill(2)+'.tif'
        os.rename(path+g+year+g+m+g+fn,output+on)
        


os.rename("D:\python\\Rainfall2000_2017\\Rainf_f_tavg\\2000\\1\\Rainf_f_tavg_1.tif","D:\python\\Rainfall2000_2017\\output\\rainfall_200001.tif")