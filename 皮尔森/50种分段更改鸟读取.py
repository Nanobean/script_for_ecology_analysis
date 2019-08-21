# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 00:01:26 2019

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

#____________________输出具体的排名文件
import xlsxwriter
workbook = xlsxwriter.Workbook("50AOU.xlsx") 
worksheet = workbook.add_worksheet()
worksheet.write(0,0,"50aou")
for year in range(len(ifelse)):
    worksheet.write(year+1,0,ifelse[year])
             
workbook.close()        
#——————————————————————————————————————————不管用了哪种排序，接下来将根据排序信息得到



largelist=[]
for i in range(50):
    largelist.append([])
#生成50个种类的容器    

from tqdm import tqdm  
  
for i in tqdm(range(len(weaou))):
    ao=weaou[i]
    for j in range(len(ifelse)):
        if ao==ifelse[j]:
            smalllist=[]
            smalllist.append(weyear[i])
            smalllist.append(weaou[i])
            smalllist.append(wepos[i])
            smalllist.append(webridnum[i])
            smalllist.append(webridmass[i])
            largelist[j].append(smalllist)
            break    
tlargelist=[]    
for i in tqdm(largelist):
    tlargelist.append(np.array(i).T)


from functools import reduce
lisyear,lisnum,lispos=[],[],[]
for aou in tqdm(range(len(tlargelist))):#对五十种鸟一起进行处理的for循环
    #开始制造这一轮的容器
    aouyearlist,aounumlist=[],[]
    posnum=len(set(tlargelist[aou][2]))#获得地点的数量
    for i in range(posnum):#这个用来提前制造容器
        aouyearlist.append([])
        aounumlist.append([])
    #容器制造完成
    for i in range(len(tlargelist[aou][2])):#对每个地点进行遍历
        pos=tlargelist[aou][2][i]
        posifelse=list(set(tlargelist[aou][2]))
        for p in range(len(posifelse)):
            if pos==posifelse[p]:
                yelist,nulist=[],[]
                yelist.append(tlargelist[aou][0][i])
                nulist.append(tlargelist[aou][3][i])
                aouyearlist[p].append(yelist)
                aounumlist[p].append(nulist)
                break
                #到此为止获得了listgroup的效果，但是还没有排序。需要在整个for循环结束后排序，排序要在一种鸟结束后再分别对每个都排序。
    newye,newnu=[],[] #准备给排序后的东西容器
    for i in range(len(aouyearlist)):
        combaouyearlist=reduce(lambda x,y :x+y,aouyearlist[i])
        newaounum=[aounumlist[i][j] for j in np.argsort(combaouyearlist)]  
        newaouyear=sorted(combaouyearlist)
        newnu.append(newaounum)
        newye.append(newaouyear)
    lisyear.append(newye)
    lisnum.append(newnu)    
    #这时lisyear和lisnum就相当于原本的lisgroup函数的结果了，剩下的就可以与原本的操作对接了  
    
biglisy30,biglisx30=[],[]
for k in tqdm(range(len(lisyear))):
    lisy30,lisx30=qiepian(lisyear[k],lisnum[k],2018,1987)  #对每一个物种进行切片操作。
    biglisy30.append(lisy30)
    biglisx30.append(lisx30)


#def qiepian30(y,x):     这是废弃的map版本进行切片操作
#    return qiepian(float(y),float(x),2018,1987)

#lisyear30,lisnum30=list(map(qiepian30,lisyear,lisnum))

#这是废弃的过滤，在某处数据为零并不是数据缺失，而是这里就是没有这种鸟，所以不需要过滤
#def myf0(n,lisx,lisy,yr):
#    newlisp,newlisx,newlisy=[],[],[]   
#    for i in range(0,len(lisx)):
#      if (yr-(len(lisx[i])))<n and pd.notnull(lisx[i]).all() :
#          newlisx.append(lisx[i])
#          newlisp.append(list(nonapos)[i])
#          newlisy.append(lisy[i])
#      else:
#          
#    return newlisx,newlisp,newlisy

