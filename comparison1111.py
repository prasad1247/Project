from project import data,svm,knn1,decisionTree,knn
import numpy as np
import _thread
import time
import multiprocessing as mp

dat=data.parseData("path")
dataset=np.array(dat)
X = dataset[:,0:5] #Feature set
Y = dataset[:,5]    #target
Xt,Yt=data.loadDataset(0.8,offset=0,cnt=200)
def main():
    pool = mp.Pool(processes=4)
    t1=pool.apply_async(knn.main,(Xt,Yt,"path"))
    t2=pool.apply_async(svm.predict,(X,Y))
    t3=pool.apply_async(knn1.predict,(X,Y))
    t4=pool.apply_async(decisionTree.predict,(X,Y))
    # pool.close()
    t1.get()
    t2.get()
    t3.get()
    t4.get()

def timerAnalysis():
    time1 = int(round(time.time_ns() / 1000))
    knn.main,(Xt,Yt,"path")
    time2 = int(round(time.time_ns() /1000)) 
    svm.predict,(X,Y)
    time3 = int(round(time.time_ns() / 1000)) 
    knn1.predict,(X,Y)
    time4 = int(round(time.time_ns() / 1000)) 
    decisionTree.predict,(X,Y)
    time5 = int(round(time.time_ns() / 1000)) 
    times={}
    times['knn']=(time2-time1)
    times['svm']=(time3-time2)
    times['knn1']=(time4-time3)
    times['decisionTree']=(time5-time4)
    return times

times=timerAnalysis()
print(times)