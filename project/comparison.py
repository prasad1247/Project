import data
import numpy as np
import svm
import knn1
import decisionTree
import knn
from neurtu import Benchmark, delayed,timeit,memit
bench = Benchmark(wall_time=True, peak_memory=True)
dat=data.parseData("path")
dataset=np.array(dat)
X = dataset[:,0:5] #Feature set
Y = dataset[:,5]    #target
def getSvm():
    yield delayed(svm).predict(X,Y)
bench = Benchmark(wall_time=True, peak_memory=True)
df = bench(getSvm())
print(df)

knn1.predict(X,Y)
decisionTree.predict(X,Y)
Xt,Yt=data.loadDataset(0.8,offset=0,cnt=200)
knn.main(Xt,Yt,"path")