#biglisxs,biglisps,biglisys=[],[],[]  
#for aou in tqdm(range(len(biglisy30))):
#    nonapos=list(set(tlargelist[aou][2]))  这是过滤前每种鸟类对应的地点信息，之后会用到
#    lisxs,lisps,lisys=myf(1,biglisx30[aou],biglisy30[aou],30)
#    biglisxs.append(lisxs)
#    biglisys.append(lisys)
#    biglisps.append(lisps)#这就相当于每种鸟类对应的地点信息了，可以对照
yl=[i for i in range(1988,2018)]
bigczy,bigczx=[],[]
for aou in range(len(biglisy30)):
    poczy,poczx=[],[]
    for pos in range(len(biglisy30[aou])):
       yel=biglisy30[aou][pos]
       indy=[yl.index(i) for i in yel]
       czy,czx=[],[]
       a=0
       for i in range(len(yl)):
          if len(indy)==0:
              czx.append(0)
              czy.append(yl[i])
          else:
              if i==indy[a]:
                  czx.append(biglisx30[aou][pos][a])
                  czy.append(biglisy30[aou][pos][a])
                  if a!=(len(indy)-1):
                      a=a+1
              else:
                  czx.append(0)
                  czy.append(yl[i])
       poczy.append(czy)        
       poczx.append(czx)
    bigczy.append(poczy)
    bigczx.append(poczx)

    
    
    
bigalllisy,bigalllisx=[],[]
for aou in tqdm(range(len(bigczy))):
     alllisy,alllisx=[],[]
     for i in range(1987,2017,5):
            bigyearlist,bignumlist=qiepian(bigczy[aou],bigczx[aou],i+6,i)
            alllisy.append(bigyearlist)
            alllisx.append(bignumlist)
     bigalllisy.append(alllisy)
     bigalllisx.append(alllisx)

    

#def newf(y,x):
#     alllisy,alllisx=[],[]
#     for i in range(1987,2017,5):
#            bigyearlist,bignumlist=qiepian(y,x,i+6,i)
#            alllisy.append(bigyearlist)
#            alllisx.append(bignumlist)
#     return alllisy,alllisx
#bigalllisy,bigalllisx=map(newf,biglisy30,biglisx30)
#目前为止该切的切完了，接下来是计算操作，所以对数组类型转成高速计算的类型

biglisms=[]
for aou in range(len(bigalllisx)):
    pianmass=[]
    for pian in bigalllisx[aou]:
        posmass=[]
        for pos in pian:
            yearmass=[]
            for year in pos:
                if year!=0:
                    totalmass=(int(year[0]))*dictmass[ifelse[aou]]
                    yearmass.append(totalmass)
                else:
                    yearmass.append(0)
            posmass.append(yearmass)
        pianmass.append(posmass)    
    biglisms.append(pianmass)
#这数组太多维度了，展开写了好几层for，以后看看对于多重循环怎么优化可读性
    
    


bigallcorr=[]
for j in biglisms:
    allallcorr=[]
    for i in j:
        allcorr=np.corrcoef(np.array(i))       
        allallcorr.append(allcorr)
    bigallcorr.append(allallcorr)


#def corrmap(j):
#    allallcorr=map(np.corrcoef(np.array()),j)
#    return allallcorr
#bigallcorr=list(map(corrmap,biglisms))
#map版
arbigallcorr=np.array(bigallcorr)




#——————————————————————————接下来获取经纬度，计算距离进行分类就可以了

we = pd.read_csv("mergedData.csv")

position=we['NewID']

date = pd.DataFrame({
        'pos':position,
        'wei':we['Latitude'],
         'jing':we['Longitude'] })
    

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
del date

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



lisps=list(set(tlargelist[0][2])) 
newlati,newlongi=guolv(newpos,newwei,newjing,lisps)

biglati,biglongi=[],[]
for aou in range(len(tlargelist)):
    lisps=list(set(tlargelist[aou][2])) 
    allnewlati,allnewlongi=[],[]
    for i in range(len(alllisy)):
        newlati,newlongi=guolv(newpos,newwei,newjing,lisps)
        allnewlati.append(newlati)
        allnewlongi.append(newlongi)
    biglati.append(allnewlati)
    biglongi.append(allnewlongi)
 
from math import radians, cos, sin, asin, sqrt

