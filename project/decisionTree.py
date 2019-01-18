from project import data
from sklearn import tree
from sklearn import neighbors
from sklearn import model_selection
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def predict(X,Y):
    dat=data.parseData("path")
    dataset=np.array(dat)
    # X = dataset[:,0:5] #Feature set
    # Y = dataset[:,5]    #target
    clf = tree.DecisionTreeRegressor()
    
    X_train,X_test,Y_train,Y_test = model_selection.train_test_split(X, Y, test_size = 0.2, train_size=0.8, random_state=0)
    clf = clf.fit(X_train, Y_train)
    print("DecisionTree")
    print(clf.score(X_test, Y_test))

    clfRaw = tree.DecisionTreeRegressor()
    clfRaw = clfRaw.fit(X_train,Y_train)
    cnt = 0
    k=0
    for i in clfRaw.predict(X_test):
        if(int(round(i)) == Y_test[k]):
            cnt = cnt+1
        k=k+1

    print("DecisionTree")
    print(float(cnt)/len(Y_test))
    return float(cnt)/len(Y_test)