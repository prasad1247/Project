from project import data,svm,knn1,decisionTree,knn
import numpy as np
import _thread
import time
import multiprocessing as mp


def timerAnalysis(cnt):
    
    dat=data.parseData1("path",cnt)
    dataset=np.array(dat)
    X = dataset[:,0:5] #Feature set
    Y = dataset[:,5]    #target
    print(len(X))
    div=30
    Xt,Yt=data.loadDataset(0.8,offset=0,cnt=200)

    times={}    
    time1 = int(round(time.time()*1000))
    kdata=knn.main(Xt,Yt,"path")
    print('KNN')
    print(kdata['accuracy'])
    
    time2 = int(round(time.time() *1000)) 
    times['knn']=(time2-time1)/div
    print(svm.predict(X,Y))
    div=100
    time3 = int(round(time.time() *1000)) 
    times['svm']=(time3-time2)
    print(knn1.predict(X,Y))
    time4 = int(round(time.time()*1000 )) 
    times['knn1']=(time4-time3)
    print(decisionTree.predict(X,Y))
    time5 = int(round(time.time()*1000 )) 
    times['decisionTree']=(time5-time4)
    return times

# if __name__ == "__main__":
    # mp.freeze_support()
# print(timerAnalysis())