aoudis=[]
for aou in tqdm(range(len(biglati))):
    duandis=[]
    for duan in range(len(biglati[aou])):
        latilonggi=[biglati[aou][duan],biglongi[aou][duan]]
        bigdistence=[]
        for i in range(len(latilonggi[0])):
            distence=[]
            for j in range(len(latilonggi[1])):
                lon1, lat1, lon2, lat2 = map(radians, [latilonggi[1][i],latilonggi[0][i],latilonggi[1][j],latilonggi[0][j]])
                dlon = lon2 - lon1 
                dlat = lat2 - lat1 
                aa = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * asin(sqrt(aa)) 
                r = 6371 # 地球平均半径，单位为公里
                distence.append(c*r*1000)
            bigdistence.append(distence) 
        duandis.append(bigdistence)
    aoudis.append(duandis)
        

alldisten=np.array(aoudis)


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
alloklist=[]
for aou in tqdm(range(len(arbigallcorr))):
    aoupearson,aoudis=arbigallcorr[aou],alldisten[aou]
    duannum=9
    aouoklist=segmen(duannum)
    alloklist.append(aouoklist)
#距离分类完成，接下来是输出





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
     





birdsort=ifelse

os.chdir('D:\python')
import xlsxwriter
workbook = xlsxwriter.Workbook('aou_oktable.xlsx') 
worksheet = workbook.add_worksheet()
worksheet.write(0,0,'year')
worksheet.write(0,1,'dis')
for year in range(6):
    for dis in range(duannum):
        worksheet.write((year*duannum+dis+1),1,(10*(2**dis)))
        if dis==0:
            worksheet.write((((year*duannum)+dis)+1),0,(1987+(year*5)))
            
for aou in tqdm(range(len(birdsort))):
    toklist=alloklist[aou]
    worksheet.write(0,(aou+2),birdsort[aou])
    for year in range(len(toklist)):
        for dis in range(len(toklist[year])):
            worksheet.write((year*duannum+dis+1),aou+2,meann(toklist[year][dis]))
workbook.close()     
    
    

we = pd.read_excel("aou_oktable.xlsx")

workbook = xlsxwriter.Workbook('aou_oktable_2.xlsx') 
worksheet = workbook.add_worksheet()
for dis in range(duannum):
    worksheet.write((dis+1),0,(10*(2**dis)))
for aou in tqdm(range(len(birdsort))):
    bird=we[int(birdsort[aou])]
    yearnum=6
    worksheet.write(0,((aou*(yearnum+1))+1),birdsort[aou])
    for year in range(yearnum):
        for dis in range(duannum):
            worksheet.write(dis+1,aou*(yearnum+1)+year+1,bird[int(year*duannum+dis)])
workbook.close()
    

#一通到底版本
os.chdir('D:\python')

we = pd.read_excel("aou_oktable.xlsx")
di=pd.read_csv('AOU50mass_traits.csv')
namedict=dict(zip(list(di['AOU']),list(di['Diet_AOU'])))
workbook = xlsxwriter.Workbook('aou_oktable_3.xlsx') 
worksheet = workbook.add_worksheet()
worksheet.write(0,0,'year')
worksheet.write(0,1,'dis')
worksheet.write(0,2,'diet-species')
worksheet.write(0,3,'Pearson_birds')
for aou in range(len(birdsort)):
    for year in range(6):
        for dis in range(duannum):
            worksheet.write(aou*duannum*6+(year*duannum+dis+1),1,(10*(2**dis)))
            worksheet.write((((year*duannum)+dis)+1)+aou*duannum*6,0,str((1987+(year*5)))+'-'+str((1987+(year*5))+4))
birdlist,namelist=[],[]
for aou in range(len(birdsort)):
    bird=list(we[int(birdsort[aou])])
    birdlist.extend(bird)#数量列表
    diet=[]
    for i in range(len(bird)):
        diet.append(namedict[birdsort[aou]])
    namelist.extend(diet)#名称列表
for i in range(len(namelist)):
    worksheet.write(i+1,2,namelist[i])
    worksheet.write(i+1,3,birdlist[i])
    #遍历写入
workbook.close()    
    

    