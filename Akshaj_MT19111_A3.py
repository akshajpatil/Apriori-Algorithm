
# coding: utf-8

# In[13]:

from itertools import combinations 
import time
#data=[["1","3","4"],["2","3","5"],["1","2","3","5"],["2","5"],["1","3","5"]]
#data=[["11","2","55"],["2","4"],["2","3"],["11","2","4"],["11","3"],["2","3"],["11","3"],["11","2","3","55"],["11","2","3"]]
#print(data[1])
#=====Opening of Data
dataSet=open("E:/IIIT Delhi/DMG/Assignment3/kosarak.dat","r")
d1=dataSet.readlines()
data=[line.split()for line in d1]

#print(data)



# In[21]:

import matplotlib.pyplot as plt

minsuppGraph=[0.02,0.04,0.07,0.1]
minconfGraph=[0.1,0.2]
for loopconf in minconfGraph: #..For Confidence Pruning graph
    #loopconf=0.2
    itemSetGraph=[]
    timing=[]
    for loopsupp in minsuppGraph:
        startingTime=time.time()
        freq=0
        dataFreqDict=dict({})
        uniqueEle=set()
        uniquelist=[]
        supportCount={}
        crossFlag=0

        length=len(data)
        minSuppThresh=loopsupp
        minHconfThresh=loopconf

        for lists in data:
            for items in lists:
                uniqueEle.add(items)

        


        dataFreqDict=calculateFrequency(uniqueEle,data)    
        supportCount=dataFreqDict
        
        
        for items in uniqueEle:
            uniquelist.append(items)

        uniquelist,crossFlag=prune(uniquelist,dataFreqDict,1)
         


        countDict={}
        countDict[1]=len(uniquelist)

        #=============
        updatedlist=uniquelist
        i=2
        crossFlag=0
        
        while len(updatedlist) > 0:
            uniqueEle=set()
            if i==2:
                for lists in updatedlist:
                    uniqueEle.add(lists)
            else:
                for lists in updatedlist:
                    for items in lists:
                        uniqueEle.add(items)
            updatedlist=calculateSet(uniqueEle,i)
           
            
            freqDict=dict({})
            for items in updatedlist:
                freqDict[items]=0
            
            for items in updatedlist:
                for it in data:
                    if(set(items).issubset(set(it))):
                        freqDict[items]=freqDict[items]+1

            
            updatedlist,crossFlag=prune(updatedlist,freqDict,i)
            
            countDict[i]=len(updatedlist)
            i=i+1
            
            
        
        itemSetGraph.append(sum(countDict.values())) #..For Confidence Pruning Graph
        finishingTime=time.time()
        
        timing.append(finishingTime-startingTime)
    #plt.plot(minsuppGraph,itemSetGraph,label="HConf Value "+str(loopconf)) ..For Confidence Pruning Graph
    plt.plot(minsuppGraph,timing,label="HConf Value "+str(loopconf))
# plt.title('Confidence Pruning effect')
# plt.xlabel('Minimun Support Threshold')
# plt.ylabel('Number of Hyperclique patterns')  For Confidence pruning graph
# plt.legend()
# plt.show()        #=============

plt.title('Time vs Support')
plt.xlabel('Support')
plt.ylabel('Time')
plt.legend()
plt.show()


# In[3]:

def prune(uniquelist,dataFreqDict,i):
    crossFlag=1
    crossUniqueList=[]
    for items in dataFreqDict:
        if dataFreqDict[items]/length < minSuppThresh:
            uniquelist.remove(items)
            crossFlag=0
        elif checkHConfidence(items,dataFreqDict,i): 
            uniquelist.remove(items)
            crossFlag=0
        else:
            crossUniqueList=crossSupport(dataFreqDict,i)
            crossFlag=0
    #print(uniquelist,dataFreqDict)
    
    if crossFlag==1:
        return crossUniqueList,crossFlag
    else:
        return uniquelist,crossFlag


# In[4]:

