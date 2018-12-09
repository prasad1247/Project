import data
import numpy as np
import svm
import knn1
import decisionTree
import knn
import _thread
import time
import multiprocessing as mp
import neurtu
dat=data.parseData("path")
dataset=np.array(dat)
X = dataset[:,0:5] #Feature set
Y = dataset[:,5]    #target
Xt,Yt=data.loadDataset(0.8,offset=0,cnt=200)
def main():
   
    yield neurtu.delayed(knn,tags={"al":"knn1"}).main(Xt,Yt,"path")
    yield neurtu.delayed(svm,tags={"al":"SVM"}).predict(X,Y)
    yield neurtu.delayed(knn1,tags={"al":"KNN"}).predict(X,Y)
    yield neurtu.delayed(decisionTree,tags={"al":"tree"}).predict(X,Y)
    

if __name__ == "__main__":
    # mp.freeze_support()
    bench = neurtu.Benchmark(wall_time=True,  peak_memory=True)
    df = bench(main())
    print(df)
    # ax = df.wall_time.unstack().plot(marker='o')
    # ax.set_xscale('log')
    # ax.set_yscale('log')
    # ax.set_ylabel('Wall time (s)')
    # ax.set_title('Time complexity of numpy.sort')
