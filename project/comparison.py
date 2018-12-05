import data
import numpy as np
import svm
import knn1
import decisionTree
import knn
dat=data.parseData("path")
dataset=np.array(dat)
X = dataset[:,0:5] #Feature set
Y = dataset[:,5]    #target
svm.predict(X,Y)
knn1.predict(X,Y)
decisionTree.predict(X,Y)
Xt,Yt=data.loadDataset(0.8,offset=0,cnt=200)
knn.main(Xt,Yt,"path")