def calculateFrequency(uniqueEle,data):
    
    for items in uniqueEle:
        dataFreqDict[items]=0
    for lists in data:
        for items in lists:
        #freq=freq+lists.count(items)
            dataFreqDict[items]=dataFreqDict[items]+1
    return dataFreqDict


# In[5]:

def calculateSet(uniquelist,num):
    updatedlist=list(combinations(uniquelist, num))
    return updatedlist
    


# In[6]:

def checkHConfidence(items,dataFreqDict,j):
    max1=0
    if j==1:
        max1=supportCount[items]
    else:
        for i in items:
            if supportCount[i] > max1:
                max1=supportCount[i]
    
    if((dataFreqDict[items]/length)/(max1/length) >= minHconfThresh) :
        return 0
    else:
        return 1
        


# In[7]:

def crossSupport(key_value,i):
    key_value1=sorted(key_value.items(), key =lambda kv:(kv[1], kv[0]),reverse=True)
    #print("Dictionary is",key_value)
    #print(key_value1)
    key_value1=dict(key_value1)
    list1=key_value1.keys()
    
    finalSet=set()
    itemp1=0
    for itemp in list1:
        jtemp1=0
        uniqueEle1=set()
        for jtemp in list1:
            if(minHconfThresh*key_value1[itemp]/length>=key_value1[jtemp]/length):
                for l in itemp:
                    uniqueEle1.add(l)
                for l in jtemp:
                    uniqueEle1.add(l)
                    
            else:
                break
            jtemp1=jtemp1+1
        itemp1=itemp1+1
        
        combList=calculateSet(uniqueEle1,i)
        
        for l in combList:
            itemp3=[]
            if set(itemp).issubset(set(l)):
                finalSet.add(l)


    return list(finalSet)


# In[65]:

##==For checking scalibility
import matplotlib.pyplot as plt

#print(len(data))
loopconf=0.1
loopsupp=0.5
timeRequired=[]
itemSetGraph1=[]
dataScale=[100000,200000,300000,400000]
for k in range(1,5):
    data1=[]
    #startingTime=time.time()
    for items in range(100000*k):
        data1.append(data[items])

    
    #print(startingTime)
    freq=0
    dataFreqDict=dict({})
    uniqueEle=set()
    uniquelist=[]
    supportCount={}
    crossFlag=0

    length=len(data1)
    minSuppThresh=loopsupp
    minHconfThresh=loopconf

    for lists in data1:
        for items in lists:
            uniqueEle.add(items)




    dataFreqDict=calculateFrequency(uniqueEle,data1)    
    supportCount=dataFreqDict


    for items in uniqueEle:
        uniquelist.append(items)

    uniquelist,crossFlag=prune(uniquelist,dataFreqDict,1)



    countDict={}
    countDict[1]=len(uniquelist)

    #=============
    updatedlist=uniquelist
    i=2
    crossFlag=0

    while len(updatedlist) > 0:
        uniqueEle=set()
        if i==2:
            for lists in updatedlist:
                uniqueEle.add(lists)
        else:
            for lists in updatedlist:
                for items in lists:
                    uniqueEle.add(items)
        updatedlist=calculateSet(uniqueEle,i)


        freqDict=dict({})
        for items in updatedlist:
            freqDict[items]=0

        for items in updatedlist:
            for it in data:
                if(set(items).issubset(set(it))):
                    freqDict[items]=freqDict[items]+1


        updatedlist,crossFlag=prune(updatedlist,freqDict,i)

        countDict[i]=len(updatedlist)
        i=i+1
    finishingTime=time.time()
    itemSetGraph1.append(sum(countDict.values()))
    #print(finishingTime)
    #print(finishingTime-startingTime)
    #print("==========")
    timeRequired.append(finishingTime-startingTime)
    
    

plt.plot(dataScale,timeRequired,label="Support=0.1 and Confidence=0.2")
plt.title('Scalability')
plt.xlabel('Number of Data Rows')
plt.ylabel('Time')
plt.legend()
plt.show()
#print(data1)


# In[ ]:



